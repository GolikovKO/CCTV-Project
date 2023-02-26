from save_cropped_human_image import save_people_get_in_image, save_people_get_off_image
#from DbService import DbService
from StopCoords import StopCoords


def check_human_position(current_points, tracking_people, human_id, returned_frame, stop_id, frame_number,
                         humans_get_in_total_count, humans_get_off_total_count):

    stop_сoord = StopCoords()
    humans_count = 0

    if (((((current_points[0] <= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and  # если текущие координаты снаружи, а прошлые внутри, значит человек вышел с остановки
            current_points[0] <= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
            current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
            current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
           (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
            current_points[0] >= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
            current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
            current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
           (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
            current_points[0] >= stop_сoord.getX3() and current_points[0] <= stop_сoord.getX4() and
            current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
            current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
           (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
            current_points[0] <= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
            current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
            current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()))) == False) and
        ((((tracking_people[human_id][0] <= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and  # для xy первой координаты ног
            tracking_people[human_id][0] <= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
            tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
            tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
           (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
            tracking_people[human_id][0] >= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
            tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
            tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
           (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
            tracking_people[human_id][0] >= stop_сoord.getX3() and tracking_people[human_id][0] <= stop_сoord.getX4() and
            tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
            tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
           (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
            tracking_people[human_id][0] <= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
            tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
            tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()))) == True)):
            humans_count += 1
            humans_get_off_total_count += humans_count
            save_people_get_off_image(returned_frame, current_points, humans_get_off_total_count)
            time = int(frame_number / 30)

            x1 = current_points[0] - 60
            y1 = current_points[1] - 130
            x4 = current_points[0] + 60
            y4 = current_points[0] + 130

            #dbService = DbService()
            #dbService.loadPeopleGetoff(stop_id, time, x1, y1, x4, y4, people_getoff_total)
            flag = 1

            return humans_count, flag, returned_frame, current_points

    elif (((((current_points[0] <= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and  # если текущие координаты внутри, а прошлые снаружи, значит человек вошёл на остановку
              current_points[0] <= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
              current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
              current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
             (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
              current_points[0] >= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
              current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
              current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
             (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
              current_points[0] >= stop_сoord.getX3() and current_points[0] <= stop_сoord.getX4() and
              current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
              current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()) or
             (current_points[0] >= stop_сoord.getX1() and current_points[0] <= stop_сoord.getX2() and
              current_points[0] <= stop_сoord.getX3() and current_points[0] >= stop_сoord.getX4() and
              current_points[1] >= stop_сoord.getY1() and current_points[1] >= stop_сoord.getY2() and
              current_points[1] <= stop_сoord.getY3() and current_points[1] <= stop_сoord.getY4()))) == True) and
          ((((tracking_people[human_id][0] <= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and  # для xy первой координаты ног
              tracking_people[human_id][0] <= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
              tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
              tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
             (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
              tracking_people[human_id][0] >= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
              tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
              tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
             (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
              tracking_people[human_id][0] >= stop_сoord.getX3() and tracking_people[human_id][0] <= stop_сoord.getX4() and
              tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
              tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()) or
             (tracking_people[human_id][0] >= stop_сoord.getX1() and tracking_people[human_id][0] <= stop_сoord.getX2() and
              tracking_people[human_id][0] <= stop_сoord.getX3() and tracking_people[human_id][0] >= stop_сoord.getX4() and
              tracking_people[human_id][1] >= stop_сoord.getY1() and tracking_people[human_id][1] >= stop_сoord.getY2() and
              tracking_people[human_id][1] <= stop_сoord.getY3() and tracking_people[human_id][1] <= stop_сoord.getY4()))) == False)):
            humans_count += 1
            humans_get_in_total_count += humans_count
            save_people_get_in_image(returned_frame, current_points, humans_get_in_total_count)
            time = int(frame_number / 30)

            x1 = current_points[0] - 60
            y1 = current_points[1] - 130
            x4 = current_points[0] + 60
            y4 = current_points[0] + 130

            #dbService = DbService()
            #dbService.loadPeopleGetin(stop_id, time, x1, y1, x4, y4, people_getin_total)
            flag = 0

            return humans_count, flag, returned_frame, current_points

    else: # если изменений нет, люди не выходили и не входили, то возвращаем два
        return 2
