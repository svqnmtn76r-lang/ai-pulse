# AI-Pulse Day 1 実行指示書（Claude Code 用）

> このドキュメントは Claude Code が AI-Pulse プロジェクトの Day 1 タスクを
> **思い込みを排除しつつ、トークンを節約しながら** 完遂するための指示書です。
>
> Hiroが Claude Code を起動したら、まず `CLAUDE.md` を読み、次にこのファイル
> (`docs/day1_instructions.md`) を読んでから着手してください。

---

## 0. 絶対遵守ルール

### 0.1 思い込み禁止チェックポイント

以下のタイミングで**必ず立ち止まって確認**すること：

| タイミング | 確認内容 |
|---|---|
| 各タスクの開始時 | 「このタスクの完了条件は何か？」を1行で記述してから着手 |
| API/ライブラリの選定時 | requirements.txt にバージョンを書く前に `pip index versions <pkg>` で最新を確認 |
| 外部APIのエンドポイント記述時 | 公式ドキュメントのURLを WebFetch で1回だけ確認 |
| 環境変数名を決める時 | 既存 AutoAffil の命名規則と一致しているか確認（X_CONSUMER_KEY等のパターン） |
| ファイル作成時 | 同名ファイルが既に存在しないか `ls` で確認 |
| コミット前 | `git status` で意図しないファイルが含まれていないか確認 |

### 0.2 トークン節約ルール

| 行動 | 推奨 | 禁止 |
|---|---|---|
| ファイル一覧 | `ls -la` 単発 | 再帰的な `tree` を全リポに適用 |
| ファイル内容確認 | `head -50` or 特定行範囲 | 大きいファイルの全文read |
| 依存関係インストール | `requirements.txt` 一括 | 個別 pip install ×複数回 |
| テスト実行 | 単一テスト関数を指定 | リポ全体のpytest |
| ログ確認 | `tail -50` | 全ログ表示 |
| Web検索 | このドキュメント内で完結 | 不要な追加検索 |

ただし、**確実性を犠牲にしてまでトークン節約しない**。判断に迷ったら確実性を優先。

### 0.3 確実性ラベル運用

このドキュメント内の指示で出てくる数値・コマンド・URLには信頼度ラベルを付けている：

- 🟢: 公式ドキュメント or 検証済み
- 🟡: 一般的だが要確認
- 🔴: 推測、必ず実行前に確認

---

## 1. 前提確認（着手前に必ず実行）

### 1.1 環境チェック

```bash
# 以下を実行して、各項目の出力を確認
python3 --version          # 3.10以上であること 🟢
git --version              # 任意のバージョン 🟢
node --version             # 18以上推奨（Astro用）🟡
gh --version               # GitHub CLI 🟡
ls ~/sns-affiliate-system  # AutoAffil既存リポ存在確認 🟢
```

### 1.2 Hiroに確認が必要なもの（揃ってなければ作業中断して質問）

- [ ] ドメイン取得済みか？（候補：ai-pulse.dev, aipulse.news, aipulse-stack.com）
- [ ] GitHubの新規リポ `ai-pulse` 作成済みか？
- [ ] X新規アカウント作成済みか？
- [ ] 環境変数として以下が手元にあるか？
  - `ANTHROPIC_API_KEY`（既存）
  - `GH_TOKEN`（GitHub Releases監視用、`repo:read` スコープ）
  - X系（`X_CONSUMER_KEY`等、新規アカウント分）← Day 1 後半でOK

揃っていない項目があれば、**勝手に代替策で進めずに Hiro に確認**してください。

---

## 2. Day 1 タスクリスト

トークン節約のため、各タスクは「完了条件」を明示し、達成したら次へ進む。
無駄なreadme出力やverboseログは省く。

### Task 1: リポ初期化（所要15分）

**完了条件**: `git status` がclean、最初のコミットが作成されている

```bash
cd ~  # or 任意の作業ディレクトリ
git clone git@github.com:<Hiroのユーザー名>/ai-pulse.git
cd ai-pulse

# 既に CLAUDE.md と data/affiliate_sources.yml が
# Hiroによって配置されている前提（前ターンで作成済み）
# 配置されていなければHiroに確認

ls -la  # CLAUDE.md と data/affiliate_sources.yml の存在確認

# .gitignore 作成
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env
.env.local
.venv/
venv/
env/
.pytest_cache/
.coverage
htmlcov/
*.db
*.sqlite
*.sqlite3
node_modules/
.astro/
dist/
.DS_Store
*.log
data/seen_articles.db
.claude/
EOF

# 最小限の README.md（後で拡張）
cat > README.md << 'EOF'
# AI-Pulse

AI業界速報×高単価アフィリエイトの自動化システム。

詳細は `CLAUDE.md` 参照。
EOF

git add .gitignore README.md
git commit -m "chore: initial repo structure"
```

**確認**: `git log --oneline` で1コミットあること。

---

### Task 2: Python環境セットアップ（所要10分）

**完了条件**: `pip install -r requirements.txt` がエラーなく完了

```bash
# venv作成（既存のAutoAffilのvenvと分離）
python3 -m venv .venv
source .venv/bin/activate

# requirements.txt 作成
# 注意: バージョンは執筆時(2026年5月)の安定版を指定するが、
#       pip install 実行時にエラーが出たら最新版に変更すること
cat > requirements.txt << 'EOF'
# Core
anthropic>=0.40.0
feedparser>=6.0.11
requests>=2.32.0
PyYAML>=6.0.2
python-dotenv>=1.0.1

# Data
pydantic>=2.9.0

# Logging
structlog>=24.4.0

# Testing
pytest>=8.3.0
pytest-mock>=3.14.0

# X (Twitter) API - 後で必要
tweepy>=4.14.0
EOF

pip install -r requirements.txt
```

**思い込み禁止チェック**: 
- バージョンが取得できない/install失敗するパッケージがあれば、`pip index versions <パッケージ名>` で利用可能なバージョンを確認してから修正する
- 勝手に他のパッケージで代替しない

---

### Task 3: ディレクトリ構造作成（所要5分）

**完了条件**: `CLAUDE.md` 4節の構造と一致

```bash
# CLAUDE.md 4節「リポ構造」と照合してから実行すること
mkdir -p src/{sources,processors,publishers,affiliates,analytics,utils}
mkdir -p .github/workflows
mkdir -p blog/src
mkdir -p templates
mkdir -p tests
mkdir -p docs

# __init__.py 作成
for dir in src src/sources src/processors src/publishers src/affiliates src/analytics src/utils; do
    touch $dir/__init__.py
done

# 確認
find . -type d -not -path './.git*' -not -path './.venv*' | sort
```

**思い込み禁止チェック**: `CLAUDE.md` の4節と上記出力を目視で照合。差異があればCLAUDE.mdを優先し、ディレクトリを調整。

---

### Task 4: RSS監視 PoC 実装（所要45分）

**完了条件**: `python -m src.sources.rss_monitor` を実行して、新規記事のリストがJSON形式で標準出力に出る

これは Day 1 の **最重要タスク**。ここが動けば全パイプラインの起点ができる。

#### 4.1 RSSフィード設定ファイル

```bash
cat > data/rss_feeds.yml << 'EOF'
# AI業界公式RSSフィード
# 確実性ラベル: 全て🟢（前ターンで実在確認済み）
# ただし、URLが変わっている可能性は常にあるため、初回実行時にエラーがあれば
# 個別に WebFetch で公式サイトのRSS位置を再確認すること

official_ai_companies:
  openai:
    url: https://openai.com/news/rss.xml
    confidence: green
  anthropic:
    url: https://www.anthropic.com/news/rss.xml
    confidence: green
  google_deepmind:
    url: https://deepmind.google/blog/rss.xml
    confidence: green
  meta_ai:
    url: https://ai.meta.com/blog/rss/
    confidence: green
  mistral:
    url: https://mistral.ai/news/feed.xml
    confidence: yellow
  huggingface:
    url: https://huggingface.co/blog/feed.xml
    confidence: green

tool_makers:
  cursor:
    url: https://cursor.com/blog/rss.xml
    confidence: yellow
  perplexity:
    url: https://www.perplexity.ai/hub/feed
    confidence: yellow
EOF
```

#### 4.2 状態管理（SQLite）

```python
# src/utils/state_store.py
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path("data/seen_articles.db")


class SeenArticleStore:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_schema(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS seen_articles (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    title TEXT,
                    url TEXT,
                    seen_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def exists(self, article_id: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "SELECT 1 FROM seen_articles WHERE id = ?", (article_id,)
            )
            return cur.fetchone() is not None

    def mark_seen(self, article_id: str, source: str, title: str, url: str):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seen_articles (id, source, title, url) VALUES (?, ?, ?, ?)",
                (article_id, source, title, url),
            )
            conn.commit()
```

#### 4.3 RSS監視本体

```python
# src/sources/rss_monitor.py
import feedparser
import hashlib
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import yaml
import structlog

from src.utils.state_store import SeenArticleStore

log = structlog.get_logger()


def load_feeds(config_path: Path = Path("data/rss_feeds.yml")) -> dict:
    with open(config_path) as f:
        data = yaml.safe_load(f)
    feeds = {}
    for category in data.values():
        if isinstance(category, dict):
            for name, info in category.items():
                feeds[name] = info["url"]
    return feeds


def parse_pub_date(entry) -> datetime | None:
    """安全に published_parsed をdatetimeに変換"""
    for key in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, key, None)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


def poll_all_sources(window_hours: int = 24) -> list[dict]:
    """全RSSをポーリングして新規記事のみ返す"""
    store = SeenArticleStore()
    feeds = load_feeds()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    new_articles = []

    for source_name, url in feeds.items():
        log.info("polling", source=source_name, url=url)
        try:
            feed = feedparser.parse(url, request_headers={"User-Agent": "ai-pulse/0.1"})
            if feed.bozo and not feed.entries:
                log.warning("feed_parse_failed", source=source_name, error=str(feed.bozo_exception))
                continue

            for entry in feed.entries[:15]:
                article_id = hashlib.md5(entry.link.encode()).hexdigest()
                if store.exists(article_id):
                    continue

                pub = parse_pub_date(entry)
                if pub and pub < cutoff:
                    continue

                article = {
                    "id": article_id,
                    "source": source_name,
                    "title": entry.title,
                    "url": entry.link,
                    "summary": getattr(entry, "summary", "")[:500],
                    "published": pub.isoformat() if pub else None,
                }
                new_articles.append(article)
                store.mark_seen(article_id, source_name, entry.title, entry.link)
        except Exception as e:
            log.error("source_failed", source=source_name, error=str(e))

        time.sleep(0.5)  # マナー

    return new_articles


if __name__ == "__main__":
    articles = poll_all_sources(window_hours=24)
    print(json.dumps(articles, indent=2, ensure_ascii=False))
    log.info("poll_complete", new_count=len(articles))
```

#### 4.4 テスト実行

```bash
# 初回実行（過去24時間の記事を全部取ってくる、これがベースライン）
python -m src.sources.rss_monitor > /tmp/first_poll.json
wc -l /tmp/first_poll.json
head -50 /tmp/first_poll.json

# 2回目実行（既出のため0件になることを確認）
python -m src.sources.rss_monitor > /tmp/second_poll.json
cat /tmp/second_poll.json  # [] が出れば成功
```

**思い込み禁止チェック**:
- 1回目で0件しか出ない場合 → 各RSSのURLが変わっている可能性。`curl -I <RSS_URL>` で200か確認、404なら公式サイトでRSSパスを再確認
- ある特定ソースだけ毎回エラーが出る場合 → そのソースをスキップ（confidence: red に降格）

---

### Task 5: GitHub Releases 監視 PoC（所要20分）

**完了条件**: `python -m src.sources.github_releases` で過去48時間のリリース一覧が出る

```python
# src/sources/github_releases.py
import os
import json
import requests
from datetime import datetime, timedelta, timezone
import structlog

log = structlog.get_logger()

WATCHED_REPOS = [
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    "anthropics/claude-code",
    "langchain-ai/langchain",
    "vercel/ai",
]


def fetch_recent_releases(hours_back: int = 48) -> list[dict]:
    token = os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    new_releases = []

    for repo in WATCHED_REPOS:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=5"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            for release in r.json():
                pub = datetime.strptime(
                    release["published_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
                if pub < cutoff:
                    continue
                new_releases.append({
                    "repo": repo,
                    "tag": release["tag_name"],
                    "title": release.get("name") or release["tag_name"],
                    "body": (release.get("body") or "")[:1000],
                    "url": release["html_url"],
                    "published": pub.isoformat(),
                })
        except Exception as e:
            log.error("repo_fetch_failed", repo=repo, error=str(e))

    return new_releases


if __name__ == "__main__":
    releases = fetch_recent_releases(hours_back=48)
    print(json.dumps(releases, indent=2, ensure_ascii=False))
```

**実行**:
```bash
# GH_TOKEN が設定されていれば認証あり、なくても unauthenticated で動く（60req/h制限）
python -m src.sources.github_releases | head -100
```

**思い込み禁止チェック**: 何件か出るはず。0件の場合は `hours_back=720` （30日）に増やしてテスト。

---

### Task 6: 環境変数テンプレート（所要5分）

```bash
cat > .env.example << 'EOF'
# Required
ANTHROPIC_API_KEY=
GH_TOKEN=

# For X (Twitter) - 新規アカウント作成後に取得
X_CONSUMER_KEY=
X_CONSUMER_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=

# For Beehiiv newsletter (Month 2以降)
BEEHIIV_API_KEY=
BEEHIIV_PUBLICATION_ID=

# For Dub.co affiliate link tracking (Month 1で取得)
DUB_API_KEY=

# Affiliate IDs (取得次第ここに追加)
PERPLEXITY_AFFILIATE_ID=
ELEVENLABS_AFFILIATE_ID=
HUBSPOT_AFFILIATE_ID=
NOTION_AFFILIATE_ID=
EOF

# Hiroが .env を作成（Claude Code側で勝手に作らない）
echo ".env file should be created manually by Hiro with actual values"
```

**思い込み禁止チェック**: `.env` を勝手に作らない。Hiroが値を埋めるべき。

---

### Task 7: 最初のテスト（所要10分）

**完了条件**: `pytest` 実行で全テスト通過

```python
# tests/test_rss_monitor.py
import pytest
from src.sources.rss_monitor import load_feeds, parse_pub_date


def test_load_feeds_returns_dict():
    feeds = load_feeds()
    assert isinstance(feeds, dict)
    assert len(feeds) > 0
    # すべての値がURLであること
    for name, url in feeds.items():
        assert url.startswith("http")


def test_load_feeds_includes_anthropic():
    feeds = load_feeds()
    assert "anthropic" in feeds


def test_parse_pub_date_handles_missing():
    class FakeEntry:
        pass
    assert parse_pub_date(FakeEntry()) is None
```

```python
# tests/test_state_store.py
import pytest
import tempfile
from pathlib import Path
from src.utils.state_store import SeenArticleStore


def test_mark_and_exists():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        store = SeenArticleStore(db_path)
        
        assert not store.exists("abc123")
        store.mark_seen("abc123", "test_source", "Test Title", "https://example.com")
        assert store.exists("abc123")


def test_mark_seen_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        store = SeenArticleStore(db_path)
        
        store.mark_seen("abc123", "s1", "T", "https://x.com")
        store.mark_seen("abc123", "s1", "T", "https://x.com")  # 2回呼んでも問題ないこと
        assert store.exists("abc123")
```

```bash
pytest tests/ -v
```

---

### Task 8: 最初の GitHub Actions ワークフロー（所要15分）

**完了条件**: `poll-news.yml` が GitHub上で手動実行できる状態にコミットされている

```yaml
# .github/workflows/poll-news.yml
name: Poll AI News

on:
  schedule:
    - cron: '*/30 * * * *'  # 30分ごと（無料枠を節約、Day 1は手動実行優先）
  workflow_dispatch:  # 手動実行可能

jobs:
  poll:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Restore seen articles DB
        uses: actions/cache@v4
        with:
          path: data/seen_articles.db
          key: seen-articles-${{ github.run_id }}
          restore-keys: |
            seen-articles-
      
      - name: Poll RSS sources
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          mkdir -p data
          python -m src.sources.rss_monitor > /tmp/articles.json
          echo "New articles found:"
          cat /tmp/articles.json | python -c "import json,sys; print(len(json.load(sys.stdin)))"
      
      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: articles-${{ github.run_id }}
          path: /tmp/articles.json
          retention-days: 7
```

**思い込み禁止チェック**:
- `actions/checkout@v4` と `actions/setup-python@v5` は2026年5月時点で🟢の最新メジャー
- 初回実行前にHiroに「これでcommitしてpushしていいか？」確認
- cron は 30分ごとに設定（CLAUDE.mdでは15分と書いたが、Day 1は無料枠節約のため30分。Month 2以降に頻度上げる）

---

### Task 9: Day 1 完了レポート作成（所要5分）

**完了条件**: `docs/day1_completion_report.md` が作成されている

```bash
cat > docs/day1_completion_report.md << 'EOF'
# Day 1 完了レポート

実行日: <YYYY-MM-DD>

## 完了タスク
- [ ] Task 1: リポ初期化
- [ ] Task 2: Python環境セットアップ
- [ ] Task 3: ディレクトリ構造作成
- [ ] Task 4: RSS監視 PoC
- [ ] Task 5: GitHub Releases 監視 PoC
- [ ] Task 6: 環境変数テンプレート
- [ ] Task 7: 最初のテスト
- [ ] Task 8: GitHub Actions ワークフロー

## 検出された問題
（あれば記載）

## Hiroへの確認事項
- [ ] ドメイン取得
- [ ] X新規アカウント作成
- [ ] アフィリ申請（Perplexity, ElevenLabs, Notion）
- [ ] .env 作成

## 次のステップ
Day 2 で実装予定:
- importance_scorer.py（Claude Haikuで重要度判定）
- claude_writer.py（記事生成）
- affiliate_matcher.py（商品マッチング）
- Astro ブログテンプレ

## 採点
- 完了条件達成率: __/8
- 思い込み禁止チェック: 各タスクで実施したか？: __
EOF
```

最後に commit:

```bash
git add .
git status  # 思い込み禁止: 意図しないファイルが含まれていないか確認
git commit -m "feat: Day 1 - RSS monitor PoC, GitHub releases poller, initial workflow"
git push origin main
```

---

## 3. Day 1 でやらないこと（Day 2以降）

トークン節約と確実性のため、以下は明日以降:

- Claude API での重要度スコアリング（API費用がかかるので、まず無料部分を完成させてから）
- Astro ブログテンプレ（Day 2: フロントエンド設計を別途）
- X投稿パイプライン（X新規アカウント作成待ち）
- アフィリリンクビルダー（アフィリ申請の承認待ち）
- Beehiiv ニュースレター（Month 2）

---

## 4. 困ったときの対応

### 4.1 RSSフィードが404を返す

1. `curl -IL <URL>` でステータス確認
2. リダイレクト先があれば yml 更新
3. 完全に廃止なら confidence: red に降格、別ソース候補をHiroに提案

### 4.2 pip install が失敗する

1. パッケージ名のタイポ確認
2. `pip index versions <pkg>` で利用可能バージョン確認
3. requirements.txt のバージョン制約を緩める（`>=` を一段下げる）
4. それでも失敗したら **勝手に代替パッケージを選ばずに Hiro に確認**

### 4.3 GitHub Actions が失敗する

1. ワークフローログを確認（Hiroにスクショ依頼）
2. ローカルで `act` でテスト（インストールされていれば）
3. シークレットの不足が原因なら、必要なシークレットをHiroに明示して依頼

### 4.4 トークンが想定以上に消費されている

1. 現在のタスクを中断、Hiroに状況報告
2. 残タスクを Day 2 に繰り越す判断を仰ぐ
3. **勝手に低品質な省略形で完遂しない**

---

## 5. 採点（Day 1 完了後にHiroと一緒に実施）

| 軸 | 配点 | 達成基準 |
|---|---|---|
| 完了条件達成率 | 30 | 8タスク中何タスク完了したか × 3.75 |
| 思い込み禁止チェック実施率 | 20 | 各タスクでチェックポイントを実施した割合 |
| トークン節約 | 15 | 想定トークン内で完了したか |
| コード品質 | 20 | テスト通過、型ヒント有無、エラーハンドリング |
| ドキュメント | 15 | 完了レポート作成、各モジュールにdocstring |
| **合計** | **100** | **70点未満なら Day 2 開始前に改善** |

---

## 6. このドキュメント自体の品質維持

このドキュメントを Claude Code が読んで進める中で、**不正確な記述や古い情報** を発見した場合：

1. 該当箇所を引用
2. 修正案を提示
3. Hiro の承認を得てから本ファイルを更新

これにより、Day 2 以降の指示書品質が継続的に向上する。
