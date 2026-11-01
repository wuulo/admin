# Handover — wuulo Etsy shop review (claude.ai session, 31 Oct – 1 Nov 2026)

Read this first. It carries everything from the claude.ai conversation that produced the files in this folder, so a Claude Code session in VS Code can continue without re-doing the work.

## 1. Who and what

- **wuulo** — Etsy shop `etsy.com/shop/wuulo`, handmade knitwear (alpaca, merino, lambswool, mohair). Owner: Flavia Goga (`flaviagoga@gmail.com`), originally from Bucharest, workshop in Kyiv since 2024. Knits on hand-driven (no-electricity) knitting machines. Website wuulo.eu; Instagram/Pinterest `wuulo_boutique`.
- Shop open since 2024. 18 active listings in two sections: *wool sweaters* (9) and *wool scarfs and throws* (9). Prices EUR 65–148 (shown to US buyers as $76–173). 13 sales, 5 reviews (all 5★), 14 followers, 193 favorites.
- Flavia writes in English and Romanian; these files are in English.

## 2. Files in this folder (`etsy/2026.11.01_stats/`)

| File | What it is |
|---|---|
| `../etsy_ads_stats_2024-10-31_2026-10-31.csv` | Etsy Ads daily export, all time (Flavia's upload). Columns: Date (ET), Views, Clicks, Orders, Revenue (USD), Spend (USD), ROAS, Click rate, Ending budget (USD). |
| `../Stats - Etsy.pdf` | Print of Shop Manager › Stats, all time, as of 31 Oct 2026 15:54. Visits, conversion, AOV, revenue, traffic sources, top listings. |
| `../EtsyListingsDownload.csv` | Etsy's listings export (backup before editing). 18 rows: TITLE, DESCRIPTION, PRICE (EUR), QUANTITY, TAGS, MATERIALS, IMAGE1–10 URLs, VARIATION 1–3 TYPE/NAME/VALUES, SKU (empty). **No listing IDs in it** — IDs are in the listing doc below. |
| `shop-review-2026-10-31.md` | The full review: diagnosis, numbers, ads analysis, 30-day plan. |
| `listing-titles-tags-descriptions.md` | New title, 13 tags, description and a per-listing fix for all 18 listings, plus four shared description blocks and a shop-level checklist. Repo copy of the Claude doc https://claude.ai/artifact/XMsz71NgcEXFQ5N3pKFTU8 (Flavia may keep editing the doc; re-export if in doubt). |
| `etsy-ads-analysis.py` / `etsy-ads-analysis-output.txt` | Script that computed every ads number in the review, and its output. Re-run after a fresh export. |

Not in the repo: the public shop page and the 18 listing pages were read live on 31 Oct 2026 (titles, prices, materials, variations, measurements, photo alt-texts, reviews, policies, About text). The listing doc contains what was extracted.

## 3. The diagnosis in one paragraph

Conversion is the problem, visibility second. All time: 3,455 visits → 13 orders = **0.4%** (Etsy norm 1–3%); revenue EUR 1,065; AOV EUR 82. Interest exists (177 favoriters, 15 abandoned carts worth EUR 1,382, 6 people with the tweed sweater in cart) but doesn't close: first photos are folded stacks not worn shots, shipping/returns/lead time aren't in the listings, free shipping is inconsistent (6 scarves under $100 lack it), most sizes/colours show "sold out". Organic Etsy search sent only **195 visits in two years** (6%); titles led with "artisanal/luxury/handcrafted" and never said scarf/sweater first or who the piece is for. Etsy Ads: $794 spent, 8 orders, $879 revenue → ROAS 1.1; CTR 1.7% and CPC $0.32 are fine, post-click conversion 0.33% is not. The only profitable month was Nov 2025 (ROAS 3.6 at ~$3.50/day); raising the budget (Sep–Oct 2026 at $7–8.50/day, Mar 2026 at $25/day) lowered conversion. Recommendation: $3–5/day Nov–Jan only, proven listings only, no scaling until conversion > 1%.

## 4. What was delivered and what state it is in

1. **Review** — delivered in chat, saved here. Flavia has read it.
2. **Listing rewrite** — drafted for all 18 listings, **not yet applied on Etsy**. Flavia has the doc open and made one small edit (bolded listing 1's new title). Titles follow Etsy's 27 Apr 2026 guidance (< 15 words, item first, no subjective/promo words): https://www.etsy.com/seller-handbook/article/1399426136697
3. **Ads** — analysis only; no changes made to the campaign.

## 5. Decisions still open (ask Flavia before acting)

- **Unisex vs women's.** Draft sells straight-cut sweaters, the vest and all scarves as *unisex*, the two batwing/poncho styles as *for women*. Asked in a doc comment; no answer yet.
- **Duplicates.** Listings 4485196479 and 4558302209 (batwing sweater) have identical titles/descriptions → merge proposed. Listings 4561814952 ($76) and 4484532519 ($108) look like the same 40×220 cm baby alpaca scarf → merge or differentiate; Flavia must say whether the knit differs.
- **Processing / lead time.** Missing from every listing; the shared "Shipping & returns" block has a `[Ready-to-ship … X working days; made-to-order … X days]` placeholder to fill.
- **Colour of listing 4473253283** (merino tuck-stitch sweater): no colour option, title doesn't say; placeholder `[colour]` in the new title.
- **Three listings carry two different sizes** (4405853758, 1844108063, 4405823463): which measurement is right.

## 6. Findings from `EtsyListingsDownload.csv` that the review did not have

Checked on 1 Nov 2026 after the review was written:

- **All 13 tag slots are already used on every listing, but every tag is written with underscores** (`wool_scarf`, `gift_for_her`, `Christmas_gift`, `wolldecke`). Etsy's help says tags "can only include spaces, letters, numbers" (plus apostrophes/hyphens inside): https://help.etsy.com/hc/en-us/articles/360000336307 . Either the CSV export encodes spaces as underscores, or the tags were entered that way. The MATERIALS column in the same file keeps its spaces ("brushed alpaca", "natural fiber"), which argues for the second. **First thing to verify in Shop Manager:** open one listing's tags. If they really contain underscores, `wool_scarf` is one token that never matches the query "wool scarf" — replacing underscores with spaces across all 18 listings may be the single biggest search fix, and it should happen before or together with the title rewrite.
- Current tags are heavy on brand/story words (artisan_fashion, wool_handmade, made_in_Ukraine, handcrafted_knitwear, luxury_gift_for_her) and light on product nouns, colours and wearer. The proposed tags in the listing doc replace them wholesale.
- Variations in the CSV: most garments use a combined `colour & size` variation (e.g. "petrol size S"); scarves use `colour`; two garments use `size` only; two scarves (1844108063, 4394681620) have no variation at all. Quantities are 1–8 per listing (not per variant in this export).
- The export has no listing IDs and no `processing time`/shipping-profile columns; those live only in Shop Manager.
- Etsy's listings CSV is **export-only**; Etsy does not bulk-import it. Applying the rewrite means editing each listing in Shop Manager (or Etsy's bulk-edit tool for titles/tags), or using the Etsy Open API v3 with an app key. A script that maps old title → new title/tags/description from the CSV + listing doc would make the manual pass faster.

## 7. Key numbers (for quick reference)

- Traffic sources, all time: Etsy Ads 1,392 · Etsy app & pages 1,065 · direct/referral 414 · Etsy marketing & SEO 322 · Etsy search 195 · other 45 · social 22.
- Visits by year: 2024 ≈ 450, 2025 ≈ 850, 2026 ≈ 2,150 (to 31 Oct). Revenue: ≈ EUR 150 / 405 / 510.
- Top listings all time: tweed sweater 4473310667 (914 views, 49 favs, 2 orders, EUR 100) · baby alpaca shawl scarf 4561814952 (600 / 27 / 2 / EUR 147) · brushed alpaca-mohair scarf 4405823463 (398 / 11 / 1 / EUR 102) · royal alpaca fine scarf (inactive, 338 / 10 / 0) · lambswool vest 4473219712 (326 / 12 / 0).
- Ads: 8 orders all time on 2025-11-06, 11-13, 11-27, 12-11, 2026-02-28, 09-04, 10-02 (×2). Ads AOV $110. Spend by month in `etsy-ads-analysis-output.txt`.
- Reviews: Dec 2024 (alpaca scarf, now inactive), Dec 2025 (4405853758), Apr 2026 (4397950200), Oct 2026 ×2 (4473310667 tweed sweater; a merino top no longer listed).

## 8. Caveats carried over

- Stats page is in EUR, ads export in USD; they don't reconcile exactly.
- Photo observations come from shop-page thumbnails and listing-page alt text, not from viewing every image.
- Etsy stats were read once (31 Oct 2026 15:54); the ads CSV covers 31 Oct 2024 – 31 Oct 2026.

## 9. Suggested next steps for the VS Code session

1. Verify the tag-underscore question in Shop Manager (§6) — it changes the priority order.
2. Get Flavia's answers to §5, then update `listing-titles-tags-descriptions.md` (and the Claude doc if she wants them in sync).
3. Build a small mapping (old title → listing ID → new title/tags/description) from `EtsyListingsDownload.csv` + the listing doc, so the Shop Manager pass is copy-paste.
4. After the rewrite is live: note the date, re-export stats and ads in ~4 weeks, re-run `etsy-ads-analysis.py`, compare search visits and conversion.
5. Keep new AI-written material in this `ai/` folder; raw Etsy exports go in the dated parent folder.

## 10. Repo

`github.com/wuulo/admin` (private), branch `main`, clean at handover; `.github/ISSUE_TEMPLATE/production-template-.md` is a production checklist unrelated to this work. `admin.code-workspace` opens the repo root.
