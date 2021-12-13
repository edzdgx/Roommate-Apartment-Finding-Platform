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

#     apt_data_from_gbq =  pull_from_gbp('apartment') # type: list

def show_results(request):
    '''
    TODO: please put the results here and I can show them on the result page
    <QueryDict: {'csrfmiddlewaretoken': ['EmwCZrYwE79kaghvqgUA39De26046g8SjyPwwWktTTPDz974gEjX5mVfOBdAX76H'],
    'First Name': ['Jiaxiang'],
    'Last Name': ['Zhang'],
    'Uni': ['jz3275'],
    'Age': ['22'],
    'Gender': ['Male'],
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
     'Same Major': ['No'],
     'Same Gender': ['Yes']}>
    '''
#     print(f'request: {request.POST}')
    results_data= {}
    if request.POST:
        query_apt_data = process_apt_data(request)
        print(query_apt_data)
#         results_data['roommatesRecommendation'] = "Roommates Recommendation"
#         results_data['apartmentRecommendation'] = "Apartment Recommendation"
#         results_data['roommateRatio'] = "95%"
#         results_data['apartmentRatio'] = "98%"
#         results_data['location'] = "Upper West Side"
#         results_data['apartment'] = "Cozy Clean Guest Room - Family Apt"
# #         results_data['roomType'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')
#         results_data['roomType'] = "Private room"
#         results_data['price'] = "79"
#         results_data['distance'] = "1 mile"
#
#         results_data['apartmentRatio1'] = "94%"
#         results_data['location1'] = "Morningside Heights"
#         results_data['apartment1'] = "Couldn't Be Closer To Columbia Uni"
# #         results_data['roomType1'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')
#         results_data['price1'] = "99"
#         results_data['roomType1'] = "Private room"
#         results_data['distance1'] = "1.3 miles"
#
#         results_data['firstName'] = request.POST['First Name']
#         results_data['lastName'] = request.POST['Last Name']
#         results_data['fullName'] = results_data['firstName'] + " " + results_data['lastName']
#         results_data['gender'] = request.POST['Gender']
#         results_data['nationality'] = request.POST['Nationality']
#         results_data['email'] = request.POST['Email']
#         # results_data['apartment'] = request.POST.getlist('Apartment')
#         results_data['habit'] = request.POST['Habit']


#         push_to_gbq(results_data)
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
#     print(query_data)
    return query_data

def pull_apt_from_gbp(distance, budget, roomType):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    length = len(roomType)
    if length == 3:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 3"
    elif length == 2:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where room_type = '" + roomType[0] +"' or room_type = '" + roomType[1] +"' order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 300"
    else:
        string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where room_type = '" + roomType[0] +"' order by (-reviews_per_month *0.2 + abs(price_raw * 30 / Capacity - " + budget + ") * 0.4 + abs(distance_line - " + distance +") * 0.4) limit 3"
    query = string1
    query_job = client.query(query)
    # TODO: store query into spark dataframe
    # list of dict
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data
