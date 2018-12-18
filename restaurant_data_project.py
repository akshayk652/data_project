'''
Name : Available restaurants
Description : The program will read data from the file(.csv) provided by the user and based on the input data given by the
user, the list of all the resaturants available with respect to the data provided will be printed.
Input : User will input the filename and the date and time(dd/mm/yy hh:mm am/pm). 
Output : The result will be a list containing all the names of the restauants available on given particular day.
Usage : python restaurant_data_project.py <filename> 
                                         <datetime>
Example : python restaurant_data_project.py
        Provide file name(csv format): restaurant.csv
        Input Date and time in given format (dd/mm/yy hh:mm am/pm): 10/12/2018 10:00 am

>>['All Season Restaurant', 'Herbivore', 'Sabella & La Torre', 'Tong Palace', 'India Garden Restaurant', "Santorini's Mediterranean Cuisine"]

'''
import csv
from datetime import datetime
import calendar
import time

#Funtion to return list of open restaurants on a specific day.
def find_open_restaurants(csv_filename,search_status):
    date = search_status[0]
    input_time = " ".join(search_status[1:])
    input_time = input_time.replace(' ','')
    restaurants = {}
    open_restaurants = []
    #Get specific week day regarding a particular date.
    try:
        date = datetime.strptime(date,'%d/%m/%Y')
        given_day = calendar.day_name[date.weekday()][:3]
        #Read data from csv into python dictionary. 
        with open(csv_filename, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                restaurants[row[0]] = row[1]
        #Access data in dictionary.    
        for key in restaurants:
            restaurants[key] = restaurants[key].split("/")
            for i in range(len(restaurants[key])):
                #Remove whitespaces and make data efficient to process.
                d = restaurants[key][i].strip()
                d = d.replace(' am','am')
                d = d.replace(' pm','pm')
                d = d.replace(' - ','-')
                if ',' in d:
                    d = d.replace(', ',',')
                days,timing = d.split(' ')
                #Check whether restaurant is open or not.
                if (check_day(days,given_day) and check_time(timing,input_time)):
                    open_restaurants.append(key)
                    break
        return open_restaurants if (open_restaurants) else "Sorry no restaurant is available"
    except FileNotFoundError:
        print("File Not Found")
    except ValueError:
        print("Date does not match format 'dd/mm/yy'.\n Invalid Data ")

#Function to return whether if restaurant is available on given day or not.
def check_day(present_days,check_day):
    weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    if ',' in present_days:
        present_days = present_days.split(',')
        for day in present_days:
            if '-' in day:
                start_day,end_day = day.split('-')
                if check_day in weekdays[weekdays.index(start_day):weekdays.index(end_day)+1]:
                    return True
            elif check_day == day:
                return True
    elif '-' in present_days:
        start_day,end_day = present_days.split('-')
        if check_day in weekdays[weekdays.index(start_day):weekdays.index(end_day)+1]:
            return True
    elif present_days == check_day:
        return True
               
#Function to change time strings into time objects. 
def provide_time(times):
    if ':' in times:
        return time.strptime(times, "%I:%M%p")
    else:
        return time.strptime(times, "%I%p")
    
#Function to return whether if restaurant is available in given timing.
def check_time(present_timing,given_time):
    try:
        start_time,end_time = present_timing.split('-')
        start_time = provide_time(start_time)
        end_time = provide_time(end_time)
        given_time = provide_time(given_time)
        #compare time in between time range.
        if start_time < end_time:
            return given_time >= start_time and given_time <= end_time
        else: #Over midnight
            return given_time >= start_time or given_time <= end_time   
    except ValueError:
            print("Time does not match format 'hh:mmam/pm'\n Invalid Data ")
    
input_file = input("Provide file name(csv format): ")
search_datetime = input("Input Date and time in given format (dd/mm/yy hh:mm am/pm): ").split(" ")
print()#newline
available_restaurants = find_open_restaurants(input_file,search_datetime)
print(available_restaurants)

