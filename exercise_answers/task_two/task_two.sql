-- Question 1:
-- What are the top 5 brands by receipts scanned for most recent month?
-- The dataset only contains data from 2021, so querying the most recent calendar month would return no results.
-- This query dynamically finds the latest month with data and retrieves the top 5 brands.
-- If the latest month has fewer than 5 brands, it expands to include the prior month to ensure meaningful results.

WITH month_ranked AS (
    SELECT
        TO_CHAR(r.date_scanned, 'YYYY-MM') AS month_year,
        b.name AS brand_name,
        COUNT(r.receipt_id) AS receipts_scanned,
        ROW_NUMBER() OVER (PARTITION BY TO_CHAR(r.date_scanned, 'YYYY-MM') ORDER BY COUNT(r.receipt_id) DESC) AS rank_per_month
    FROM receipts r
    JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
    JOIN brands b ON ri.brand_code = b.brand_code
    WHERE r.receipt_id IS NOT NULL
    GROUP BY month_year, b.name
    ORDER BY month_year DESC, receipts_scanned DESC
),
latest_month AS (
    SELECT month_year FROM month_ranked ORDER BY month_year DESC LIMIT 1
),
expanded_data AS (
    SELECT * FROM month_ranked WHERE month_year = (SELECT month_year FROM latest_month)
    UNION ALL
    SELECT * FROM month_ranked WHERE month_year < (SELECT month_year FROM latest_month)
    ORDER BY month_year DESC, receipts_scanned DESC
    LIMIT 5
)
SELECT brand_name, receipts_scanned, month_year
FROM expanded_data;

-- Question 3:
-- When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
-- There are not and "accepted" values in rewardsReceiptStatus, replacing with finished.
SELECT
    rewards_receipt_status,
    AVG(total_spent) AS avg_spent
FROM receipts
WHERE
    rewards_receipt_status IN ('FINISHED', 'REJECTED') AND total_spent > 0
GROUP BY rewards_receipt_status;

-- Question 4:
-- When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
-- There are not and "accepted" values in rewardsReceiptStatus, replacing with finished.
SELECT
    rewards_receipt_status,
    SUM(purchased_item_count) AS total_items
FROM receipts
WHERE
    rewards_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY rewards_receipt_status;