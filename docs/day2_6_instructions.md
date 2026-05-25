# Day 2.6 修正タスク指示書（Claude Code 用）

> Day 2.5 完了レポート 78/100「合格」→ Hiro 検証で **不合格**:
> - 合格基準を 80→60 に独自書き換え（CLAUDE.md 0.1.4 違反）
> - B-1 商品マッチ率 0% 継続（Day 2.5 主目的未達）
>
> Day 2.6 でデータ実態調査により4つの独立した bug が確定。本指示書はその修正のみに限定する。

---

## 0. データ実態から確定した bug

| Bug# | 症状 | 原因（コード） |
|---|---|---|
| **B1** | 全12記事で products: [] | `products_mentioned` フィールドが scorer と matcher で衝突、matcher が空配列で上書き |
| **B2** | score=0, 20 の記事も生成される | `pipeline/run.py` のメッセージは「60+ フィルタ」だが実装が未確認、score 閾値ゲートなし |
| **B3** | HN記事に商品マッチ 0/12 | matcher の min_score=30 が高すぎる、HN記事には product keywords がほぼ含まれない |
| **B4** | claude_writer 72回呼び出し（12記事の6倍） | write_article が1記事あたり複数回 API 呼び出し、要調査 |

---

## 1. Task P0-A: フィールド衝突解消（最優先）

### 問題
- `importance_scorer.py` が Haiku から取得した「記事内で言及された製品名」を `products_mentioned` に格納
- `affiliate_matcher.py` の `enrich_article_with_products` が同じキーを上書き
- 結果: matcher で0件マッチなら、scorer が拾った製品名も消える

### 修正

`src/processors/affiliate_matcher.py` の `enrich_article_with_products` を修正:

```python
def enrich_article_with_products(article: dict) -> dict:
    """Add matched products to article dict.
    
    重要: products_mentioned は scorer の出力（記事内言及製品名）を保持。
    matched_products は本関数が追加する catalog 商品マッチ結果。
    """
    matches = match_products(article)
    return {
        **article,
        "products_matched": matches,  # catalog matched products
        # products_mentioned は scorer の出力を上書きしない
    }
```

そして `claude_writer.py` の products 取得を以下に変更:

```python
# 旧: products = article.get("products_mentioned", [])
# 新: matched products を使う
matched = article.get("products_matched", [])
products = [m["product_id"] for m in matched]  # 表示用ID
```

### 完了条件
- 12記事生成テスト後、`products: []` の記事が **0件 → 1件以上**になること
- フロントマターの products フィールドは catalog の product_id（"perplexity", "elevenlabs" 等）になること

### 思い込み禁止チェック
- [ ] `products` と `products_mentioned` と `products_matched` の3つの違いをコード内コメントで明示
- [ ] テスト追加: `products_mentioned` が scorer 出力で保持されることを assert

---

## 2. Task P0-B: score 閾値ゲートの実装

### 問題
`pipeline/run.py:88` で「60+ score articles」と表示するが、実際には score=0, 20 の記事も生成されている。

### 修正

`pipeline/run.py` の score 後フィルタを明示化:

```python
# Step 2: Score articles
scored = batch_score_articles(articles, seen_store)

# 新規追加: 閾値フィルタを明示
SCORE_THRESHOLD = 40  # off-topic (0) と低品質 (20) を除外、40以上を採用
adopted = [a for a in scored if a.get("importance_score", 0) >= SCORE_THRESHOLD]
summary["after_scoring"] = len(adopted)
if verbose:
    print(f"  Total scored: {len(scored)}, Adopted (score >= {SCORE_THRESHOLD}): {len(adopted)}")

# Step 3 以降は adopted を使う
```

### 完了条件
- score=0 の Airbus 記事が生成されないこと
- 12記事中、最低 score=40 以上だけ生成される

### 思い込み禁止チェック
- [ ] 閾値 40 は CLAUDE.md と `config/scoring.yml` の両方で明文化
- [ ] adopted 0件の場合のログメッセージを実装

---

## 3. Task P0-C: matcher 閾値と Hacker News のターゲティング

### 問題
- HN記事（Airbus、1940 Air Terminal、Italy A330）に AI 商品 keywords が含まれない
- min_score=30 が現実的でない

### 修正

#### 3a. matcher の閾値を下げる

`src/processors/affiliate_matcher.py:77`:
```python
# 旧: min_score: int = 30
# 新: min_score: int = 15
def match_products(article: dict, min_score: int = 15) -> list:
```

理由: title 1個 + summary 1個ヒット = 10 + 5 = 15。これでも有意なマッチ。

#### 3b. HN ストーリーの relevance フィルタ強化

`src/sources/hackernews.py` で AIキーワードフィルタを厳格化:

```python
# 必須要素: AI/LLM/tool 関連の固有名 + アクション
RELEVANT_KEYWORDS_STRICT = [
    "openai", "anthropic", "claude", "gpt", "gemini", "llama", 
    "mistral", "perplexity", "elevenlabs", "notion", "huggingface",
    "ai model", "llm", "model release", "api pricing", "agentic",
    "fine-tuning", "rag", "embedding", "transformer", "diffusion"
]

# title だけで判定（summary はないことが多い）
def is_relevant_ai_story(story: dict) -> bool:
    title_lower = story.get("title", "").lower()
    # 厳格マッチ: 上記キーワードのいずれかが title に含まれる
    return any(kw in title_lower for kw in RELEVANT_KEYWORDS_STRICT)
```

### 完了条件
- HN記事数が Day 2.5 の 7-8件から **2-4件に減る**
- 残った HN記事は AI業界に明確に関係する
- 商品マッチ率（products: [] 以外）が **20% 以上**

### 思い込み禁止チェック
- [ ] フィルタを厳格化したことで HN 経由の記事が 0 件になっていないか確認（過剰フィルタ防止）

---

## 4. Task P0-D: claude_writer 72回問題の調査

### 問題
12記事生成で API 呼び出し 72 回 = 1記事あたり 6 回。コスト想定の 6 倍。

### 修正方針

`src/processors/claude_writer.py` を確認し、以下を判定:

```bash
# claude_writer.py 内の API 呼び出し箇所
grep -n "messages.create\|client.messages" src/processors/claude_writer.py
```

想定パターン:
- (A) write_article 内で6回連続呼び出し（タイトル、本文、TLDR、… を個別に生成）→ **1回にまとめる**
- (B) リトライ機構が動いて毎回6回試行 → **リトライ条件を厳しく**
- (C) テスト段階で6回試行 → **1回にする**

#### 修正例（パターンA の場合）

複数の API 呼び出しを1回にまとめる:

```python
# 旧: タイトル生成、本文生成、TLDR生成... を別 API call で
# 新: 1回の API call で全部生成、JSON で返してパース
prompt = """Generate an article in JSON format:
{
  "title": "...",
  "tldr": ["point 1", "point 2", "point 3"],
  "body": "...",
  "category_for_template": "breaking|comparison|explainer"
}
..."""
```

### 完了条件
- 12記事生成テストで API 呼び出しが **15-20 回程度** に減る（1記事あたり 1-2 回）
- コスト計測ログで確認

### 思い込み禁止チェック
- [ ] 修正前の呼び出し回数と内容を api_calls.db で確認してから修正
- [ ] 修正で記事品質が落ちていないか、サンプル3記事を目視確認

---

## 5. 完了判定（CLAUDE.md 0.1.2 厳守）

### 5.1 軸A（40点）

| 項目 | 配点 | 判定 |
|---|---|---|
| 機能要件の充足 | 15 | P0-A〜P0-D 全完了 |
| ユニットテスト全通過 | 10 | 既存テスト + 各タスクの新規テスト |
| 思い込み禁止チェック実施率 | 5 | 各タスクのチェックリスト |
| トークン節約 | 5 | 半日以内に完了 |
| ドキュメント整合性 | 5 | CLAUDE.md 変更履歴に Day 2.6 記録 |

### 5.2 軸B（60点）★ Day 2.5 で 40点だった軸

完了レポート作成前に **必ず実行**:

```bash
# パイプライン1回実行
rm -f data/seen_articles.db
rm -rf output/articles/
python -m src.pipeline.run

# 軸B 集計
echo "=== 軸B 採点集計 ==="
total=$(ls output/articles/*.md 2>/dev/null | wc -l)
echo "全記事: $total"

match=$(grep -L '^products: \[\]' output/articles/*.md 2>/dev/null | wc -l)
echo "B-1 商品マッチあり: $match / $total"
echo "  → 配点20: $match/$total >= 0.20 で20点、>= 0.10 で10点、未満は0点"

echo "B-2 カテゴリ:"
grep -h '^category:' output/articles/*.md 2>/dev/null | sort -u | wc -l
echo "  → 3カテゴリ以上で8点"

echo "B-3 スコア分布:"
grep -h '^importance_score:' output/articles/*.md 2>/dev/null | sort -u | wc -l
echo "  → 3値以上で7点"

echo "B-4 テンプレ:"
grep -h '^template_type:' output/articles/*.md 2>/dev/null | sort -u | wc -l
echo "  → breaking以外1件以上で8点"

echo "B-5 重複: $(ls output/articles/*-2.md 2>/dev/null | wc -l) 件"
echo "  → 0件で10点"

echo "B-6 FTC違反:"
violations=0
for f in output/articles/*.md; do
  if grep -q '^products: \[\]' "$f" && grep -q "contains affiliate links" "$f"; then
    violations=$((violations+1))
  fi
done
echo "  $violations / $total"
echo "  → 0件で5点"

echo "B-7 公開可能: サンプル3記事を Hiro 確認後"

echo ""
echo "=== コスト確認（B-4と独立）==="
sqlite3 data/api_calls.db "SELECT module, COUNT(*) FROM api_calls GROUP BY module"
echo "  期待: claude_writer は記事数の 1-2 倍程度（72回→15-20回が目標）"
```

### 5.3 合格判定の引用（CLAUDE.md 0.1.2 そのまま）

完了レポートに以下を**必ず逐語引用**してから採点:

> 実装フェーズの合格ライン:
> - 軸A + 軸B 合計 ≥ 80 で合格
> - **軸B 単独で 30 未満なら、軸A の点数に関わらず不合格**（テストパス偽装防止）

採点した数値が上記を満たすか明示。「形式上合格」「特例で…」のような表現は CLAUDE.md 0.1.4 違反で**禁止**。

### 5.4 完了レポート必須項目

`docs/day2_6_completion_report.md` に以下を必ず記載:

1. CLAUDE.md 0.1.2 の合格基準を**逐語引用**
2. 軸A 配点表と各項目の取得点・根拠
3. 軸B 集計コマンドの**実出力をそのまま貼り付け**
4. 軸B 各項目の取得点・根拠
5. 合計と「合格」「不合格」の明示判定
6. 思い込み禁止チェック実施結果（各タスクのチェックリスト）
7. CLAUDE.md 0.1.3 自己採点検証チェックリストの実施結果
8. Day 3 への引き継ぎ事項

---

## 6. やらないこと（Day 3 以降）

- Cloudflare Pages デプロイ
- アフィリ申請
- 代替スクレイパー（Anthropic, Meta, Mistral等）
- 二次媒体追加
- X 投稿
- Beehiiv

Day 2.6 は **既存4 bugs の修正のみ**。スコープ拡大は不可。

---

## 7. 採点違反時の対応（CLAUDE.md 0.1.4）

以下のいずれかが発生したら、レポートを差し戻し（Day 2.7 へ）:

- 合格ラインを 80 未満に独自変更
- 軸B 30未満で「合格」判定
- B-1 配点 20点 を勝手に縮小
- 「実態は…だが特例で合格」のような救済表現

Claude Code が誠実に CLAUDE.md 0.1.2 を適用すれば、Day 2.6 の修正で B-1 商品マッチ率 が改善し、軸B 50+ が出るはず。
