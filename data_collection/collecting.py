import requests

url = "https://api.hyperliquid.xyz/info"
payload = {"type": "meta"}  # Получить список доступных рынков
response = requests.post(url, json=payload).json()
print("Hyperliquid Markets:", response, sep='')