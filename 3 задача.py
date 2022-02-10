import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
import math

SCREEN_SIZE = [600, 450]

LAT_STEP = 0.008
LON_STEP = 0.002
coord_to_geo = 0.0000428

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = 37.530887
        self.lat = 55.894568
        self.z = 15
        self.getImage()
        self.initUI()

    def getImage(self):
        params = {
            'll': f'{self.lon},{self.lat}',
            'z': self.z,
            'l': 'map'
        }
        api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def view_image(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.z < 19:
            self.z += 1
            self.view_image()
        elif event.key() == Qt.Key_PageDown and self.z > 0:
            self.z -= 1
            self.view_image()
        elif event.key() == Qt.Key_Left:
            self.lon -= LON_STEP * math.pow(2, 15 - self.z)
            self.lon %= 180
        elif event.key() == Qt.Key_Right:
            self.lon += LON_STEP * math.pow(2, 15 - self.z)
            self.lon %= 180
        elif event.key() == Qt.Key_Up and self.lat < 90:
            self.lat += LAT_STEP * math.pow(2, 15 - self.z)
        elif event.key() == Qt.Key_Down and self.lat > -90:
            self.lat -= LAT_STEP * math.pow(2, 15 - self.z)

        if -90 < self.lon < 90 and 0 < self.lat < 180:
            self.view_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
