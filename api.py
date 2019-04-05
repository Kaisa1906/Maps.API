import sys
import requests
import pygame
import os
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QInputDialog, QHBoxLayout, QLabel

print(dir(PyQt5))
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi('untitled.ui', self)
        self.btn.clicked.connect(self.fun)

    def fun(self):
        try:
            toponym_longitude = self.x.text()
            toponym_lattitude = self.y.text()

            delta = "0.005"

            # Собираем параметры для запроса к StaticMapsAPI:
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join([delta, delta]),
                "l": "map"
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
            while pygame.event.wait().type != pygame.QUIT:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            delta = str(int(delta + 0.005))
                            # Собираем параметры для запроса к StaticMapsAPI:
                            map_params = {
                                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                                "spn": ",".join([delta, delta]),
                                "l": "map"
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
                        if event.key == pygame.K_DOWN:
                            delta = str(int(delta - 0.005))
                            # Собираем параметры для запроса к StaticMapsAPI:
                            map_params = {
                                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                                "spn": ",".join([delta, delta]),
                                "l": "map"
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
            pygame.quit()

            # Удаляем за собой файл с изображением.
            os.remove(map_file)
        except Exception:
            pass

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())