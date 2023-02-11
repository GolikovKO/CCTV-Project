#from DbService import DbService
from StopCoords import StopCoords

class BoxesCoords():

    def loadBoxesCoords(self, x1, y1, x4, y4, coordNumber, coords): # записываем координаты каждого найденного человека

        coords[coordNumber][0] = x1 # верхний левый
        coords[coordNumber][1] = y1
        coords[coordNumber][2] = x4 # верхний правый
        coords[coordNumber][3] = y1
        coords[coordNumber][4] = x1 # нижний левый
        coords[coordNumber][5] = y4
        coords[coordNumber][6] = x4 # нижний правый
        coords[coordNumber][7] = y4

        return coords

    def locatingInsideStop(self, stop_id, time, boxesCoords, stopCoord):
        
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