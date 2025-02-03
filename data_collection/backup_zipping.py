from data_collection.collecting import *


def backup_data(self):
    """Создание резервных копий данных"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_name = f"backup_{timestamp}.zip"
    # Здесь можно реализовать архивирование данных
    # Например, с использованием библиотеки zipfile
