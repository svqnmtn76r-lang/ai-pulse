#!/usr/bin/env python3
"""Phase 4 DRY SIMULATION — run N consecutive "days" of the pipeline's commercial
arm against the topic pool, IN MEMORY (no disk writes, no API, no publish).

Each simulated day:
  1. top-up the pool (plan_replenishment) BEFORE selection — exactly as
     run_pipeline Step 0 does;
  2. select K = product_cadence_count(news) fresh topics top-down (the cadence);
  3. mark them "published" (consumed).

Invariants checked:
  * the pool never empties (>=1 commercial topic available every day);
  * ZERO duplicate slugs are ever produced (no topic consumed twice, none
    colliding with an already-published article).

Usage: PYTHONPATH=. python scripts/simulate_topic_pool.py [days] [news_per_day]
Defaults: days=10, news_per_day=15  (-> K=5/day at the 0.25 commercial target).
Exit 0 = all invariants hold; 1 = a violation (pool emptied or a duplicate).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from src.processors.claude_writer import create_slug
from src.pipeline.run import product_cadence_count
from src.pipeline import topic_pool as tp


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    news = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    K = product_cadence_count(news)

    # Snapshot real starting state (copies — disk is never touched).
    pool = [dict(t) for t in tp.load_pool()]
    pub_slugs = set(tp.published_slugs())
    pub_titles = list(tp.published_titles())

    consumed_all = []          # every slug produced by the commercial arm
    total_generated = 0
    total_warns = 0
    ok = True

    print(f"SIMULATION: {days} days, news={news}/day -> K={K} commercial articles/day")
    print(f"start: pool={len(pool)} fresh={tp._fresh_count(pool, pub_slugs)} "
          f"(LOW={tp._low_threshold()} TARGET={tp._target_buffer()})")
    print("-" * 86)
    print(f"{'day':>3} {'fresh→topup':>12} {'+add':>5} {'fresh':>6} "
          f"{'make':>5} {'left':>5} {'newdups':>8} {'warn':>5}")
    print("-" * 86)

    for day in range(1, days + 1):
        # 1) top-up (in memory)
        to_add, fresh_before, reserve, warn = tp.plan_replenishment(pool, pub_slugs, pub_titles)
        pool.extend(to_add)
        total_generated += len(to_add)
        if warn:
            total_warns += 1

        # 2) select K fresh topics top-down (mirrors the cadence)
        fresh_topics = [t for t in pool
                        if create_slug((t.get("title") or "").strip()) not in pub_slugs
                        and (t.get("title") or "").strip()]
        fresh_after_topup = len(fresh_topics)
        make = fresh_topics[:K]

        # 3) consume — detect any duplicate slug at point of production
        newdups = 0
        for t in make:
            s = create_slug(t["title"].strip())
            if s in pub_slugs or s in consumed_all:
                newdups += 1
                ok = False
            consumed_all.append(s)
            pub_slugs.add(s)
            pub_titles.append(t["title"].strip())

        left = fresh_after_topup - len(make)
        if fresh_after_topup < 1:
            ok = False
        print(f"{day:>3} {fresh_before:>12} {len(to_add):>5} {fresh_after_topup:>6} "
              f"{len(make):>5} {left:>5} {newdups:>8} {'YES' if warn else '-':>5}")

    print("-" * 86)
    uniq = len(set(consumed_all))
    dup_total = len(consumed_all) - uniq
    print(f"commercial articles produced : {len(consumed_all)}  (unique slugs: {uniq})")
    print(f"DUPLICATE slugs produced     : {dup_total}   <-- MUST be 0")
    print(f"topics auto-generated        : {total_generated}")
    print(f"days a low-supply warning fired: {total_warns}")
    print(f"pool never emptied           : {ok and dup_total == 0}")
    print("=" * 86)
    print("RESULT:", "PASS" if (ok and dup_total == 0) else "FAIL")
    return 0 if (ok and dup_total == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
