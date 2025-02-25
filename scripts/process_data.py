from collections import defaultdict
import json
import re
import os

def parse_malformed_json(file_path):
    """
    Reads and parses a malformed JSON file, ensuring each object is formatted properly.
    Returns a list of parsed JSON objects.
    """
    data = []
    skipped_entries = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        raw_data = file.read()

        # Ensure JSON objects are properly separated
        raw_objects = re.split(r'}\s*{', raw_data.strip())

        formatted_objects = []
        for obj in raw_objects:
            obj = obj.strip()
            if not obj.startswith("{"):
                obj = "{" + obj
            if not obj.endswith("}"):
                obj = obj + "}"
            formatted_objects.append(obj)

        for obj in formatted_objects:
            try:
                data.append(json.loads(obj))
            except json.JSONDecodeError as e:
                skipped_entries += 1
                print(f"Skipping malformed JSON object #{skipped_entries}: {e}")

    print(f"\n✅ Successfully parsed {len(data)} data points")
    print(f"⚠️ Skipped {skipped_entries} malformed entries (logged above)")

    return data

def camel_to_snake(name: str) -> str:
    """
    Converts a camelCase or CamelCase string to snake_case.
    """
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

def convert_keys_to_snake_case(data):
    """
    Recursively converts dictionary keys to snake_case.
    """
    if isinstance(data, dict):
        return {camel_to_snake(key): convert_keys_to_snake_case(value)
                for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data

def save_cleaned_data_to_json(data, output_dir, output_filename):
    """
    Saves cleaned data to a JSON file.
    """
    
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
    output_file_path = os.path.join(output_dir, output_filename)
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  # Pretty-print JSON
        print(f"✅ Successfully saved cleaned data to: {output_file_path}")
    except Exception as e:
        print(f"❌ An error occurred while saving the data: {e}")

def extract_receipts_and_items(data):
    """
    Extracts receipts and their respective items into separate JSON structures.
    """
    receipts_data = []
    items_data = []

    for receipt in data:
        receipt_id = receipt.get("_id", {}).get("$oid", None)  # Extract receipt UUID
        user_id = receipt.get("userId", None)

        # Extract parent receipt fields
        receipt_record = {
            "receipt_id": receipt_id,
            "user_id": user_id,
            "purchase_date": receipt.get("purchase_date", {}).get("$date", None),
            "date_scanned": receipt.get("date_scanned", {}).get("$date", None),
            "create_date": receipt.get("create_date", {}).get("$date", None),
            "finished_date": receipt.get("finished_date", {}).get("$date", None),
            "modify_date": receipt.get("modify_date", {}).get("$date", None),
            "rewards_receipt_status": receipt.get("rewards_receipt_status", ""),
            "bonus_points_earned": receipt.get("bonus_points_earned", 0),
            "points_awarded_date": receipt.get("points_awarded_date", {}).get("$date", None),
            "points_earned": receipt.get("points_earned", 0),
            "purchased_item_count": receipt.get("purchased_item_count", 0),
            "total_spent": receipt.get("total_spent", 0),
            "bonus_points_earned_reason": receipt.get("bonus_points_earned_reason", ""),
        }

        receipts_data.append(receipt_record)

        # Extract items within rewardsReceiptItemList
        items = receipt.get("rewards_receipt_item_list", [])
        for item in items:
            item_record = {
                "receipt_id": receipt_id,  # Maintain relationship to the receipt
                "brand_code": item.get("brand_code", ""),
                "barcode": item.get("barcode", ""),
                "quantity_purchased": item.get("quantity_purchased", 0),
                "final_price": item.get("final_price", 0),
                "item_price": item.get("item_price", 0),
                "price_after_coupon": item.get("price_after_coupon", 0),
                "points_earned": item.get("points_earned", 0),
                "points_payer_id": item.get("points_payer_id", ""),
                "needs_fetch_review": item.get("needs_fetch_review", False),
                "needs_fetch_review_reason": item.get("needs_fetch_review_reason", ""),
                "description": item.get("description", ""),
                "original_receipt_item_text": item.get("original_receipt_item_text", ""),
                "metabrite_campaign_id": item.get("metabrite_campaign_id", ""),
                "original_meta_brite_barcode": item.get("original_meta_brite_barcode", ""),
                "original_meta_brite_description": item.get("original_meta_brite_description", ""),
                "original_final_price": item.get("original_final_price", 0),
                "original_meta_brite_item_price": item.get("original_meta_brite_item_price", 0),
                "original_meta_brite_quantity_purchased": item.get("original_meta_brite_quantity_purchased", 0),
                "user_flagged_barcode": item.get("user_flagged_barcode", ""),
                "user_flagged_description": item.get("user_flagged_description", ""),
                "user_flagged_new_item": item.get("user_flagged_new_item", False),
                "user_flagged_price": item.get("user_flagged_price", 0),
                "user_flagged_quantity": item.get("user_flagged_quantity", 0),
                "item_number": item.get("item_number", ""),
                "partner_item_id": item.get("partner_item_id", ""),
                "points_not_awarded_reason": item.get("points_not_awarded_reason", ""),
                "rewards_group": item.get("rewards_group", ""),
                "rewards_product_partner_id": item.get("rewards_product_partner_id", ""),
                "target_price": item.get("target_price", 0),
                "prevent_target_gap_points": item.get("prevent_target_gap_points", False),
                "competitor_rewards_group": item.get("competitor_rewards_group", ""),
                "competitive_product": item.get("competitive_product", 0),
                "discounted_item_price": item.get("discounted_item_price", 0),
                "deleted": item.get("deleted", False),
            }
            items_data.append(item_record)

    return receipts_data, items_data

def extract_unique_keys(data):
    """
    Extracts all unique keys from:
      1. Parent-level data fields 
      2. Nested fields in rewardsReceiptItemList.
    """
    parent_keys = defaultdict(set)
    item_keys = defaultdict(set)
    total_items = 0  
    total_data_points_with_items = 0  
    max_items = 0  
    max_data_id = None  
    list_of_review_reasons = set()
    list_of_sign_up_sources = set()
    list_of_brand_refs = set() 
    list_of_user_roles = set()

    def process_item(item, key_dict, prefix=""):
        """
        Recursively extracts keys and types, handling nested dictionaries.
        """
        for key, value in item.items():
            full_key = f"{prefix}{key}" if prefix else key
            key_dict[full_key].add(type(value).__name__)

            if isinstance(value, dict):
                process_item(value, key_dict, prefix=f"{full_key}.")

    def process_review_reasons_values(item, review_reasons_set):
        """ 
        Extracts all unique values from 'needsFetchReviewReason' and adds them to a given set. Only for receipts.
        """
        if "needsFetchReviewReason" in item:
            review_reasons = item["needsFetchReviewReason"]
            
            if isinstance(review_reasons, list):
                review_reasons_set.update(filter(None, review_reasons))
            elif isinstance(review_reasons, str):
                for reason in review_reasons.split(","):
                    cleaned_reason = reason.strip()
                    if cleaned_reason:
                        review_reasons_set.add(cleaned_reason)               

    def process_user_roles(item, user_roles_set):
        """ 
        Extracts all unique values from 'role' and adds them to a given set. Only for users.
        """
        if "role" in item:
            user_roles = item["role"]
            
            if isinstance(user_roles, list):
                user_roles_set.update(filter(None, user_roles))
            elif isinstance(user_roles, str):
                for role in user_roles.split(","):
                    cleaned_role = role.strip()
                    if cleaned_role:
                        user_roles_set.add(cleaned_role)
    
    def process_sign_up_sources(item, sign_up_sources_set):
        """ 
        Extracts all unique values from 'signUpSource' and adds them to a given set. Only for users.
        """
        if "signUpSource" in item:
            sign_up_sources = item["signUpSource"]
            
            if isinstance(sign_up_sources, list):
                sign_up_sources_set.update(filter(None, sign_up_sources))
            elif isinstance(sign_up_sources, str):
                for source in sign_up_sources.split(","):
                    cleaned_source = source.strip()
                    if cleaned_source:
                        sign_up_sources_set.add(cleaned_source)
   
    def process_unique_ref_values(data, ref_set):
        """
        Extracts all unique values from 'cpg.$ref' and adds them to a given set. Only for brands.
        """
        for entry in data:
            ref_value = entry.get("cpg", {}).get("$ref")  # Safely access nested key
            if ref_value:  # Ensure value is not None or empty
                ref_set.add(ref_value)  # Store unique values

    for data_point in data:
        # Process parent-level fields (direct keys in the receipt object)
        process_item(data_point, parent_keys)
        process_user_roles(data_point, list_of_user_roles)
        process_sign_up_sources(data_point, list_of_sign_up_sources)
        process_unique_ref_values([data_point], list_of_brand_refs)
        
        # Find and process all lists in the current data point
        for key, value in data_point.items():
            if isinstance(value, list):
                num_items = len(value)
                total_items += num_items
                total_data_points_with_items += 1  

                if num_items > max_items:
                    max_items = num_items
                    max_data_id = data_point.get("_id", {}).get("$oid", "Unknown ID")

                # Process each item in the list
                for item in value:
                    if isinstance(item, dict):  # Ensure it's a dictionary before processing
                        process_item(item, item_keys)
                        process_review_reasons_values(item, list_of_review_reasons)

    return parent_keys, item_keys, total_items, total_data_points_with_items, max_items, max_data_id, list_of_review_reasons, list_of_user_roles, list_of_sign_up_sources, list_of_brand_refs

def get_rewards_receipt_status(receipts):
    """
    Extracts the rewardsReceiptStatus field from each receipt.
    Returns a dictionary with the count of each status.
    """
    status_counts = defaultdict(int)

    for receipt in receipts:
        status = receipt.get("rewardsReceiptStatus", "Unknown")
        status_counts[status] += 1

    return status_counts

# --- Main Execution ---
if __name__ == "__main__":
    # Define the file path (Change this as needed)
    file_dir = "data"
    file_path = "brands.json"

    # Step 1: Parse JSON data
    parsed_data = parse_malformed_json(f"{file_dir}/{file_path}")

    parsed_data = convert_keys_to_snake_case(parsed_data)

    # Step 2: Extract unique keys and count items
    parent_keys, item_keys, total_items, total_data_points_with_items, max_items, max_data_id, needs_fetch_review_reason, list_of_user_roles, list_of_sign_up_sources, list_of_brand_refs = extract_unique_keys(parsed_data)
    
    # Get rewardsReceiptStatus (for receipts only)
    reward_receipt_status = get_rewards_receipt_status(parsed_data)

    # Common Statistics
    total_data_points = len(parsed_data)

    # **Dictionary-based dispatch pattern for cleaner conditional logic**
    file_stats = {
        "receipts.json": {
            "title": "Receipts Data Statistics",
            "total": total_data_points,
            "with_items": total_data_points_with_items,
            "without_items": total_data_points - total_data_points_with_items,
            "avg_items": total_items / total_data_points if total_data_points else 0,
            "avg_items_with": total_items / total_data_points_with_items if total_data_points_with_items else 0,
            "top_item_count": max_items,
            "top_item_receipt": max_data_id,
            "extra": f"📊 Rewards Receipt Status: {reward_receipt_status}",
        },
        "users.json": {
            "title": "User Data Statistics",
            "total": total_data_points,
            "roles": f"📝 User Roles:\n{json.dumps(list(list_of_user_roles), indent=2)}",
            "extra": f"📝 Sign Up Sources:\n{json.dumps(list(list_of_sign_up_sources), indent=2)}",
        },
        "brands.json": {
            "title": "Brand Data Statistics",
            "total": total_data_points,
            "extra": f"📝 Brand References:\n{json.dumps(list(list_of_brand_refs), indent=2)}",
        }
    }

    # 📌 Print relevant statistics based on file type
    if file_path in file_stats:
        stats = file_stats[file_path]
        print(f"\n📋 **{stats['title']}**")
        print(f"🧾 Total entries: {stats['total']}")

        if "with_items" in stats:
            print(f"📊 Entries with items: {stats['with_items']} ({(stats['with_items'] / stats['total']) * 100:.2f}%)")
            print(f"📊 Entries without items: {stats['without_items']} ({(stats['without_items'] / stats['total']) * 100:.2f}%)")
            print(f"📊 Average items per entry: {stats['avg_items']:.2f}")
            print(f"📊 Average items per entry (only those that contain items): {stats['avg_items_with']:.2f}")
            print(f"🏆 Entry with most items: {stats['top_item_count']} (ID: {stats['top_item_receipt']})")

        print(f"\n🔍 **Extracted Parent-Level Keys & Data Types:**")
        for key, types in sorted(parent_keys.items()):
            print(f"{key}: {', '.join(types)}")
        
        if "roles" in stats:
            print(f"\n{stats['roles']}")

        if "extra" in stats:
            print(f"\n{stats['extra']}")
            
    output_dir = "data/cleaned"

    if file_path == "receipts.json":
        receipts_data, items_data = extract_receipts_and_items(parsed_data)
        save_cleaned_data_to_json(receipts_data, output_dir, "cleaned_receipts.json")
        save_cleaned_data_to_json(items_data, output_dir, "cleaned_receipt_items.json")
    else:
        output_file = f"cleaned_{file_path}"
        save_cleaned_data_to_json(parsed_data, "data/cleaned", output_file)