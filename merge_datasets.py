"""
merge_datasets.py
-----------------
Merges multiple Apify JSON exports into one deduplicated English-only file.
Supports both old (altimis/scweet) and new (apidojo/twitter-scraper-lite) formats.

Usage:
    python merge_datasets.py file1.json file2.json ...
"""

import json
import sys
from pathlib import Path


def get_lang(item):
    """Get language from either actor format."""
    if "createdAt" in item:
        return item.get("lang", "")
    else:
        if isinstance(item.get("tweet"), dict):
            return item["tweet"].get("lang", "")
        return item.get("lang", "")


def get_id(item):
    """Get tweet ID from either actor format."""
    return str(item.get("id") or item.get("id_str") or "")


def merge(files):
    seen_ids      = set()
    all_tweets    = []
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
            if get_lang(tweet) != "en":
                skipped_lang += 1
                continue

            tweet_id = get_id(tweet)
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
        print("Usage: python merge_datasets.py file1.json file2.json ...")
        sys.exit(1)
    merge(sys.argv[1:])
