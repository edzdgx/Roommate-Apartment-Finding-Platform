# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

# 接收POST请求数据
def search_post(request):
    '''
    please upload the data to DB there, and get the result
    '''
    original_data= {}
    if request.POST:
        '''
        print(request.POST)

        <QueryDict: {'csrfmiddlewaretoken': ['Mevza3aCOACHG7V47lPNHpy5NllqpigjnUXdhx1DkPaytFLfiAeXsevYSGmAqnhE'],
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
        'Room Type': ['Studio', '1b1b', '2b1b', '2b2b'],
        'Roommate': ['Yes'],
        'Number': ['One', 'Two'],
        'Same Major': ['No'],
        'Same Gender': ['Yes'],
        'Time': ['Early Bird']}>
        '''

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
        original_data['time'] = request.POST.getlist('Time')
    show_results(request)
    return render(request, "post.html", original_data)


def show_results(request):
    '''
    please put the result there and I can show them on the result page
    '''
    results_data= {}
    if request.POST:
        results_data['roommatesRecommendation'] = "Roommates Recommendation"
        results_data['apartmentRecommendation'] = "Apartment Recommendation"
        results_data['roommateRatio'] = "95%"
        results_data['apartmentRatio'] = "98%"
        results_data['location'] = "400 W 113th Street, New York, NY 10025"
        results_data['contact'] = "833-781-0089"
        results_data['apartment'] = "Enclave at the Cathedral"

        results_data['apartmentRatio1'] = "94%"
        results_data['location1'] = "752 West End Avenue, New York, NY, 10025"
        results_data['contact1'] = "646-518-7640"
        results_data['apartment1'] = "The Paris New York"
        results_data['roomType1'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')

        results_data['firstName'] = request.POST['First Name']
        results_data['lastName'] = request.POST['Last Name']
        results_data['fullName'] = results_data['firstName'] + " " + results_data['lastName']
        results_data['gender'] = request.POST['Gender']
        results_data['nationality'] = request.POST['Nationality']
        results_data['email'] = request.POST['Email']
#         results_data['apartment'] = request.POST.getlist('Apartment')
        results_data['roomType'] = str(request.POST.getlist('Room Type')).replace('[','').replace(']','').replace("'",'')
    return render(request, 'results.html', results_data)
