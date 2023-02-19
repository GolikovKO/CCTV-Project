#from DbService import DbService
from StopCoords import StopCoords


def load_boxes_coords(x1, y1, x4, y4, human_id, boxes_coords):  # Записываем координаты каждого найденного человека

    boxes_coords[human_id][0] = x1  # Верхний левый угол
    boxes_coords[human_id][1] = y1
    boxes_coords[human_id][2] = x4  # Верхний правый угол
    boxes_coords[human_id][3] = y1
    boxes_coords[human_id][4] = x1  # Нижний левый угол
    boxes_coords[human_id][5] = y4
    boxes_coords[human_id][6] = x4  # Нижний правый угол
    boxes_coords[human_id][7] = y4

    return boxes_coords


def locating_inside_stop(stop_id, time, boxesCoords, stopCoord):

    stopCoord = StopCoords()

    people = 0

    for i in range(len(boxesCoords)): # проверка на нахождение точек ног внутри остановки
        if (
        ((boxesCoords[i][4] <= stopCoord.getX1() and boxesCoords[i][4] <= stopCoord.getX2() and # для xy первой координаты ног
        boxesCoords[i][4] <= stopCoord.getX3() and boxesCoords[i][4] >= stopCoord.getX4() and
        boxesCoords[i][5] >= stopCoord.getY1() and boxesCoords[i][5] >= stopCoord.getY2() and
        boxesCoords[i][5] <= stopCoord.getY3() and boxesCoords[i][5] <= stopCoord.getY4()) or
        (boxesCoords[i][4] >= stopCoord.getX1() and boxesCoords[i][4] <= stopCoord.getX2() and
        boxesCoords[i][4] >= stopCoord.getX3() and boxesCoords[i][4] >= stopCoord.getX4() and
        boxesCoords[i][5] >= stopCoord.getY1() and boxesCoords[i][5] >= stopCoord.getY2() and
        boxesCoords[i][5] <= stopCoord.getY3() and boxesCoords[i][5] <= stopCoord.getY4()) or
        (boxesCoords[i][4] >= stopCoord.getX1() and boxesCoords[i][4] <= stopCoord.getX2() and
        boxesCoords[i][4] >= stopCoord.getX3() and boxesCoords[i][4] <= stopCoord.getX4() and
        boxesCoords[i][5] >= stopCoord.getY1() and boxesCoords[i][5] >= stopCoord.getY2() and
        boxesCoords[i][5] <= stopCoord.getY3() and boxesCoords[i][5] <= stopCoord.getY4()) or
        (boxesCoords[i][4] >= stopCoord.getX1() and boxesCoords[i][4] <= stopCoord.getX2() and
        boxesCoords[i][4] <= stopCoord.getX3() and boxesCoords[i][4] >= stopCoord.getX4() and
        boxesCoords[i][5] >= stopCoord.getY1() and boxesCoords[i][5] >= stopCoord.getY2() and
        boxesCoords[i][5] <= stopCoord.getY3() and boxesCoords[i][5] <= stopCoord.getY4())) or # разграничение ИЛИ для двух точек
        ((boxesCoords[i][6] <= stopCoord.getX1() and boxesCoords[i][6] <= stopCoord.getX2() and # для xy второй координаты ног
        boxesCoords[i][6] <= stopCoord.getX3() and boxesCoords[i][6] >= stopCoord.getX4() and
        boxesCoords[i][7] >= stopCoord.getY1() and boxesCoords[i][7] >= stopCoord.getY2() and
        boxesCoords[i][7] <= stopCoord.getY3() and boxesCoords[i][7] <= stopCoord.getY4()) or
        (boxesCoords[i][6] >= stopCoord.getX1() and boxesCoords[i][6] <= stopCoord.getX2() and
        boxesCoords[i][6] >= stopCoord.getX3() and boxesCoords[i][6] >= stopCoord.getX4() and
        boxesCoords[i][7] >= stopCoord.getY1() and boxesCoords[i][7] >= stopCoord.getY2() and
        boxesCoords[i][7] <= stopCoord.getY3() and boxesCoords[i][7] <= stopCoord.getY4()) or
        (boxesCoords[i][6] >= stopCoord.getX1() and boxesCoords[i][6] <= stopCoord.getX2() and
        boxesCoords[i][6] >= stopCoord.getX3() and boxesCoords[i][6] <= stopCoord.getX4() and
        boxesCoords[i][7] >= stopCoord.getY1() and boxesCoords[i][7] >= stopCoord.getY2() and
        boxesCoords[i][7] <= stopCoord.getY3() and boxesCoords[i][7] <= stopCoord.getY4()) or
        (boxesCoords[i][6] >= stopCoord.getX1() and boxesCoords[i][6] <= stopCoord.getX2() and
        boxesCoords[i][6] <= stopCoord.getX3() and boxesCoords[i][6] >= stopCoord.getX4() and
        boxesCoords[i][7] >= stopCoord.getY1() and boxesCoords[i][7] >= stopCoord.getY2() and
        boxesCoords[i][7] <= stopCoord.getY3() and boxesCoords[i][7] <= stopCoord.getY4()))
        ):
            people += 1
            x1 = boxesCoords[i][0]
            y1 = boxesCoords[i][1]
            x4 = boxesCoords[i][6]
            y4 = boxesCoords[i][7]

            #dbService = DbService()
            #dbService.loadPeopleInside(stop_id, time, x1, y1, x4, y4)

    return people
