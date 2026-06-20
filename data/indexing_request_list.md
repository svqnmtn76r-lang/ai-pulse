# インデックス申請リスト（money pages）

作成: 2026-06-20 / 更新: 2026-06-20 / プロパティ: https://aitickerhq.com/（GSC, hiro19820820@gmail.com）

## 前提（重要・順序）
- サイトマップ `/sitemap-index.xml` は提出済み・Status Success・**415ページ discovered**（健全）。
- 現状 Indexed=1 / Crawled-not-indexed=8。Googleが新ドメインをまだ大半クロールできていない。
- **記事のcanonicalは末尾スラッシュあり** → 申請は必ず末尾スラッシュ版で行う。
- ⚠️ **ライブの5本はまだ旧版**。深掘り版は 2026-06-20 に「プロ記者品質」へ全面リライト済（一次情報TODO削除・公式価格反映・Kinsta帯域の誤り修正・5本相互内部リンク追加）だが **未デプロイ**。先にデプロイしないと旧版が登録される。

## 推奨手順
1. **先にデプロイ**: `seo-deepdive-5` を rebase→push→main マージ（Cloudflare再ビルドで深掘り版が反映）。
2. 反映を1本 web で確認（価格表・FAQが出ているか）。
3. **その後** GSC でインデックス申請（下記URLを1本ずつ URL Inspection に貼付→「Request Indexing」）。
   - Request Indexing の最終クリックは送信＝HUMAN-ONLY（Hiroが実行）。

## 申請対象URL（canonical・末尾スラッシュ版）
1. https://aitickerhq.com/articles/2026-06-09-elevenlabs-vs-murf-best-ai-voice-generator-for-cre/
2. https://aitickerhq.com/articles/2026-06-03-shopify-vs-woocommerce-best-ecommerce-platform-to-/
3. https://aitickerhq.com/articles/2026-06-03-semrush-vs-ahrefs-the-better-seo-tool-for-keyword-/
4. https://aitickerhq.com/articles/2026-06-11-kinsta-vs-wp-engine-managed-wordpress-hosting-comp/
5. https://aitickerhq.com/articles/2026-06-08-jasper-vs-copyai-which-ai-writer-for-marketing-tea/

補助（任意・優先度高い基幹ページ）:
- https://aitickerhq.com/
- https://aitickerhq.com/reviews/

## 既知の技術課題（インデックス促進に寄与）
- canonical 末尾スラッシュ不一致: スラッシュ無しURLも200で到達可。内部リンク/サイトマップを canonical（スラッシュ有）に統一し、無し→有りを301に。インデックス信号の分散を防ぐ。
- 1日のRequest Indexing回数には上限あり。5本＋基幹2本なら問題なし。連打は不可。
