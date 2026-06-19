# 価格検証ログ（公式pricing fetch証跡）

CLAUDE.md §0.3.1 ハードルールに基づく一次情報の取得記録。
取得方法: Claude in Chrome（JSレンダリング実行）で公式pricingページを直接読取。

| 取得日 | 製品 | 公式URL | 確実性 |
|---|---|---|---|
| 2026-06-19 | ElevenLabs | https://elevenlabs.io/pricing | 🟢 |
| 2026-06-19 | Murf | https://murf.ai/pricing | 🟢 |
| 2026-06-19 | Semrush | https://www.semrush.com/pricing/seo/ | 🟢 |
| 2026-06-19 | Ahrefs | https://ahrefs.com/pricing | 🟢 |
| 2026-06-19 | Kinsta | https://kinsta.com/pricing/ | 🟢 |
| 2026-06-19 | WP Engine | https://wpengine.com/plans/ | 🟢 |
| 2026-06-19 | Jasper | https://www.jasper.ai/pricing | 🟢 |
| 2026-06-19 | Copy.ai | https://www.copy.ai/prices | 🟢 |
| 2026-06-19 | Shopify | https://www.shopify.com/pricing | 🟡 構造/手数料は🟢、USD金額は地域がJPY表示で未取得 |
| 2026-06-19 | WooCommerce | （コア無料・未fetch） | 🟡 公式fetch証跡なし、要確認 |

---

## ElevenLabs 🟢（2026-06-19, elevenlabs.io/pricing）
- Free $0 / 10k credits/mo（非商用）
- Starter $6/mo / 30k credits（Commercial License, Instant Voice Cloning）
- Creator $22/mo（初月50%オフ $11）/ 121k credits（Professional Voice Cloning）
- Pro $99/mo / 600k credits
- Scale $299/mo / 1.8M credits / 3 seats
- Business $990/mo / 6M credits / 10 seats（low-latency TTS as low as 5c/min）
- Enterprise: custom
- 差分: 記事値と一致。Creator初月50%オフ（$11）は未記載だった→追記可。

## Murf 🟢（2026-06-19, murf.ai/pricing）※年払い表示
- Free $0 / 10 projects / 10 min / 1 editor（No Commercial Rights, No Downloads）
- Creator $19/mo（年払い $228/yr）/ 100 projects / 24 hrs/year / Commercial Rights
- Business $66/mo（年払い $792/yr）/ 500 projects / 96 hrs/year
- Enterprise: custom（Custom Voice Clones は Add-on）
- **音声/言語: 200+ voices, 30+ languages & accents**
- ⚠️差分（要修正）: 記事は「120+ voices / 20+ languages」→ 公式「200+ voices / 30+ languages」。**公式採用**。
- 月払い価格（$29/$99）はトグルが年払い表示のため未取得→月払いは🟡。

## Semrush 🟢（2026-06-19, semrush.com/pricing/seo/）
- Pro $139/mo（年払い $117.33/mo）/ 5 sites / Position Tracking 500 kw
- Guru $249/mo（年払い $208.33/mo）/ 15 sites
- Business $499/mo（年払い $416.66/mo）/ 40 sites / API access
- Additional Users add-on: from $45/mo/user
- ⚠️差分: 記事「$139.95 / $499.95」→ 公式「$139 / $499」（.95は廃止）。Guru $249 は記事未記載。

## Ahrefs 🟢（2026-06-19, ahrefs.com/pricing）
- Starter $29/mo
- Lite $129/mo（1 user, 追加 +$40/mo/user）
- Standard $249/mo（追加 +$60/mo/user）
- Advanced $449/mo（追加 +$80/mo/user）
- Enterprise $1,499/mo（年契約）
- Brand Radar from $199/mo / Project Boost Max $200/mo/project
- 「割引・トライアルなし（Ahrefs Freeのみ）」
- 差分: 記事値と一致🟢。per-seat（追加ユーザー課金）確認。Standard $249 / Enterprise $1,499 追記可。

## Kinsta 🟢（2026-06-19, kinsta.com/pricing/）
- Single 20GB $35/mo（年払い実質 $30/mo・$350/yr, save $70）/ 1 install / 20GB server bandwidth / 10GB storage / 125GB CDN / **14 days backup retention**
- WP 2 $70/mo（$59 annual）, WP 5 $115, WP 10 $225, WP 20 $340, WP 40 $450
- Agency from $340/mo / Enterprise from $500/mo / Dedicated servers from $300/mo
- ⚠️差分（要修正）: ①記事「unlimited bandwidth」は誤り→現行は**サーバー帯域メーター制**（エントリー20GB）。②記事「backups 14–30 days」→公式「**14 days**」。③記事「35,000 visits」は現行ページに非表示（帯域基準）→数値を弱める。

## WP Engine 🟢（2026-06-19, wpengine.com/plans/）
- Essential / Startup $30/mo（年払い・$350 today）/ 1 site / 25,000 visits/mo / 10GB storage / **75GB bandwidth/mo**
- Add-ons: Additional Site +$20, Automated Plugin Updates +$3, Extra Security(WAF) +$19, NitroPack +$20
- ⚠️差分: 記事「50GB bandwidth」→公式「75GB」。月払い$40は年払い表示のため未確認（🟡）。

## Jasper 🟢（2026-06-19, jasper.ai/pricing）
- Pro **$59/mo（年払い）/ $69/mo（月払い）** / 1 user / 複数ブランド・キャンペーン
- Business: custom pricing（seats追加・AI Agent Builder・SSO・API access）
- ⚠️差分（要修正・重要）: 記事「Creator $39/mo」「Pro/Teams up to $99」は**古い**。現行は Pro $59($69) と Business(custom) の2本立て。SurferSEO等の旧記述も要再確認。

## Copy.ai 🟢（2026-06-19, copy.ai/prices）
- Self-Serve「Chat」$29/mo（月払い, 年払い20%オフ）/ **5 seats** / Unlimited Words in Chat / OpenAI・Anthropic・Gemini models
- Enterprise: custom（GTM AI / Workflows / credits）
- ページ全体がGTM AI（営業・マーケの「revenue engine」）。純粋なライティングのプラン構成は消滅。
- ⚠️差分（要修正）: 記事「$36（individual）/ Advanced $49（5 seats）/ free plan」→現行は **Chat $29（5 seats）+ Enterprise**。無料プランは当ページに非表示→「free plan available」は🟡（要確認）。GTMピボットは公式構成からも裏付け。

## Shopify 🟡（2026-06-19, shopify.com/pricing ※JPY地域表示）
- プラン構成（🟢）: **Basic / Grow / Advanced / Plus**（旧「Shopify」中位プランは「Grow」に改称）
- サードパーティ取引手数料（🟢）: Basic **2%** / Grow **1%** / Advanced **0.6%** / Plus **0.2%**
- オンラインカード手数料（🟢）: Basic 3.55% / Grow 3.4% / Advanced 3.25% / Plus 2.9%（+¥0）
- 月額（JPY表示・参考）: Basic ¥4,850(月)/¥4,365(年), Grow ¥13,500/¥12,150, Advanced ¥58,500/¥52,650, Plus from ¥368,000
- ⚠️差分: ①中位プラン名「Shopify」→「Grow」。②Advanced取引手数料「0.5%」→公式「0.6%」。③**USD金額は未取得**（ページがJPY地域表示）。USDは要再取得（地域切替 or Hiro確認）。

## WooCommerce 🟡（未fetch）
- コアプラグインは無料（オープンソース）という記述は一般に正しいが、**今回公式fetchの証跡なし**。
- 要対応: woocommerce.com を公式fetchし、コア無料＋有料拡張/ホスティング前提を証跡化。現状🟡。
