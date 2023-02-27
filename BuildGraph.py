import datetime
import math
import matplotlib.pyplot as plt

from matplotlib import dates
from db_functions import get_humans_count_by_time, get_arrivals_by_time


def get_hours_minutes_humans_count(flag, sql_data):
    if flag == 1:
        x_axis_humans_count = []
        y_axis_humans_time = []
        for row in sql_data:
            x_axis_humans_count.append(row[1])
            seconds = row[0].total_seconds()
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            hours_minutes = str(hours) + ':' + str(minutes)
            y_axis_humans_time.append(hours_minutes)
        return x_axis_humans_count, y_axis_humans_time
    else:
        vehicle_arrival_time = []
        for row in sql_data:
            seconds = row[2].total_seconds()
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            hours_minutes = str(hours) + ':' + str(minutes)
            vehicle_arrival_time.append(hours_minutes)
        return vehicle_arrival_time


def build_graph():
    humans_and_time = get_humans_count_by_time()
    vehicles_and_time = get_arrivals_by_time()

    x_axis_humans_count, y_axis_humans_time = get_hours_minutes_humans_count(1, humans_and_time)
    y_axis_humans_time = [datetime.datetime.strptime(i, "%H:%M") for i in y_axis_humans_time]

    fig, ax = plt.subplots()
    ax.plot(y_axis_humans_time, x_axis_humans_count, "-o")

    vehicle_arrival_time = get_hours_minutes_humans_count(0, vehicles_and_time)
    y_axis_vehicle_arrival_time = [datetime.datetime.strptime(i, "%H:%M") for i in vehicle_arrival_time]

    ax.vlines(y_axis_vehicle_arrival_time, min(x_axis_humans_count), max(x_axis_humans_count), colors='red')

    vehicle_arrival_in_graph_position = 0
    for i in y_axis_vehicle_arrival_time:
        ax.text(i, max(x_axis_humans_count) + 0.2, str(vehicles_and_time[vehicle_arrival_in_graph_position][4]) +
                str(vehicles_and_time[vehicle_arrival_in_graph_position][6]) + '(' +
                str(vehicles_and_time[vehicle_arrival_in_graph_position][3]) + ')',
                fontsize=12, horizontalalignment='center')
        vehicle_arrival_in_graph_position += 1

    date_formatter = dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(date_formatter)
    new_y_int_list = range(math.floor(min(x_axis_humans_count)), math.ceil(max(x_axis_humans_count)) + 1)

    plt.yticks(new_y_int_list)
    plt.xlabel('Время на момент обработки')
    plt.ylabel('Количество людей')
    plt.show()
    plt.savefig('./source/video_data/graph/graph.png')
