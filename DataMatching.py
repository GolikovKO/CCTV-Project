"""from DbService import DbService

class DataMatching():

    def matchData(self):

        dbService = DbService()
        vehicle_data = dbService.getVehicleData()
        people_data = dbService.getAllDataFromDb()

        path = r"C:\Users\Oleg\Desktop\matching.txt"
        file = open(path, "w")

        for peo, veh in zip(people_data, vehicle_data):
            file.write('stop_id = ' + str(peo[0]) + ', ' + 'amount = ' + str(peo[1]) + ', ' + 'time = ' + str(peo[2]) + ' | ' + 'time = ' + str(veh[0]) + ', ' + 'id = ' + str(veh[1]) + ', ' + 'type = ' + str(veh[2]) + ', ' + 'number = ' + str(veh[3]) + '\n')

        file.close()
        """