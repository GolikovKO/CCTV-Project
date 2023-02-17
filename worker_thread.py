import os
import math

from PyQt5.QtCore import QThread, pyqtSignal
from imageai.Detection import VideoObjectDetection

from StopCoords import StopCoords
from boxes_coords import BoxesCoords
from StopCheck import StopCheck

center_points_prev_frame = []
tracking_people = {}
people_id = 0
people_inside_total = 0
people_getoff_total = 0
people_getin_total = 0
stopCoord = StopCoords()
# video_path = ''
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

        def for_frame(frame_number, output_array, output_count, returned_frame):

            people_boxes_array = output_array

            self.update_frame_number.emit(frame_number)

            center_points_cur_frame = []

            global people_id
            global center_points_prev_frame
            global people_getoff_total
            global people_getin_total
            global people_inside_total
            global tracking_people
            global stopCoord
            # global video_path
            global stop_id

            #boxes = BoxesCoords()

            x, y = len(people_boxes_array), 8  # Cоздаём двумерный список, в котором количество элементов зависит от количества обнаруженных людей на этом кадре,
            # и у каждого человека 8 координат - края ограничивающего прямоугольника
            boxes_coords = [[0 for j in range(y)] for i in range(x)]

            humans_counter = 0
            for people_box in people_boxes_array:  # В массиве из ограничивающих прямоугольников
                x1, y1, x4, y4 = people_box["box_points"]  # Для каждого найденного человека imageai даёт только четыре координаты: левый верхний угол и правый нижний
                central_box_point_x = int((x1 + x4) / 2)  # Ищем центральный х каждого прямоугольника
                central_box_point_y = int((y1 + y4) / 2)  # Ищем центральный y каждого прямоугольника
                center_points_cur_frame.append((central_box_point_x, central_box_point_y))  # Добавляем в список центры каждого прямоугольника
                boxes_coords = BoxesCoords.load_boxes_coords(self, x1, y1, x4, y4, people_box, boxes_coords)  # Отправляем координаты в функцию чтобы найти остальные координаты
                humans_counter += 1  # Считаем каждый прямоугольник как найденного человека

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

            center_points_prev_frame = center_points_cur_frame.copy()  # Копируем центральные точки текущего кадра в массив точек прошлого кадра

            if frame_number % 30 == 0:  # Каждый 30 кадр делаем следующие действия, то есть, каждую секунду
                time = int(float(frame_number / 30))

                self.update_time.emit(time)

                people_at_sec = BoxesCoords.locatingInsideStop(stop_id, time, boxes_coords, stopCoord)
                print('people inside stop count - ', people_at_sec)

                people_inside_total += people_at_sec

                # graph = BuildGraph()
                # graph.buildGraph()

                self.update_graph.emit()

            self.update_getin_amount.emit(people_getin_total)
            self.update_getoff_amount.emit(people_getoff_total)

            print("people count leave bus stop - ", people_getoff_total)
            print("people count in bus stop - ", people_getin_total)

        #  Настройка сети
        execution_path = os.getcwd()  # Записываем путь к папке проекта

        resnet_path = execution_path + '/resnet'  # Указываем путь к весам сети в папке проекта
        output_path = execution_path + '/detected_video'  # Указываем путь для обработанного видео в папке проекта

        detector = VideoObjectDetection()  # Создаём экземпляр класса поиска предметов на видео
        detector.setModelTypeAsRetinaNet()  # Настраиваем класс на определённый вид модели
        detector.setModelPath(os.path.join(resnet_path, 'resnet.pth'))  # Веса для этого вида модели

        detector.loadModel()  # Загружаем тип сети и веса, под капотом какие-то алгоритмы для взаимодействия

        custom = detector.CustomObjects(person=True)  # Указываем что нужно искать только людей

        video = detector.detectObjectsFromVideo(  # Остальные настройки поиска, типа кадров в секунду, выводить логи в консоль и т.д.
            custom_objects=custom,
            input_file_path=os.path.join('/home/kostya/PycharmProjects/CCTV/video/videos/cropped.mp4'),  # video_path),
            output_file_path=os.path.join(output_path, 'detected'),
            frames_per_second=30,
            display_box=True,
            display_percentage_probability=False,
            display_object_name=False,
            log_progress=True,
            per_frame_function=for_frame,
            return_detected_frame=True
        )
