from SaveImage import SaveImage
#from DbService import DbService
from StopCoords import StopCoords

class StopCheck():

    def peopleAmount(self, cur_points, stopCoord, tracking_people, people_id, returned_frame, stop_id, frame_number, people_getin_total, people_getoff_total):

        stopCoord = StopCoords()
        people = 0

        if (((((cur_points[0] <= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and # если текущие координаты снаружи, а прошлые внутри, значит человек вышел с остановки
            cur_points[0] <= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or       
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] >= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] >= stopCoord.getX3() and cur_points[0] <= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] <= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()))) == False) and
            ((((tracking_people[people_id][0] <= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and # для xy первой координаты ног
            tracking_people[people_id][0] <= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or       
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] >= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] >= stopCoord.getX3() and tracking_people[people_id][0] <= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] <= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()))) == True)):
                people += 1
                people_getoff_total += people
                saveImage = SaveImage()
                saveImage.savePeopleGetOff(returned_frame, cur_points, people_getoff_total)
                time = int(frame_number / 30)

                x1 = cur_points[0] - 60
                y1 = cur_points[1] - 130
                x4 = cur_points[0] + 60
                y4 = cur_points[0] + 130

                #dbService = DbService()
                #dbService.loadPeopleGetoff(stop_id, time, x1, y1, x4, y4, people_getoff_total)
                flag = 1

                return people, flag, returned_frame, cur_points

        elif (((((cur_points[0] <= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and # если текущие координаты внутри, а прошлые снаружи, значит человек вошёл на остановку
            cur_points[0] <= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or       
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] >= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] >= stopCoord.getX3() and cur_points[0] <= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()) or
            (cur_points[0] >= stopCoord.getX1() and cur_points[0] <= stopCoord.getX2() and
            cur_points[0] <= stopCoord.getX3() and cur_points[0] >= stopCoord.getX4() and
            cur_points[1] >= stopCoord.getY1() and cur_points[1] >= stopCoord.getY2() and
            cur_points[1] <= stopCoord.getY3() and cur_points[1] <= stopCoord.getY4()))) == True) and
            ((((tracking_people[people_id][0] <= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and # для xy первой координаты ног
            tracking_people[people_id][0] <= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or       
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] >= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] >= stopCoord.getX3() and tracking_people[people_id][0] <= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()) or
            (tracking_people[people_id][0] >= stopCoord.getX1() and tracking_people[people_id][0] <= stopCoord.getX2() and
            tracking_people[people_id][0] <= stopCoord.getX3() and tracking_people[people_id][0] >= stopCoord.getX4() and
            tracking_people[people_id][1] >= stopCoord.getY1() and tracking_people[people_id][1] >= stopCoord.getY2() and
            tracking_people[people_id][1] <= stopCoord.getY3() and tracking_people[people_id][1] <= stopCoord.getY4()))) == False)):
                people += 1
                people_getin_total += people
                saveImage = SaveImage()
                saveImage.savePeopleGetIn(returned_frame, cur_points, people_getin_total)
                time = int(frame_number / 30)

                x1 = cur_points[0] - 60
                y1 = cur_points[1] - 130
                x4 = cur_points[0] + 60
                y4 = cur_points[0] + 130

                #dbService = DbService()
                #dbService.loadPeopleGetin(stop_id, time, x1, y1, x4, y4, people_getin_total)
                flag = 0

                return people, flag, returned_frame, cur_points

        else: # если изменений нет, люди не выходили и не входили, то возвращаем два
            return 2
