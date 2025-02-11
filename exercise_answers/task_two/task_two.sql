-- Query 1: Find the top 5 brands by distinct receipts scanned in the most recent full month.
WITH recent_month AS (
  SELECT
    DATE( MAX("date_scanned")) AS start_date,
    DATE( MAX("date_scanned")) + INTERVAL '1 month' AS end_date
  FROM receipts
)
SELECT
  b.name AS brand_name,
  COUNT(DISTINCT r.receipt_id) AS receipt_count
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
JOIN brands b ON ri.brand_code = b.brand_code
JOIN recent_month rm
    ON DATE(r.date_scanned) >= rm.start_date
    AND DATE(r.date_scanned) < rm.end_date
GROUP BY b.name
ORDER BY receipt_count DESC
LIMIT 5;



-- Query 2: Compare brand rankings by receipt count for the recent and previous months.
WITH recent AS (
  SELECT b.name AS brand_name,
         COUNT(DISTINCT r.receipt_id) AS receipt_count,
         'recent' AS period
  FROM receipts r
  JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
  JOIN brands b ON ri.brand_code = b.brand_code
  WHERE r.date_scanned >= date_trunc('month', current_date) - interval '1 month'
    AND r.date_scanned < date_trunc('month', current_date)
  GROUP BY b.name
),
previous AS (
  SELECT b.name AS brand_name,
         COUNT(DISTINCT r.receipt_id) AS receipt_count,
         'previous' AS period
  FROM receipts r
  JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
  JOIN brands b ON ri.brand_code = b.brand_code
  WHERE r.date_scanned >= date_trunc('month', current_date) - interval '2 month'
    AND r.date_scanned < date_trunc('month', current_date) - interval '1 month'
  GROUP BY b.name
),
combined AS (
  SELECT * FROM recent
  UNION ALL
  SELECT * FROM previous
)
SELECT period,
       brand_name,
       receipt_count,
       RANK() OVER (PARTITION BY period ORDER BY receipt_count DESC) AS rank_position
FROM combined
ORDER BY period, rank_position;




-- Query 3: Compare the average total_spent for receipts with Accepted vs Rejected status.
SELECT rewards_receipt_status,
       AVG(total_spent) AS avg_spend
FROM receipts
WHERE rewards_receipt_status IN ('Accepted', 'Rejected')
GROUP BY rewards_receipt_status;




-- Query 4: Compare the sum of purchased_item_count for receipts with Accepted vs Rejected status.
SELECT rewards_receipt_status,
       SUM(purchased_item_count) AS total_items_purchased
FROM receipts
WHERE rewards_receipt_status IN ('Accepted', 'Rejected')
GROUP BY rewards_receipt_status;



-- Query 5: Identify the brand with the highest spend among users created within the past 6 months.
SELECT b.name AS brand_name,
       SUM(r.total_spent) AS total_spend
FROM receipts r
JOIN users u ON r.user_id = u.user_id
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
JOIN brands b ON ri.brand_code = b.brand_code
WHERE u.create_date >= current_date - interval '6 month'
GROUP BY b.name
ORDER BY total_spend DESC
LIMIT 1;



-- Query 6: Identify the brand with the most transactions among users created within the past 6 months.
SELECT b.name AS brand_name,
       COUNT(DISTINCT r.receipt_id) AS transaction_count
FROM receipts r
JOIN users u ON r.user_id = u.user_id
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
JOIN brands b ON ri.brand_code = b.brand_code
WHERE u.create_date >= current_date - interval '6 month'
GROUP BY b.name
ORDER BY transaction_count DESC
LIMIT 1;
