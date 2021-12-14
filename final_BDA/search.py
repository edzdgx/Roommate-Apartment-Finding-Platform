# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

import os
from google.cloud import bigquery

# this method will run when we first go to http://127.0.0.1:8000/search/ website
def search_post(request):
    return render(request, "post.html")

def process_apt_data(request):
    if request.POST['Certain Apartment'] == 'Yes':
        apartment = request.POST['Apartment']
        query_apt_data = pull_apt_from_gbp_by_certain(apartment)
    else:
        distance = request.POST['numDistance']
        budget = request.POST['numBudget']
        roomType = request.POST.getlist('Room Type')
        query_apt_data = pull_apt_from_gbp(distance, budget, roomType)
    return query_apt_data

def process_user_data(request):
    if request.POST['Roommate'] == 'No':
        return []

    if request.POST['Same School'] == 'Yes' and request.POST['Same Gender'] == 'Yes':
        school = request.POST['School']
        gender = request.POST['Gender']
        query_user_data = roommate_sameSchool_sameGender(school, gender)

    elif request.POST['Same School'] == 'No' and request.POST['Same Gender'] == 'Yes':
        gender = request.POST['Gender']
        query_user_data = roommate_sameGender(gender)

    elif request.POST['Same School'] == 'Yes' and request.POST['Same Gender'] == 'No':
        school = request.POST['School']
        query_user_data = roommate_sameSchool(school)
    else:
        query_user_data = pull_from_gbp('user')

    return query_user_data

def show_results(request):
    '''
    TODO: Make sure how to calculate this ration
    <QueryDict: {'csrfmiddlewaretoken': ['EmwCZrYwE79kaghvqgUA39De26046g8SjyPwwWktTTPDz974gEjX5mVfOBdAX76H'],
    'First Name': ['Jiaxiang'],
    'Last Name': ['Zhang'],
    'Uni': ['jz3275'],
    'Age': ['22'],
    'Gender': ['1'],
    'Nationality': ['China'],
    'Email': ['jz3275@columbia.edu'],
    'School': ['SEAS'],
     'Major': ['Electrical Engineering'],
     'Smoking': ['No'],
     'Alcohol': ['No'],
     'Habit': ['Early Bird'],
     'Pets': ['0'],
     'Certain Apartment': ['No'],
     'Apartment': ['ART LOFT/HOME:  DINNERS, GATHERINGS, PHOTO'],
     'numDistance': ['3'],
     'Room Type': ['Private room', 'Entire home/apt'],
     'numBudget': ['1600'],
     'Roommate': ['Yes'],
     'Number': ['1', '2'],
     'Same School': ['No'],
     'Same Gender': ['Yes']}>
    '''
#     print(f'request: {request.POST}')
#     push_to_gbq(request)
    results_data= {}
    if request.POST:
        query_apt_data = process_apt_data(request)
        length_apt = len(query_apt_data)
        query_user_data = process_user_data(request)
        length_user = len(query_user_data)

        for i in range(length_apt):
            apartment_Position = "apartment" + str(i)
            roomType_Position = "roomType" + str(i)
            location_Position = "location" + str(i)
            distance_Position = "distance" + str(i)
            results_data[apartment_Position] = query_apt_data[i]["name"]
            results_data[roomType_Position] = query_apt_data[i]["room_type"]
            results_data[location_Position] = query_apt_data[i]["neighbourhood"]
            results_data[distance_Position] = round(query_apt_data[i]["distance_line"],2)

        if length_user != 0:
            for i in range(length_user):
                fullName_Position = "fullName" + str(i)
                email_Position = "email" + str(i)
                gender_Position = "gender" + str(i)
                nationality_Position = "nationality" + str(i)
                roommateRatio_Position = "roommateRatio" + str(i)
                results_data[fullName_Position] = query_user_data[i]["Full_Name"]
                results_data[email_Position] = query_user_data[i]["Email_address"]
                if query_user_data[i]["Gender"] == 1:
                    results_data[gender_Position] = "Male"
                else:
                    results_data[gender_Position] = "Female"
                results_data[nationality_Position] = query_user_data[i]["Nationality"]
#                 results_data[roommateRatio_Position] = query_user_data[i]["Full_Name"]


        results_data['roommatesRecommendation'] = "Roommates Recommendation"
        results_data['apartmentRecommendation'] = "Apartment Recommendation"
        results_data['apartmentRatio0'] = "98%"
        results_data['apartmentRatio1'] = "95%"
        results_data['apartmentRatio2'] = "91%"



    return render(request, 'results.html', results_data)


# def push_to_gbq(results_data):
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
#     client = bigquery.Client()
#     table_id = "big-data-6893-326823.roommate.users"
#
#
#     rows_to_insert = [
#         {
#         'roommatesRecommendation': results_data['roommatesRecommendation'],
#         'apartmentRecommendation': results_data['apartmentRecommendation'],
#         'firstName': results_data['roommateRatio'],
#         'lastName': results_data['apartmentRatio'],
#         'uni': results_data['location'],
#         'gender': results_data['contact1'],
#         'nationality': results_data['apartment'],
#         'email': results_data['apartmentRatio1'],
#         'school': results_data['location1'],
#         'major': results_data['contact1'],
#         'smoking': results_data['apartment1'],
#         'alcohol': results_data['roomType1'],
#         'certainApartment': results_data['firstName'],
#         'apartment': results_data['lastName'],
#         'distance': results_data['fullName'],
#         'roomType': results_data['gender'],
#         'roommate': results_data['nationality'],
#         'number': results_data['email'],
#         'sameMajor': results_data['apartment'],
#         'sameGender': results_data['roomType'],
#         'habit': results_data['habit']
#         }
#     ]
#     errors = client.insert_rows_json(
#         table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
#     )  # Make an API request.
#     if errors == []:
#         print("New rows have been added.")
#     else:
#         print("Encountered errors while inserting rows: {}".format(errors))

def pull_from_gbp(option):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    if option == 'apartment':
        query = """
            SELECT *
            FROM `big-data-6893-326823.roommate.apartment`
        """
    elif option == 'user':
        query = """
            SELECT *
            FROM `big-data-6893-326823.roommate.roommates`
        """

    query_job = client.query(query)

    # TODO: store query into spark dataframe

    # list of dict
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data

def pull_apt_from_gbp_by_certain(apartment):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where name = '"+ apartment  +"'"
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def pull_apt_from_gbp(distance, budget, roomType):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    length = len(roomType)
    if length == 3:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 3"
    elif length == 2:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where room_type = '" + roomType[0] +"' or room_type = '" + roomType[1] +"' order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 3"
    else:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where room_type = '" + roomType[0] +"' order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 3"
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def roommate_sameSchool_sameGender(school, gender):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where School = '" + school + "' and Gender = " + gender
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data

def roommate_sameSchool(school):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where School = '" + school + "'"
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data

def roommate_sameGender(gender):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where Gender = '" + gender
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data

def find_your_roommate():
    pass