# 🎮 steam_games  
**Analysis of Best-Selling Steam Games of All Time**

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

## 📁 Dataset Notes

- The game list was scraped from Steam's **Bestsellers page** on **June 1, 2025**.
- Price data reflects **MENA (Middle East & North Africa) USD** pricing.
- Games were excluded if download estimates were not available via **SteamDB**.
- Qualitative columns like `rating`, `difficulty`, and `length` were filled from **GameFAQs**, or estimated from user reviews when unavailable.
- Tag data was cleaned and standardized into a fixed vocabulary of **42 tags**.

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
- ✅ `estimated_downloads` — как основная метрика успеха  
- ⚠️ `age_restriction`, `rating`, `difficulty`, `length` — не будут использоваться из-за неопределённости в методах сбора

---
Представим, что вы - разработчик. Вы хотите сделать игру. Вы не знаете, про что она, в каком жанре, какие у неё будут особенности. Пока что у вас просто есть желание сделать что-то, что поможет вам заплатить
за жильё и поставить пару пломб на правую верхнюю пятёрку. Что повысит шансы на успех? Для этого нам нужно разработать ряд гипотез.

## ❓ Hypotheses and Analytical Questions

### 🧠 Разработчики:
- Есть ли связь между **числом игр от разработчика** и **успешностью** новых релизов?

### 🧪 Жанры и Теги (`user_defined_tags`):
1. Как **жанровые предпочтения** игроков изменялись со временем? Есть ли циклы?
2. Какие **топ-5 жанров** были самыми популярными за последние 5 лет?
3. Можно ли предсказать рост популярности жанров с помощью **линейной регрессии**?

### 📛 Название игры:
- Влияет ли **длина названия** на успех?
- Влияет ли наличие **двоеточий или специальных символов**?
- Можно ли провести **ANOVA** по числу слов в названии?

### 💻 Поддержка ОС:
- Обязательно ли наличие **Windows-версии** для достижения успеха?
- Есть ли успешные игры без поддержки Windows?

### 🌍 Языковая доступность:
- Обрекает ли **отсутствие английского языка** игру на неудачу?

---

## 🛠️ To Do Next

- Очистка и подготовка данных (`release_date`, `tags`, `features`, разбивка списков)
- Построение визуализаций (тренды, жанры, платформы, цены)
- Разработка модели или метрик для оценки «успешности»
