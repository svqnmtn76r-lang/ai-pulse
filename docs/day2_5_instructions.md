# Day 2.5 修正タスク指示書（Claude Code 用）

> Day 2 完了後の Hiro 検証で実態が 63/100 と判明した。
> 採点規則を二軸化（CLAUDE.md 0.1.2 改訂）してから、本指示書で実装改修する。
>
> **本指示書の合格基準は CLAUDE.md 0.1.2 の「軸A 40点 + 軸B 60点」体系を適用する**。
> 「テスト通過 = 高得点」の自己採点は無効。実出力品質を必ず測定。

---

## 0. 必読：Day 2 で何が起きていたか

Day 2 自己採点 99/100 → Hiro 検証で実態 63/100。原因：

| 問題 | 実態 | 影響 |
|---|---|---|
| products: [] が 45/45 (100%) | アフィリ商品マッチ完全失敗 | 収益化不能 |
| category: other が 45/45 (100%) | スコアリングのカテゴリ判定が機能していない | テンプレ選択不可 |
| importance_score が全部 50 | プロンプトが弱く、デフォルト 50 ばかり返す | 採点機能なし |
| template_type: breaking が 45/45 (100%) | テンプレ選択ロジックが breaking 固定 | 多様性ゼロ |
| FTC開示が products=[] 記事にも付与 | 法的リスク（虚偽の開示） | 公開即トラブル |
| 重複ファイル -2.md が 16/45 (35%) | pipeline の冪等性なし、API費用2倍、SEOペナルティ | 直接的損失 |
| word_count 298-418 に集中 | max_tokens=1024 ハードコード | 長文記事不可 |
| Hacker News 62% 偏重、公式RSS 0% | データソース偏重 | ターゲット外記事大量 |

これらを順次解消する。

---

## 1. Day 2.5 タスクリスト（P0 4件 + P1 3件 + 検証）

### Task P0-1: affiliate_sources.yml への trigger_keywords 配置確認

**前提**: Hiro が `data/affiliate_sources.yml` を Day 2.5 版に差し替え済み。9プログラム全てに `trigger_keywords` と `category` フィールドが追加されている。

**確認コマンド**:
```bash
cd ~/ai-pulse
python3 -c "
import yaml
with open('data/affiliate_sources.yml') as f:
    data = yaml.safe_load(f)
for pid, p in data['programs'].items():
    if 'trigger_keywords' in p:
        print(f'{pid}: {len(p[\"trigger_keywords\"])} keywords, category={p.get(\"category\", [])}')"
```

期待出力: 9プログラム全てに trigger_keywords があること。

**思い込み禁止チェック**:
- [ ] `confidence: green` のプログラムだけ運用対象に含めること（red は除外）
- [ ] `tier: 2` の Kinsta/Liquid Web も含まれているか確認（Day 2 では tier 1 のみ想定だったが、ここで catalog 全体を整備）
- [ ] verification_log に Day 2.5 改修記録が追記されているか

---

### Task P0-2: pipeline 冪等性の確保

**問題**: 同じ URL/トピックで `-2.md` 重複ファイルが 16/45 件発生。SeenArticleStore が `pipeline/run.py` で使われていない。

**修正方針**:

`src/pipeline/run.py` で記事生成前に以下チェック：

1. **URL ベース重複検出**: `data/seen_articles.db` の `seen_articles` テーブルに同 URL がすでに記録されているか
2. **ファイル名ベース重複検出**: `output/articles/{slug}.md` が既に存在するか（slug は title から正規化）
3. **両方ヒットしたらスキップ**（生成しない、API費用節約）

**思い込み禁止チェック**:
- [ ] Day 1 で実装した `SeenArticleStore` のメソッドシグネチャを確認（`mark_seen(article_id, source, title, url)`）
- [ ] mark_seen は **記事生成完了後** に呼ぶ（生成失敗時のリトライを許すため）
- [ ] slug 生成ロジックは既存の claude_writer.py から流用

**完了条件**:
```bash
# 同じパイプラインを2回実行
rm -rf output/articles_test/
python -m src.pipeline.run --output-dir output/articles_test
count1=$(ls output/articles_test/*.md 2>/dev/null | wc -l)
python -m src.pipeline.run --output-dir output/articles_test
count2=$(ls output/articles_test/*.md 2>/dev/null | wc -l)
echo "1回目: $count1 件、2回目: $count2 件"
echo "期待: 2回目は新規追加のみ (差分 < 5 件)"
```

---

### Task P0-3: FTC開示の条件化

**問題**: `products: []` の記事 45/45 全件に "*Disclosure: This article contains affiliate links*" が付与されている。これは **虚偽の開示** で FTC 規制違反リスク。

**修正方針**:

`src/processors/claude_writer.py` の FTC 開示生成箇所で、`products` リストが空かどうかで分岐：

```
if products:
    insert "*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*"
else:
    # 開示なし、または以下の中立文言:
    insert "*This article does not contain affiliate links.*"
    # ※「アフィリ無し」を明示するかは品質判断。最低限「affiliate links 含む」と書かない
```

**思い込み禁止チェック**:
- [ ] FTC 規則の正式名: 「FTC Endorsement Guides」（https://www.ftc.gov/business-guidance/resources/ftc-endorsement-guides-what-people-are-asking）
- [ ] 「アフィリ無し」と明示するか、開示文自体を出さないかは Hiro 判断で決定
- [ ] 既存45記事の処分（P1-7）と連動

---

### Task P0-4: importance_scorer プロンプト改善

**問題**: 全記事 score=50、category=other → Claude Haiku が JSON を返しても中身がデフォルト値のまま。

**修正方針**:

1. **スコアを離散値強制**: プロンプトに「Score must be one of: 0, 20, 40, 60, 80, 100」と明示
2. **カテゴリを enum 強制**: 以下から1つ必須選択
   ```
   - model_release       (新モデル発表)
   - feature_update      (機能追加)
   - pricing_change      (価格改定)
   - sdk_release         (SDKリリース)
   - research_paper      (研究論文)
   - tool_launch         (新ツール発表)
   - industry_news       (業界ニュース)
   - tutorial            (チュートリアル)
   - opinion             (意見記事)
   - off_topic           (AI業界外)
   ```
3. **products_mentioned 強制抽出**: 記事に含まれる製品名を `affiliate_sources.yml` の `competes_with` と照合
4. **JSON Schema 検証**: 返ってきた JSON が以下を満たすか確認、満たさない場合は1度だけ再試行
   - score in [0, 20, 40, 60, 80, 100]
   - category in [上記10種類]
   - products_mentioned is list

**プロンプト追加例（実装時に Claude Code が調整）**:
```
You are scoring an AI industry news article for relevance to AI tool buyers.

SCORE (must be one of 0/20/40/60/80/100):
- 100: Major new model launch (GPT-5, Claude Opus 5)
- 80: Price changes, major new features, SDK major versions
- 60: New product launches, important tutorials
- 40: Research papers, technical blog posts
- 20: Generic industry news, opinion pieces
- 0: Off-topic, not AI related

CATEGORY (must be exactly one):
model_release | feature_update | pricing_change | sdk_release | research_paper | tool_launch | industry_news | tutorial | opinion | off_topic

OUTPUT FORMAT (strict JSON):
{"score": int, "category": string, "products_mentioned": [string], "reason": string}
```

**思い込み禁止チェック**:
- [ ] Haiku 4.5 が JSON Schema 厳守できるか、3記事でテスト
- [ ] 厳守できない場合は Sonnet 4.5 にアップグレード検討（コスト 5倍）
- [ ] スコア分散テスト: 10記事処理して、最頻値が50に集中しないこと

**完了条件**:
```bash
# 10記事で実行、スコア分布を確認
python -m src.processors.importance_scorer --test-batch 10
# 期待: 0/20/40/60/80/100 のうち、最低3種類以上が出現
```

---

### Task P1-5: template_type 動的選択

**問題**: 全記事 breaking 固定。

**修正方針**:

`src/processors/claude_writer.py` でテンプレ選択ロジック：

```
- breaking:    importance_score >= 80 AND category in [model_release, pricing_change]
- comparison:  category in [tool_launch] AND products_mentioned has 2+ items
- explainer:   category in [research_paper, sdk_release, tutorial]
- breaking:    上記いずれにも該当しない場合のデフォルト
```

**思い込み禁止チェック**:
- [ ] 各テンプレが少なくとも1記事は使われるか、10記事バッチで確認
- [ ] comparison が出る条件（製品2つ以上）は厳しすぎないか確認

---

### Task P1-6: max_tokens テンプレ別動的化

**問題**: max_tokens=1024 ハードコード → 全記事 298-418 word に収束。

**修正方針**:

`claude_writer.py` でテンプレ別に動的化：

```python
TEMPLATE_MAX_TOKENS = {
    "breaking":   1024,   # 200-400 word
    "comparison": 2048,   # 500-900 word
    "explainer":  3072,   # 700-1200 word
}
```

**思い込み禁止チェック**:
- [ ] Haiku 4.5 の最大 output tokens を公式確認（200K context, output 上限は4096 ~ 8192の可能性）
- [ ] 公式: https://docs.anthropic.com/en/docs/about-claude/models
- [ ] 上限超過時はエラー、上限内なら設定通り出力されること

---

### Task P1-7: 既存45記事の処分

**問題**: 現在の45記事は全て品質基準を満たさない（products:[], category:other, テンプレ固定, 重複あり）。Day 2.5 の改修テストで混在すると検証ができない。

**修正方針**:

```bash
cd ~/ai-pulse

# バックアップ作成（万一のため）
mkdir -p output/articles_day2_archive
mv output/articles/*.md output/articles_day2_archive/

# seen_articles.db もリセット（同じトピックを Day 2.5 で再生成するため）
rm -f data/seen_articles.db

# 確認
ls output/articles/ 2>/dev/null | wc -l
# 期待: 0

ls output/articles_day2_archive/ | wc -l
# 期待: 45
```

**思い込み禁止チェック**:
- [ ] 削除ではなくアーカイブ移動（万一のロールバック用）
- [ ] seen_articles.db 削除後、Day 2.5 再実行で過去のトピックが再ピックアップされること

---

## 2. Day 2.5 完了判定（CLAUDE.md 0.1.2 採点規則 適用）

### 軸A: テスト/プロセス品質（配点 40）

| 評価項目 | 配点 | 判定基準 |
|---|---|---|
| 機能要件の充足 | 15 | P0-1〜P0-4 + P1-5〜P1-7 全タスク完了 |
| ユニットテスト全通過 | 10 | pytest 全通過、新規テスト追加（FTC条件、冪等性、スコア分散） |
| 思い込み禁止チェック実施率 | 5 | 各タスクのチェックリストを実施 |
| トークン節約 | 5 | 半日以内に完了 |
| ドキュメント整合性 | 5 | CLAUDE.md 変更履歴に Day 2.5 記録 |

### 軸B: 実出力品質（配点 60）★ Day 2 で欠けていた軸

**実行コマンド**: パイプライン1回実行後、生成された記事に対して以下を測定：

```bash
cd ~/ai-pulse

# パイプライン実行
python -m src.pipeline.run

# 採点用集計
echo "=== 軸B 採点集計 ==="
echo "全記事: $(ls output/articles/*.md | wc -l)"

# B-1: 商品マッチ率
match_count=$(grep -L '^products: \[\]' output/articles/*.md | wc -l)
total=$(ls output/articles/*.md | wc -l)
echo "B-1 商品マッチあり: $match_count / $total ($(echo "scale=1; $match_count * 100 / $total" | bc)%)"

# B-2 カテゴリ多様性
echo "B-2 カテゴリ分布:"
grep -h '^category:' output/articles/*.md | sort | uniq -c

# B-3 スコア分散
echo "B-3 importance_score 分布:"
grep -h '^importance_score:' output/articles/*.md | awk -F: '{print $2}' | sort -n | uniq -c

# B-4 テンプレ多様性
echo "B-4 template_type 分布:"
grep -h '^template_type:' output/articles/*.md | sort | uniq -c

# B-5 重複ファイル
echo "B-5 重複ファイル ('-2.md'): $(ls output/articles/*-2.md 2>/dev/null | wc -l)"

# B-6 FTC開示の妥当性
echo "B-6 products=[] かつ Disclosure 付き記事:"
for f in output/articles/*.md; do
  if grep -q '^products: \[\]' "$f" && grep -q "contains affiliate links" "$f"; then
    echo "  問題あり: $(basename $f)"
  fi
done | head -5
```

**配点基準（実物検査）**:

| 評価項目 | 配点 | 合格基準 |
|---|---|---|
| B-1: 商品マッチ率 | 20 | match_count / total ≥ 30%（残り70%は AI業界周辺だが直接マッチしないHN記事等）|
| B-2: カテゴリ多様性 | 8 | 3カテゴリ以上が出現 |
| B-3: スコア分散 | 7 | 最頻値が50に集中せず、3スコア以上で分散 |
| B-4: テンプレ多様性 | 8 | breaking 以外が最低1件 |
| B-5: 重複ゼロ | 10 | `-2.md` が 0 件 |
| B-6: FTC開示の妥当性 | 5 | products=[] 記事に "contains affiliate links" 付与 = 0 件 |
| B-7: 公開可能レベル | 2 | サンプル3記事を読んで読み物として成立 |

**合計**: 軸A 40 + 軸B 60 = 100

**合格ライン**:
- 総合 ≥ 80
- かつ 軸B ≥ 30（軸B単独30未満は自動不合格、CLAUDE.md 0.1.2）

### Day 2.5 完了レポート（必須提出）

`docs/day2_5_completion_report.md` に以下を必ず記載：

1. **軸A 採点と根拠**（各項目の点数と理由）
2. **軸B 採点と根拠**（実測コマンド出力と判定）
3. **軸B 集計コマンド出力の貼り付け**（B-1〜B-6）
4. **思い込み禁止チェックの実施結果**（各タスクのチェックリスト）
5. **Day 3 への引き継ぎ事項**

---

## 3. やらないこと（Day 3 以降に繰り越し）

- Cloudflare Pages 実デプロイ
- アフィリ申請（Perplexity / ElevenLabs / Notion）
- Anthropic/Meta/Mistral/Cursor/Perplexity の代替スクレイパー
- 二次媒体（TechCrunch等）の追加
- X 投稿パイプライン
- Beehiiv ニュースレター

Day 2.5 は **生成パイプラインの品質改善** に集中。

---

## 4. 困ったときの対応

### 4.1 Haiku 4.5 が JSON Schema を守らない
- 1度だけ再試行、それでもダメなら Sonnet 4.5 にアップグレード
- コスト増は許容（Day 2.5 の検証段階）

### 4.2 商品マッチ率が30%に届かない
- データソース側の問題（HN偏重）の可能性
- Hacker News フィルタを厳格化（AI製品名・企業名で絞る）
- それでもダメなら trigger_keywords を追加

### 4.3 既存テストが壊れる
- Day 1, Day 2 で追加した既存テストの想定が変わる可能性
- 期待値を新仕様に合わせて更新
- ただし**テストパスのために本来の品質基準を緩めない**

### 4.4 トークンが想定以上に消費される
- Day 2.5 は max 7時間想定
- 超えたら Hiro に状況報告、Day 2.6 に分割

---

## 5. このドキュメントの品質維持

不正確な記述・実装中に判明した思い込みを発見したら：

1. 該当箇所を引用
2. 修正案を提示
3. `docs/day2_5_completion_report.md` に記録

特に「採点規則 0.1.2 の軸B 評価項目」自体が実装後にずれていた場合は、CLAUDE.md 0.1.2 の修正も提案する。
