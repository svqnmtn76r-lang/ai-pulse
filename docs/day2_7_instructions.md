# Day 2.7 実行指示書（データソース改善、Claude Code 用）

> Day 2.6 で実装品質は完璧（軸B 38/40）だが、データソース不足で軸C 10/30。
> Day 2.7 では **軸C を 20+/30 に引き上げる** ことだけに集中する。
>
> Day 3（公開）と並行進行可能。Day 3 の Cloudflare Pages デプロイは Day 2.7 を待たない。

---

## 0. Day 2.7 の目的

軸C 配点 30 のうち、Day 2.6 時点で：

| 項目 | 配点 | Day 2.6 取得 | 原因 |
|---|---|---|---|
| 商品マッチ率 | 12 | 0 | データソースに product keywords がない |
| カテゴリ多様性 | 6 | 3 | 2種類のみ（off_topic, sdk_release 等） |
| スコア分散 | 4 | 2 | 2値のみ |
| テンプレ多様性 | 4 | 4 | breaking + explainer 既達 ✅ |
| ターゲティング精度 | 4 | 1 | HN記事の AI関連度が低い |

Day 2.7 で **軸C 20+/30** を達成するため、データソースを増やす：

1. **二次媒体 RSS 検証 + 統合** (TechCrunch, The Decoder, VentureBeat)
2. **Anthropic / Meta / Mistral スクレイパー実装** (Day 2 の no_official_rss から)
3. **HN フィルタの再調整** (Day 2.6 で厳格化したが、製品名キーワード追加)

---

## 1. Task A: 二次媒体 RSS の実HTTP検証

### A-1: 候補3媒体の HTTP ステータス + content-type 確認

```bash
cd ~/ai-pulse
source .venv/bin/activate

python3 << 'EOF'
import requests
candidates = {
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "the_decoder": "https://the-decoder.com/feed/",
    "venturebeat_ai": "https://venturebeat.com/category/ai/feed/",
}
headers = {"User-Agent": "Mozilla/5.0 (compatible; ai-pulse/0.2)"}
for name, url in candidates.items():
    try:
        r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        ct = r.headers.get("Content-Type", "?")
        looks_xml = r.text.strip().startswith(("<?xml", "<rss", "<feed"))
        print(f"{r.status_code} {name:20s} | {ct:40s} | XML: {looks_xml} | {len(r.text)} bytes")
    except Exception as e:
        print(f"ERR {name}: {e}")
EOF
```

**思い込み禁止チェック**:
- [ ] **3媒体すべて 200 + XML である保証はない**（Day 1.5 で公式RSS 5/8 が偽だった教訓）
- [ ] 404/403 が返ったら、別の媒体候補に切り替える（候補リスト下記）
- [ ] HTML が返ったら（Bot ブロック）、User-Agent を変えて再試行

### A-2: 動作した媒体だけ data/rss_feeds.yml の secondary_media_candidates に追加

例（A-1 の結果次第で書き換え）：

```yaml
secondary_media_candidates:
  techcrunch_ai:
    url: https://techcrunch.com/category/artificial-intelligence/feed/
    confidence: green  # 実HTTPで200確認後にyellow→greenへ昇格
    verified: 2026-05-25
    last_status: 200
    licensing_note: "記事タイトル+概要のみ引用、全文転載不可"
```

### A-3: rss_monitor.py が secondary_media_candidates も読むようにする

現状の rss_monitor.py は verified_official_rss のみ。secondary も含めて読み込み：

```python
# src/sources/rss_monitor.py の load_feeds() を拡張
def load_feeds(config_path=Path("data/rss_feeds.yml")):
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    feeds = {}
    # verified_official_rss
    for name, info in data.get("verified_official_rss", {}).items():
        if isinstance(info, dict) and "url" in info:
            feeds[name] = info["url"]
    
    # secondary_media_candidates（confidence: green のもののみ）
    for name, info in data.get("secondary_media_candidates", {}).items():
        if isinstance(info, dict) and info.get("confidence") == "green" and "url" in info:
            feeds[name] = info["url"]
    
    return feeds
```

**完了条件**:
- 3媒体のうち最低1つが 200+XML 確認、rss_feeds.yml で green
- rss_monitor.py 実行で secondary 媒体から記事取得確認

### 候補不足時のバックアップ媒体

A-1 で 3つすべて却下されたら、以下を試す：

- https://www.marktechpost.com/feed/
- https://www.zdnet.com/topic/artificial-intelligence/rss.xml
- https://www.theverge.com/rss/ai-artificial-intelligence/index.xml
- https://www.wired.com/feed/tag/ai/latest/rss

---

## 2. Task B: Anthropic スクレイパー実装

### B-1: スクレイピング対象と方針

- 対象URL: https://www.anthropic.com/news
- 取得目標: 最新10件の (title, url, published, summary)
- 取得頻度: 30分ごと（rss_monitor と同等）
- 著作権配慮: title と要約（最大100語）のみ、本文転載しない

### B-2: 実装

`src/sources/scrapers/anthropic_news.py` を新規作成。

**実装方針**（Claude Code に委ねる）:
- `requests` + `beautifulsoup4` で HTML 取得 + パース
- ニュース一覧の DOM 構造を検証してから実装
- 個別記事ページは取得しない（一覧ページから取れる情報のみ）

**思い込み禁止チェック**:
- [ ] `https://www.anthropic.com/robots.txt` を確認、スクレイピング許可状況
- [ ] DOM 構造が変わった時の検出（テストで構造変化を確認）
- [ ] User-Agent に連絡先を明示 (`ai-pulse/0.2 (+https://aipulse.pages.dev)`)

### B-3: rss_monitor との統合

scraper の出力を rss_monitor.py と同じ article dict 形式に揃え、
pipeline/run.py の articles リストに追加する。

`src/sources/scrapers/__init__.py`:
```python
def articles_from_scrapers() -> list[dict]:
    """全 scraper の出力を統合"""
    from .anthropic_news import scrape_anthropic
    articles = []
    try:
        articles.extend(scrape_anthropic())
    except Exception as e:
        log.warning("anthropic_scrape_failed", error=str(e))
    return articles
```

`src/pipeline/run.py` に追加：
```python
from src.sources.scrapers import articles_from_scrapers
# ... fetch段階で
scraped = articles_from_scrapers()
articles.extend(scraped)
```

### B-4: Meta AI / Mistral スクレイパーは Day 2.8 へ繰り越し

優先順位：Anthropic > Meta = Mistral。Day 2.7 では Anthropic だけ実装。

---

## 3. Task C: HN フィルタの調整

### C-1: 現状の問題

Day 2.6 で HN フィルタを厳格化（24キーワード → 16キーワード）した結果、
HN記事は減ったが **affiliate products のキーワード（Perplexity, ElevenLabs 等）**
が含まれない記事ばかり残った。

### C-2: フィルタ調整

`src/sources/hackernews.py` の `RELEVANT_KEYWORDS_STRICT` に
affiliate_sources.yml の trigger_keywords を **追加**する：

```python
# 既存16キーワード + affiliate products のトリガー
def load_affiliate_keywords():
    """affiliate_sources.yml の trigger_keywords を flat に取得"""
    import yaml
    with open("data/affiliate_sources.yml") as f:
        data = yaml.safe_load(f)
    keywords = set()
    for pid, p in data.get("programs", {}).items():
        for kw in p.get("trigger_keywords", []):
            keywords.add(kw.lower())
    return keywords

# 動的にフィルタキーワード生成
def is_relevant_ai_story(story: dict) -> bool:
    title_lower = story.get("title", "").lower()
    # 既存の厳格キーワード
    base_keywords = ["openai", "anthropic", "claude", "gpt", ...]
    # affiliate のキーワード追加
    affiliate_keywords = load_affiliate_keywords()
    all_keywords = set(base_keywords) | affiliate_keywords
    return any(kw in title_lower for kw in all_keywords)
```

**完了条件**: HN記事に Perplexity / ElevenLabs / Notion 等の trigger_keywords が含まれる記事が通過する

**思い込み禁止チェック**:
- [ ] affiliate_keywords を読み込むコストは 1日 1回でOK、毎回読まない（キャッシュ）
- [ ] フィルタを緩めすぎて HN記事が爆発しないか、A/B 比較

---

## 4. 完了判定（CLAUDE.md 0.1.2.b 適用）

### 軸A 実装プロセス（30点）

| 項目 | 配点 | 判定 |
|---|---|---|
| 機能要件の充足 | 10 | Task A/B/C 完了 |
| ユニットテスト全通過 | 8 | scraper のテスト追加 |
| 思い込み禁止チェック実施率 | 5 | 各タスクのチェックリスト |
| トークン節約 | 3 | 半日以内 |
| ドキュメント整合性 | 4 | CLAUDE.md と rss_feeds.yml 更新 |

### 軸B 実装品質（40点）

Day 2.6 から大きく変わらない想定（変更点は新規実装のみ、既存バグ無し）。
35-40 維持を期待。

### 軸C データ品質（30点）★ Day 2.7 の主戦場

| 項目 | 配点 | Day 2.6 → Day 2.7 目標 |
|---|---|---|
| 商品マッチ率 | 12 | 0/5 → **3/15 (20%)** = **12点** |
| カテゴリ多様性 | 6 | 2種 → **4種** = **6点** |
| スコア分散 | 4 | 2値 → **3値** = **4点** |
| テンプレ多様性 | 4 | 2種 → 2種維持 = 4点 |
| ターゲティング精度 | 4 | 1/5 → **3/5** = **2点** |

軸C 合計目標: **28/30**

### 合格ライン
- 軸A + 軸B + 軸C ≥ 70 で合格
- 軸C 単独で **20+** が Day 2.7 の質的成功基準

---

## 5. Day 2.7 完了レポート（必須提出）

`docs/day2_7_completion_report.md` に：

1. CLAUDE.md 0.1.2.b 合格基準の逐語引用
2. Task A: 二次媒体 RSS 検証結果（3媒体それぞれの HTTPステータス）
3. Task B: Anthropic スクレイパー実装、取得記事サンプル3件
4. Task C: HN フィルタ調整、Before/After で取得記事数比較
5. 軸A/B/C 採点根拠（**軸C 集計コマンド実出力を必ず貼り付け**）
6. 思い込み禁止チェック実施結果

---

## 6. やらないこと（Day 2.8 以降）

- Meta AI / Mistral / Cursor / Perplexity の個別スクレイパー
- Product Hunt API 連携
- Reddit r/MachineLearning 統合
- 多言語ソース（日本語 ITmedia、TechCrunch JP 等）

Day 2.7 は **3つの新データソース** で軸C を 20+ に引き上げることだけに集中。

---

## 7. Day 3 との並行運用

Day 3 (公開 + Cloudflare Pages) を並行で進める Hiro 想定：

- **Day 3 中**: Day 2.6 までの記事で十分（11記事、十分な記事数）
- **Day 2.7 完了後**: より多様で商品マッチ率高い記事が生成される
- **両方完了後**: Day 3 のサイトに自動反映（GitHub Actions が daily pipeline 実行）

並行性のため、Day 2.7 と Day 3 は **異なるブランチ** で作業することを推奨：

```bash
# Day 2.7 用ブランチ
git checkout -b feature/day2.7-datasource

# Day 3 用ブランチ
git checkout -b feature/day3-deploy
```

完了後、それぞれ main にマージ。
