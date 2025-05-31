import json

# Загружаем данные из файла
with open(r'D:\Git\Home-project\1_price_list.json', 'r') as f:
    data = json.load(f)

# Выводим количество уникальных токенов
num_tokens = len(data)
print(f"Всего токенов: {num_tokens}")

# И выводим количество записей для каждого токена
for token, values in data.items():
    print(f"Токен {token} содержит {len(values)} записей")