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
| 2a | How have the top 5 genres changed over the last 5 years? | The top 5 genres by success have changed significantly across years. |
| 2b | Are there genres that rise and fall in popularity cyclically? | Certain genres exhibit cyclical success patterns. |
| 2c | Do certain genre combinations outperform single genres? | Some two-genre combinations result in significantly higher success than individual genres. |
| 3a | Does the number of characters or words in a game's title affect success? | There is a difference success between games with different length. |
| 3b | Does the presence of special characters (like colons) affect success? | Titles with colons/special symbols differ in success from those without. |
| 4  | Is Windows support necessary for a game’s success? | Games without Windows support have lower average success. |
| 5  | Is English support necessary for global success? | Games without English support have lower average success. |
| 6  | Is the overall success of top Steam games rising or falling? | There is a statistically significant trend in average success scores over time. |

## Methodology Summary

| Hypothesis | Method |
|-----------|--------|
| 1 | Two-sample t-test + One-way ANOVA for 1 vs 2 vs 3+ games per developer. |
| 2a | Aggregate average `success` by genre/year → visualize top 5 per year. |
| 2b | Time series plots per genre → rolling averages, optional Fourier/seasonal decomposition. |
| 2c | One-hot encode genres → generate genre pairs → compare average success via t-test or permutation test. |
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
reviews_activity_rate: proxy for engagement, calculated as the ratio of a game’s number of reviews to the maximum review count in the dataset (i.e., normalized to the range 0–1)

## 🚧 Limitations

- Only includes games in Steam’s **best-sellers** as of mid-2025.
- Does not account for all titles in a developer's portfolio.
- Genres may have inconsistent tag behavior or low sample size.
- `release_date` may not match original launch date (e.g., ports).
- Some qualitative variables were estimated, not scraped.
- The `success` metric is heuristic and not equivalent to revenue or ROI.

---

## 📈 Visualizations Planned

- Top 5 genre bar charts (per year)
- Genre trend line plots (with smoothing or decomposition)
- Heatmaps for genre pair success
- Title-length histograms vs success
- OS/language support boxplots
- Overall success trends by release year


## ❓ Hypotheses and Analytical Questions

### Hypothesis 1: Do developers with multiple best-selling games produce more successful titles?

***Business Question***
Do developers who have multiple games in the best-sellers list on Steam tend to release more successful games than developers with only one game in the same list?

***Rationale***
If having more than one hit in this list correlates with stronger performance, that may support the idea that developer reputation or portfolio size impacts future game success. This could be useful for investors and publishers when evaluating studios.

***Limitations***
This dataset includes only 2380 Steam's best sellers games. We can not evaluate all developer's products, only those presented in this dataset. 

***Metric of Success***
We define a custom metric success as follows:

success = estimated_downloads × reviews_like_rate × reviews_activity_rate

estimated_downloads: proxy for audience reach

reviews_like_rate values (e.g., 95) will be scaled to 0–1 by dividing by 100 before calculation: proxy for sentiment

reviews_activity_rate: proxy for engagement, calculated as the ratio of a game’s number of reviews to the maximum review count in the dataset (i.e., normalized to the range 0–1)

***Method***
Use an independent two-sample t-test to compare the success scores of:

Group A: Developers with only 1 game in the dataset

Group B: Developers with 2 or more games in the dataset

***Exploratory Task***
Additionally, we will examine whether developers with 3 or more games in the dataset perform significantly better than the rest. This will be tested using one-way ANOVA, comparing three groups:

Group 1: Developers with 1 game

Group 2: Developers with 2 games

Group 3: Developers with 3+ games


### Hypothesis 2: Genre Trends Over Time

***Business Question***  
How have player genre preferences on Steam changed over time? 

***Rationale***
Identifying long-term growth or decline and especially cyclic behavior. It can help anticipate future market demand.

***Hypotheses***  
- *2a*: The top 5 most successful game genres have changed significantly over the last 5 years.  
- *2b*: Certain genres demonstrate cyclical popularity trends over the years.
- *2c*: Two-genre combination can be found that leads to significantly higher game success than any individual genre or other genre pairs.

***Method***
* 2a: Top Genres per Year
Aggregate games by release year and genre.
For each year, calculate average success per genre.
Identify and visualize the top 5 genres by average success for each of the last 5 years.
Compare yearly lists to assess stability or variation in genre rankings.

* 2b: Cyclical Behavior
For each genre (with enough sample size), plot time series of average success per year.
Apply:
Rolling averages to smooth trends.
Optionally, Fourier Transform or seasonal decomposition to detect periodic patterns.
Assess whether certain genres show repeated rises and falls.

* 2c: Synergistic Genre Combinations
One-hot encode genres.
Generate all unordered two-genre combinations per game.
Compute:
Frequency of each genre pair.
Average success per pair.
Compare top genre pairs to top individual genres:
Use t-tests or permutation tests to assess significance.

Limitations
Some genres or combinations may have low sample sizes.
Steam release date may not reflect actual launch (e.g., for older games or ports).

Potential Visualizations
Bar charts of top genres by year.
Line charts of genre success over time.
Heatmaps of genre pair success.
Radar plots or stacked area charts to show shifting genre dominance.

### Hypothesis 3: Does the Game Title Affect Success?

***Business Question***
Can characteristics of a game’s name such as its length, complexity, or presence of certain symbols influence its market success?

***Rationale***
Game titles serve as a first impression for potential players. Short names may be easier to remember or market, while longer or more descriptive titles (e.g., with subtitles separated by colons) might convey genre, lore, or value. If certain naming patterns correlate with success, this insight could support decisions in branding or title design.

***Hypotheses***

3a. There is a statistically significant relationship between title length (in characters) and game success.
3b. Games that contain colons (:) or special characters in their titles are more (or less) successful than those that don’t.

### Hypothesis 4: Is Windows Support Essential for Success?

Business Question
Do games that support Windows perform significantly better than those that don’t?

Rationale
Windows is the dominant PC gaming platform. If support for it is necessary for success, developers must prioritize it. However, if games without Windows support can also succeed, that could encourage more cross-platform or niche development (e.g., Mac/Linux exclusives).

Hypothesis
Games without Windows support have significantly lower success scores than those with Windows support.

### Hypothesis 5: Does English Language Support Determine Success?

Business Question
Does having English as a supported language significantly affect a game's success?

Rationale
English is often the default for global reach. If games without English support perform worse, localization becomes a critical business decision.

Hypothesis
Games without English language support have significantly lower success scores than games that support English.

### Hypothesis 6: Is Game Success Trending Up or Down?

Business Question
Is the average success of best-selling Steam games improving or declining over the years?

Rationale
Tracking the health of the top-selling segment can give insight into overall industry trends: is user engagement and satisfaction growing, stable, or declining?

Hypothesis
There is a significant trend (upward or downward) in the average success score of games released between 2010 and 2025.
