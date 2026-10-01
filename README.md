# Movie Industry Analysis: SQL + Python

End-to-end analysis of movie industry trends, built to answer the questions a studio or investor would ask before funding new films.

> **Note:** This is a portfolio project based on a sample dataset (543 movies), not client work.

## Business questions

1. Which genres generate the highest revenue?
2. Does a bigger budget guarantee bigger earnings?
3. Which countries produce the most successful films?
4. What are the top-performing movies overall?

## Tools

Python, SQL (SQLite / MySQL), pandas, Matplotlib, Seaborn

## Approach

1. **Loaded and cleaned the data**: converted `box_office` to numeric, removed one row with an invalid value ("unknown"), leaving 542 movies.
2. **Split multi-genre fields**: movies list several genres in one cell (e.g. "Action, Drama"), so I created a separate movie-genre table with one row per genre.
3. **Queried with SQL**: `GROUP BY`, `SUM()`, `AVG()`, `JOIN`, `HAVING`, `ORDER BY`, `LIMIT`.
4. **Analyzed with pandas**: aggregation, grouping and Pearson correlation.
5. **Visualized with Matplotlib and Seaborn.**

## Key findings

### 1. Top genres by total box office

| Genre | Total revenue | Movies |
|---|---|---|
| Adventure | ~$48.0B | 83 |
| Action | ~$44.4B | 106 |
| Drama | ~$36.1B | 369 |

![Top genres](charts/1_top_genres.png)

### 2. Budget vs. revenue

Pearson correlation: **r = 0.75**, a strong positive relationship. Bigger budgets tend to earn more, but it is no guarantee: about 16% of movies earned less than their budget, and films with $100-200M budgets show very different results.

![Budget vs revenue](charts/2_budget_vs_revenue.png)

### 3. Countries by average box office

Only countries with at least 5 movies are included, so a single hit does not distort the average.

| Country | Avg. revenue per film | Movies |
|---|---|---|
| USA | ~$380M | 184 |
| UK | ~$129M | 58 |
| France | ~$69M | 41 |
| Spain | ~$52M | 8 |
| South Korea | ~$40M | 71 |

![Top countries](charts/3_top_countries.png)

### 4. Bonus: return on investment (ROI)

ROI = box office / budget, genres with at least 10 movies. Horror (10.7x), Thriller (8.8x), Comedy (8.2x), Crime (8.1x) and Music (7.7x) return the most per dollar invested, because they typically have lower budgets.

![ROI by genre](charts/4_roi_by_genre.png)

### 5. Top 10 movies

See [`top10_movies.csv`](top10_movies.csv). The list is led by Avatar, Avengers: Endgame and Avatar: The Way of Water.

## Recommendations

- **Maximize total revenue:** invest in **Adventure, Action and Drama**, the top three genres by box office.
- **Maximize return per dollar:** consider **Horror and Thriller**, which deliver the highest ROI with smaller budgets.
- **Budgets:** a larger budget raises expected revenue, but it also raises risk, so large budgets should go to proven genres.
- **Countries:** the **USA** is the strongest market by far, followed by the **UK** and **France**.

## Limitations

- Box office figures are not adjusted for inflation, so older films are undervalued.
- ROI uses gross box office, not actual profit (marketing and distribution costs are not included).
- Some groups are small (Spain: 8 films, Horror: 17 films), so those results are less reliable.

## Files

| File | Description |
|---|---|
| `movie_analysis.py` | Main analysis script (commented) |
| `movie_queries.sql` | SQL queries used in the analysis |
| `movies.csv` | Dataset |
| `top10_movies.csv` | Output: top 10 movies by box office |
| `charts/` | Generated visualizations |

## How to run

```bash
pip install pandas matplotlib seaborn
python movie_analysis.py
```

To read from a MySQL database (`movies_db`) instead of the CSV:

```bash
pip install sqlalchemy pymysql
USE_MYSQL=1 DB_PASSWORD=your_password python movie_analysis.py
```# movie-industry-analysis
Portfolio project: end-to-end analysis of movie industry trends using SQL and Python.
