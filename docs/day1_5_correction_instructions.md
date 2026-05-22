# Day 1.5 修正タスク指示書

> Day 1完了後の実検証で判明した思い込み（RSS 8つ中5つが公式RSSなし）を訂正する。
> 工数最小、トークン節約優先。

## 背景

Day 1 で実装したRSS監視は 8 フィード設定だが、実検証で 3 つしか動作していなかった：

| フィード | 結果 |
|---|---|
| openai | ✅ 200 |
| google_deepmind | ✅ 200 |
| huggingface | ✅ 200 |
| anthropic | ❌ 404（公式RSSなし） |
| meta_ai | ❌ 404（公式RSSなし） |
| mistral | ❌ 404（公式RSSなし） |
| cursor | ❌ 404（公式RSSなし） |
| perplexity | ❌ 403（Bot拒否） |

## タスク

### Task A: CLAUDE.md 差し替え（所要1分）

Hiroが手動配置済み。確認のみ：

```bash
cd ~/ai-pulse
grep -c "verified: 2026-05-22" CLAUDE.md
# 期待出力: 1 以上（修正版が配置済み）
```

### Task B: data/rss_feeds.yml 差し替え（所要1分）

Hiroが手動配置済み。検証：

```bash
cd ~/ai-pulse
grep -c "verified_official_rss" data/rss_feeds.yml
# 期待出力: 2（key定義と参照）
```

### Task C: rss_monitor.py を新スキーマ対応（所要15分）

現状の load_feeds() は旧スキーマ（`official_ai_companies` / `tool_makers`）を読んでいる。
新スキーマ（`verified_official_rss`）に変更。

**思い込み禁止チェック**: 既存テスト `tests/test_rss_monitor.py` が新スキーマに対応しているか確認、未対応なら更新。

修正案：

```python
def load_feeds(config_path: Path = Path("data/rss_feeds.yml")) -> dict:
    """data/rss_feeds.yml の verified_official_rss セクションのみを読む。
    
    no_official_rss セクションは Phase 2 で個別スクレイパー実装するため、
    rss_monitor.py の対象外。
    """
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    feeds = {}
    verified = data.get("verified_official_rss", {})
    for name, info in verified.items():
        if isinstance(info, dict) and "url" in info:
            feeds[name] = info["url"]
    return feeds
```

完了条件: `python -m src.sources.rss_monitor` を実行すると 3 フィードのみポーリングされ、エラーゼロ。

### Task D: 動作確認（所要5分）

```bash
cd ~/ai-pulse
source .venv/bin/activate
rm -f data/seen_articles.db  # 既出DBをリセット
python -m src.sources.rss_monitor 2>&1 | head -50
```

期待: 3 フィードから記事取得、エラーログなし、SQLite に記録。

### Task E: テスト更新（所要10分）

`tests/test_rss_monitor.py` の以下を修正：

- `test_load_feeds_includes_anthropic` を削除または `test_load_feeds_includes_openai` に変更
- 新たに `test_load_feeds_returns_only_verified` を追加（3 フィード返ることを確認）

```bash
pytest tests/ -v
# 全テスト通過すること
```

### Task F: コミット（所要1分）

```bash
git add CLAUDE.md data/rss_feeds.yml src/sources/rss_monitor.py tests/
git commit -m "fix: correct RSS feed sources after empirical verification

8つ中5つの公式RSSが存在しないことが判明（HTTPで404/403確認）。
- verified_official_rss セクションに動作確認済み3フィードを集約
- no_official_rss セクションに代替手段リスト追加
- rss_monitor.py を新スキーマ対応
- CLAUDE.md 5節を実検証ベースに改訂"
```

## 完了条件サマリー

- [ ] CLAUDE.md 5節が「verified_official_rss」「no_official_rss」構造に
- [ ] data/rss_feeds.yml が新スキーマ
- [ ] rss_monitor.py が3フィードを読む
- [ ] python -m src.sources.rss_monitor がエラーゼロで完了
- [ ] pytest 全通過
- [ ] git commit 完了

## やらないこと（Day 2 へ繰り越し）

- Anthropic/Meta/Mistral/Cursor/Perplexity の代替スクレイパー実装
- 二次媒体（TechCrunch等）の追加
- Hacker News API 統合

これらは Day 2 タスクとして別途設計。

## 採点（Day 1.5 完了後）

| 軸 | 配点 | 達成基準 |
|---|---|---|
| 思い込み訂正の完全性 | 30 | CLAUDE.md/yml/code/test の4箇所すべて訂正されたか |
| 既存テストの維持 | 20 | pytest 全通過 |
| トークン節約 | 20 | 30分以内に完了したか |
| ドキュメント整合性 | 15 | 変更履歴に記録、コミットメッセージ明確 |
| Day 2 への準備 | 15 | Phase 2 タスクが明確に分離されているか |
| **合計** | **100** | **80点以上で Day 2 へ移行可能** |
