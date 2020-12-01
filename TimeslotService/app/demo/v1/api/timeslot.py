# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json

class Timeslot(Resource):

    def put(self):
        print("Put Route")
        data = json.loads(str(request.data, encoding='utf-8'))
        with open('database.txt',"r") as outfile:
            json_data = json.load(outfile)
            print(json.dumps(data, indent=1))
            length = len(json_data['Dentists'])
            for i in range(0, length): 
                if (json_data['Dentists'][i]['Name'] == data['dentistName']): 
                    print("1--------")
                    for x in range(0, 7):
                        print("2--------")
                        if (json_data['Dentists'][i]['Appointments'][x]['AppointmentTime'] == data['appointmentTime']):
                            if (json_data['Dentists'][i]['Appointments'][x]['PatientName'] != ""):
                                return None, 400, None 
                            else: 
                                json_data['Dentists'][i]['Appointments'][x]['PatientName'] = data["patientName"]
                                with open('database.txt', "w") as outfile: 
                                    json.dump(json_data, outfile, indent=4)
            
        return data, 200, None

        #return {}, 200, None

    def delete(self):
        print("Delete route")
        data = json.loads(str(request.data, encoding='utf-8'))
        print("appointmentTime {}".format(data['appointmentTime']))
        print("dentistName {}".format(data['dentistName']))
        print("patientName {}".format(data['patientName']))

        with open('database.txt',"r") as outfile:
            json_data = json.load(outfile)
            print(json.dumps(data, indent=1))
            length = len(json_data['Dentists'])
            for i in range(0, length): 
                if (json_data['Dentists'][i]['Name'] == data["dentistName"]): 
                    print("1--------")
                    for x in range(0, 7):
                        if (json_data['Dentists'][i]['Appointments'][x]['AppointmentTime'] == data['appointmentTime']): 
                            if ((json_data['Dentists'][i]['Appointments'][x]['PatientName'] == data['patientName'])): 
                                print(data["patientName"])
                                print("--------")
                                json_data['Dentists'][i]['Appointments'][x]['PatientName'] = ""
                                with open('database.txt', "w") as outfile: 
                                    json.dump(json_data, outfile, indent=4)
                                return None, 204, None 

        return None, 404, None