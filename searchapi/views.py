from django.shortcuts import render, redirect
from difflib import get_close_matches
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
import csv
import os



#fuction for postman  and url is 127.0.0.1:8000/api/v1/<str:keywd>
@api_view(['GET'])
def file_details(request, keywd):
    res = json.loads(json.dumps(class_search_api(keywd)))
    print(res)
    if not bool(res):                             #if no match is found return None
        content = {'ErrorNotFound': 'The is no matching word in dictionary'}
        return Response(content)
    else:
        return Response(res)            #return result in json format



@api_view(['GET'])
def keyword_search_api(request):
    q = request.GET.get("q", None)
    res_temp = {}
    context={}
    if q:
        res_temp = class_search_api(q)
        context = {'result': class_search_api(q)}
        #print(context)
        q = ""
    return render(request, 'searchapi/index.html', context)
    #return JsonResponse(json.loads(json.dumps(res_temp)))



#function to search given word
def class_search_api(keywd):
    #Open .TSV file path
    filename = 'word_search.tsv'
    abs_path = os.path.dirname(__file__)
    myfile = os.path.join(abs_path, filename)


    all = []
    res_list = []

#open .tsv file in reading mood
    with open(myfile) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:                              #itrating lines
            # all.append(row[0])
            str_row = str(row[0])

            if keywd in str_row:                        #If the keyword found in list then store in a new list
                x = [row[0], int(row[1])]
                res_list.append(x)


        res_list.sort(reverse=True, key=lambda x: x[1])         #sort the list based in frequency of the word
        exclusive_res = res_list[0:25]                          #selecct 25 top words including the exact match word


        for excl_res in exclusive_res:
            all.append(excl_res[0])
        res_temp = get_close_matches(keywd, all, n=25, cutoff=0)           #sorting all 25 words based on matching
        res_temp = dict(zip(range(1, 26),res_temp ))                       #convet the result into dict

    return res_temp

def redirect_index(request):
    response = redirect('api/v2/search')
    return response
