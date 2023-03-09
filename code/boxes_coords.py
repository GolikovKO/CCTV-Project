from code.database.db_functions import load_human
#from stop_coords import StopCoords


def load_boxes_coords(coord_x1, coord_y1, coord_x4, coord_y4, human_id, boxes_coords):  # Записываем координаты каждого найденного человека
    boxes_coords[human_id][0] = coord_x1  # Верхний левый угол
    boxes_coords[human_id][1] = coord_y1
    boxes_coords[human_id][2] = coord_x4  # Верхний правый угол
    boxes_coords[human_id][3] = coord_y1
    boxes_coords[human_id][4] = coord_x1  # Нижний левый угол
    boxes_coords[human_id][5] = coord_y4
    boxes_coords[human_id][6] = coord_x4  # Нижний правый угол
    boxes_coords[human_id][7] = coord_y4

    return boxes_coords


def locating_inside_stop(stop_id, time, boxes_coords, stop_coords):
    human_inside_count = 0
    # Проверка на нахождение точек ног внутри остановки
    for i in range(len(boxes_coords)):
        if (
        ((boxes_coords[i][4] <= stop_coords.getX1() and boxes_coords[i][4] <= stop_coords.getX2() and  # для xy первой координаты ног
          boxes_coords[i][4] <= stop_coords.getX3() and boxes_coords[i][4] >= stop_coords.getX4() and
          boxes_coords[i][5] >= stop_coords.getY1() and boxes_coords[i][5] >= stop_coords.getY2() and
          boxes_coords[i][5] <= stop_coords.getY3() and boxes_coords[i][5] <= stop_coords.getY4())
         or
         (boxes_coords[i][4] >= stop_coords.getX1() and boxes_coords[i][4] <= stop_coords.getX2() and
          boxes_coords[i][4] >= stop_coords.getX3() and boxes_coords[i][4] >= stop_coords.getX4() and
          boxes_coords[i][5] >= stop_coords.getY1() and boxes_coords[i][5] >= stop_coords.getY2() and
          boxes_coords[i][5] <= stop_coords.getY3() and boxes_coords[i][5] <= stop_coords.getY4())
         or
         (boxes_coords[i][4] >= stop_coords.getX1() and boxes_coords[i][4] <= stop_coords.getX2() and
          boxes_coords[i][4] >= stop_coords.getX3() and boxes_coords[i][4] <= stop_coords.getX4() and
          boxes_coords[i][5] >= stop_coords.getY1() and boxes_coords[i][5] >= stop_coords.getY2() and
          boxes_coords[i][5] <= stop_coords.getY3() and boxes_coords[i][5] <= stop_coords.getY4())
         or
         (boxes_coords[i][4] >= stop_coords.getX1() and boxes_coords[i][4] <= stop_coords.getX2() and
          boxes_coords[i][4] <= stop_coords.getX3() and boxes_coords[i][4] >= stop_coords.getX4() and
          boxes_coords[i][5] >= stop_coords.getY1() and boxes_coords[i][5] >= stop_coords.getY2() and
          boxes_coords[i][5] <= stop_coords.getY3() and boxes_coords[i][5] <= stop_coords.getY4()))
                or  # разграничение ИЛИ для двух точек
        ((boxes_coords[i][6] <= stop_coords.getX1() and boxes_coords[i][6] <= stop_coords.getX2() and  # для xy второй координаты ног
          boxes_coords[i][6] <= stop_coords.getX3() and boxes_coords[i][6] >= stop_coords.getX4() and
          boxes_coords[i][7] >= stop_coords.getY1() and boxes_coords[i][7] >= stop_coords.getY2() and
          boxes_coords[i][7] <= stop_coords.getY3() and boxes_coords[i][7] <= stop_coords.getY4())
         or
         (boxes_coords[i][6] >= stop_coords.getX1() and boxes_coords[i][6] <= stop_coords.getX2() and
          boxes_coords[i][6] >= stop_coords.getX3() and boxes_coords[i][6] >= stop_coords.getX4() and
          boxes_coords[i][7] >= stop_coords.getY1() and boxes_coords[i][7] >= stop_coords.getY2() and
          boxes_coords[i][7] <= stop_coords.getY3() and boxes_coords[i][7] <= stop_coords.getY4())
         or
         (boxes_coords[i][6] >= stop_coords.getX1() and boxes_coords[i][6] <= stop_coords.getX2() and
          boxes_coords[i][6] >= stop_coords.getX3() and boxes_coords[i][6] <= stop_coords.getX4() and
          boxes_coords[i][7] >= stop_coords.getY1() and boxes_coords[i][7] >= stop_coords.getY2() and
          boxes_coords[i][7] <= stop_coords.getY3() and boxes_coords[i][7] <= stop_coords.getY4())
         or
         (boxes_coords[i][6] >= stop_coords.getX1() and boxes_coords[i][6] <= stop_coords.getX2() and
          boxes_coords[i][6] <= stop_coords.getX3() and boxes_coords[i][6] >= stop_coords.getX4() and
          boxes_coords[i][7] >= stop_coords.getY1() and boxes_coords[i][7] >= stop_coords.getY2() and
          boxes_coords[i][7] <= stop_coords.getY3() and boxes_coords[i][7] <= stop_coords.getY4()))
        ):
            human_inside_count += 1
            coord_x1 = boxes_coords[i][0]
            coord_y1 = boxes_coords[i][1]
            coord_x4 = boxes_coords[i][6]
            coord_y4 = boxes_coords[i][7]
            human_state_not_changed_flag = 0
            load_human(stop_id, time, coord_x1, coord_y1, coord_x4, coord_y4, human_state_not_changed_flag)

    return human_inside_count
