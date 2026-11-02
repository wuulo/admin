#!/usr/bin/env python3
"""Build one paste-ready file per listing from listing-titles-tags-descriptions.md.

Each file has the new title, the 13 tags as one comma-separated line, and the full
description (unique part + shared blocks) as plain text for Etsy's editor.
Re-run after editing the listing doc:  python3 -I make-paste-files.py
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "listing-titles-tags-descriptions.md"
OUT = HERE / "paste"
OUT.mkdir(exist_ok=True)

text = SRC.read_text(encoding="utf-8")

# --- shared blocks -------------------------------------------------------
shared_src = text.split("## Shared blocks for every listing", 1)[1].split("## Sweaters, vests and tops", 1)[0]
paras = [p.strip() for p in re.split(r"\n\s*\n", shared_src) if p.strip()]
shared = []  # (name, body)
i = 0
while i < len(paras):
    m = re.match(r"^\*\*(.+?)\*\*", paras[i])
    if m and i + 1 < len(paras):
        shared.append((m.group(1).strip(), paras[i + 1]))
        i += 2
    else:
        i += 1
assert [n for n, _ in shared] == ["Sizing & fit", "Shipping & returns", "Care", "Packaging & gifting"], shared

def plain(md: str) -> str:
    """Markdown → Etsy plain text."""
    s = md
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", s)
    s = re.sub(r"^- ", "• ", s, flags=re.M)
    return s.strip()

# --- listings ------------------------------------------------------------
body = text.split("## Sweaters, vests and tops", 1)[1].split("## Shop-level fixes", 1)[0]
sections = re.split(r"^### ", body, flags=re.M)[1:]

GARMENT_IDS = set()
rows = []
warnings = []
for sec in sections:
    head, _, rest = sec.partition("\n")
    hm = re.match(r"^(\d+(?: & \d+)?)\.\s+(.+?)\s+—\s+listings?\s+(.+)$", head.strip())
    if not hm:
        sys.exit(f"cannot parse heading: {head!r}")
    num, name, idpart = hm.groups()
    ids = re.findall(r"\d{10}", idpart)
    is_garment = int(num.split()[0]) <= 9
    lines = rest.split("\n")

    def grab(prefix_re):
        for ln in lines:
            if re.match(prefix_re, ln):
                return ln
        return None

    current = grab(r"^\*\*Current")
    newline = grab(r"^\*\*New \(")
    tagline = grab(r"^\*\*Tags:\*\*")
    fixline = grab(r"^\*\*Fix:\*\*")
    if not all([current, newline, tagline, fixline]):
        sys.exit(f"missing field in section {num}")

    current_title = re.sub(r"^\*\*Current[^*]*\*\*\s*", "", current).strip()
    title = re.sub(r"^\*\*New \([^)]*\)[^*]*\*\*\s*", "", newline).strip().strip("*").strip()
    tags = [t.strip() for t in re.sub(r"^\*\*Tags:\*\*\s*", "", tagline).split(",")]
    fix = re.sub(r"^\*\*Fix:\*\*\s*", "", fixline).strip()

    # description = from the line after **Description:** up to **Fix:**
    d0 = lines.index(grab(r"^\*\*Description:\*\*")) + 1
    d1 = lines.index(fixline)
    desc_md = "\n".join(lines[d0:d1]).strip()

    blocks = shared if is_garment else shared[1:]
    full = plain(desc_md) + "\n\n" + "\n\n".join(f"{n.upper()}\n{plain(b)}" for n, b in blocks)

    # checks
    wc = len(title.split())
    if wc >= 15:
        warnings.append(f"{num}: title has {wc} words (Etsy guidance: under 15)")
    if len(tags) != 13:
        warnings.append(f"{num}: {len(tags)} tags, not 13")
    for t in tags:
        if len(t) > 20:
            warnings.append(f"{num}: tag '{t}' is {len(t)} chars (max 20)")
    placeholders = re.findall(r"\[[^\]]+\]", title + " " + full)
    rows.append((num, name, ids, current_title, title, wc, tags, full, fix, placeholders))

    fname = "-".join(n.zfill(2) for n in num.split(" & ")) + f"-{ids[0]}.md"
    idlist = ", ".join(ids)
    sm = "\n".join(f"- Edit in Shop Manager: https://www.etsy.com/your/shops/me/tools/listings/{i}" for i in ids)
    pub = "\n".join(f"- Public page: https://www.etsy.com/listing/{i}" for i in ids)
    ph = ""
    if placeholders:
        ph = "\n> **FILL BEFORE PASTING:** " + "; ".join(sorted(set(placeholders))) + "\n"
    out = f"""# {num}. {name} — listing {idlist}

{sm}
{pub}
- Current title (to find it in the list): {current_title}
{ph}
## 1. Title ({wc} words) — paste into the Title field

{title}

## 2. Tags — delete the existing 13, then paste this whole line into the Tags field

{", ".join(tags)}

## 3. Description — select all in the Description field, then paste this whole block

```
{full}
```

## 4. Fix on this listing

{fix}
"""
    (OUT / fname).write_text(out, encoding="utf-8")
    print(f"wrote paste/{fname}")

print()
for w in warnings:
    print("WARNING:", w)
print(f"\n{len(rows)} sections, {sum(len(r[2]) for r in rows)} listing ids")
