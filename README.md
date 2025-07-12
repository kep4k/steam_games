# steam_games  
**Analysis of Best-Selling Steam Games of All Time**
---

## Dataset Overview: Column Descriptions

| Column Name            | Type     | Description |
|------------------------|----------|-------------|
| `game_name`            | object   | Official title of the game. |
| `reviews_like_rate`    | int64    | Recommendation rate from user reviews on Steam (e.g., "95% of reviews are positive"). |
| `all_reviews_number`   | int64    | Total number of user reviews the game has received on Steam. |
| `release_date`         | object   | Official release date of the game on Steam, including Early Access if applicable. |
| `developer`            | object   | Primary developer or studio behind the game. |
| `user_defined_tags`    | object   | A curated set of user-assigned genres and tags (from a standardized vocabulary of 42 tags). |
| `supported_os`         | object   | Operating systems supported by the game (e.g., Windows, macOS, Linux). |
| `supported_languages`  | object   | List of supported languages for UI, audio, or subtitles. |
| `price`                | float64  | Game price in MENA (Middle East & North Africa) U.S. Dollar equivalent. A value of `0` means Free-to-Play. |
| `other_features`       | object   | Steam-supported gameplay features (e.g., "Single-player", "Online Co-op", "VR Supported"). |
| `age_restriction`      | int64    | Age recommendation: 0 (Everyone), 10 (10+), 13 (13+), 17 (17+). |
| `rating`               | float64  | Overall user rating on a 1–5 scale (1 = lowest, 5 = highest). |
| `difficulty`           | int64    | Estimated difficulty level (1 = easiest, 5 = hardest). |
| `length`               | int64    | Average gameplay length in hours (capped at 80h). |
| `estimated_downloads`  | int64    | Estimated number of owners/downloads from SteamDB. |

The dataset (`bestSelling_games.csv`) is included in this repository.
> Thanks to **H. Buğra Eken** for preparing and providing this dataset!
---

## Dataset Notes

- The game list was scraped from Steam's **Bestsellers page** on **June 1, 2025**.
- Price data reflects **MENA (Middle East & North Africa) USD** pricing.
- Games were excluded if download estimates were not available via **SteamDB**.
- Qualitative columns like `rating`, `difficulty`, and `length` were filled from **GameFAQs**, or estimated from user reviews when unavailable.
- Tag data was cleaned and standardized into a fixed vocabulary of **42 tags**.
---

## Selected Columns for Analysis

We will use the following variables in our analysis:

- `game_name` — for identifying each game  
- `reviews_like_rate` — as a measure of user satisfaction  
- `all_reviews_number` — as an indicator of community engagement  
- `release_date` — to track temporal trends  
- `developer` — to evaluate developer impact  
- `user_defined_tags` — for genre and thematic analysis  
- `supported_os` and `supported_languages` — to assess accessibility  
- `price` — as a monetization factor  
- `estimated_downloads` — as the primary measure of popularity  

The following columns will *not* be used due to uncertainty in their collection methods:  
`age_restriction`, `rating`, `difficulty`, `length`

---

## Research Questions & Hypotheses

| ID | Research Question | Hypothesis |
|----|-------------------|------------|
| 1  | Do developers with multiple games in the best-sellers list produce more successful titles? | Developers with 2+ games in the dataset have higher average success scores. |
| 2a | What are the top 5 genres over the last 5 years? | -//- |
| 2b | Do certain genre combinations outperform single genres? | -//- |
| 3a | Does the number of characters or words in a game's title affect success? | -//- |
| 3b | Does the presence of special characters (like colons) affect success? | -//- |
| 4  | Is Windows support necessary for a game’s success? | Games without Windows support have lower average success. |
| 5  | Is English support necessary for global success? | Games without English support have lower average success. |
| 6  | Is the overall success of top Steam games rising or falling? | -//- |

## Methodology Summary

| Hypothesis | Method |
|-----------|--------|
| 1 | Two-sample t-test. |
| 2a | Aggregate average `success` by genre/year → visualize top 5 per year. |
| 2b | One-hot encode genres → generate genre pairs → compare average success via t-test or permutation test. |
| 3a | One-way ANOVA on game success across groups defined by title length. |
| 3b | Two-sample t-test: titles with special characters vs without. |
| 4 | Two-sample t-test: Windows support (yes/no) vs success. |
| 5 | Two-sample t-test: English support (yes/no) vs success. |
| 6 | Linear regression: year of release vs success score (2010–2025). |

## Success Metric Definition

We define a custom metric success as follows:
success = estimated_downloads × reviews_like_rate × reviews_activity_rate

estimated_downloads: proxy for audience reach
reviews_like_rate values (e.g., 95) will be scaled to 0–1 by dividing by 100 before calculation: proxy for sentiment
reviews_activity_rate: proxy for engagement, calculated as the ratio of a game’s number of reviews to the amount of downloads of this game (i.e., normalized to the range 0–1). Initially, it was planned to calculate it as the ratio of a game’s number of reviews to the maximum review count in the dataset, but this would have created an evaluation of the game in relation to the best, so we changed it.

## Limitations

- Only includes games in Steam’s **best-sellers** as of mid-2025.
- Does not account for all titles in a developer's portfolio.
- Genres may have inconsistent tag behavior or low sample size.
- `release_date` may not match original launch date (e.g., ports).
- Some qualitative variables were estimated, not scraped.
- The `success` metric is heuristic and not equivalent to revenue or ROI.

## Key Findings (Linked to Hypotheses)

| ID | Research Question | Result & Key Finding |
|----|------------|----------------------|
| 1  | Do developers with multiple games in the best-sellers list produce more successful titles? | **Confirmed.** Developers with multiple games in the best-sellers list produce more successful titles. Significant but small effect was found.  |
| 2a | What are the top 5 genres over the last 5 years? | <img width="1000" height="400" alt="top5genres" src="https://github.com/user-attachments/assets/cde3242c-38ae-4849-86a1-a438b1dce927" /> |
| 2b | Do certain genre combinations outperform single genres? | **Rejected.** Although some genre pairs like *(FPS, Tactical)* had higher average success, no combinations were statistically significant. |
| 3a | Does the number of characters or words in a game’s title affect success? | **Rejected.** As a result of ANOVA, we did not receive evidence that games of different lengths have significantly different success rates |
| 3b | Does the presence of special characters (like colons) affect success? | **Rejected.** Games with colons showed slightly higher average success, but the difference was not statistically significant. |
| 4  | Is Windows support necessary for a game’s success? | **Not testable.** All games in the dataset support Windows. Instead, we tested **Linux support**, which was associated with significantly higher success, but effect size was small. |
| 5  | Is English support necessary for global success? | **Not testable.** All games supported English. Instead, we tested **Traditional Chinese support**, which was associated with significantly higher success, but effect size was also small. |
| 6  | Is the overall success of top Steam games rising or falling? | Linear regression shows a **small but statistically significant decline** in success over time. <img width="1200" height="600" alt="success downloads" src="https://github.com/user-attachments/assets/c90fa776-f547-457d-a7a5-fe646cb6a62a" />

---

## Additional Findings

- **Success distribution is heavily left-skewed**, so we applied a log transformation for visualization.
<img width="1200" height="600" alt="success" src="https://github.com/user-attachments/assets/460f2353-6117-4b52-ad1c-1ab1a403270e" />

- **Number of top-selling games per year has increased**, indicating growing developer presence or platform saturation.
<img width="1200" height="500" alt="games" src="https://github.com/user-attachments/assets/909d14a6-d3ef-4e8e-8fb8-ef9d81aa2ecf" />

- **Average game price has remained relatively stable over time**, with no clear upward trend.
<img width="1400" height="500" alt="price" src="https://github.com/user-attachments/assets/18ea340e-4643-4754-9e2a-8456ea93fbf7" />

---

## Practical Implications

- Developers targeting global markets should consider localizing into Traditional Chinese.
- The popularity of fantasy, souls-like, and open-world genres over multiple years suggests continued market demand in those areas.
- Declining success over time suggests increasing market saturation — studios should invest in innovation.

---

## How to run project

Install libraries from requirements.txt
Use code from steam_analysis.py
