# Receipts Table

| Column Name                | Data Type    | Key Type    | Description                                                                                       |
| -------------------------- | ------------ | ----------- | ------------------------------------------------------------------------------------------------- |
| id                         | UUID         | Primary Key | uuid for this receipt                                                                             |
| user_id                    | UUID         | Foreign Key | uuid ID of the user who submitted the receipt                                                     |
| bonus_points_earned        | INT          |             | Number of bonus points that were awarded upon receipt completion                                  |
| bonus_points_earned_reason | VARCHAR(255) |             | Event that triggered bonus points                                                                 |
| create_date                | TIMESTAMP    |             | The date that the event was created                                                               |
| date_scanned               | TIMESTAMP    |             | Date that the user scanned their receipt                                                          |
| finished_date              | TIMESTAMP    |             | Date that the receipt finished processing                                                         |
| modify_date                | TIMESTAMP    |             | The date the event was modified                                                                   |
| points_awarded_date        | TIMESTAMP    |             | The date we awarded points for the transaction                                                    |
| points_earned              | DECIMAL      |             | The number of points earned for the receipt                                                       |
| purchase_date              | TIMESTAMP    |             | The date of the purchase                                                                          |
| purchased_item_count       | TINYINT      |             | Count of number of items on the receipt                                                           |
| rewards_receipt_status     | ENUM         |             | Status of the receipt. Possible values: `FINISHED`, `PENDING`, `REJECTED`, `SUBMITTED`, `FLAGGED` |
| total_spent                | DECIMAL      |             | Total amount spent                                                                                |

#### Receipts Notes:

    Receipts table ID orginally is a MongoDB ObjectID and will need to be converted to a UUID.

# Receipt Item Table

| Column Name                            | Data Type    | Key Type    | Description                                |
| -------------------------------------- | ------------ | ----------- | ------------------------------------------ |
| id                                     | UUID         | Primary Key | uuid unique identifier for each receipt    |
| receipt_id                             | UUID         | Foreign Key | Links to receipts.id                       |
| barcode                                | VARCHAR(255) |             | Barcode of the purchased item              |
| description                            | TEXT         |             | Description of the purchased item          |
| final_price                            | DECIMAL      |             | Final price of the item after discounts    |
| item_price                             | DECIMAL      |             | Original item price                        |
| item_number                            | VERCHAR(125) |             | item number of product                     |
| price_after_coupon                     | DECIMAL      |             | Price after applying coupon                |
| needs_fetch_review                     | BOOLEAN      |             | Whether the item requires review           |
| needs_fetch_review_reason              | VARCHAR(255) |             | Reason for flag for fetch review           |
| metabrite_campaign_id                  | TEXT         |             | Campaign Id for metabrite                  |
| original_receipt_item_text             | TEXT         |             | Text from original receipt                 |
| original_final_price                   | DECIMAL      |             | Original final price                       |
| original_meta_brite_item_price         | DECIMAL      |             | Original meta brite price                  |
| original_meta_brite_barcode            | VARCHAR(255) |             | Orginal meta brite barcode                 |
| original_meta_brite_description        | TEXT         |             | Description of meta brite barcode          |
| original_meta_brite_quantity_purchased | VARCHAR(50)  |             | meta brite quantity purchased              |
| partner_item_id                        | VARCHAR(50)  |             | Partner's item ID for reference            |
| points_not_awarded_reason              | TEXT         |             | Reason points were not rewarded            |
| points_earned                          | VARCHAR(50)  |             | Points Earned                              |
| points_payer_id                        | VARCHAR(255) |             | ID for points payer                        |
| quantity_purchased                     | TINYINT      |             | Quantity purchased                         |
| rewards_group                          | TEXT         |             | Reward group description                   |
| rewards_product_partner_id             | VARCHAR(255) |             | ID of rewards product partner              |
| target_price                           | TINYTEXT     |             | Target price                               |
| prevent_target_gap_points              | BOOLEAN      |             | Flag to prevent awarding target gap points |
| user_flagged_barcode                   | VARCHAR(255) |             | User-submitted barcode (if flagged)        |
| user_flagged_description               | TEXT         |             | Description why it is flagged              |
| user_flagged_new_item                  | BOOLEAN      |             | When user flags new item                   |
| user_flagged_price                     | DECIMAL      |             | When user flags price                      |
| user_flagged_quantity                  | TINYINT      |             | When user flags quantity                   |
| brand_code                             | VARCHAR(75)  |             | code of brand                              |
| competitor_rewards_group               | VARCHAR(255) |             | competitor reward group                    |
| competitive_product                    | BOOLEAN      |             | Is it a competitive product                |
| discounted_item_price                  | DECIMAL      |             | Price of discounted Item                   |
| deleted                                | BOOLEAN      |             | was item deleted                           |

#### Receipt Item Notes:

    Barcode is a VARCHAR instead of a INT because it leads with a zero in some cases. Moreover, before querying the data I do n't know if there are any letters in the barcode.
