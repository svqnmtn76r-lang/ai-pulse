# Day 2 実行指示書（Claude Code 用）

> このドキュメントは Day 1.5 完了後（採点 97/100）の次ステップ。
> Importance Scorer、Claude Writer、Affiliate Matcher、Hacker News 統合を実装する。
>
> **設計判断は Claude Code に委ねる**。私（仕様作成者）は規格・完了条件・思い込み禁止チェックのみ提示。
> 実装の妥当性は採点制（80点未満は次へ進まない）で担保する。

---

## 0. Day 1.5 で学んだ教訓（必読）

| 教訓 | Day 2 への適用 |
|---|---|
| 公式情報なしのURLは8つ中5つが偽だった | 新規追加するURL・APIエンドポイントは**実HTTPで200確認**してから設定ファイルへ |
| heredoc + load_dotenv() でフレーム問題発生 | load_dotenv はパス明示 `load_dotenv(".env")` |
| `.env` に複数行ペーストで残骸混入 | `.env` 変更後は必ず `grep '=' .env` で全行が KEY=VALUE 形式か検証 |
| 私が「3.9 で動くから問題ない」と妥協 | Python 3.10+ 推奨は明記、3.9で型ヒント警告出るなら `from __future__ import annotations` を使う |
| RSS 8つ中5つで「公式RSSと思い込んでた」 | データソース追加時は必ず公式提供を確認、二次媒体は yellow ラベル |

---

## 1. Day 2 全体ゴール

Day 1 で取得した RSS / GitHub Releases データを、**ブログ公開可能な記事 + アフィリ商品リンク** まで変換するパイプラインを完成させる。

エンドツーエンド：
```
RSS監視（Day 1完了）
  ↓
[NEW] Importance Scorer：ノイズ除去（60%カット）
  ↓
[NEW] Affiliate Matcher：商品マッチング
  ↓
[NEW] Claude Writer：Markdown記事生成
  ↓
output/articles/{date}-{slug}.md
```

加えて：
- **[NEW] Hacker News API 統合**（速報性向上）
- **[NEW] コスト計測**（API呼び出しごとに input/output トークンを SQLite に記録）

---

## 2. 完了条件（採点制）

Day 2 完了時に以下を満たしているか採点する。**総合80点未満は Day 3 に進まない**。

| カテゴリ | 配点 | 完了条件 |
|---|---|---|
| **Importance Scorer** | 20 | 第1段階（ルール）で60%カット、第2段階（Claude）でスコア0-100付与、テスト3件以上通過 |
| **Affiliate Matcher** | 15 | `affiliate_sources.yml` を読み、記事1件で商品3つ以内をスコア順に返す、テスト3件以上通過 |
| **Claude Writer** | 25 | Markdownファイル生成、FTC開示自動挿入、3テンプレ（速報/比較/解説）切り替え、テスト3件以上通過 |
| **End-to-End** | 15 | `python -m src.pipeline.run` で RSS取得→記事1本以上を `output/articles/` に生成、エラーゼロ |
| **Hacker News統合** | 10 | `src/sources/hackernews.py` 実装、AIキーワードフィルタ、Day1 のRSSと同等パイプラインに統合 |
| **コスト計測** | 10 | SQLite テーブル `api_calls` に各呼び出し記録、`python -m src.analytics.cost_report` で日次集計表示 |
| **テスト/品質** | 5 | pytest 全通過（Day 1.5 の 6 + Day 2 で 9 以上 = 15+） |

---

## 3. モジュール別仕様

### 3.1 Importance Scorer (`src/processors/importance_scorer.py`)

#### 入力
記事dict（rss_monitor.py / github_releases.py / hackernews.py からの出力）:
```python
{
    "id": str,           # MD5 hash
    "source": str,       # "openai" / "github:openai/openai-python" / "hackernews"
    "title": str,
    "url": str,
    "summary": str,
    "published": str,    # ISO format
}
```

#### 出力
```python
{
    **input,             # 元のdict保持
    "importance_score": int,        # 0-100
    "category": str,                # "model_release" / "feature_update" / "pricing" / "research" / "tool" / "other"
    "products_mentioned": list[str],# catalog.yml の product_id リスト
    "skip_reason": str | None,      # None なら採用、文字列なら却下理由
    "scoring_method": str,          # "rule_v1" or "claude_v1"
}
```

#### 第1段階：ルールベース（API不要、無料）
以下のいずれかで `skip_reason` 設定して却下：
- title が10文字未満 → "title_too_short"
- title に絵文字のみ → "non_ascii_title"
- 公式RSS以外で title に "招待" "interview" "podcast" のみ → "low_signal_format"
- 過去30日以内に同じ url が seen_articles.db にある → "duplicate"

却下されなかった記事は第2段階へ。

#### 第2段階：Claude Haiku 4.5 によるスコアリング
プロンプト設計の方針（実装は Claude Code に委ねる）：
- 出力は **必ず JSON**（`response_format` 相当の指示）
- 評価軸：「AI業界プロが今日読むべきか」「BigCompany発表か個人プロダクトか」「既存読者の購買判断に影響するか」
- スコア基準を具体的に：
  - 90+：GPT-5、Claude Opus 5 のような major model release
  - 70-89：価格改定、新機能発表、SDKメジャーアップデート
  - 50-69：研究論文、技術ブログ
  - 30-49：通常ブログポスト
  - 0-29：人事異動、コミュニティ告知、低シグナル

#### 思い込み禁止チェック
- [ ] Claude API モデル名は実コードで `claude-haiku-4-5-20251001`（Day 1.5検証済み）or 最新を確認
- [ ] JSON パースエラー時のフォールバック実装
- [ ] 1記事あたり input token 上限（500token 以下）を超えないよう summary を truncate
- [ ] スコア閾値（60+ で採用等）は CLAUDE.md に明記、ハードコード禁止 → `config/scoring.yml` を新設

---

### 3.2 Affiliate Matcher (`src/processors/affiliate_matcher.py`)

#### 入力
- スコアリング済み記事dict
- `data/affiliate_sources.yml` の商品カタログ

#### 出力
```python
[
    {
        "product_id": str,       # "perplexity", "elevenlabs" など
        "name": str,
        "affiliate_url": str | None,  # 未承認段階では None
        "match_score": int,      # 0-100
        "match_reason": str,     # "keyword:voice,tts in summary"
    },
    ...
]
```
最大3商品、`match_score >= 30` のもののみ。

#### マッチングロジック
1. `affiliate_sources.yml` から `tier: 1` の商品を抽出（Day 2 段階では Tier 1 のみ）
2. 各商品の `trigger_keywords` を記事 title + summary で全文検索
3. キーワードヒット数 × 10 + CPA順位ボーナス で `match_score` 計算
4. 上位3つを返す

#### 思い込み禁止チェック
- [ ] `trigger_keywords` フィールドが affiliate_sources.yml にない場合の挙動を確認（Day 1.5 ファイル要確認）
- [ ] **存在しない場合は affiliate_sources.yml への追加が必要 → Day 2 タスクに含める**
- [ ] CPA が `cpa` / `cpa_min` / `recurring_pct` で複数フィールドある場合の優先順位を決める
- [ ] 未承認商品（`status != ready_to_apply` / `approved`）の扱いを決める

---

### 3.3 Claude Writer (`src/processors/claude_writer.py`)

#### 入力
- スコアリング済み記事dict（Importance Scorer の出力）
- マッチした商品リスト（Affiliate Matcher の出力）
- テンプレート種別（"breaking" / "comparison" / "explainer"）

#### 出力
- Markdownファイル: `output/articles/{YYYY-MM-DD}-{slug}.md`
- フロントマター必須項目:
  ```yaml
  ---
  title: str
  date: YYYY-MM-DD
  source_url: str            # 元記事URL
  source_name: str
  importance_score: int
  category: str
  products: [str]            # product_id リスト
  word_count: int
  generated_at: ISO timestamp
  generated_by: "claude-haiku-4-5-{date}"
  ---
  ```

#### 本文構造（テンプレ別）

**速報型 (breaking)**：120-300 word
```
## TL;DR
{3 bullet points}

## What happened
{200 word}

## Related tools
{affiliate products with affiliate_url or "申請中"}

## Source
{source_url}
```

**比較型 (comparison)**：400-800 word
- Tool A vs Tool B 形式
- スコアテーブル付き

**解説型 (explainer)**：500-1000 word
- TL;DR → 背景 → 詳細 → 影響 → ツール紹介

#### 全テンプレ共通
- **FTC開示文を末尾に自動挿入**:
  ```
  ---
  *Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*
  ```
- 商品が0個でも記事として成立すること
- 文字数を カウントして フロントマターに記録

#### 思い込み禁止チェック
- [ ] Claude API モデル名（claude-haiku-4-5 or claude-sonnet-4-5）はコスト・品質トレードオフで判断
  - 推奨：Haiku（コスト優先、Day 2はテスト段階）
  - 後で品質不足ならSonnetへ
- [ ] スラグ生成は title から英数字+ハイフン、日本語混入時はトランスリット or 削除
- [ ] 元記事のテキスト引用は **15語以内かつ1引用のみ**（CLAUDE.md 9節の方針）
- [ ] 同じ url から複数回生成しないよう、`output/articles/` の既存ファイル check

---

### 3.4 Hacker News 統合 (`src/sources/hackernews.py`)

#### 仕様
- API: `https://hacker-news.firebaseio.com/v0/topstories.json`（無料、認証不要）
- 取得方法:
  1. topstories の上位 100 件 ID を取得
  2. 各 ID の詳細を `https://hacker-news.firebaseio.com/v0/item/{id}.json` で取得
  3. AIキーワードでフィルタ
- AIキーワード（最低限）: `["AI", "LLM", "GPT", "Claude", "Gemini", "OpenAI", "Anthropic", "machine learning", "neural"]`
- 出力フォーマット: rss_monitor.py / github_releases.py と同じ記事dict形式

#### 思い込み禁止チェック
- [ ] HN API レートリミット確認（緩いが念のため公式ドキュメントで確認）
- [ ] 100件全部叩くと 100 HTTP requests、5分以内に完了するか
- [ ] URL がない HN ポスト（Ask HN等）の扱いを決める
- [ ] 既存の SeenArticleStore と統合（HN ID を `id` フィールドに）

---

### 3.5 コスト計測 (`src/analytics/cost_report.py`)

#### 役割
すべての Claude API 呼び出しを SQLite に記録、月次集計可能にする。

#### スキーマ案
```sql
CREATE TABLE api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,    -- ISO format
    module TEXT NOT NULL,        -- "importance_scorer" / "claude_writer"
    model TEXT NOT NULL,         -- "claude-haiku-4-5-20251001"
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd REAL,               -- 計算済みコスト
    success BOOLEAN
)
```

#### コスト計算ルール
- Haiku 4.5: input $1/MTok, output $5/MTok
- 計算はモデル別の単価テーブルを持つ
- 単価は `config/api_pricing.yml` で管理

#### 思い込み禁止チェック
- [ ] **Haiku 4.5 の最新価格を公式で確認**（私が思い込んでる単価が古い可能性）
- [ ] 公式ソース: https://www.anthropic.com/pricing（実HTTPで確認）

---

## 4. ファイル構造（Day 2 完了時の追加分）

```
ai-pulse/
├── src/
│   ├── processors/
│   │   ├── importance_scorer.py    [NEW]
│   │   ├── affiliate_matcher.py    [NEW]
│   │   └── claude_writer.py        [NEW]
│   ├── sources/
│   │   └── hackernews.py           [NEW]
│   ├── pipeline/
│   │   ├── __init__.py             [NEW]
│   │   └── run.py                  [NEW] End-to-End
│   └── analytics/
│       ├── __init__.py             [NEW]
│       └── cost_report.py          [NEW]
├── config/
│   ├── scoring.yml                 [NEW] スコア閾値・基準
│   └── api_pricing.yml             [NEW] 公式価格表
├── output/
│   └── articles/                   [NEW] 生成された記事
├── templates/
│   ├── breaking_news.md            [NEW]
│   ├── comparison.md               [NEW]
│   └── explainer.md                [NEW]
├── data/
│   ├── seen_articles.db            (Day 1で存在)
│   └── (NEW) api_calls.db          [NEW] コスト計測用
├── tests/
│   ├── test_importance_scorer.py   [NEW]
│   ├── test_affiliate_matcher.py   [NEW]
│   ├── test_claude_writer.py       [NEW]
│   └── test_hackernews.py          [NEW]
└── docs/
    └── day2_completion_report.md   [NEW] 完了レポート
```

---

## 5. 実装の順番（推奨）

工数低いものから着手。各タスクは前のタスクに依存しないよう設計。

1. **api_pricing.yml 作成**（公式価格確認、5分） → Anthropic公式から取得
2. **cost_report.py 実装**（30分） → DB初期化、記録関数
3. **importance_scorer.py 実装**（60分）→ ルールベース → Claude API 統合
4. **affiliate_matcher.py 実装**（30分）→ catalog読み込み、キーワードマッチ
5. **templates/ 作成**（30分）→ 3テンプレ
6. **claude_writer.py 実装**（90分）→ テンプレ選択、生成、ファイル出力
7. **hackernews.py 実装**（30分）→ API呼び出し、フィルタ
8. **pipeline/run.py 実装**（60分）→ End-to-End統合
9. **テスト追加**（60分）→ 各モジュール3+件
10. **動作確認**（30分）→ 実際にRSS取得→記事生成
11. **採点 + 完了レポート**（15分）

総工数目安: **約7時間**（休憩込みで1日）

---

## 6. 困ったときの対応

### 6.1 Claude API がコスト超過しそう
- まず1記事だけテスト実行、コストを確認
- 想定: importance_scorer 1記事 < $0.0005、claude_writer 1記事 < $0.02
- 1日合計 < $1 想定。超えるなら設定見直し

### 6.2 RSS の3フィードから記事が出ない日がある
- 想定内。Day 2 は機能実装が目的、データ量少なくてもOK
- 1記事だけ生成できれば End-to-End 成立

### 6.3 思い込みに気づいた
- 即修正、CLAUDE.md の変更履歴に追記
- ドキュメントの整合性を維持

### 6.4 Sonnet が必要か迷う
- 原則 Haiku 4.5。Claude Writer の品質が著しく低い時のみ Sonnet 検討
- 切り替えは config/scoring.yml の `writer_model` で

### 6.5 トークン超過しそう
- Day 1.5 ルール踏襲：再帰read禁止、verbose出力禁止、テストは関数単位
- 行き詰まったらHiroに状況報告、Day 3に分割提案

---

## 7. 採点（Day 2 完了後）

| カテゴリ | 配点 | 達成基準 |
|---|---|---|
| Importance Scorer | 20 | 完了条件3.1 全部満たす |
| Affiliate Matcher | 15 | 完了条件3.2 全部満たす |
| Claude Writer | 25 | 完了条件3.3 全部満たす |
| End-to-End | 15 | `python -m src.pipeline.run` 成功、記事1本+生成 |
| Hacker News | 10 | 完了条件3.4 全部満たす |
| コスト計測 | 10 | 完了条件3.5 全部満たす |
| テスト/品質 | 5 | pytest 全通過、15+件 |
| **合計** | **100** | **80点以上で Day 3 移行可能** |

---

## 8. やらないこと（Day 3 以降に繰り越し）

- Anthropic/Meta/Mistral/Cursor/Perplexity の直接スクレイパー
- 二次媒体（TechCrunch等）の追加
- ブログ実際の公開（Cloudflare Pages デプロイ）
- アフィリ申請の実施（コンテンツ出てから）
- X 投稿パイプライン
- ニュースレター（Beehiiv 連携）

これらは Day 3 / Day 4 / Phase 2 で対応。Day 2 は **生成パイプライン** に集中。

---

## 9. Hiro へのフィードバック依頼

Day 2 完了レポート（`docs/day2_completion_report.md`）に以下を含めてHiroに共有：

- [ ] 各カテゴリの採点と理由
- [ ] 思い込み禁止チェックで引っかかった箇所（あれば）
- [ ] 生成された記事のサンプル（1本）
- [ ] コスト計測の実測値（Claude API 呼び出し合計コスト）
- [ ] Day 3 への引き継ぎ事項

---

## 10. このドキュメントの品質維持

不正確な記述・古い情報・実装中に判明した思い込み を発見したら：

1. 該当箇所を引用
2. 修正案を提示
3. Hiro の承認を得てから本ファイルを更新（または `docs/day2_completion_report.md` に記録）

Day 1.5 で「公式RSSと思い込んでいた」誤りを Claude Code が発見したように、
Day 2 でも疑問を持ったら止まって確認すること。
