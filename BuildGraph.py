"""import datetime
import math

from matplotlib import dates
#from DbService import DbService
import numpy as np
import matplotlib.pyplot as plt

class BuildGraph():

    def buildGraph(self):

        dbService = DbService()
        people_data = dbService.getTimeAndPeople()
        ts_data = dbService.getPodezd()

        x_people = []
        y_people = []

        for row in people_data:
           x_people.append(row[1])
           seconds = row[0].total_seconds()
           hours = int(seconds // 3600)
           minutes = int((seconds % 3600) // 60)
           prom = str(hours) + ':' + str(minutes)
           y_people.append(prom)

        toDateTime_people = [datetime.datetime.strptime(i, "%H:%M") for i in y_people]

        fig, ax = plt.subplots()
        ax.plot(toDateTime_people, x_people, "-o")

        ts_time = []
        for row in ts_data:
           seconds = row[2].total_seconds()
           hours = int(seconds // 3600)
           minutes = int((seconds % 3600) // 60)
           proms = str(hours) + ':' + str(minutes)
           ts_time.append(proms)

        toDateTime_ts = [datetime.datetime.strptime(i, "%H:%M") for i in ts_time]

        ax.vlines(toDateTime_ts, min(x_people), max(x_people), colors = 'red')

        inside_list = 0
        for i in toDateTime_ts:
           ax.text(i, max(x_people) + 0.2, str(ts_data[inside_list][4]) + str(ts_data[inside_list][6]) + '(' + str(ts_data[inside_list][3]) + ')', fontsize = 12, horizontalalignment = 'center')
           inside_list += 1

        fmt = dates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(fmt)
        new_y_int_list = range(math.floor(min(x_people)), math.ceil(max(x_people)) + 1)

        plt.yticks(new_y_int_list)
        plt.xlabel('Время на момент обработки')
        plt.ylabel('Количество людей')
        plt.show()
        plt.savefig('D:\Dev\\vsCodeProjects\CCTV\\video_data\graph\graph.png')"""