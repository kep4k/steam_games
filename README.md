# 🎮 steam_games  
**Analysis of Best-Selling Steam Games of All Time**
---

### 📊 Dataset Overview: Column Descriptions

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

> 🙏 Thanks to **H. Buğra Eken** for preparing and providing this dataset!
---

## 📁 Dataset Notes

- The game list was scraped from Steam's **Bestsellers page** on **June 1, 2025**.
- Price data reflects **MENA (Middle East & North Africa) USD** pricing.
- Games were excluded if download estimates were not available via **SteamDB**.
- Qualitative columns like `rating`, `difficulty`, and `length` were filled from **GameFAQs**, or estimated from user reviews when unavailable.
- Tag data was cleaned and standardized into a fixed vocabulary of **42 tags**.
---

## 🔍 Selected Columns for Analysis

Мы используем следующие переменные:

- ✅ `game_name` — для идентификации игр  
- ✅ `reviews_like_rate` — как показатель удовлетворённости пользователей  
- ✅ `all_reviews_number` — как индикатор вовлечённости  
- ✅ `release_date` — для отслеживания трендов  
- ✅ `developer` — чтобы анализировать влияние разработчиков  
- ✅ `user_defined_tags` — для анализа жанров  
- ✅ `supported_os` и `supported_languages` — для изучения доступности  
- ✅ `price` — как фактор монетизации  
- ✅ `estimated_downloads` — как основная метрика популярности  
- ⚠️ `age_restriction`, `rating`, `difficulty`, `length` — не будут использоваться из-за неопределённости в методах сбора
---

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


### 📚 Hypothesis 2: Genre Trends Over Time

***Business Question***  
How have player genre preferences on Steam changed over time? Can we observe popularity cycles or genre-specific “eras”?

***Rationale***
Identifying long-term growth or decline — and especially cyclic behavior — can help anticipate future market demand.

***Hypotheses***  
- *2a*: The top 5 most successful game genres have changed significantly over the last 5 years.  
- *2b*: Certain genres demonstrate cyclical popularity trends over the years.

***Method***
- Genre extraction and standardization from `user_defined_tags`.  
- Time-based aggregation (by release year) of `success` and `estimated_downloads` per genre.  
- Visualization using line charts, heatmaps, and rolling averages.  
- Cyclicity analysis using ACF, STL decomposition, and exploratory time series tools.



### 📛 Название игры:
- Влияет ли **длина названия** на успех?
- Влияет ли наличие **двоеточий или специальных символов**?
- Можно ли провести **ANOVA** по числу слов в названии?

### 💻 Поддержка ОС:
- Обязательно ли наличие **Windows-версии** для достижения успеха?
- Есть ли успешные игры без поддержки Windows?

### 🌍 Языковая доступность:
- Обрекает ли **отсутствие английского языка** игру на неудачу?

- ещё интересно, падает или повышается за последние годы успешность игр в понимании репутации, которое я разработал
