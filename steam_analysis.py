# Load required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import re
from itertools import combinations
from scipy.stats import ttest_ind, f_oneway, linregress

# Load dataset (adjust the path if needed)
df = pd.read_csv("data/bestSelling_games.csv")

## Initial overview

# Preview the dataset
print(df.head())
print(df.info())

# Check for missing values
print(df.isna().sum().sort_values(ascending=False))

# Explore sample unique values and data types for selected columns
columns_to_check = [
    'game_name', 'reviews_like_rate', 'all_reviews_number', 'release_date',
    'developer', 'user_defined_tags', 'supported_os', 'supported_languages',
    'price', 'estimated_downloads'
]

for col in columns_to_check:
    print(f"\n{col} — unique values / types:")
    print(df[col].unique()[:10])

## Investigate odd values

# Find unrealistic like rates (<0% or >100%)
df_weird_reviews = df[(df['reviews_like_rate'] < 0) | (df['reviews_like_rate'] > 100)]
print(df_weird_reviews[['game_name', 'reviews_like_rate']])

# Check games with extremely low download numbers
df_low_downloads = df[df['estimated_downloads'] < 500]
print(df_low_downloads[['game_name', 'estimated_downloads']])
# Observation: many games in the dataset have very low estimated downloads. This limits the strength of conclusions we can draw, but no games are excluded. 

## Parse release dates and detect anomalies

# Convert release_date column to datetime format
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
print(df['release_date'].isna().sum())

# Check for games with future release dates
df_future = df[df['release_date'] > pd.Timestamp("2025-07-05")]
print(df_future[['game_name', 'release_date']])

# Create normalized download count in thousands (K)
df['estimated_downloads_K'] = df['estimated_downloads'] / 1000
df['estimated_downloads_K'] = df['estimated_downloads_K'].round(2)

# Convert like rate from percentage to fraction
df['reviews_like_rate_%'] = df['reviews_like_rate'] / 100

# Calculate review activity rate as number of reviews divided by number of downloads
df['reviews_activity_rate'] = df['all_reviews_number'] / df['estimated_downloads']

# Define custom success metric: downloads × like rate × review activity
df['success'] = (df['estimated_downloads_K'] * df['reviews_like_rate_%'] * df['reviews_activity_rate'])

# Check for duplicate game entries
print(df['game_name'].duplicated().sum())

# Plot distribution of success: skewed data, using log scale for better readability
plt.figure(figsize=(12, 6))
sns.histplot(df['success'], kde=True, log_scale=True)
plt.title(f'Success Distribution')
plt.xlabel('Success')
plt.ylabel('Number of games')
plt.show()

# Display top 10 games based on success score
top_success = df.sort_values('success', ascending=False).head(10)
print(top_success[['game_name', 'developer', 'success']])

# Display top 10 games by estimated downloads
top_downloads = df.sort_values('estimated_downloads_K', ascending=False).head(10)
print(top_downloads[['game_name', 'developer', 'estimated_downloads']])

# Display top 10 games by like rate
top_like_rate = df.sort_values('reviews_like_rate', ascending=False).head(10)
print(top_like_rate[['game_name', 'developer', 'reviews_like_rate']])

# Display top 10 games by number of reviews
top_reviews = df.sort_values('all_reviews_number', ascending=False).head(10)
print(top_reviews[['game_name', 'developer', 'all_reviews_number']])

# Extract release year from release_date
df['release_year'] = df['release_date'].dt.year

# Count number of games released each year and plot
games_by_year = df['release_year'].value_counts().sort_index()
games_by_year.plot(kind='bar', figsize=(12,5))
plt.title('Number of Games by Release Year')
plt.ylabel('Number of Games')
plt.xlabel('Year')
plt.show()

# Scatterplot: like rate vs number of downloads
sns.scatterplot(data=df, x='reviews_like_rate_%', y='estimated_downloads_K', alpha=0.5)
plt.title('Downloads in Ks vs Like Rate')
plt.show()

# Correlation heatmap between key metrics
sns.heatmap(df[['estimated_downloads_K', 'reviews_like_rate_%', 'reviews_activity_rate', 'success']].corr(), annot=True)
plt.title('Correlation Heatmap')
plt.show()

# Check most common OS support
df['supported_os'].value_counts().head(10)

# Price. Check format and anomalies in price column
print(df['price'].unique()[:20])  
print(df['price'].dtype)          

# Price. Identify any non-numeric price values
non_numeric_prices = df[pd.to_numeric(df['price'], errors='coerce').isna()]
print(non_numeric_prices[['game_name', 'price']])

# Price. Average game price by year
avg_price_by_year = df.groupby('release_year')['price'].mean()
plt.figure(figsize=(14, 5))
avg_price_by_year.plot(kind='bar', color='skyblue')
plt.title('Average Game Price by Year')
plt.ylabel('Average Price (MENA)')
plt.xlabel('Year')
plt.xticks(rotation=90) 
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# HYPOTHESIS 1

# Count number of games per developer
dev_counts = df['developer'].value_counts()
df['dev_game_count'] = df['developer'].map(dev_counts)

# Create grouping: Group A = 1 game, Group B = multiple games
df['group'] = df['dev_game_count'].apply(lambda x: 'Group A' if x == 1 else 'Group B')
group_a = df[df['group'] == 'Group A']['success']
group_b = df[df['group'] == 'Group B']['success']

# Independent t-test between the two groups
t_stat, p_value = ttest_ind(group_a, group_b, equal_var=False)
print(f"T-Statistic: {t_stat:.4f}")
print(f"P-Value: {p_value:.4f}")

# Compute effect size (Cohen's d)
mean_a = np.mean(group_a)
mean_b = np.mean(group_b)
std_a = np.std(group_a, ddof=1)
std_b = np.std(group_b, ddof=1)
pooled_std = np.sqrt((std_a**2 + std_b**2) / 2)
cohen_d = (mean_a - mean_b) / pooled_std
print(f"Cohen's d: {cohen_d:.3f}")

# HYPOTHESIS 2a

# Clean and split genre tags
df['genres'] = df['user_defined_tags'].str.split(',')
df['genres'] = df['genres'].apply(lambda x: [tag.strip().strip(',') for tag in x])

# Explode genres for analysis
df_exploded = df.explode('genres')
df_exploded['release_year'] = df_exploded['release_date'].dt.year

# Average success by genre and year
genre_year_success = (
    df_exploded
    .groupby(['genres', 'release_year'])['success']
    .mean()
    .reset_index()
)

# Filter for recent years
target_years = [2021, 2022, 2023, 2024, 2025]
filtered = genre_year_success[genre_year_success['release_year'].isin(target_years)]

# Top 5 genres per year
top5_by_year = (
    filtered
    .sort_values(['release_year', 'success'], ascending=[True, False])
    .groupby('release_year')
    .head(5)
    .copy()
)

# Assign rank to top genres
top5_by_year['rank'] = top5_by_year.groupby('release_year')['success'].rank(method='first', ascending=False).astype(int)

# Pivot for visual table
table = top5_by_year.pivot(index='release_year', columns='rank', values='genres')
table.columns = [f'#{i}' for i in table.columns]  # Переименовываем колонки

# Display top genres table visually
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('off')
table_visual = ax.table(cellText=table.values,
                        rowLabels=table.index,
                        colLabels=table.columns,
                        cellLoc='center',
                        loc='center')
table_visual.auto_set_font_size(False)
table_visual.set_fontsize(10)
table_visual.scale(1.1, 1.5)
plt.title('Top 5 Genres by Average Success (2021–2025)', fontsize=14)
plt.show()

# HYPOTHESIS 2b

# Find best-performing single genre
single_genre_success = (
    df_exploded
    .groupby('genres')['success']
    .agg(['mean', 'count'])
    .sort_values('mean', ascending=False)
    .reset_index()
)
top_single_genre = single_genre_success.iloc[0]
best_genre = top_single_genre['genres']
best_genre_mean = top_single_genre['mean']
print(f"Best single genre: {best_genre} with avg success {best_genre_mean:.2f}")

# Generate all genre pairs per game
def genre_pairs(genres):
    return list(combinations(sorted(set(genres)), 2)) if len(genres) >= 2 else []
df['genre_pairs'] = df['genres'].apply(genre_pairs)
df_pairs = df.explode('genre_pairs')
df_pairs = df_pairs[df_pairs['genre_pairs'].notna()]

# Evaluate mean success for each genre pair
pair_success = (
    df_pairs
    .groupby('genre_pairs')['success']
    .agg(['mean', 'count'])
    .reset_index()
)
pair_success = pair_success[pair_success['count'] >= 10]  

# Compare each genre pair to best single genre
best_genre_games = df[df['genres'].apply(lambda x: best_genre in x)]
best_genre_successes = best_genre_games['success']
results = []

for _, row in pair_success.iterrows():
    pair = row['genre_pairs']
    mean_success = row['mean']
    
    if mean_success > best_genre_mean:
        pair_successes = df_pairs[df_pairs['genre_pairs'] == pair]['success']
        
        if len(pair_successes) > 1 and len(best_genre_successes) > 1:
            t_stat, p_val = ttest_ind(pair_successes, best_genre_successes, equal_var=False)
            
            results.append({
                'pair': pair,
                'mean_success': mean_success,
                'n_pair': len(pair_successes),
                't_stat': t_stat,
                'p_val': p_val
            })

results_df = pd.DataFrame(results).sort_values('mean_success', ascending=False)

# Show genre pairs that outperform the top single genre
pd.set_option("display.max_rows", 100)
print(results_df[['pair', 'mean_success', 'n_pair', 't_stat', 'p_val']])
pd.reset_option("display.max_rows")

# HYPOTHESIS 3a

# Token counting
def count_tokens(title):
    if not isinstance(title, str):
        return 0
    words = re.findall(r'\b[^\W\d_]+\b', title)  
    digits = re.findall(r'\d+', title)           
    specials = re.findall(r'[^\w\s]', title)     
    return len(words) + len(digits) + len(specials)

df['title_token_count'] = df['game_name'].apply(count_tokens)

# Group games by title token count
grouped = df.groupby('title_token_count')['success'].apply(list)
grouped = grouped[grouped.apply(len) >= 5]

# ANOVA test for differences in success by title length
anova_result = f_oneway(*grouped)
print(f"F-Statistic: {anova_result.statistic:.4f}")
print(f"P-Value: {anova_result.pvalue:.4f}")

# Boxplot to visualize
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[df['title_token_count'].isin(grouped.index)],
            x='title_token_count', y='success')
plt.title('Success by Title Token Count')
plt.xlabel('Title Token Count')
plt.ylabel('Success')
plt.grid(True)
plt.show()

# HYPOTHESIS 3b

# Create groups for comparing
df['has_colon'] = df['game_name'].apply(lambda x: ':' in str(x))
group_with_colon = df[df['has_colon'] == True]['success']
group_without_colon = df[df['has_colon'] == False]['success']
print(f"С двоеточием: {len(group_with_colon)} игр")
print(f"Без двоеточия: {len(group_without_colon)} игр")

# Independent t-test
t_stat, p_value = ttest_ind(group_with_colon, group_without_colon, equal_var=False)
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Boxplot
sns.boxplot(data=df, x='has_colon', y='success')
plt.title('Success of Games: With vs Without Colon in Title')
plt.xlabel('Has Colon in Title')
plt.ylabel('Success')
plt.show()

# HYPOTHESIS 4

# Check OS options
print(df['supported_os'].unique())
df['os'] = df['supported_os'].str.split(',')
df['os'] = df['os'].apply(lambda x: [tag.strip().strip(',') for tag in x])
print(df['os'].value_counts())
# All games have Windows - we can't test this hypothesis

# Check how many games with Linux we have
df['has_linux'] = df['os'].apply(lambda os_list: any('linux' in os for os in os_list))
print(df['has_linux'].value_counts())

# Compare games with Linux vs other
linux_games = df[df['has_linux'] == True]['success']
non_linux_games = df[df['has_linux'] == False]['success']

mean_linux = linux_games.mean()
mean_non_linux = non_linux_games.mean()
print(f"\n🎮 Средняя успешность игр с Linux: {mean_linux:.2f}")
print(f"🎮 Средняя успешность игр без Linux: {mean_non_linux:.2f}")

# Independent t-test
t_stat, p_val = ttest_ind(linux_games, non_linux_games, equal_var=False)
print(f"T-статистика: {t_stat:.4f}")
print(f"P-значение: {p_val:.4f}")

# HYPOTHESIS 5

df['lang'] = df['supported_languages'].str.split(',')
df['lang'] = df['lang'].apply(lambda x: [tag.strip().lower() for tag in x])
df['has_eng'] = df['lang'].apply(lambda lang_list: any('english' == lang for lang in lang_list))
print(df['has_eng'].value_counts())
# All games have English - can't test this hypothesis

# Check impact of Traditional Chinese
df['has_zh_trad'] = df['lang'].apply(lambda langs: 'traditional chinese' in langs)
print(df['has_zh_trad'].value_counts())

# Compare games with Traditional Chinese vs other
group_trad = df[df['has_zh_trad'] == True]['success']
group_no_trad = df[df['has_zh_trad'] == False]['success']

# Independent t-test
t_stat, p_val = ttest_ind(group_trad, group_no_trad, equal_var=False)
mean_trad = np.mean(group_trad)
mean_no_trad = np.mean(group_no_trad)
std_trad = np.std(group_trad, ddof=1)
std_no_trad = np.std(group_no_trad, ddof=1)
pooled_std = np.sqrt((std_trad ** 2 + std_no_trad ** 2) / 2)
cohen_d = (mean_trad - mean_no_trad) / pooled_std
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")
print(f"Mean success with Traditional Chinese: {group_trad.mean():.2f}")
print(f"Mean success without Traditional Chinese: {group_no_trad.mean():.2f}")
print(f"Cohen's d: {cohen_d:.3f}")

# HYPOTHESIS 6 

# Success and downloads over the years
yearly_stats = df.groupby('release_year').agg(
    avg_success=('success', 'mean'),
    avg_downloads=('estimated_downloads', 'mean')
).reset_index()

# Dual-axis plot: success and downloads by year
fig, ax1 = plt.subplots(figsize=(12, 6))
color = 'tab:blue'
ax1.set_xlabel('Год выпуска')
ax1.set_ylabel('Средняя успешность', color=color)
ax1.plot(yearly_stats['release_year'], yearly_stats['avg_success'], color=color, marker='o', label='Успешность')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Средние скачивания', color=color)
ax2.plot(yearly_stats['release_year'], yearly_stats['avg_downloads'], color=color, marker='s', label='Скачивания')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Средняя успешность и скачивания по годам')
fig.tight_layout()
plt.show()

# Regression analysis over all years
df_reg = df[df['release_year'].notna()]
x_all = df_reg['release_year']
y_all = df_reg['success']
slope_all, intercept_all, r_value_all, p_value_all, std_err_all = linregress(x_all, y_all)

print("Регрессия за всё время:")
print(f"Коэффициент наклона (slope): {slope_all:.2f}")
print(f"Свободный член (intercept): {intercept_all:.2f}")
print(f"R²: {r_value_all**2:.3f}")
print(f"p-value: {p_value_all:.4f}")
print(f"Размер эффекта (r): {r_value_all:.3f}")

# Regression since 2015
df_recent = df_reg[df_reg['release_year'] >= 2015]
x_recent = df_recent['release_year']
y_recent = df_recent['success']
slope_recent, intercept_recent, r_value_recent, p_value_recent, std_err_recent = linregress(x_recent, y_recent)

print("Регрессия с 2015 года:")
print(f"Коэффициент наклона (slope): {slope_recent:.2f}")
print(f"Свободный член (intercept): {intercept_recent:.2f}")
print(f"R²: {r_value_recent**2:.3f}")
print(f"p-value: {p_value_recent:.4f}")
print(f"Размер эффекта (r): {r_value_recent:.3f}")
