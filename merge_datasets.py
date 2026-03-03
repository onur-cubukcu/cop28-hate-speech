"""
merge_datasets.py
-----------------
Merges multiple daily Apify JSON exports into a single deduplicated
tweets.json, keeping only English tweets.

Usage:
    python merge_datasets.py day1.json day2.json day3.json ...

Output:
    tweets.json  (English only, deduplicated, ready for pipeline.py)
"""

import json
import sys
from pathlib import Path


def merge(files):
    seen_ids   = set()
    all_tweets = []
    skipped_lang  = 0
    skipped_dupes = 0

    for filepath in files:
        path = Path(filepath)
        if not path.exists():
            print(f"[warn] File not found, skipping: {filepath}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        file_added = 0
        for tweet in data:
            # --- Language filter: keep only English ---
            lang = tweet.get("tweet", {}).get("lang", "") or tweet.get("lang", "")
            if lang != "en":
                skipped_lang += 1
                continue

            # --- Deduplicate by ID ---
            tweet_id = str(tweet.get("id") or tweet.get("id_str") or "")
            if tweet_id and tweet_id in seen_ids:
                skipped_dupes += 1
                continue

            seen_ids.add(tweet_id)
            all_tweets.append(tweet)
            file_added += 1

        print(f"[{path.name}]  +{file_added} English tweets  (total: {len(all_tweets)})")

    output = Path("tweets.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=2)

    print(f"\n=== Merge complete ===")
    print(f"  Kept (English, unique): {len(all_tweets)}")
    print(f"  Skipped (non-English):  {skipped_lang}")
    print(f"  Skipped (duplicates):   {skipped_dupes}")
    print(f"\n  Saved to '{output}'")
    print("  You can now run:  python pipeline.py --input tweets.json --output results.xlsx")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_datasets.py day1.json day2.json ...")
        sys.exit(1)
    merge(sys.argv[1:])
