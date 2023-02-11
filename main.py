from os import environ

# from DataMatching import DataMatching
# from BuildGraph import BuildGraph
# from DbService import DbService
from BoxesCoords import BoxesCoords
from StopCheck import StopCheck
from StopCoords import StopCoords
from imageai.Detection import VideoObjectDetection
from pynput import mouse
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)
# import numpy
import math
import os
import pygame
import cv2
import sys

center_points_prev_frame = []
tracking_people = {}
people_id = 0
people_inside_total = 0
people_getoff_total = 0
people_getin_total = 0
stopCoord = StopCoords()
videoPath = ''
stop_id = 0


class WorkerThread(QThread):
    update_frame_number = pyqtSignal(int)
    update_time = pyqtSignal(int)
    update_getin_amount = pyqtSignal(int)
    update_getoff_amount = pyqtSignal(int)
    update_graph = pyqtSignal()
    update_getin_labels = pyqtSignal(object, object)
    update_getoff_labels = pyqtSignal(object, object)

    def run(self):

        def forFrame(frame_number, output_array, output_count, returned_frame):

            self.update_frame_number.emit(frame_number)

            coord_id = 0
            center_points_cur_frame = []

            global people_id
            global center_points_prev_frame
            global people_getoff_total
            global people_getin_total
            global people_inside_total
            global tracking_people
            global stopCoord
            global videoPath
            global stop_id

            boxes = BoxesCoords()

            x, y = len(
                output_array), 8  # создаём двумерный список, в котором количество элементов зависит от количества обнаруженных людей,
            # и у каждого человека 8 координат - края ограничивающего прямоугольника
            boxesCoords = [[0 for j in range(y)] for i in range(x)]

            for eachObject in output_array:
                x1, y1, x4, y4 = eachObject[
                    "box_points"]  # для каждого найденного человека imageai даёт только четыре координаты
                cx = int((x1 + x4) / 2)
                cy = int((y1 + y4) / 2)
                center_points_cur_frame.append((cx, cy))  # центры каждого прямоугольника
                boxesCoords = boxes.loadBoxesCoords(x1, y1, x4, y4, coord_id,
                                                    boxesCoords)  # отправляем их в функцию чтобы найти остальные координаты
                coord_id += 1  # счётчик людей

            if frame_number <= 2:
                for cur_points in center_points_cur_frame:
                    for prev_points in center_points_prev_frame:
                        distance = math.hypot(prev_points[0] - cur_points[0], prev_points[1] - cur_points[1])

                        if distance < 25:
                            tracking_people[people_id] = cur_points
                            people_id += 1
            else:
                prom_dict = {}  # была проблема что близкие люди записываются под одними координатами дав раза и чтобы это решить чистим одинаковые значения
                [prom_dict.update({k: v}) for k, v in tracking_people.items() if v not in prom_dict.values()]
                tracking_people = prom_dict

                tracking_people_copy = tracking_people.copy()
                center_points_cur_frame_copy = center_points_cur_frame.copy()

                for object_id, prev_points in tracking_people_copy.items():
                    object_exists = False
                    for cur_points in center_points_cur_frame_copy:
                        distance = math.hypot(prev_points[0] - cur_points[0], prev_points[1] - cur_points[1])

                        if distance < 25:
                            tracking_people[object_id] = cur_points
                            object_exists = True  # если центр на новом кадре не внутри остановки, а прошлый внутри, то человек выходит с остановки

                            stopCheck = StopCheck()
                            amount = stopCheck.peopleAmount(cur_points, stopCoord, tracking_people_copy, object_id,
                                                            returned_frame, stop_id, frame_number, people_getin_total,
                                                            people_getoff_total)

                            if amount == 2:
                                pass

                            elif amount[1] == 0:
                                people_getin_total += amount[0]
                                self.update_getin_labels.emit(amount[2], amount[3])

                            elif amount[1] == 1:
                                people_getoff_total += amount[0]
                                self.update_getoff_labels.emit(amount[2], amount[3])

                            if cur_points in center_points_cur_frame:
                                center_points_cur_frame.remove(cur_points)
                            continue

                    if not object_exists:
                        tracking_people.pop(object_id)

                for pt in center_points_cur_frame:
                    tracking_people[people_id] = pt
                    people_id += 1

            center_points_prev_frame = center_points_cur_frame.copy()

            if frame_number % 30 == 0:
                time = int(float(frame_number / 30))

                self.update_time.emit(time)

                people_at_sec = boxes.locatingInsideStop(stop_id, time, boxesCoords, stopCoord)
                print('people inside stop count - ', people_at_sec)

                people_inside_total += people_at_sec

                # graph = BuildGraph()
                # graph.buildGraph()

                self.update_graph.emit()

            self.update_getin_amount.emit(people_getin_total)
            self.update_getoff_amount.emit(people_getoff_total)

            print("people count leave bus stop - ", people_getoff_total)
            print("people count in bus stop - ", people_getin_total)

        execution_path = os.getcwd()

        resnet_path = execution_path + './resnet'
        output_path = execution_path + './detected_video'

        detector = VideoObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(resnet_path, "resnet.pth"))

        detector.loadModel()

        custom = detector.CustomObjects(person=True)

        video = detector.detectObjectsFromVideo(
            custom_objects=custom,
            input_file_path=os.path.join(videoPath),
            output_file_path=os.path.join(output_path, "detected"),
            frames_per_second=30,
            display_box=True,
            display_percentage_probability=False,
            display_object_name=False,
            log_progress=True,
            per_frame_function=forFrame,
            return_detected_frame=True
        )


label_in1_img = False
label_in2_img = False
label_in3_img = False

label_off1_img = False
label_off2_img = False
label_off3_img = False


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./interface/interface.ui', self)

        self.comboBox.addItems(['1', '2', '3', '4', '5'])

        self.videoLoadBtn.clicked.connect(self.evt_videoLoadBtn_clicked)

    def evt_videoLoadBtn_clicked(self):

        global videoPath
        global stop_id

        stop_id = int(self.comboBox.currentText())
        self.comboBox.setEnabled(False)

        videoPath = QtWidgets.QFileDialog.getOpenFileName(None, 'Выберите видео')[
            0]  # вызов проводника для выбора видео

        vidcap = cv2.VideoCapture(videoPath)
        success, image = vidcap.read()  # считываем первый кадр видео, чтобы указать границу остановки

        imagePath = './source/video_data/first_video_frame/stop_frame.png'  # путь для сохранения кадра остановки с границами
        cv2.imwrite(imagePath, image)
        stop_image = imagePath
        pygame.display.init()
        img = pygame.image.load(stop_image)  # загружаем картинку остановки
        screen = pygame.display.set_mode(img.get_size(),
                                         pygame.FULLSCREEN)  # настраиваем картинку на весь экран для правильной ориентации координат
        screen.blit(img, (0, 0))
        pygame.display.flip()  # открываем картинку

        stopCoords = []  # промежуточный список для координат остановки

        def on_click(x, y, button, pressed):  # добавление координат остановки

            if pressed == True:
                stopCoords.append(x)  # само добавление
                stopCoords.append(y)

            if not pressed:
                return False  # to stop Listener

        for i in range(4):  # границы остановки определяются четырьмя точками, поэтому цикл на 4
            with mouse.Listener(
                    on_click=on_click) as listener:
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
        pygame.display.flip()
        pygame.image.save(screen, './source/video_data/stop_area_frame/stop_area.png')  # сохраняем эту картинку с границами
        pygame.display.quit()
        pygame.quit()  # закрываем отображение картинки на весь экран

        img = cv2.imread('./source/video_data/stop_area_frame/stop_area.png')  # обрезаем чёрные зоны по бокам
        cropped_image = img[0:1040, 652:1265]
        cv2.imwrite('./source/video_data/stop_area_frame/stop_area.png', cropped_image)

        pixmap = QPixmap('./source/video_data/stop_area_frame/stop_area.png')
        self.label_stop_area.setPixmap(pixmap)

        self.worker = WorkerThread()
        self.worker.start()
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


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
