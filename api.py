import sys
import requests
import pygame
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QHBoxLayout, QLabel

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.btn.clicked.connect(self.fun)
        self.shem.setChecked(True)
        self.shem.toggled.connect(self.v1)
        self.gibr.toggled.connect(self.v2)
        self.sput.toggled.connect(self.v3)
        self.vid = "map"
    def v1(self):
        self.vid = "map"
    def v2(self):
        self.vid = "sat,skl"
    def v3(self):
        self.vid = "sat"

        
    def fun(self):
        try:
            toponym_longitude = self.x.text()
            toponym_lattitude = self.y.text()
            
            delta = "0.005"
            # Собираем параметры для запроса к StaticMapsAPI:
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join([delta, delta]),
                "l": self.vid
            }
            print(map_params)
            map_api_server = "http://static-maps.yandex.ru/1.x/"
            # ... и выполняем запрос
            response = requests.get(map_api_server, params=map_params)

            # Запишем полученное изображение в файл.
            map_file = "map.png"
            try:
                with open(map_file, "wb") as file:
                    file.write(response.content)
            except IOError as ex:
                print("Ошибка записи временного файла:", ex)
                sys.exit(2)

            # Инициализируем pygame
            pygame.init()
            screen = pygame.display.set_mode((600, 450))
            # Рисуем картинку, загружаемую из только что созданного файла.
            screen.blit(pygame.image.load(map_file), (0, 0))
            # Переключаем экран и ждем закрытия окна.
            pygame.display.flip()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if float(delta) < 45:
                                delta = str(float(delta)*2)
                        if event.key == pygame.K_DOWN:
                            delta = str(float(delta)/2)
                        if event.key == pygame.K_w:
                            toponym_lattitude = str(float(toponym_lattitude) + float(delta))
                        if event.key == pygame.K_a:
                            toponym_longitude = str(float(toponym_longitude) - float(delta)*2)
                        if event.key == pygame.K_s:
                            toponym_lattitude = str(float(toponym_lattitude) - float(delta))
                        if event.key == pygame.K_d:
                            toponym_longitude = str(float(toponym_longitude) + float(delta)*2)
                        map_params = {
                                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                                "spn": ",".join([delta, delta]),
                                "l": self.vid
                            }
                        print(map_params)
                        map_api_server = "http://static-maps.yandex.ru/1.x/"
                        # ... и выполняем запрос
                        response = requests.get(map_api_server, params=map_params)

                        # Запишем полученное изображение в файл.
                        map_file = "map.png"
                        try:
                            with open(map_file, "wb") as file:
                                file.write(response.content)
                        except IOError as ex:
                            print("Ошибка записи временного файла:", ex)
                            sys.exit(2)
                            screen.blit(pygame.image.load(map_file), (0, 0))
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        
            pygame.quit()

            # Удаляем за собой файл с изображением.
            os.remove(map_file)
        except Exception:
            pass

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())