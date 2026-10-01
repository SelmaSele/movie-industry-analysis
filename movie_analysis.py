"""
Movie Industry Analysis: SQL + Python (pandas, Matplotlib, Seaborn)

Pokretanje:
    pip install pandas matplotlib seaborn
    python movie_analysis.py                       # cita movies.csv
    USE_MYSQL=1 DB_PASSWORD=xxx python movie_analysis.py   # cita tabelu movies iz MySQL movies_db
    (za MySQL dodatno: pip install sqlalchemy pymysql)
"""
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

CSV_PATH = "movies.csv"
USE_MYSQL = os.getenv("USE_MYSQL") == "1"
MIN_MOVIES_PER_COUNTRY = 5      # da jedan film ne iskrivi prosjek zemlje
OUT_DIR = "charts"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

def millions(x, _):
    return f"${x/1e6:,.0f}M"

def billions(x, _):
    return f"${x/1e9:,.1f}B"

# ---------- 1. UCITAVANJE I CISCENJE ----------
if USE_MYSQL:
    from sqlalchemy import create_engine
    pwd = os.environ["DB_PASSWORD"]          # lozinka nikad u kodu
    engine = create_engine(f"mysql+pymysql://root:{pwd}@localhost/movies_db")
    df = pd.read_sql("SELECT * FROM movies", engine)
else:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")   # utf-8-sig uklanja BOM

# box_office ima tekst ("unknown") -> pretvori u broj, nevalidne redove izbaci
df["box_office"] = pd.to_numeric(df["box_office"], errors="coerce")
before = len(df)
df = df.dropna(subset=["box_office", "budget"])
df = df[(df["budget"] > 0) & (df["box_office"] > 0)].copy()
print(f"Ucitano {before} filmova, nakon ciscenja ostaje {len(df)}.")

# Kolona genre sadrzi vise zanrova ("Action, Drama") -> posebna tabela, 1 red po zanru
genres = (df[["title", "genre"]]
          .assign(genre=df["genre"].str.split(","))
          .explode("genre"))
genres["genre"] = genres["genre"].str.strip()

# SQL se izvrsava nad SQLite bazom u memoriji (isti upiti rade i u MySQL-u)
conn = sqlite3.connect(":memory:")
df.to_sql("movies", conn, index=False)
genres.to_sql("movie_genres", conn, index=False)

def run(query):
    return pd.read_sql(query, conn)

# ---------- 2. TOP 3 ZANRA ----------
top_genres = run("""
    SELECT g.genre, SUM(m.box_office) AS total_revenue, COUNT(*) AS num_movies
    FROM movies m JOIN movie_genres g ON m.title = g.title
    GROUP BY g.genre ORDER BY total_revenue DESC LIMIT 3
""")
print("\nTop 3 zanra po zaradi:\n", top_genres)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=top_genres, x="genre", y="total_revenue", hue="genre", legend=False, ax=ax)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(billions))
ax.set(title="Top 3 zanra po ukupnoj zaradi", xlabel="Zanr", ylabel="Ukupna zarada")
plt.tight_layout(); plt.savefig(f"{OUT_DIR}/1_top_genres.png", dpi=150); plt.close()

# ---------- 3. BUDZET VS ZARADA ----------
avg = run("SELECT AVG(budget) AS avg_budget, AVG(box_office) AS avg_revenue FROM movies")
print("\nProsjecan budzet i zarada:\n", avg)

correlation = df[["budget", "box_office"]].corr().iloc[0, 1]
print(f"Pearson korelacija izmedju budzeta i zarade: {correlation:.2f}")

fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(data=df, x="budget", y="box_office", scatter_kws={"alpha": 0.4, "s": 20},
            line_kws={"color": "red"}, ax=ax)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(millions))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(millions))
ax.set(title=f"Budzet vs zarada (Pearson r = {correlation:.2f})", xlabel="Budzet", ylabel="Zarada")
plt.tight_layout(); plt.savefig(f"{OUT_DIR}/2_budget_vs_revenue.png", dpi=150); plt.close()

# Dodatno: ROI = zarada / budzet po zanru (zanrovi s najmanje 10 filmova)
roi = run("""
    SELECT g.genre, AVG(m.box_office * 1.0 / m.budget) AS avg_roi, COUNT(*) AS num_movies
    FROM movies m JOIN movie_genres g ON m.title = g.title
    GROUP BY g.genre HAVING COUNT(*) >= 10
    ORDER BY avg_roi DESC LIMIT 5
""")
print("\nTop 5 zanrova po ROI-u:\n", roi)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=roi, x="genre", y="avg_roi", hue="genre", legend=False, ax=ax)
ax.set(title="Prosjecan ROI po zanru (zarada / budzet)", xlabel="Zanr", ylabel="ROI (x)")
plt.tight_layout(); plt.savefig(f"{OUT_DIR}/4_roi_by_genre.png", dpi=150); plt.close()

# ---------- 4. ZEMLJE ----------
countries = run(f"""
    SELECT country, AVG(box_office) AS avg_revenue, COUNT(*) AS num_movies
    FROM movies GROUP BY country
    HAVING COUNT(*) >= {MIN_MOVIES_PER_COUNTRY}
    ORDER BY avg_revenue DESC LIMIT 5
""")
print("\nTop 5 zemalja po prosjecnoj zaradi:\n", countries)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=countries, x="country", y="avg_revenue", hue="country", legend=False, ax=ax)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(millions))
ax.set(title=f"Top 5 zemalja po prosjecnoj zaradi (min. {MIN_MOVIES_PER_COUNTRY} filmova)",
       xlabel="Zemlja", ylabel="Prosjecna zarada")
plt.tight_layout(); plt.savefig(f"{OUT_DIR}/3_top_countries.png", dpi=150); plt.close()

# ---------- 5. TOP 10 FILMOVA ----------
top10 = run("""
    SELECT title, release_year, genre, country, budget, box_office
    FROM movies ORDER BY box_office DESC LIMIT 10
""")
print("\nTop 10 filmova po zaradi:\n", top10.to_string())
top10.to_csv("top10_movies.csv", index=False)
print(f"\nGotovo. Grafikoni su u folderu '{OUT_DIR}/'.")
