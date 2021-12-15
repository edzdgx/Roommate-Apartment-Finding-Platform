# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

import os
from google.cloud import bigquery
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import hamming

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

    school = request.POST['School']
    gender = request.POST['Gender']
    number = str(request.POST.getlist('Number')).replace("[", "").replace("]", "").replace("'", "")

    if request.POST['Same School'] == 'Yes' and request.POST['Same Gender'] == 'Yes':
        query_user_data = roommate_sameSchool_sameGender(school, gender, number)

    elif request.POST['Same School'] == 'No' and request.POST['Same Gender'] == 'Yes':
        query_user_data = roommate_sameGender(gender, number)

    elif request.POST['Same School'] == 'Yes' and request.POST['Same Gender'] == 'No':
        query_user_data = roommate_sameSchool(school, number)
    else:
        query_user_data = roommate_flexible(number)

    res = find_your_roommate(query_user_data)
    return res

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
        query_user_data = process_user_data(request)
        length_user = len(query_user_data)
        number = str(request.POST.getlist('Number')).replace("[", "").replace("]", "").replace("'", "")
        max = int(number[len(number) - 1]) * 2

        query_apt_data = process_apt_data(request)
        length_apt = len(query_apt_data)


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
            for i in range(max):
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
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def pull_apt_from_gbp_by_certain(apartment):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.apartment` where name = '"+ apartment  +"'"
    query = string1
    query_job = client.query(query)
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
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def roommate_sameSchool_sameGender(school, gender, number):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
#     max = int(number[len(number) - 1]) * 2
#     string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where School = '" + school + "' and Gender = " + gender + " and Number_of_Roommates = '" + number + "' limit " + str(max)
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where School = '" + school + "' and Gender = " + gender + " and Number_of_Roommates = '" + number + "'"
    query = string1
    print(query)
    query_job = client.query(query)
    query_data = [dict(row.items()) for row in query_job]
#     print(query_data)
    return query_data

def roommate_sameSchool(school, number):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where School = '" + school + "' and Number_of_Roommates = '" + number + "'"
    query = string1
    query_job = client.query(query)
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def roommate_sameGender(gender, number):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where Gender = " + gender + " and Number_of_Roommates = '" + number + "'"
    query = string1
    query_job = client.query(query)
    query_data = [dict(row.items()) for row in query_job]
    return query_data

def roommate_flexible(number):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    string1 = "SELECT * FROM `big-data-6893-326823.roommate.roommates` where Number_of_Roommates = '" + number + "'"
    query = string1
    query_job = client.query(query)
    query_data = [dict(row.items()) for row in query_job]
    return query_data


####################################find_your_roommate_algorithm#######################################
# helper function to normalize features
def normalize(df, features):
    result = df.copy()
    for feature_name in features:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = ((df[feature_name] - min_value) / (max_value - min_value))*2-1
    return result


def find_your_roommate(query_user_data, algo='euclidean'):
    # print(f'find_your_roommate query_user_data: {query_user_data}')
    # print(f'type query_user_data: {type(query_user_data)}')
    df = pd.DataFrame(query_user_data)
    meta_data = df.drop(
        labels=['int64_field_0', 'Full_Name', 'Email_address', 'Last_Name', 'First_Name', 'Uni', 'Nationality',
                'School', 'Major', 'Roommate', 'Number_of_Roommates'], axis=1)
    print(meta_data.columns)
    # Index(['Gender', 'Smoking', 'Alchohol', 'Habit', 'Roommate', 'Age',
    #        'Accept_Animals', 'Preferred_Budgets', 'Preferred_Distance'],
    #       dtype='object')
    features = ['Preferred_Budgets', 'Preferred_Distance', 'Age']
    normalized_data = normalize(meta_data, features)
    test_person = normalized_data.iloc[0]
    if algo == 'euclidean':
        x = test_person
        dist_list = []
        for i in range(normalized_data.shape[0]):
            y = normalized_data.iloc[i]
            dist = np.sqrt(np.sum([(a - b) * (a - b) for a, b in zip(x, y)]))
            dist_list.append(dist)
        idx = np.argsort(dist_list)[:10]
        print(f'idx:{idx}')
        res = df.iloc[idx]

        return res.to_dict('records')

    elif algo == 'kmeans':
        from sklearn.cluster import KMeans
        n_clusters = int(meta_data.shape[0] / 10)
        km = KMeans(n_clusters=n_clusters)
        mat = normalized_data.values
        km.fit(mat)
        # Get cluster assignment labels
        labels = km.labels_
        # Format results as a DataFrame
        res = pd.DataFrame([normalized_data.index, labels]).T
        return res.to_dict('records')

    return query_user_data