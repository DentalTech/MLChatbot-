from .credentials import TOKEN
import requests
import json
import pandas as pd
from datetime import datetime

context_cancel = 0
cancel_data = None
context_booking = 0
booking_data = {}


def getAvailableTimes(timeslots):
    print("Get available Times")
    length = len(timeslots['Dentists'])
    output_string = ""
    for i in range(0, length):
        output_string += "{} has the following availabilites:<br />".format(timeslots['Dentists'][i]["Name"])
        for x in range(0, 8):
            if ((timeslots['Dentists'][i]['Appointments'][x]['PatientName']) == ""):
                time = timeslots['Dentists'][i]['Appointments'][x]['AppointmentTime'] + ":00<br />"
                output_string += time
    return output_string

def getTimes(timeslots):
    print("Get available Times")
    print(timeslots)
    output_string = "{} has the following availabilities:<br />".format(timeslots["Name"])
    count = 0
    for x in range(0, 8):
            if ((timeslots["Appointments"][x]['PatientName']) == ""):
                count += 1
                output_string += timeslots["Appointments"][x]['AppointmentTime'] + ":00<br />"
    if (count == 0):
        return "There are no available times for {}. Please book an appointment with another dentist.".format(timeslots["Name"])
    else:
        return output_string

def validateAppointment(wit_response): 
    print(wit_response['entities'])
    try:
        time_entity = wit_response['entities']['wit$datetime:datetime'][0]['value']
        time_entity = time_entity.split(':')
        hour = time_entity[0].split('T')
        hour = hour[-1]
        minutes = time_entity[1].split('T')
        print(time_entity)
        if (minutes != ['00']): 
            return "Bookings can only be made at the start of each hour e.g. 1pm. Please re-book at this time."
        else: 
            if ((hour< "09") or (hour > "16")):
                return "Appointments can only be booked between 9:00 am and 4:00 pm."
            else: 
                pass 
    except:
        return "We did not recieve a valid time to book the appointment at. Please re-book the appointment with a valid time included" 
    try:
        wit_response['entities']['wit$contact:contact'][0]['value']
        pass
    except:
        return "You must specify valid Patient and Dentist name in your booking (e.g Please book an appointment for Alex with Dr.John at 2pm). "
        
    length = len(wit_response['entities']['wit$contact:contact'])
    print("Length {}".format(length))
    if (length < 2): 
        name = wit_response['entities']['wit$contact:contact'][0]['value']
        print(name[0:3])
        if (name[0:3] == "Dr."):
            return "You must also specify a valid patient name for us to book the appointment (e.g Please book an appointment for Alex with Dr.John at 2pm)."
        else: 
            return "You must also specify a valid dentist name for us to book the appointment (e.g Please book an appointment for Alex with Dr.John at 2pm)."
    elif (length == 2):
        for i in range(0, 2): 
            name = wit_response['entities']['wit$contact:contact'][i]['value']
            if (name[0:3] == "Dr."):
                print("6")
                return 1
    else: 
        print("7")
        return "We have recieved information for too many people. Please only specify a valid Dentist and single patient name as appointments can only be made for one person (e.g Please book an appointment for Alex with Dr.John at 2pm)."
    
def validateCancellation(wit_response): 
    print(wit_response['entities'])
    try:
        time_entity = wit_response['entities']['wit$datetime:datetime'][0]['value']
        time_entity = time_entity.split(':')
        hour = time_entity[0].split('T')
        hour = hour[-1]
        minutes = time_entity[1].split('T')
        print(time_entity)
        if (minutes != ['00']): 
            return "Bookings can only be made at the start of each hour e.g. 1pm. Please specify a valid appointment that you want to cancel."
        else: 
            if ((hour< "09") or (hour > "16")):
                return "Appointments can only be booked between 9:00 am and 4:00 pm. Please specify a valid appointment that you want to cancel"
            else: 
                pass 
    except:
        return "We did not recieve a valid time for the appointment that you would like to cancel" 
    try:
        wit_response['entities']['wit$contact:contact'][0]['value']
        pass
    except:
        return "You must specify valid Patient and Dentist name in your cancellation (e.g Please cancel appointment for Alex with Dr.John at 2pm). "
        
    length = len(wit_response['entities']['wit$contact:contact'])
    print("Length {}".format(length))
    if (length < 2): 
        name = wit_response['entities']['wit$contact:contact'][0]['value']
        print(name[0:3])
        if (name[0:3] == "Dr."):
            return "You must also specify a valid patient name for us to cancel the appointment (e.g Please cancel appointment for Alex with Dr.John at 2pm)."
        else: 
            return "You must also specify a valid dentist name for us to cancel the appointment (e.g Please cancel appointment for Alex with Dr.John at 2pm)."
    elif (length == 2):
        for i in range(0, 2): 
            name = wit_response['entities']['wit$contact:contact'][i]['value']
            if (name[0:3] == "Dr."):
                return 1
    else: 
        print("7")
        return "We have recieved cancellation information for too many people. Please only specify a valid Dentist and single patient name as appointments can only be made for one person (e.g Please book an appointment for Alex with Dr.John at 2pm)."
    

def ask_wit(expression):
    global context_cancel
    global cancel_data
    global context_booking
    global booking_data
    print("Ask_wit function triggered")
    print("Expression={}".format(expression))
    wit_response = requests.get('https://api.wit.ai/message?v=20201114&q={}'.format(expression), headers={'Authorization': TOKEN})
    wit_response = wit_response.json()
    print("Wit Response\n {}".format((json.dumps(wit_response, indent = 1))))
    try:
     intent = wit_response['intents'][0]['name']
     print("Intent={}".format(intent))
    except: 
        print("No Intent detected")
    if (intent == "AllDentistTimeSlot"):
        print("All DentistTimeSlot Route")
        timeslots = requests.get("http://0.0.0.0:5001/timeslot")
        timeslots = timeslots.json()
        timeslots = getAvailableTimes(timeslots)
        return timeslots
    if (intent == "DentistTimeslot"):
        print("DentistTimeSlot Route")
        entity = wit_response['entities']['wit$contact:contact'][0]['value']
        timeslots = requests.get("http://0.0.0.0:5001/timeslot/{}".format(entity))
        print(timeslots.status_code)
        if (timeslots.status_code == 200):
            timeslots = timeslots.json()
            timeslots = getTimes(timeslots)
            return timeslots
        else: 
            return "Sorry, that dentist is not available at our practice. Please specify a different dentist. (You may need to specify the detist as Dr.X"
    elif (intent == 'DentistDetails'):
        print("DentistInformation Route")
        entity = wit_response['entities']['wit$contact:contact'][0]['value']
        print("Entitiy={}".format(entity))
        dentist_details = requests.get("http://0.0.0.0:5002/dentist/{}".format(entity))
        dentist_details = dentist_details.json()
        dentist_details = json.loads(dentist_details)
        return "{} runs a practice in {} and specialises in {}. Can I help you with anything else?".format(dentist_details['name'], dentist_details['location'], dentist_details['specialisation'])
    elif (intent == "AllDentistAvailability"): 
        print("AvailableDentists Route")
        dentists = requests.get("http://0.0.0.0:5002/dentist")
        dentists = dentists.json()
        line_break = "<br />"
        dentist_details = "The available dentists are: {} {} {} {} {} {} {}Can I help you with anything else? ".format(line_break, dentists['Dentists'][0]['name'], line_break, dentists['Dentists'][1]['name'], 
        line_break, dentists['Dentists'][2]['name'], line_break)
        return dentist_details
    elif (intent == "Greetings"):
        print("Greetings Route")
        return "Hi, welcome to the chatbot. How can I help you?"
    elif (intent == "Custom_Greeting"):
        print("Custom Greetings Route")
        return "I am the Dentist Bot. I have no feelings."
    elif (intent == "BookAppointment"):
        validation = validateAppointment(wit_response)
        if (validation != 1):
            print("Validation {}".format(validation))
            return validation
        else:
            time_entity = wit_response['entities']['wit$datetime:datetime'][0]['value']
            time_entity = time_entity.split(':')
            time_entity = time_entity[0].split('T')
            time_entity = time_entity[-1]
            person = wit_response['entities']['wit$contact:contact'][0]['value']
            if (person[0:3] == "Dr."): 
                booking_data['dentistName'] = wit_response['entities']['wit$contact:contact'][0]['value']
                booking_data['patientName'] = wit_response['entities']['wit$contact:contact'][1]['value']
            else: 
                booking_data['dentistName'] = wit_response['entities']['wit$contact:contact'][1]['value']
                booking_data['patientName'] = wit_response['entities']['wit$contact:contact'][0]['value']

            booking_data['appointmentTime'] = time_entity
            context_booking = 1
            return "Do you want to confirm your booking for {} at {}:00 with {}? (Yes/No)".format(booking_data['patientName'], time_entity, booking_data['dentistName'])
    elif (intent == "CancelAppointment"):
        print("Cancel appointment reached")
        validation = validateCancellation(wit_response)
        if (validation!= 1):
            return validation
        else: 
            payload = {}
            time_entity = wit_response['entities']['wit$datetime:datetime'][0]['value']
            time_entity = time_entity.split(':')
            time_entity = time_entity[0].split('T')
            time_entity = time_entity[-1]
            payload['appointmentTime'] = time_entity
            length = len(wit_response['entities']['wit$contact:contact'])
            person = wit_response['entities']['wit$contact:contact'][0]['value']
            if (person[0:3] == "Dr."): 
                payload['dentistName'] = wit_response['entities']['wit$contact:contact'][0]['value']
                payload['patientName'] = wit_response['entities']['wit$contact:contact'][1]['value']
            else: 
                payload['dentistName'] = wit_response['entities']['wit$contact:contact'][1]['value']
                payload['patientName'] = wit_response['entities']['wit$contact:contact'][0]['value']
        cancel_data = json.dumps(payload, indent=1)
        context_cancel = 1
        return "Are you sure you want to delete your appointment? (Yes/No)"
    elif (intent == "YesNo"):
        print("YesNo")
        try:
            if ((context_cancel == 1) and (wit_response['entities']['Yes:Yes'] != None)): 
                r = requests.delete("http://0.0.0.0:5001/timeslot", data=cancel_data)
                if (r.status_code == 204):
                    context_cancel = 0
                    return "Your appointment has now been successfully cancelled. Is there anything else we can help you with?"
                else: 
                    return "We were unable to find your appointment. It may already be deleted or does not exist in our database."
        except: 
            pass
        try: 
            if ((context_cancel == 1) and (wit_response['entities']['No:No'] != None)):
                context_cancel = 0
                return "Your appointment has not been cancelled and still remains in place."
        except:
            pass
        try:
            print(booking_data['dentistName'])
            if ((context_booking == 1) and (wit_response['entities']['Yes:Yes'] != None)):
                context_booking = 0
                context_booking = 0
                print("________")
                local_data = json.dumps(booking_data)
                r = requests.put("http://0.0.0.0:5001/timeslot", data=local_data)
                print(r.status_code)
                if (r.status_code == 400):
                    timeslots = requests.get("http://0.0.0.0:5001/timeslot/{}".format(booking_data['dentistName']))
                    timeslots = timeslots.json()
                    string = "Your selected timeslot is unavailable. <br />"
                    timeslots = getTimes(timeslots)
                    string += timeslots
                    return string
                else:
                    data = json.loads(r.text)
                    return "Your appointment has been booked at {}:00 with {}.Is there anything else we can help you with?".format(data['appointmentTime'], data['dentistName'])
                return 0
        except:
            pass
        try: 
            if ((context_booking == 1) and (wit_response['entities']['No:No'] != None)):
                context_booking = 0
                return "Your appointment has not been booked. Please re-book if you would like an appointment." 
        except:
            pass 
    else:
        print("Query not recorded")
        return "Sorry we were unable to resolve your query. Please try again. Altering your phrasing may help."