from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#from imageai.Detection import VideoObjectDetection
from pynput import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

# from DataMatching import DataMatching
# from BuildGraph import BuildGraph
# from DbService import DbService
#from boxes_coords import BoxesCoords
#from human_stop_status_check import StopCheck
from StopCoords import StopCoords
from worker_thread import WorkerThread
import numpy
import math
import os
import pygame
import cv2
import sys

center_box_points_previous_frame = []
tracked_humans = {}
human_count = 0
humans_inside_total_count = 0
humans_get_off_total_count = 0
humans_get_in_total_count = 0
stopCoord = StopCoords()
# video_path = ''
stop_id = 0

label_in1_img = False
label_in2_img = False
label_in3_img = False

label_off1_img = False
label_off2_img = False
label_off3_img = False


class MainWindow(QMainWindow):

    def __init__(self):  # При инициализации происходит следующее:
        super().__init__()  # Инициализируем вызов родительского конструктора QMainWindow, или можно указать класс родителя напрямую
        #  QMainWindow.__init__(self)
        uic.loadUi('./interface/interface.ui', self)  # Загружаем файл с интерфейсом
        self.worker = WorkerThread()  # Инициализируем поток по конкретному классу
        self.stops_combo_box.addItems(['1', '2', '3', '4', '5'])  # Добавляем в комбо-бокс номера остановок
        self.video_load_btn.clicked.connect(self.evt_video_load_btn_clicked)  # Отслеживаем нажатие кнопки выбора видеозаписи

    def evt_video_load_btn_clicked(self):

        # global video_path
        global stop_id

        stopCoords = []  # Список координат остановки

        def on_click(x, y, button, pressed):  # добавление координат остановки

            if pressed:
                stopCoords.append(x)  # само добавление
                stopCoords.append(y)

            if not pressed:
                return False  # to stop Listener

        stop_id = int(self.stops_combo_box.currentText())  # Получаем номер выбранной остановки из комбо-бокса
        self.stops_combo_box.setEnabled(False)  # Выключаем комбо-бокс с номерами остановки после выбора видеозаписи

        video_path, _filters = QtWidgets.QFileDialog.getOpenFileName(None, 'Выберите видео')  # Вызов проводника для выбора видео TODO: Video path not working in other thread
        video_capture = cv2.VideoCapture(video_path)  # Передаём путь к видео к библиотеке cv2 для вырезки первого кадра
        success, image = video_capture.read()  # Считываем первый кадр видео

        first_frame_path = './source/video_data/first_video_frame/frame.png'  # Путь для сохранения первого кадра
        cv2.imwrite(first_frame_path, image)  # Сохраняем вырезанное изображение

        pygame.display.init()  # Инициализируем доступ к дисплею монитора
        img = pygame.image.load(first_frame_path)  # Загружаем путь сохранённого первого кадра видео
        screen = pygame.display.set_mode(img.get_size(),
                                         pygame.FULLSCREEN)  # Настраиваем отображение первого кадра видео для правильной ориентации координат
        screen.blit(img, (0, 0))  # Помещаем первый кадр видео на дисплей монитора с координатами верхнего левого угла
        pygame.display.flip()  # Обновляем дисплей монитора

        for i in range(4):  # Нужно получить границы остановки нажатием мыши, ставим слушатель на нажатие мышии добавляем координаты в список
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()

        stopCoord.setX1(stopCoords[0])  # верхний левый x # запись координат остановки в класс
        stopCoord.setY1(stopCoords[1])  # y
        stopCoord.setX2(stopCoords[2])  # верхний правый x
        stopCoord.setY2(stopCoords[3])  # y
        stopCoord.setX3(stopCoords[4])  # нижний правый x
        stopCoord.setY3(stopCoords[5])  # y
        stopCoord.setX4(stopCoords[6])  # нижний левый x
        stopCoord.setY4(stopCoords[7])  # y

        pygame.draw.lines(screen, (255, 0, 0), True,
                          [(stopCoord.getX1(), stopCoord.getY1()), (stopCoord.getX2(), stopCoord.getY2()),
                           (stopCoord.getX3(), stopCoord.getY3()), (stopCoord.getX4(), stopCoord.getY4())],
                          10)  # отрисовываем на картинке границы, нажатые мышкой
        pygame.display.flip()  # Обновляем дисплей монитора

        stop_image_path = './source/video_data/stop_area_frame/stop_area.png'  # Путь для сохранения кадра с остановкой

        pygame.image.save(screen, stop_image_path)  # Сохраняем картинку с границами
        pygame.display.quit()  # Выключаем доступ к дисплею монитора
        pygame.quit()  # Убираем картинку со всего экрана

        img = cv2.imread(stop_image_path)  # Загружаем путь к картинке остановки с границами
        cropped_image = img[0:1040, 652:1265]  # Обрезка чёрных зон по бокам для отображения в интерфейсе
        cv2.imwrite(stop_image_path, cropped_image)  # Пересохраняем картинку уже без чёрных зон

        pixmap = QPixmap(stop_image_path)  # Загружаем путь картинки для label'a в интерфейсе
        self.label_stop_area.setPixmap(pixmap)  # Устанавливаем эту картинку

        # Необходим второй поток для вычислений, чтобы интерфейс не зависал. Создаём его
        self.worker.start()  # Запускаем поток

        # Подключаем к потоку сигналы, то есть настройка события, при котором нужно вернуть значение в основной поток и обновить интерфейс
        self.worker.update_frame_number.connect(self.evt_update_frame_number)
        self.worker.update_time.connect(self.evt_update_time)
        self.worker.update_getin_amount.connect(self.evt_update_people_getin_amount)
        self.worker.update_getoff_amount.connect(self.evt_update_people_getoff_amount)
        self.worker.update_graph.connect(self.evt_update_graph)
        self.worker.update_getin_labels.connect(self.evt_update_getin_labels)
        self.worker.update_getoff_labels.connect(self.evt_update_getoff_labels)

    def evt_update_getoff_labels(self, frame, points):

        global label_off1_img
        global label_off2_img
        global label_off3_img

        ret = frame[points[1] - 130:points[1] + 130, points[0] - 60:points[0] + 60]
        image = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        converted_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        ready_image = QPixmap.fromImage(converted_image)

        if label_off1_img == False and label_off2_img == False and label_off3_img == False:

            self.label_out1.setPixmap(ready_image)
            label_off1_img = True

        elif label_off1_img == True and label_off2_img == False and label_off3_img == False:

            self.label_out2.setPixmap(ready_image)
            label_off2_img = True

        elif label_off1_img == True and label_off2_img == True and label_off3_img == False:

            self.label_out3.setPixmap(ready_image)
            label_off1_img = False
            label_off2_img = False

    def evt_update_getin_labels(self, frame, points):

        global label_in1_img
        global label_in2_img
        global label_in3_img

        ret = frame[points[1] - 130:points[1] + 130, points[0] - 60:points[0] + 60]
        image = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        converted_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        ready_image = QPixmap.fromImage(converted_image)

        if label_in1_img == False and label_in2_img == False and label_in3_img == False:

            self.label_in1.setPixmap(ready_image)
            label_in1_img = True

        elif label_in1_img == True and label_in2_img == False and label_in3_img == False:

            self.label_in2.setPixmap(ready_image)
            label_in2_img = True

        elif label_in1_img == True and label_in2_img == True and label_in3_img == False:

            self.label_in3.setPixmap(ready_image)
            label_in1_img = False
            label_in2_img = False

    def evt_update_graph(self):

        pixmap = QPixmap('./source/video_data/graph/graph.png')
        self.label_graph.setPixmap(pixmap)

    def evt_update_people_getoff_amount(self, amount):

        self.label_getoff_count.setText(str(amount))

    def evt_update_people_getin_amount(self, amount):

        self.label_getin_count.setText(str(amount))

    def evt_update_time(self, time):

        self.label_seconds_done.setText(str(time))

    def evt_update_frame_number(self, frame_number):

        self.label_frame_number.setText(str(frame_number))
