# Hate Speech Detection on X During COP28 🌍

> **You are viewing the `scweet` branch** — this version of the pipeline uses the [`altimis/scweet`](https://apify.com/altimis/scweet) Apify actor (snake_case JSON format). For the primary pipeline using `apidojo/twitter-scraper-lite`, see the [`main` branch](https://github.com/onur-cubukcu/cop28-hate-speech).

> **Portfolio Recreation** — This project was originally completed as a graded assignment for the course *Language in the Media* (WiSe 2023/2024) at TU Dortmund, Faculty of Cultural Studies, in collaboration with a fellow student. The original files were lost after submission. This repository is a recreation of the pipeline rebuilt from scratch for portfolio purposes, based on the original poster and methodology.

**Grade received:** 1.7 (German grading scale) — equivalent to a B+/A-
**Original poster:** [View PDF](poster.pdf)

> **Note on results:** The recreation produces different results from the original study. This is expected and is explained by two factors of limiations: (1) the original classification model (`ctoraman/hate-speech-bert`) could not been reused in recreation of the pipeline and had to be replaced with a functionally similar but a more conservative (not to judge hatefulness) alternative, and (2) tweet collection(s) via Apify in 2026 returns a different sample than what was collected live during the conference in 2023 — archive availability, scraper behaviour, and the use of different actors to scrape the datasets all affect which tweets are retrieved. The methodology and pipeline logic are reproduced; the differences in output are documented and discussed in the Limitations section.

---

## What This Project Is About

The 28th United Nations Climate Change Conference (COP28) took place in Dubai from **30 November to 13 December 2023**. During this period, the conference generated significant discussion — and controversy — on social media.

This project investigates:

> *To what extent does hate speech related to climate change appear on the social media platform X (formerly Twitter) during COP28, and under which categories can it be classified?*

To answer this, we collected all posts tagged **#COP28** during the conference, and used an AI model to automatically classify each post as **neutral**, **offensive**, or **hate speech**.

### Why Does This Matter?

Hate speech on social media during major political events is a well-documented phenomenon. Studies on COVID-19, for example, found that hate speech spiked sharply when restrictions directly affected people's daily lives (Faloppa et al., 2023). Climate change is different — its consequences are perceived as more distant — so we wanted to measure whether this resulted in comparatively less hate speech, and what form it takes when it does appear.

---

## Key Findings (Original Study)

| Category | Posts | Percentage |
|----------|-------|------------|
| Neutral | 4,279 | 88.54% |
| Offensive (insults, profanity) | 509 | 10.54% |
| Hate (threats of violence) | 44 | 0.92% |

The amount of hate speech under **#COP28** was **more than twice as high** as in a control sample of posts without any search criteria collected in the same period — suggesting that the conference topic actively attracted hostile content.

**Note:** Findings from the recreation are highly different from those of original study, as mentioned those are relevant to limiations and usage of differing models/actors.

---

## Repository Structure — Two Branches

This repository contains two branches, each corresponding to a different Apify scraping actor. The two actors export data in different JSON formats, which requires separate versions of the pipeline and merge scripts.

| Branch | Apify Actor | JSON Format | Status |
|--------|------------|-------------|--------|
| [`main`](../../tree/main) | [`apidojo/twitter-scraper-lite`](https://apify.com/apidojo/twitter-scraper-lite) | camelCase (`createdAt`, `likeCount`, `isReply`) | ✅ Primary |
| [`scweet`](../../tree/scweet) | [`altimis/scweet`](https://apify.com/altimis/scweet) | snake_case (`created_at`, `favorite_count`) | 📦 Alternative |

### Why Two Actors?

During the recreation process, the first actor used was `altimis/scweet` (the `scweet` branch). It worked but had limitations: it returned fewer unique tweets per run and struggled to reliably filter by language. I later switched to `apidojo/twitter-scraper-lite`, which offers native `lang` filtering, a cleaner JSON structure, and more consistent results. Both approaches are preserved here as they represent two valid methodological paths to the same pipeline.

### Files in Each Branch

```
── pipeline.py           # Classifies tweets and outputs colour-coded Excel + charts
── merge_datasets.py     # Merges multiple JSON exports, filters English, removes duplicates
── demo.py               # Runs the pipeline on synthetic data (no Apify or model needed)
── requirements.txt      # Python dependencies
── README.md             # This file (main branch only)
│
── file1.json            # Sample raw Apify export (apidojo/twitter-scraper-lite format)
── file2.json            # Second sample raw export — shows deduplication when merged
│
── results.xlsx          # Classification output from the full 11,996-tweet dataset
── charts/
│   ── pie_chart.png     # Distribution pie chart
│   └── bar_chart.png    # Breakdown bar chart
```
The sample JSON files (`file1.json` [trimmed for size], `file2.json`) are real exports from the `apidojo/twitter-scraper-lite` actor collected during COP28. They are included so you can run the pipeline immediately without needing an Apify account. `results.xlsx` and the charts show the output from the full dataset run.

---

## How the Pipeline Works

The project is broken into three automated stages:

```
┌─────────────────────┐      ┌──────────────────────┐     ┌─────────────────────┐
│   1. DATA           │      │  2. CLASSIFICATION   │     │   3. OUTPUT         │
│                     │      │                      │     │                     │
│  Apify scraper      │────▶│  BERT model reads    │────▶│  Excel file with    │
│  collects all       │      │  each tweet and      │     │  every tweet        │
│  #COP28 tweets      │      │  labels it:          │     │  colour-coded       │
│  from X and         │      │  Neutral /           │     │  + pie chart        │
│  exports as JSON    │      │  Offensive /         │     │  + bar chart        │
│                     │      │  Hate                │     │                     │
└─────────────────────┘      └──────────────────────┘     └─────────────────────┘
```

### Stage 1 — Data Collection (Apify)

**Apify** is a cloud platform that runs automated web scrapers (called *actors*). We used it to collect all public posts containing **#COP28** between 30 Nov and 13 Dec 2023.

**Primary actor (`main` branch):** [`apidojo/twitter-scraper-lite`](https://apify.com/apidojo/twitter-scraper-lite)
Use this input:
```json
{
  "searchTerms": [
    "#COP28 lang:en since:2023-11-30_00:00:00_UTC until:2023-12-13_23:59:59_UTC",
    "COP28 lang:en since:2023-11-30_00:00:00_UTC until:2023-12-13_23:59:59_UTC"
  ],
  "lang": "en",
  "filter:replies": false
}
```

**Alternative actor (`scweet` branch):** [`altimis/scweet`](https://apify.com/altimis/scweet)
Use this input:
```json
{
  "search": "#COP28",
  "search_sort": "Latest",
  "since": "2023-11-30",
  "until": "2023-12-13",
  "lang": "en",
  "max_items": 1000
}
```

> **Free tier limit:** Apify allows 1,000 tweets per day on a free account. Run the scraper across multiple days or use date range splitting to build up a larger dataset. The merge script handles deduplication automatically.

### Stage 2 — AI Classification (HuggingFace + BERT)

**HuggingFace** is a platform that hosts pre-trained AI models, similar to how GitHub hosts code. The model runs locally — no ongoing cost and no external API calls once downloaded.

**Original study model:** The assignment used **`ctoraman/hate-speech-bert`**, a BERT model fine-tuned on the Toraman22 v2 dataset with native three-class output (neutral / offensive / hate). In the recreation of the original pipeline, I could not reuse this model as it returned with errors of accessibility and had to replace it with similar models using the same logic.

**Recreation model:** This recreation uses **`cardiffnlp/twitter-roberta-base-offensive`**, a RoBERTa model fine-tuned specifically on Twitter data. Despite being a different model, the classification logic mirrors the original:

1. The model reads each tweet and decides: *offensive* or *not offensive*
2. If offensive, a violence keyword check (`kill`, `shoot`, `bomb`, etc.) escalates it to *hate speech*

This two-step approach reproduces what the original model did natively — as the original poster noted: *"the AI module only detects words such as swear words ('idiot') or words associated with violence ('kill', 'shoot')"*.

**PyTorch** (`torch`) powers the model computations. It can be explained using the metaphor of an engine, thus if HuggingFace provides the car, PyTorch makes it move.

### Stage 3 — Output

Results are written to a colour-coded Excel file:
- 🟢 **Green rows** = Neutral
- 🟠 **Orange rows** = Offensive
- 🔴 **Red rows** = Hate

A Summary sheet shows the overall counts and percentages. Two charts (pie and bar) are generated as PNG images.

---

## Dependencies Explained

| Dependency | What it is | Why we need it |
|------------|-----------|----------------|
| **Python 3.10+** | Programming language | The scripts are written in Python |
| **transformers** | HuggingFace library | Loads and runs the BERT classification model |
| **torch** (PyTorch) | Deep learning framework by Meta | Powers the model computations under the hood |
| **pandas** | Data analysis library | Reads/writes the tweet data as a table |
| **openpyxl** | Excel file library | Creates and formats the output `.xlsx` file |
| **matplotlib** | Charting library | Generates the pie and bar charts |

### External Tools

| Tool | What it is | Why we need it |
|------|-----------|----------------|
| **Apify** | Cloud web scraping platform | Collects tweets from X (Twitter blocks direct scraping) |
| **HuggingFace** | AI model repository | Hosts the pre-trained classification model |

---

## How to Run It

### Step 1 — Clone the branch you want

For the primary pipeline:
```bash
git clone --branch scweet https://github.com/onur-cubukcu/cop28-hate-speech.git
```

For the alternative pipeline:
```bash
git clone --branch scweet https://github.com/onur-cubukcu/cop28-hate-speech.git
```

### Step 2 — Install dependencies

```bash
pip install transformers torch pandas openpyxl matplotlib
```

### Step 3 — Collect tweets via Apify

Follow the actor-specific input in Stage 1 above. Primary pipeline uses [`apidojo/twitter-scraper-lite`](https://apify.com/apidojo/twitter-scraper-lite). Alternative pipeline uses [`altimis/scweet`](https://apify.com/altimis/scweet). Export each run as a `.json` file.
**Note:** If these steps are too technical, the newly developed desktop app can be used, as it can also detect the required pipeline for the exported `.json` file format.

### Step 4 — Merge the files

```bash
python merge_datasets.py file1.json file2.json file3.json
```

Produces `tweets.json` — deduplicated, English-only.

### Step 5 — Run the classification pipeline

```bash
python pipeline.py --input tweets.json --output results.xlsx
```

On first run, the model (~500 MB) downloads automatically and is cached. Processing ~12,000 tweets takes roughly 30–60 minutes on a standard laptop.

### Try it without any data

```bash
python demo.py
```

Runs the full pipeline on synthetic data — no Apify account or model download required.

---

## Results (Recreation)

| Category | Count | Percentage |
|----------|-------|------------|
| Neutral | 11,830 | 98.62% |
| Offensive | 156 | 1.30% |
| Hate | 10 | 0.08% |
| **Total** | **11,996** | |

### Comparison with Original Study

| Category | Original (2024) | Recreation (2026) | Difference |
|----------|----------------|-------------------|------------|
| Neutral | 88.54% | 98.62% | ▲ 10.08% |
| Offensive | 10.54% | 1.30% | ▼ 9.24% |
| Hate | 0.92% | 0.08% | ▼ 0.84% |

The recreation shows a significantly higher neutral rate than the original study. This is primarily attributable to the model difference and the data collection gap explained in Limitations below. It represents a genuine methodological observation: the definition of "offensive" built into a model directly shapes what any study using it will find.

---

## Limitations

- **Model difference — the most significant factor:** The original `ctoraman/hate-speech-bert` was trained to capture a broad spectrum of Twitter hostility including mild insults, sarcasm, and passive-aggressive phrasing. The replacement model applies a stricter definition, primarily flagging explicit profanity and clear threats. This likely explains the majority of the gap in offensive rates (10.54% vs 1.30%). This is a known challenge in computational hate speech research: results are only as broad as the training data of the model used.
- **Data collection gap:** The original study collected tweets live during COP28 in late 2023. This recreation collected the same tweets retrospectively in 2026. Historical scraping via Apify does not guarantee identical coverage — popular tweets may be over-represented, some replies may no longer be accessible, and scraper sort order affects which 1,000 tweets are retrieved per run.
- **Language filtering:** This recreation filters to English-only using Twitter's `lang: en` field. The original study included all languages but classified non-English tweets as neutral by default, which inflated its neutral count in the opposite direction.
- **Model accuracy:** No model perfectly captures pragmatic language. Sarcasm, political idiom, and context-dependent hostility remain difficult to classify automatically.
- **Data scope:** Scraping tools do not guarantee complete coverage. Spam, bots, and near-duplicate content may appear even after deduplication.

---

## References

- Dowlagar, S., & Mamidi, R. (2020). *Using BERT and Multilingual BERT Models for Hate Speech Detection*. arXiv. https://arxiv.org/pdf/2101.09007.pdf
- Faloppa, F., et al. (2023). *Study on Preventing and Combating Hate Speech in Times of Crisis*. Council of Europe: CDADI.
- Landesanstalt für Medien NRW (2023). *Hate Speech – Forsa-Studie 2023*.
- Perera, S., et al. (2023). *A comparative study of the characteristics of hate speech propagators and their behaviours over Twitter*. http://tinyurl.com/46cdk6eu
- Toraman, C., Şahinuç, F., & Yilmaz, E. (2022). *Large-Scale Hate Speech Detection with Cross-Domain Transfer*. LREC 2022, pp. 2215–2225.
- United Nations (2024). *Understanding Hate Speech*. https://www.un.org/en/hate-speech/understanding-hate-speech/what-is-hate-speech

---

👉  Desktop app version can be found here [cop28-hate-speech-app](https://github.com/onur-cubukcu/cop28-hate-speech-app)

*Course: Language in the Media — TU Dortmund, Faculty of Cultural Studies, WiSe 2023/2024*
*Originally submitted: February 2024 | Recreated for portfolio: February 2026*
