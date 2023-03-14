from code.database.db_functions import load_human


# Записываем координаты каждого найденного человека
def load_boxes_coords(coord_x1, coord_y1, coord_x4, coord_y4, human_id, boxes_coords):
    boxes_coords[human_id][0] = coord_x1  # Верхний левый угол
    boxes_coords[human_id][1] = coord_y1
    boxes_coords[human_id][2] = coord_x4  # Верхний правый угол
    boxes_coords[human_id][3] = coord_y1
    boxes_coords[human_id][4] = coord_x1  # Нижний левый угол
    boxes_coords[human_id][5] = coord_y4
    boxes_coords[human_id][6] = coord_x4  # Нижний правый угол
    boxes_coords[human_id][7] = coord_y4

    return boxes_coords


def locating_inside_stop(stop_id, time, boxes_coords, stop_points):
    human_inside_count = 0
    # Проверка на нахождение точек ног внутри остановки
    for human_id in range(len(boxes_coords)):
        if (  # Для xy первой координаты ног
        ((boxes_coords[human_id][4] <= stop_points.getX1() and boxes_coords[human_id][4] <= stop_points.getX2() and
          boxes_coords[human_id][4] <= stop_points.getX3() and boxes_coords[human_id][4] >= stop_points.getX4() and
          boxes_coords[human_id][5] >= stop_points.getY1() and boxes_coords[human_id][5] >= stop_points.getY2() and
          boxes_coords[human_id][5] <= stop_points.getY3() and boxes_coords[human_id][5] <= stop_points.getY4())
         or
         (boxes_coords[human_id][4] >= stop_points.getX1() and boxes_coords[human_id][4] <= stop_points.getX2() and
          boxes_coords[human_id][4] >= stop_points.getX3() and boxes_coords[human_id][4] >= stop_points.getX4() and
          boxes_coords[human_id][5] >= stop_points.getY1() and boxes_coords[human_id][5] >= stop_points.getY2() and
          boxes_coords[human_id][5] <= stop_points.getY3() and boxes_coords[human_id][5] <= stop_points.getY4())
         or
         (boxes_coords[human_id][4] >= stop_points.getX1() and boxes_coords[human_id][4] <= stop_points.getX2() and
          boxes_coords[human_id][4] >= stop_points.getX3() and boxes_coords[human_id][4] <= stop_points.getX4() and
          boxes_coords[human_id][5] >= stop_points.getY1() and boxes_coords[human_id][5] >= stop_points.getY2() and
          boxes_coords[human_id][5] <= stop_points.getY3() and boxes_coords[human_id][5] <= stop_points.getY4())
         or
         (boxes_coords[human_id][4] >= stop_points.getX1() and boxes_coords[human_id][4] <= stop_points.getX2() and
          boxes_coords[human_id][4] <= stop_points.getX3() and boxes_coords[human_id][4] >= stop_points.getX4() and
          boxes_coords[human_id][5] >= stop_points.getY1() and boxes_coords[human_id][5] >= stop_points.getY2() and
          boxes_coords[human_id][5] <= stop_points.getY3() and boxes_coords[human_id][5] <= stop_points.getY4()))
                or  # Разграничение ИЛИ для двух точек | # Для xy второй координаты ног
        ((boxes_coords[human_id][6] <= stop_points.getX1() and boxes_coords[human_id][6] <= stop_points.getX2() and
          boxes_coords[human_id][6] <= stop_points.getX3() and boxes_coords[human_id][6] >= stop_points.getX4() and
          boxes_coords[human_id][7] >= stop_points.getY1() and boxes_coords[human_id][7] >= stop_points.getY2() and
          boxes_coords[human_id][7] <= stop_points.getY3() and boxes_coords[human_id][7] <= stop_points.getY4())
         or
         (boxes_coords[human_id][6] >= stop_points.getX1() and boxes_coords[human_id][6] <= stop_points.getX2() and
          boxes_coords[human_id][6] >= stop_points.getX3() and boxes_coords[human_id][6] >= stop_points.getX4() and
          boxes_coords[human_id][7] >= stop_points.getY1() and boxes_coords[human_id][7] >= stop_points.getY2() and
          boxes_coords[human_id][7] <= stop_points.getY3() and boxes_coords[human_id][7] <= stop_points.getY4())
         or
         (boxes_coords[human_id][6] >= stop_points.getX1() and boxes_coords[human_id][6] <= stop_points.getX2() and
          boxes_coords[human_id][6] >= stop_points.getX3() and boxes_coords[human_id][6] <= stop_points.getX4() and
          boxes_coords[human_id][7] >= stop_points.getY1() and boxes_coords[human_id][7] >= stop_points.getY2() and
          boxes_coords[human_id][7] <= stop_points.getY3() and boxes_coords[human_id][7] <= stop_points.getY4())
         or
         (boxes_coords[human_id][6] >= stop_points.getX1() and boxes_coords[human_id][6] <= stop_points.getX2() and
          boxes_coords[human_id][6] <= stop_points.getX3() and boxes_coords[human_id][6] >= stop_points.getX4() and
          boxes_coords[human_id][7] >= stop_points.getY1() and boxes_coords[human_id][7] >= stop_points.getY2() and
          boxes_coords[human_id][7] <= stop_points.getY3() and boxes_coords[human_id][7] <= stop_points.getY4()))
        ):
            human_inside_count += 1
            coord_x1 = boxes_coords[human_id][0]
            coord_y1 = boxes_coords[human_id][1]
            coord_x4 = boxes_coords[human_id][6]
            coord_y4 = boxes_coords[human_id][7]
            human_state_not_changed_flag = 0
            load_human(stop_id, time, coord_x1, coord_y1, coord_x4, coord_y4, human_state_not_changed_flag)

    return human_inside_count
