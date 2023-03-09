import os
import math

from PyQt5.QtCore import QThread, pyqtSignal
from imageai.Detection import VideoObjectDetection

from stop_coords import StopCoords
from boxes_coords import locating_inside_stop, load_boxes_coords
from human_stop_status_check import check_human_position

center_box_points_previous_frame = []
tracked_humans = {}
human_count = 0
humans_inside_total_count = 0
humans_get_off_total_count = 0
humans_get_in_total_count = 0
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

            center_box_points_current_frame = []

            global human_count
            global center_box_points_previous_frame
            global humans_get_off_total_count
            global humans_get_in_total_count
            global humans_inside_total_count
            global tracked_humans
            global stopCoord
            # global video_path
            global stop_id

            #boxes = BoxesCoords()

            x, y = len(people_boxes_array), 8  # Создаём двумерный список, в котором количество элементов зависит от
            # количества обнаруженных людей на этом кадре,
            # и у каждого человека 8 координат - края ограничивающего прямоугольника
            boxes_coords = [[0 for j in range(y)] for i in range(x)]

            human_id = 0
            for human in people_boxes_array:  # В массиве из ограничивающих прямоугольников
                x1, y1, x4, y4 = human["box_points"]  # Для каждого найденного человека imageai даёт только четыре координаты: левый верхний угол и правый нижний
                central_box_point_x = int((x1 + x4) / 2)  # Ищем центральный х каждого прямоугольника
                central_box_point_y = int((y1 + y4) / 2)  # Ищем центральный y каждого прямоугольника
                center_box_points_current_frame.append((central_box_point_x, central_box_point_y))  # Добавляем в список центры каждого прямоугольника
                boxes_coords = load_boxes_coords(x1, y1, x4, y4, human_id, boxes_coords)  # Отправляем координаты в функцию чтобы найти остальные координаты
                human_id += 1  # Считаем каждый прямоугольник как найденного человека

            # Нужно определить, что человек с прошлого кадра это тот же самый человек на этом кадре
            # Для этого высчитываем расстояние между центральными точками ограничивающего прямоугольника
            # Если это расстояние меньше 25, значит это тот же самый человек

            # Чтобы начать считать по этому алгоритму, нужно добавить людей с первых двух кадров видео,
            # как координаты с текущего кадра и с прошлого кадра
            if frame_number <= 2:  # Если текущий кадр меньше или равен двум
                for current_points in center_box_points_current_frame:  # Для точек на текущем кадре
                    for previous_points in center_box_points_previous_frame:  # Для точек на предыдущем кадре
                        distance_between_points = math.hypot(previous_points[0] - current_points[0], previous_points[1]
                                                             - current_points[1])  # Высчитываем расстояние
                        if distance_between_points < 25:  # Если дистанция меньше этого значения
                            tracked_humans[human_count] = current_points  # То мы говорим что это тот же самый человек
                            human_count += 1  # Увеличиваем счётчик людей
            else:
                purified_dict = {}  # Бывает так, что некоторые люди записываются в словарь двараза. Чтобы это исправить очищаем словарь от одинаковых значений
                [purified_dict.update({k: v}) for k, v in tracked_humans.items() if v not in purified_dict.values()]
                tracked_humans = purified_dict

                tracking_human_copy = tracked_humans.copy()  # Делаем копию словаря с координатами обнаруженных людей, как словарь обнаруженных людей с прошлых кадров
                center_points_current_frame_copy = center_box_points_current_frame.copy()  # Делаем копию центральных точек текущего кадра

                for human_id, previous_points in tracking_human_copy.items():  # Для каждого человека в списке отслеженных людей с прошлых кадров
                    human_exists = False  # Ставим флаг, что человек не существует
                    for current_points in center_points_current_frame_copy:  # Для центральных точек текущего кадра
                        distance_between_points = math.hypot(previous_points[0] - current_points[0], previous_points[1] - current_points[1])  # Считаем расстояние между точками с прошлых кадров и текущими
                        # Если расстояние меньше, то это тот же самый человек
                        if distance_between_points < 25:
                            tracked_humans[human_id] = current_points  # Значит человек, находящийся в словаре обнаруженных людей с прошлых кадров, это этот же человек на этом кадре
                            human_exists = True  # Ставим флаг, что это тот же человек
                            # Когда определили,что это тот же самый человек, можно проверить вышел он с остановки или вошёл, или остался на том же месте

                            # Отправляем всё необходимое для определения в функцию
                            params = check_human_position(current_points, tracking_human_copy, human_id,
                                                          returned_frame, stop_id, frame_number,
                                                          humans_get_in_total_count, humans_get_off_total_count)
                            if params == 0:
                                pass
                            elif params[1] == 1:
                                humans_get_in_total_count += params[0]
                                self.update_getin_labels.emit(params[2], params[3])
                            elif params[1] == -1:
                                humans_get_off_total_count += params[0]
                                self.update_getoff_labels.emit(params[2], params[3])
                            if current_points in center_box_points_current_frame:  # Удаляем этого же самого человека из списка точек текущего кадра
                                center_box_points_current_frame.remove(current_points)
                    if not human_exists:  # Если этого человека не существует
                        tracked_humans.pop(human_id)  # то убираем его из списка
                for points in center_box_points_current_frame:  # Обновляем словарь на людей с этого кадра
                    tracked_humans[human_count] = points
                    human_count += 1

            center_box_points_previous_frame = center_box_points_current_frame.copy()  # Копируем центральные точки текущего кадра в массив точек прошлого кадра

            if frame_number % 30 == 0:  # Каждый 30 кадр делаем следующие действия, то есть, каждую секунду
                time = int(float(frame_number / 30))

                self.update_time.emit(time)

                humans_in_second_count = locating_inside_stop(stop_id, time, boxes_coords, stopCoord)
                print('Number of humans at the stop - ', humans_in_second_count)

                humans_inside_total_count += humans_in_second_count

                # graph = BuildGraph()
                # graph.buildGraph()

                #self.update_graph.emit()

            self.update_getin_amount.emit(humans_get_in_total_count)
            self.update_getoff_amount.emit(humans_get_off_total_count)

            print("Number of humans leave bus stop - ", humans_get_off_total_count)
            print("Number of humans came to the bus stop - ", humans_get_in_total_count)

        #  Настройка сети
        execution_path = os.getcwd()  # Записываем путь к папке проекта

        resnet_path = execution_path + '/resnet'  # Указываем путь к весам сети в папке проекта
        output_path = execution_path + '/source/detected_video/'  # Указываем путь для обработанного видео в папке проекта

        detector = VideoObjectDetection()  # Создаём экземпляр класса поиска предметов на видео
        detector.setModelTypeAsRetinaNet()  # Настраиваем класс на определённый вид модели
        detector.setModelPath(os.path.join(resnet_path, 'resnet.pth'))  # Веса для этого вида модели

        detector.loadModel()  # Загружаем тип сети и веса, под капотом какие-то алгоритмы для взаимодействия

        custom = detector.CustomObjects(person=True)  # Указываем что нужно искать только людей

        video = detector.detectObjectsFromVideo(  # Остальные настройки поиска, типа кадров в секунду, выводить логи в консоль и т.д.
            custom_objects=custom,
            input_file_path=os.path.join('D:/Dev/PyCharmProjects/CCTV-Project/source/video/cropped.mp4'), #('/home/kostya/PycharmProjects/CCTV/video/videos/cropped.mp4'),  # video_path),
            output_file_path=os.path.join(output_path, '../video'),
            frames_per_second=30,
            display_box=True,
            display_percentage_probability=False,
            display_object_name=False,
            log_progress=True,
            per_frame_function=for_frame,
            return_detected_frame=True
        )
