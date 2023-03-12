from save_cropped_human_image import save_cropped_human_image
from stop_coords_points import Point
from code.database.db_functions import load_human


def load_human_to_dict(human_flag, human_count, frame, points):
    return {'human_flag': human_flag,
            'human_count': human_count,
            'frame': frame,
            'points': points}


def inside_check(current_points):
    stop_points = StopPointsCoords()
    if (((current_points[0] <= stop_points.getX1() and current_points[0] <= stop_points.getX2() and
          current_points[0] <= stop_points.getX3() and current_points[0] >= stop_points.getX4() and
          current_points[1] >= stop_points.getY1() and current_points[1] >= stop_points.getY2() and
          current_points[1] <= stop_points.getY3() and current_points[1] <= stop_points.getY4())
         or
         (current_points[0] >= stop_points.getX1() and current_points[0] <= stop_points.getX2() and
          current_points[0] >= stop_points.getX3() and current_points[0] >= stop_points.getX4() and
          current_points[1] >= stop_points.getY1() and current_points[1] >= stop_points.getY2() and
          current_points[1] <= stop_points.getY3() and current_points[1] <= stop_points.getY4())
         or
         (current_points[0] >= stop_points.getX1() and current_points[0] <= stop_points.getX2() and
          current_points[0] >= stop_points.getX3() and current_points[0] <= stop_points.getX4() and
          current_points[1] >= stop_points.getY1() and current_points[1] >= stop_points.getY2() and
          current_points[1] <= stop_points.getY3() and current_points[1] <= stop_points.getY4())
         or
         (current_points[0] >= stop_points.getX1() and current_points[0] <= stop_points.getX2() and
          current_points[0] <= stop_points.getX3() and current_points[0] >= stop_points.getX4() and
          current_points[1] >= stop_points.getY1() and current_points[1] >= stop_points.getY2() and
          current_points[1] <= stop_points.getY3() and current_points[1] <= stop_points.getY4()))) is False:
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
        human_get_off_flag = -1

        humans_get_off_total_count += 1
        handle_human(human_get_off_flag, returned_frame, current_points,
                     humans_get_off_total_count, frame_number, stop_id)

        return load_human_to_dict(human_get_off_flag, humans_get_off_total_count, returned_frame, current_points)
    # Если текущие координаты внутри, а прошлые снаружи, значит человек вошёл на остановку
    elif (current_frame_human_points is True) and (previous_frame_human_points is False):
        human_get_in_flag = 1

        humans_get_in_total_count += 1
        handle_human(human_get_in_flag, returned_frame, current_points,
                     humans_get_in_total_count, frame_number, stop_id)

        return load_human_to_dict(human_get_in_flag, humans_get_in_total_count, returned_frame, current_points)
    # Если изменений нет, люди не выходили и не входили, то возвращаем два
    else:
        human_not_moved_flag = 0
        return load_human_to_dict(human_not_moved_flag, None, None, None)
