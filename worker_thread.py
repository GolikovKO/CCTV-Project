import os
import math

from PyQt5.QtCore import QThread, pyqtSignal
from imageai.Detection import VideoObjectDetection
from BoxesCoords import BoxesCoords
from StopCheck import StopCheck


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
            global video_path
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
            input_file_path=os.path.join(video_path),
            output_file_path=os.path.join(output_path, "detected"),
            frames_per_second=30,
            display_box=True,
            display_percentage_probability=False,
            display_object_name=False,
            log_progress=True,
            per_frame_function=for_frame,
            return_detected_frame=True
        )
