import pygame
import cv2

from stop_coords_points import Point
from worker_thread import WorkerThread
from pynput import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)


class MainWindow(QMainWindow):
    first_label_in = False
    second_label_in = False
    third_label_in = False

    first_label_off = False
    second_label_off = False
    third_label_off = False

    def __init__(self):  # При инициализации происходит следующее:
        super().__init__()  # Инициализируем вызов родительского конструктора QMainWindow,
        # или можно указать класс родителя напрямую
        #  QMainWindow.__init__(self)
        uic.loadUi('./interface/interface.ui', self)  # Загружаем файл с интерфейсом
        self.worker = WorkerThread()  # Инициализируем поток по конкретному классу
        self.stops_combo_box.addItems(['1', '2', '3', '4', '5'])  # Добавляем в комбо-бокс номера остановок
        self.video_load_btn.clicked.connect(self.video_load_btn_click_event)  # Отслеживаем нажатие кнопки выбора видеозаписи

    def video_load_btn_click_event(self):
        stopCoords = []  # Список координат остановки

        def on_click(x, y, button, pressed):  # добавление координат остановки
            if pressed:
                stopCoords.append(Point(x, y))
            if not pressed:
                return False  # to stop Listener

        stop_id = int(self.stops_combo_box.currentText())  # Получаем номер выбранной остановки из комбо-бокса
        self.stops_combo_box.setEnabled(False)  # Выключаем комбо-бокс с номерами остановки после выбора видеозаписи

        # Вызов проводника для выбора видео TODO: Video path not working in other thread
        video_path, _filters = QtWidgets.QFileDialog.getOpenFileName(None, 'Выберите видео')
        video_capture = cv2.VideoCapture(video_path)  # Передаём путь к видео к библиотеке cv2 для вырезки первого кадра
        success, image = video_capture.read()  # Считываем первый кадр видео

        first_frame_path = './source/video_data/first_video_frame/frame.png'  # Путь для сохранения первого кадра
        cv2.imwrite(first_frame_path, image)  # Сохраняем вырезанное изображение

        pygame.display.init()  # Инициализируем доступ к дисплею монитора
        img = pygame.image.load(first_frame_path)  # Загружаем путь сохранённого первого кадра видео
        # Настраиваем отображение первого кадра видео для правильной ориентации координат
        screen = pygame.display.set_mode(img.get_size(), pygame.FULLSCREEN)
        screen.blit(img, (0, 0))  # Помещаем первый кадр видео на дисплей монитора с координатами верхнего левого угла
        pygame.display.flip()  # Обновляем дисплей монитора
        # Нужно получить границы остановки нажатием мыши,ставим слушатель на нажатие мышии добавляем координаты в список
        for i in range(4):
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()

        border_points = []
        for Point in stopCoords:
            border_points.append(Point.__str__())

        # Отрисовываем на картинке границы, нажатые мышкой
        pygame.draw.lines(screen, (255, 0, 0), True, border_points, 10)
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

        # Подключаем к потоку сигналы, то есть настройка события,
        # при котором нужно вернуть значение в основной поток и обновить интерфейс
        self.worker.update_frame_number.connect(self.frame_number_update_event)
        self.worker.update_time.connect(self.time_update_event)
        self.worker.update_getin_amount.connect(self.people_get_in_amount_update_event)
        self.worker.update_getoff_amount.connect(self.people_get_off_amount_update_event)
        self.worker.update_graph.connect(self.graph_update_event)
        self.worker.update_getin_labels.connect(self.get_in_labels_update_event)
        self.worker.update_getoff_labels.connect(self.get_off_labels_update_event)

    def get_off_labels_update_event(self, frame, points):

        #global label_off1_img
        #global label_off2_img
        #global label_off3_img

        ret = frame[points[1] - 130:points[1] + 130, points[0] - 60:points[0] + 60]
        image = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        converted_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        ready_image = QPixmap.fromImage(converted_image)

        if MainWindow.first_label_off is False \
                and MainWindow.second_label_off is False \
                and MainWindow.third_label_off is False:

            self.label_out1.setPixmap(ready_image)
            MainWindow.first_label_off = True

        elif MainWindow.first_label_off is True \
                and MainWindow.second_label_off is False \
                and MainWindow.third_label_off is False:

            self.label_out2.setPixmap(ready_image)
            MainWindow.second_label_off = True

        elif MainWindow.first_label_off is True \
                and MainWindow.second_label_off is True \
                and MainWindow.third_label_off is False:

            self.label_out3.setPixmap(ready_image)
            MainWindow.first_label_off = False
            MainWindow.second_label_off = False

    def get_in_labels_update_event(self, frame, points):

        #global label_in1_img
        #global label_in2_img
        #global label_in3_img

        ret = frame[points[1] - 130:points[1] + 130, points[0] - 60:points[0] + 60]
        image = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        converted_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        ready_image = QPixmap.fromImage(converted_image)

        if MainWindow.first_label_in is False \
                and MainWindow.second_label_in is False \
                and MainWindow.third_label_in is False:

            self.label_in1.setPixmap(ready_image)
            MainWindow.first_label_in = True

        elif MainWindow.first_label_in is True \
                and MainWindow.second_label_in is False \
                and MainWindow.third_label_in is False:

            self.label_in2.setPixmap(ready_image)
            MainWindow.second_label_in = True

        elif MainWindow.first_label_in is True \
                and MainWindow.second_label_in is True \
                and MainWindow.third_label_in is False:

            self.label_in3.setPixmap(ready_image)
            MainWindow.first_label_in = False
            MainWindow.second_label_in = False

    def graph_update_event(self):

        pixmap = QPixmap('./source/video_data/graph/graph.png')
        self.label_graph.setPixmap(pixmap)

    def people_get_off_amount_update_event(self, amount):

        self.label_getoff_count.setText(str(amount))

    def people_get_in_amount_update_event(self, amount):

        self.label_getin_count.setText(str(amount))

    def time_update_event(self, time):

        self.label_seconds_done.setText(str(time))

    def frame_number_update_event(self, frame_number):

        self.label_frame_number.setText(str(frame_number))
