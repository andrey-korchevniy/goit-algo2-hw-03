import csv
import random

# Константи для генерації даних
NUM_ITEMS = 10000  # Кількість товарів
CATEGORIES = ["Electronics", "Clothing", "Food", "Books", "Home", "Sports", "Toys", "Beauty", "Health", "Garden"]
MIN_PRICE = 10.0
MAX_PRICE = 1000.0

def generate_items_data():
    items = []
    
    for i in range(1, NUM_ITEMS + 1):
        item = {
            "ID": str(i),
            "Name": f"Item {i}",
            "Category": random.choice(CATEGORIES),
            "Price": round(random.uniform(MIN_PRICE, MAX_PRICE), 2)
        }
        items.append(item)
    
    return items

def save_to_csv(items, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Category", "Price"])
        writer.writeheader()
        writer.writerows(items)

def main():
    print("Генеруємо тестові дані...")
    items = generate_items_data()
    
    file_path = "generated_items_data.csv"
    save_to_csv(items, file_path)
    
    print(f"Згенеровано {len(items)} товарів і збережено у {file_path}")

if __name__ == "__main__":
    main() 