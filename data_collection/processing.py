from data_collection.collecting import *

def process_ws_data(self, data):
    """Обработка данных WebSocket"""
    try:
        # Пример обработки данных (нужно адаптировать под структуру Hyperliquid)
        processed = {
            'timestamp': datetime.now().isoformat(),
            'symbol': data.get('s'),
            'bid': float(data.get('b')[0][0]),
            'ask': float(data.get('a')[0][0]),
            'bid_qty': float(data.get('b')[0][1]),
            'ask_qty': float(data.get('a')[0][1])
        }
        return processed
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
