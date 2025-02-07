import json
import re
from collections import defaultdict

def parse_malformed_json(file_path):
    """
    Reads and parses a malformed JSON file, ensuring each object is formatted properly.
    Returns a list of parsed JSON objects.
    """
    receipts = []
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
                receipts.append(json.loads(obj))
            except json.JSONDecodeError as e:
                skipped_entries += 1
                print(f"Skipping malformed JSON object #{skipped_entries}: {e}")

    print(f"\n✅ Successfully parsed {len(receipts)} receipts")
    print(f"⚠️ Skipped {skipped_entries} malformed entries (logged above)")

    return receipts


def extract_unique_keys(receipts):
    """
    Extracts all unique keys from:
      1. Parent-level receipt fields (e.g., totalSpent, userId, rewardsReceiptStatus)
      2. Nested fields in rewardsReceiptItemList.
    """
    parent_keys = defaultdict(set)
    item_keys = defaultdict(set)
    total_items = 0  
    total_receipts_with_items = 0  
    max_items = 0  
    max_receipt_id = None  

    def process_item(item, key_dict, prefix=""):
        """Recursively extracts keys and types, handling nested dictionaries."""
        for key, value in item.items():
            full_key = f"{prefix}{key}" if prefix else key
            key_dict[full_key].add(type(value).__name__)

            if isinstance(value, dict):
                process_item(value, key_dict, prefix=f"{full_key}.")

    for receipt in receipts:
        # Process parent-level fields (direct keys in the receipt object)
        process_item(receipt, parent_keys)

        # Process rewardsReceiptItemList separately
        if "rewardsReceiptItemList" in receipt and isinstance(receipt["rewardsReceiptItemList"], list):
            num_items = len(receipt["rewardsReceiptItemList"])
            total_items += num_items
            total_receipts_with_items += 1  

            if num_items > max_items:
                max_items = num_items
                max_receipt_id = receipt.get("_id", {}).get("$oid", "Unknown ID")

            for item in receipt["rewardsReceiptItemList"]:
                process_item(item, item_keys)

    return parent_keys, item_keys, total_items, total_receipts_with_items, max_items, max_receipt_id

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
    # File path
    file_path = "receipts.json"

    # Step 1: Parse receipts
    parsed_receipts = parse_malformed_json(file_path)

    # Step 2: Extract unique keys and count items
    parent_keys, item_keys, total_items, total_receipts_with_items, max_items, max_receipt_id = extract_unique_keys(parsed_receipts)
    
    reward_receipt_status = get_rewards_receipt_status(parsed_receipts)

    # Step 3: Print key statistics
    print("\n🔢 **Item Statistics**:")
    print(f"📦 Total individual items in rewardsReceiptItemList: {total_items}")
    print(f"📝 Number of receipts that contain rewardsReceiptItemList: {total_receipts_with_items}")
    print(f"🛒 Average items per receipt (including those without items): {total_items / len(parsed_receipts) if parsed_receipts else 0:.2f}")
    print(f"📊 Average items per receipt (only those that contain rewardsReceiptItemList): {total_items / total_receipts_with_items if total_receipts_with_items else 0:.2f}")
    print(f"🏆 Receipt with the most items: {max_items} items (Receipt ID: {max_receipt_id})")

    # Step 4: Print extracted parent-level keys
    print("\n🔍 **Extracted Parent-Level Keys & Data Types:**")
    for key, types in sorted(parent_keys.items()):
        print(f"{key}: {', '.join(types)}")

    # Step 5: Print extracted rewardsReceiptItemList keys
    print("\n🔍 **Extracted rewardsReceiptItemList Keys & Data Types:**")
    for key, types in sorted(item_keys.items()):
        print(f"{key}: {', '.join(types)}")
        
    print("\n🔍 **Extracted rewardsReceiptStatus:**")
    print(f"{reward_receipt_status}")
