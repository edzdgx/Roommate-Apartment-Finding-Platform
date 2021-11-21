# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

import os
from google.cloud import bigquery

def search_post(request):
    '''
    please upload the data to DB there, and get the result
    '''
    original_data= {}
    print('searching')

    # TODO: fix getlist()
    print('*******************************8post*************8')
    original_data['roommatesRecommendation'] = "Roommates Recommendation"
    original_data['apartmentRecommendation'] = "Apartment Recommendation"
    original_data['firstName'] = request.POST.getlist('First Name')
    original_data['lastName'] = request.POST.getlist('Last Name')
    original_data['uni'] = request.POST.getlist('Uni')
    original_data['gender'] = request.POST.getlist('Gender')
    original_data['nationality'] = request.POST.getlist('Nationality')
    original_data['email'] = request.POST.getlist('Email')
    original_data['school'] = request.POST.getlist('School')
    original_data['major'] = request.POST.getlist('Major')
    original_data['smoking'] = request.POST.getlist('Smoking')
    original_data['alcohol'] = request.POST.getlist('Alcohol')
    original_data['certainApartment'] = request.POST.getlist('Certain Apartment')
    original_data['apartment'] = request.POST.getlist('Apartment')
    original_data['distance'] = request.POST.getlist('Distance')
    original_data['roomType'] = request.POST.getlist('Room Type')
    original_data['roommate'] = request.POST.getlist('Roommate')
    original_data['number'] = request.POST.getlist('Number')
    original_data['sameMajor'] = request.POST.getlist('Same Major')
    original_data['sameGender'] = request.POST.getlist('Same Gender')
    original_data['habit'] = request.POST.getlist('Habit')
    original_data['price'] = request.POST.getlist('Price')

    print(f'orig data:{original_data}')
    show_results(request)
    return render(request, "post.html", original_data)


def show_results(request):
    '''
    TODO: please put the results here and I can show them on the result page

    request: <QueryDict: {'csrfmiddlewaretoken': ['35iCA3t6AMFbFFU0KNQ4om1vNr609sUVMx64yaLX1SMaf9XFsaxps4NfjNtmOuL2'],
    'First Name': ['Jiaxiang'],
    'Last Name': ['Zhang'],
    'Uni': ['jz3275'],
    'Gender': ['Male'],
    'Nationality': ['China'],
    'Email': ['jz3275@columbia.edu'],
    'School': ['SEAS'],
    'Major': ['Electrical Engineering'],
    'Smoking': ['No'],
    'Alcohol': ['No'],
    'Certain Apartment': ['No'],
    'Apartment': [''],
    'Distance': ['near', 'pretty near'],
    'Room Type': ['Private room', 'Entire home/apt', 'Shared room'],
    'Price': ['Cheap', 'Economical'],
    'Roommate': ['Yes'],
    'Number': ['One', 'Two'],
    'Same Major': ['No'],
    'Same Gender': ['Yes'],
    'Habit': ['Early Bird']}>
    '''
    print(f'request: {request.POST}')
    results_data= {}
    if request.POST:
        results_data['roommatesRecommendation'] = "Roommates Recommendation"
        results_data['apartmentRecommendation'] = "Apartment Recommendation"
        results_data['roommateRatio'] = "95%"
        results_data['apartmentRatio'] = "98%"
        results_data['location'] = "Upper West Side"
        results_data['apartment'] = "Cozy Clean Guest Room - Family Apt"
#         results_data['roomType'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')
        results_data['roomType'] = "Private room"
        results_data['price'] = "79"
        results_data['distance'] = "1 mile"

        results_data['apartmentRatio1'] = "94%"
        results_data['location1'] = "Morningside Heights"
        results_data['apartment1'] = "Couldn't Be Closer To Columbia Uni"
#         results_data['roomType1'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')
        results_data['price1'] = "99"
        results_data['roomType1'] = "Private room"
        results_data['distance1'] = "1.3 miles"

        results_data['firstName'] = request.POST['First Name']
        results_data['lastName'] = request.POST['Last Name']
        results_data['fullName'] = results_data['firstName'] + " " + results_data['lastName']
        results_data['gender'] = request.POST['Gender']
        results_data['nationality'] = request.POST['Nationality']
        results_data['email'] = request.POST['Email']
        # results_data['apartment'] = request.POST.getlist('Apartment')
        results_data['habit'] = request.POST['Habit']


        push_to_gbq(results_data)
    return render(request, 'results.html', results_data)


def push_to_gbq(results_data):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"
    client = bigquery.Client()
    table_id = "big-data-6893-326823.roommate.users"


    rows_to_insert = [
        {
        'roommatesRecommendation': results_data['roommatesRecommendation'],
        'apartmentRecommendation': results_data['apartmentRecommendation'],
        'firstName': results_data['roommateRatio'],
        'lastName': results_data['apartmentRatio'],
        'uni': results_data['location'],
        'gender': results_data['contact'],
        'nationality': results_data['apartment'],
        'email': results_data['apartmentRatio1'],
        'school': results_data['location1'],
        'major': results_data['contact1'],
        'smoking': results_data['apartment1'],
        'alcohol': results_data['roomType1'],
        'certainApartment': results_data['firstName'],
        'apartment': results_data['lastName'],
        'distance': results_data['fullName'],
        'roomType': results_data['gender'],
        'roommate': results_data['nationality'],
        'number': results_data['email'],
        'sameMajor': results_data['apartment'],
        'sameGender': results_data['roomType'],
        'habit': results_data['habit']
        }
    ]
    errors = client.insert_rows_json(
        table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

def pull_from_gbp(option):
    client = bigquery.Client()
    if option == 'apartment':
        query = """
            SELECT *
            FROM `big-data-6893-326823.roommate.apartments`
        """
    elif option == 'user':
        query = """
            SELECT *
            FROM `big-data-6893-326823.roommate.users`
        """

    query_job = client.query(query)

    # TODO: store query into spark dataframe

    # list of dict
    query_data = [dict(row.items()) for row in query_job]
    print(query_data)
    return query_data

