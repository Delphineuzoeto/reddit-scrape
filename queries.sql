-- ============================================
-- Beauty in Black - Reddit Sentiment Analysis
-- Author: Delphine
-- ============================================

-- 1. OVERALL SENTIMENT BREAKDOWN
SELECT 
    COUNT(*) as total,
    sentiment,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM clean_bib_sentiment
GROUP BY sentiment
ORDER BY total DESC;

-- 2. FILTER ONLY BEAUTYINBLACK SUBREDDIT WITH 3+ WORDS
CREATE VIEW IF NOT EXISTS final_bib_comments AS
SELECT * 
FROM clean_bib_sentiment
WHERE subreddit = 'BeautyinBlack'
AND LENGTH(comment_text) - LENGTH(REPLACE(comment_text, ' ', '')) >= 3;

-- 3. CHARACTER SENTIMENT ANALYSIS
CREATE VIEW IF NOT EXISTS character_sentiment AS
SELECT 'kimmie' as character, COUNT(*) as mentions, ROUND(AVG(compound),2) as avg_sentiment
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%kimmie%'
UNION ALL
SELECT 'mallory', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%mallory%'
UNION ALL
SELECT 'horace', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%horace%'
UNION ALL
SELECT 'roy', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%roy%'
UNION ALL
SELECT 'varney', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%varney%'
UNION ALL
SELECT 'angel', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%angel%'
UNION ALL
SELECT 'rain', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%rain%'
UNION ALL
SELECT 'jules', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%jules%'
UNION ALL
SELECT 'norman', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%norman%'
UNION ALL
SELECT 'olivia', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%olivia%'
UNION ALL
SELECT 'charles', COUNT(*), ROUND(AVG(compound),2)
FROM final_bib_comments WHERE LOWER(comment_text) LIKE '%charles%'
ORDER BY mentions DESC;

-- 4. SHORTEST COMMENTS (noise check)
SELECT comment_text, LENGTH(comment_text) as length
FROM clean_bib_sentiment
WHERE subreddit = 'BeautyinBlack'
ORDER BY length ASC
LIMIT 20;

-- 5. SENTIMENT BY SUBREDDIT
SELECT subreddit, COUNT(*) as total
FROM clean_bib_sentiment
GROUP BY subreddit
ORDER BY total DESC;

-- 6. TOP POSITIVE COMMENTS
SELECT comment_text, compound
FROM final_bib_comments
WHERE sentiment = 'positive'
ORDER BY compound DESC
LIMIT 10

-- 7. TOP NEGATIVE COMMENTS
SELECT comment_text, compound
FROM final_bib_comments
WHERE sentiment = 'negative'
ORDER BY compound ASC
LIMIT 10;

-- 8. SENTIMENT OVER TIME
SELECT 
    DATE(created_utc) as date,
    sentiment,
    COUNT(*) as count
FROM final_bib_comments
GROUP BY DATE(created_utc), sentiment
ORDER BY date ASC;