import csv
import timeit
from BTrees.OOBTree import OOBTree

# Функція для завантаження даних з CSV файлу
def load_data(file_path):
    items = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Перетворюємо ціну на число з плаваючою точкою
            row['Price'] = float(row['Price'])
            items.append(row)
    return items

# Функція для додавання товару до OOBTree
def add_item_to_tree(tree, price_tree, item):
    # Додаємо до основного дерева з ID у якості ключа
    tree[item['ID']] = item
    
    # Додаємо до дерева з ціною у якості ключа
    # Якщо вже є товари з такою ціною, додаємо до списку
    if item['Price'] in price_tree:
        price_tree[item['Price']].append(item)
    else:
        price_tree[item['Price']] = [item]

# Функція для додавання товару до словника
def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

# Функція для виконання діапазонного запиту в OOBTree
def range_query_tree(price_tree, min_price, max_price):
    result = []
    # Використовуємо метод items(min, max) для швидкого отримання діапазону
    for price, items_list in price_tree.items(min_price, max_price):
        result.extend(items_list)
    return result

# Функція для виконання діапазонного запиту в словнику
def range_query_dict(dictionary, min_price, max_price):
    result = []
    # Проходимо по всіх елементах у словнику - лінійний пошук
    for key, item in dictionary.items():
        if min_price <= item['Price'] <= max_price:
            result.append(item)
    return result

def main():
    # Завантаження даних з CSV файлу
    try:
        items = load_data('generated_items_data.csv')
    except FileNotFoundError:
        print("Файл з даними не знайдено. Будь ласка, переконайтеся, що 'generated_items_data.csv' існує.")
        return
    
    # Створення структур даних
    tree = OOBTree()  # Дерево з ID у якості ключа
    price_tree = OOBTree()  # Дерево з ціною у якості ключа
    dictionary = {}
    
    # Заповнення структур даних
    for item in items:
        add_item_to_tree(tree, price_tree, item)
        add_item_to_dict(dictionary, item)
    
    # Визначення діапазону цін для запиту
    min_price = 100.0
    max_price = 500.0
    
    # Перевіряємо кількість знайдених елементів для обох структур
    ootree_results = range_query_tree(price_tree, min_price, max_price)
    dict_results = range_query_dict(dictionary, min_price, max_price)
    
    # Перевірка, що результати співпадають
    ootree_count = len(ootree_results)
    dict_count = len(dict_results)
    
    print(f"Кількість товарів, знайдених в OOBTree: {ootree_count}")
    print(f"Кількість товарів, знайдених в Dict: {dict_count}")
    print()
    
    # Вимірювання часу виконання діапазонного запиту для OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(price_tree, min_price, max_price),
        number=100
    )
    
    # Вимірювання часу виконання діапазонного запиту для словника
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price),
        number=100
    )
    
    # Виведення результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main() 