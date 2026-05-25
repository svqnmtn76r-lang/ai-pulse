# Day 3 実行指示書（Claude Code + Hiro 連携）

> Day 2.6 完了（新採点 78/100 合格）を踏まえ、生成パイプラインの成果物を公開する。
> Day 2.7 のデータソース改善と並行実行可能。
>
> **採点規則**: CLAUDE.md 0.1.2.b（軸A 30 + 軸B 40 + 軸C 30、合格 ≥70、軸B ≥25）

---

## 0. Day 3 の目的

Day 2.6 で **既に動く生成パイプライン** がある状態。これを：
1. **Web に公開**: aipulse.pages.dev で記事が読める
2. **アフィリ申請に必要なURL確保**: 公開ブログURLを Perplexity に申請
3. **CI/CD自動化**: GitHub Actions で記事自動生成 + 自動デプロイ

**やらない**：
- ElevenLabs / Notion 申請（コンテンツ品質基準満たすまで保留）
- カスタムドメイン取得（aipulse-stack.com、Phase 0 ルール参照）
- X 投稿パイプライン
- Beehiiv ニュースレター

---

## 1. タスクリスト

### Task 1: Astro ブログサイト構築

**完了条件**: `cd blog && npm run dev` でローカル起動、`output/articles/*.md` が記事ページとして表示される

#### 1.1 Astro プロジェクト作成

```bash
cd ~/ai-pulse
mkdir -p blog
cd blog
npm create astro@latest . -- --template minimal --typescript strict --no-install --no-git
npm install
```

**思い込み禁止チェック**:
- [ ] `npm create astro` が対話を求めずに完了するか（`--no-install --no-git` で抑止）
- [ ] 既存の `blog/` ディレクトリと衝突しないか確認

#### 1.2 Content Collections 設定

`blog/src/content/config.ts` を作成：

```typescript
import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    category: z.string().optional(),
    importance_score: z.number().optional(),
    products: z.array(z.string()).optional(),
    source_url: z.string().url().optional(),
    source_name: z.string().optional(),
    template_type: z.string().optional(),
    word_count: z.number().optional(),
    generated_at: z.string().optional(),
    generated_by: z.string().optional(),
  }),
});

export const collections = { articles };
```

#### 1.3 記事の自動同期

`output/articles/*.md` を `blog/src/content/articles/` にコピーするスクリプト：

```python
# scripts/sync_articles_to_blog.py
import shutil
from pathlib import Path

SRC = Path("output/articles")
DST = Path("blog/src/content/articles")
DST.mkdir(parents=True, exist_ok=True)

# 全 .md ファイルを同期
synced = 0
for md_file in SRC.glob("*.md"):
    target = DST / md_file.name
    if not target.exists() or md_file.stat().st_mtime > target.stat().st_mtime:
        shutil.copy2(md_file, target)
        synced += 1

print(f"Synced {synced} articles to blog/")
```

**思い込み禁止チェック**:
- [ ] Astro Content Collections のスキーマと、`claude_writer.py` のフロントマターが一致するか確認
- [ ] 不一致なら scheme を **柔軟（optional）** に、エラーで build が止まらないこと

#### 1.4 一覧ページと記事ページ

最低限の3ページ：

- `blog/src/pages/index.astro`: トップページ、最新記事10件
- `blog/src/pages/articles/[...slug].astro`: 個別記事
- `blog/src/pages/about.astro`: About ページ（アフィリ開示文含む）

**About ページ必須記載**:
```
# About AI-Pulse

This site monitors AI industry news and aggregates updates from official 
sources (OpenAI, Google DeepMind, Hugging Face, GitHub releases, Hacker News).

## Editorial standards
- We use AI to summarize public information from cited sources
- We do not republish copyrighted content
- All citations under 15 words

## Affiliate disclosure
Some articles may contain affiliate links to AI tools we genuinely use or 
recommend. We earn a commission at no extra cost to you. We never recommend 
products solely for commission.

## Contact
[Hiro's professional contact, e.g. GitHub or X]
```

---

### Task 2: Cloudflare Pages デプロイ

**完了条件**: `https://aipulse.pages.dev` で記事が読める状態

#### 2.1 GitHub 連携準備

```bash
# upstream 警告の解決を先に
cd ~/ai-pulse
git remote -v
# もし origin が壊れていたら：
# git remote remove origin
# git remote add origin git@github.com:svqnmtn76r-lang/ai-pulse.git
# git fetch origin
```

#### 2.2 Cloudflare Pages プロジェクト作成

**Hiro が手動で実施**（私と Chrome 連携で可能、ただし Cloudflare ログインが必要）:

1. https://dash.cloudflare.com → Pages → Create application
2. Connect to Git → svqnmtn76r-lang/ai-pulse を選択
3. Build settings:
   - Framework preset: **Astro**
   - Build command: `cd blog && npm install && npm run build`
   - Build output directory: `blog/dist`
   - Root directory: 空欄（リポルート）
4. Environment variables: なし（API キー不要、静的サイトのみ）
5. Save and Deploy

**思い込み禁止チェック**:
- [ ] Cloudflare Pages の Astro プリセットが build を正しく実行するか確認
- [ ] 初回 build エラーが出たら build command を `cd blog && npm ci && npm run build` に変更

#### 2.3 デプロイ確認

```bash
# デプロイ後、curl で確認
curl -I https://aipulse.pages.dev
# 期待: HTTP/2 200
```

ブラウザで開いて：
- [ ] トップページが表示される
- [ ] 個別記事が読める
- [ ] About ページが表示される
- [ ] FTC 開示文が正しく表示される

---

### Task 3: GitHub Actions 自動化

**完了条件**: GitHub Actions で「pipeline 実行 → blog/ 同期 → コミット → push → Cloudflare Pages 自動デプロイ」が完結

`.github/workflows/daily-pipeline.yml`:

```yaml
name: Daily Article Pipeline

on:
  schedule:
    - cron: '0 1 * * *'  # 毎日 UTC 01:00（AEST 11:00）
  workflow_dispatch:

jobs:
  generate-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run pipeline
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: |
          python -m src.pipeline.run
          python scripts/sync_articles_to_blog.py

      - name: Commit new articles
        run: |
          git config user.name "AI-Pulse Bot"
          git config user.email "bot@aipulse.pages.dev"
          git add output/articles/ blog/src/content/articles/ data/
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "chore: auto-generated articles $(date -u +%Y-%m-%d)"
            git push
          fi
```

**思い込み禁止チェック**:
- [ ] GitHub Actions の Secrets に `ANTHROPIC_API_KEY` と `GH_TOKEN` が登録されているか
- [ ] 登録されていなければ Hiro に依頼（手動設定）
- [ ] cron 時刻が Hiro の活動時間に合っているか（AEST 11:00 = 投稿確認しやすい時間）

#### 3.1 Secrets 設定（Hiro 手動）

GitHub リポ → Settings → Secrets and variables → Actions → New repository secret:

| Secret name | 値 |
|---|---|
| ANTHROPIC_API_KEY | `.env` の値 |
| GH_TOKEN | `.env` の値（Fine-grained PAT） |

---

### Task 4: Perplexity アフィリ申請

**完了条件**: Perplexity Affiliate Program 申請完了、承認待ち状態

#### 4.1 申請前チェック

申請時に審査担当者が見る項目：

- [ ] ブログ URL: https://aipulse.pages.dev （Task 2 完了後）
- [ ] About ページが整っている
- [ ] 最低5記事が公開されている
- [ ] FTC 開示文が表示されている
- [ ] 商用利用可能なコンテンツ（コピペ転載なし）

#### 4.2 申請手順（Hiro 手動）

1. https://www.perplexity.ai/hub/legal/perplexity-affiliate-program-terms-of-service を確認
2. https://docs.perplexity.ai/ から申請フォームへ
3. 入力情報：
   - Name: Hiro Yamaguchi
   - Email: hiro.yama.aiwriter@gmail.com
   - Country: Australia
   - Website: https://aipulse.pages.dev
   - Audience size: 0（正直に申告、Building new project）
   - Promotion method: "Blog about AI tools comparison and industry updates. Aggregates official news from OpenAI, Google DeepMind, Anthropic, Hugging Face. Publishes 3-5 articles/week with AI-assisted summarization. Started May 2026."
   - Niche: AI tools, developer productivity

#### 4.3 やらないこと

- ElevenLabs 申請（Day 4 以降、記事 30+ 公開後）
- Notion 申請（同上、CLOSED の可能性も再確認）
- HubSpot 申請（B2B 文脈の記事が必要、Day 5 以降）

**思い込み禁止チェック**:
- [ ] Perplexity Affiliate Program 申請ページの URL が変わっていないか確認
- [ ] 申請後、Dub Partners ダッシュボード招待メールが届くか待つ
- [ ] 却下されたら、却下理由を CLAUDE.md affiliate_sources.yml の verification_log に記録

---

## 2. 完了判定（CLAUDE.md 0.1.2.b 適用）

### 軸A 実装プロセス（30点）

| 項目 | 配点 | 判定 |
|---|---|---|
| 機能要件の充足 | 10 | Task 1-3 完了 |
| ユニットテスト全通過 | 8 | pytest 既存テスト + sync スクリプトテスト |
| 思い込み禁止チェック実施率 | 5 | 各タスクのチェックリスト |
| トークン節約 | 3 | 1日以内 |
| ドキュメント整合性 | 4 | CLAUDE.md 変更履歴更新 |

### 軸B 実装品質（40点）

| 項目 | 配点 | 判定 |
|---|---|---|
| パイプライン疎通 | 10 | GitHub Actions で 1記事以上自動生成 + デプロイ完了 |
| 冪等性・再現性 | 10 | sync スクリプトが mtime チェックで重複コピー防止 |
| 法的・倫理リスク回避 | 10 | About に FTC 開示、Editorial standards 明記 |
| コスト効率 | 5 | Cloudflare Pages = 無料、GitHub Actions 無料枠内 |
| 採点規則順守 | 5 | レポートで合格基準逐語引用 |

### 軸C データ品質（30点）

Day 2.7 と並行進行、Day 3 完了時点では Day 2.6 のままなので 10点維持想定。

### 合格ライン
- 軸A + 軸B + 軸C ≥ 70 で合格
- 軸B ≥ 25 必須

---

## 3. Day 3 完了レポート（必須提出）

`docs/day3_completion_report.md` に：

1. CLAUDE.md 0.1.2.b の合格基準を**逐語引用**
2. 軸A/B/C 採点根拠
3. Cloudflare Pages デプロイ URL (https://aipulse.pages.dev)
4. 公開記事数とサンプル記事の URL
5. Perplexity 申請の状態（送信済み / 承認待ち / 却下 等）
6. Day 4 への引き継ぎ事項
7. 思い込み禁止チェック実施結果

---

## 4. 困ったときの対応

### 4.1 Astro build エラー
- 既存記事のフロントマターと Astro Content Collection スキーマが不一致
- 対処：スキーマを optional 多めにする、または build 時に問題記事をスキップ

### 4.2 GitHub Actions の `git push` 失敗
- `permissions: contents: write` が設定されているか
- リポ Settings → Actions → Workflow permissions で "Read and write" 選択

### 4.3 Cloudflare Pages の初回 build 失敗
- Cloudflare Pages のビルドログを確認
- Node.js のバージョン指定が必要なら blog/.node-version で 20+ を指定

### 4.4 Perplexity 申請が却下
- 焦らない。記事 10件以上 + 1ヶ月運用してから再申請
- 却下理由を verification_log に記録

---

## 5. Day 4 以降へ繰り越し

- ElevenLabs アフィリ申請（記事 30+ 公開後）
- Notion アフィリ申請（同上）
- X 投稿パイプライン
- Beehiiv ニュースレター連携
- 独自ドメイン取得（CLAUDE.md 2.5 トリガー達成後）
