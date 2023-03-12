from pynput import mouse

from code.database.db_connection_settings import create_db_connection


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.x, self.y


stopCoords = []  # Список координат остановки


def on_click(x, y, button, pressed):  # добавление координат остановки
    if pressed:
        stopCoords.append(Point(x, y))
    if not pressed:
        return False  # to stop Listener
# Collect events until released


def main():
    for i in range(4):
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
    for Point in stopCoords:
        print(Point.__str__())
        print(type(Point.__str__()))


if __name__ == '__main__':
    main()
