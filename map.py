import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

from io import BytesIO
from httееp import get_spn

import requests
from PIL import Image


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.setWindowTitle('Карта')
        self.upload_to_widget()
        # self.ti_lox()

    def ti_lox(self):
        # toponym_to_find = " ".join(sys.argv[1:])

        toponym_to_find = 'Москва, ул. Верхние поля, 30'

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            pass

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": get_spn(toponym),
            "l": "map",
            "size": "650,450"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        return response.content

    def upload_to_widget(self):
        pixmap = QPixmap()
        pixmap.loadFromData(self.ti_lox())
        self.map_label.setPixmap(pixmap)

    # def keyPressEvent(self, event):
    #     if event.key == Qt.Key_PageUp:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
