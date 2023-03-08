from save_cropped_human_image import save_cropped_human_image
from stop_coords import StopCoords
from code.database.db_functions import load_human


def inside_check(points):
    stop_сoord = StopCoords()
    if (((points[0] <= stop_сoord.getX1() and points[0] <= stop_сoord.getX2() and
          points[0] <= stop_сoord.getX3() and points[0] >= stop_сoord.getX4() and
          points[1] >= stop_сoord.getY1() and points[1] >= stop_сoord.getY2() and
          points[1] <= stop_сoord.getY3() and points[1] <= stop_сoord.getY4()) or
         (points[0] >= stop_сoord.getX1() and points[0] <= stop_сoord.getX2() and
          points[0] >= stop_сoord.getX3() and points[0] >= stop_сoord.getX4() and
          points[1] >= stop_сoord.getY1() and points[1] >= stop_сoord.getY2() and
          points[1] <= stop_сoord.getY3() and points[1] <= stop_сoord.getY4()) or
         (points[0] >= stop_сoord.getX1() and points[0] <= stop_сoord.getX2() and
          points[0] >= stop_сoord.getX3() and points[0] <= stop_сoord.getX4() and
          points[1] >= stop_сoord.getY1() and points[1] >= stop_сoord.getY2() and
          points[1] <= stop_сoord.getY3() and points[1] <= stop_сoord.getY4()) or
         (points[0] >= stop_сoord.getX1() and points[0] <= stop_сoord.getX2() and
          points[0] <= stop_сoord.getX3() and points[0] >= stop_сoord.getX4() and
          points[1] >= stop_сoord.getY1() and points[1] >= stop_сoord.getY2() and
          points[1] <= stop_сoord.getY3() and points[1] <= stop_сoord.getY4()))) is False:
        return False
    else:
        return True


def handle_human(human_type, returned_frame, current_points, human_type_total_count, frame_number, stop_id):
    save_cropped_human_image(human_type, returned_frame, current_points, human_type_total_count)

    time_in_seconds = int(frame_number / 30)
    coord_x1 = current_points[0] - 60
    coord_y1 = current_points[1] - 130
    coord_x4 = current_points[0] + 60
    coord_y4 = current_points[0] + 130

    load_human(stop_id, time_in_seconds, coord_x1, coord_y1, coord_x4, coord_y4, human_type)


def check_human_position(current_points, tracked_humans, human_id, returned_frame, stop_id, frame_number,
                         humans_get_in_total_count, humans_get_off_total_count):
    current_frame_human_points = inside_check(current_points)
    previous_frame_human_points = inside_check(tracked_humans[human_id])

    # Если текущие координаты снаружи, а прошлые внутри, значит человек вышел с остановки
    if (current_frame_human_points is False) and (previous_frame_human_points is True):
        human_get_off_flag = 0

        humans_get_off_total_count += 1
        handle_human(human_get_off_flag, returned_frame, current_points,
                     humans_get_off_total_count, frame_number, stop_id)

        return humans_get_off_total_count, human_get_off_flag, returned_frame, current_points

    # Если текущие координаты внутри, а прошлые снаружи, значит человек вошёл на остановку
    elif (current_frame_human_points is True) and (previous_frame_human_points is False):
        human_get_in_flag = 1

        humans_get_in_total_count += 1
        handle_human(human_get_in_flag, returned_frame, current_points,
                     humans_get_in_total_count, frame_number, stop_id)

        return humans_get_in_total_count, human_get_in_flag, returned_frame, current_points

    else:  # Если изменений нет, люди не выходили и не входили, то возвращаем два
        human_not_moved_flag = 2
        return human_not_moved_flag
