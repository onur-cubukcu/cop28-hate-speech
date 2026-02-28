"""
demo.py  –  Run the pipeline with synthetic sample data (no Apify/HF needed).

This is useful for testing the Excel output and chart generation locally
before running against real scraped data.
"""

import json, random, string, os, sys
from pathlib import Path

# Ensure we can import from the same directory
sys.path.insert(0, str(Path(__file__).parent))

from pipeline import save_excel, make_charts
import pandas as pd

SAMPLE_TWEETS = [
    ("This COP28 conference is crucial for our planet's future. #COP28 #ClimateAction", 0),
    ("Great discussions happening at #COP28. Hope for real commitments!", 0),
    ("These climate activists are idiots destroying the economy. #COP28", 1),
    ("The whole COP28 is a useless scam run by hypocrites. #COP28", 1),
    ("I'll find you climate freaks and make you pay. #COP28", 2),
    ("Important milestone for green energy transition at #COP28", 0),
    ("Scientists warn: we must act NOW. #COP28 #ClimateCrisis", 0),
    ("This conference is a waste of money. Politicians talking, nothing changes.", 1),
]

random.seed(42)

def make_sample_df(n: int = 200) -> pd.DataFrame:
    rows = []
    for i in range(n):
        text, label = random.choice(SAMPLE_TWEETS)
        rows.append({
            "id":         f"tweet_{i:04d}",
            "created_at": f"2023-12-{random.randint(1,13):02d}",
            "author":     "user_" + "".join(random.choices(string.ascii_lowercase, k=5)),
            "text":       text,
            "retweets":   random.randint(0, 500),
            "likes":      random.randint(0, 2000),
            "label_id":   label,
            "label_name": {0: "Neutral", 1: "Offensive", 2: "Hate"}[label],
            "confidence": round(random.uniform(0.70, 0.99), 4),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Generating synthetic demo data …")
    df = make_sample_df(200)

    os.makedirs("demo_output", exist_ok=True)
    save_excel(df, "demo_output/demo_results.xlsx")
    make_charts(df, "demo_output/charts", tag="#COP28 (demo)")

    print("\nDemo complete.  Check the 'demo_output/' folder.")
