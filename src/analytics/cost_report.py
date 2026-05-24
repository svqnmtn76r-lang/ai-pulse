"""API cost tracking and reporting."""

import sqlite3
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

DB_PATH = Path("data/api_calls.db")
PRICING_CONFIG = Path("config/api_pricing.yml")


def init_db():
    """Initialize api_calls table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            module TEXT NOT NULL,
            model TEXT NOT NULL,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cost_usd REAL,
            success BOOLEAN
        )
    """)
    conn.commit()
    conn.close()


def load_pricing() -> dict:
    """Load pricing config from api_pricing.yml."""
    with open(PRICING_CONFIG) as f:
        config = yaml.safe_load(f)
    return config["models"]


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate API call cost in USD."""
    pricing = load_pricing()
    if model not in pricing:
        raise ValueError(f"Unknown model: {model}")

    model_pricing = pricing[model]
    input_cost = (input_tokens / 1_000_000) * model_pricing["input_price_per_mtok"]
    output_cost = (output_tokens / 1_000_000) * model_pricing["output_price_per_mtok"]
    return round(input_cost + output_cost, 6)


def log_api_call(
    module: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    success: bool = True,
    timestamp: Optional[str] = None,
) -> float:
    """Log API call and return cost."""
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat() + "Z"

    cost = calculate_cost(model, input_tokens, output_tokens)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO api_calls (timestamp, module, model, input_tokens, output_tokens, cost_usd, success)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, module, model, input_tokens, output_tokens, cost, success))
    conn.commit()
    conn.close()

    return cost


def get_daily_summary(days_back: int = 7) -> dict:
    """Get cost summary for last N days."""
    cutoff = (datetime.utcnow() - timedelta(days=days_back)).isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(timestamp) as date, module, COUNT(*) as calls, SUM(cost_usd) as total_cost
        FROM api_calls
        WHERE timestamp >= ?
        GROUP BY date, module
        ORDER BY date DESC
    """, (cutoff,))

    rows = cursor.fetchall()
    conn.close()

    summary = {}
    for date, module, calls, cost in rows:
        if date not in summary:
            summary[date] = {}
        summary[date][module] = {"calls": calls, "cost": round(cost, 4)}

    return summary


def print_cost_report(days_back: int = 7):
    """Print human-readable cost report."""
    summary = get_daily_summary(days_back)

    print(f"\n=== API Cost Report (Last {days_back} Days) ===\n")

    total_cost = 0.0
    for date in sorted(summary.keys(), reverse=True):
        modules = summary[date]
        day_cost = sum(m["cost"] for m in modules.values())
        total_cost += day_cost

        print(f"{date}: ${day_cost:.4f}")
        for module, data in modules.items():
            print(f"  {module}: {data['calls']} calls, ${data['cost']:.4f}")

    print(f"\nTotal: ${total_cost:.4f}")
    print()


if __name__ == "__main__":
    init_db()
    print_cost_report()
