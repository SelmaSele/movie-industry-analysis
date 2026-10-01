-- movie_queries.sql  (SQLite / MySQL)
-- Tabela movies: title, release_year, genre, director, language, country, duration, budget, box_office
-- Tabela movie_genres (title, genre): svaki film ima po jedan red za svaki zanr
--   (kolona genre u movies sadrzi vise zanrova u jednom polju, npr. "Action, Drama")

-- 1. Top 3 zanra po ukupnoj zaradi
SELECT g.genre, SUM(m.box_office) AS total_revenue, COUNT(*) AS num_movies
FROM movies m JOIN movie_genres g ON m.title = g.title
GROUP BY g.genre
ORDER BY total_revenue DESC
LIMIT 3;

-- 2. Prosjecan budzet i prosjecna zarada po filmu
SELECT AVG(budget) AS avg_budget, AVG(box_office) AS avg_revenue FROM movies;

-- 3. Top 5 zemalja po prosjecnoj zaradi (samo zemlje s najmanje 5 filmova)
SELECT country, AVG(box_office) AS avg_revenue, COUNT(*) AS num_movies
FROM movies
GROUP BY country
HAVING COUNT(*) >= 5
ORDER BY avg_revenue DESC
LIMIT 5;

-- 4. Top 10 filmova po zaradi
SELECT title, release_year, genre, country, budget, box_office
FROM movies
ORDER BY box_office DESC
LIMIT 10;
