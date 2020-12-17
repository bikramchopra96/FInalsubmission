from django.shortcuts import render
from django.http import JsonResponse
import simplejson as json
from datetime import datetime
import requests
from rest_framework import viewsets
from .serializers import api_serializer
from .models import YearlyTable
from rest_framework.response import Response
from rest_framework.decorators import api_view


class apiViewSet(viewsets.ModelViewSet):
    queryset = YearlyTable.objects.all().order_by('index')
    serializer_class = api_serializer

@api_view(['GET'])
def get1api(request,id):
    a = YearlyTable.objects.filter(index=id)
    serializer = api_serializer(a,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getrangeapi(request,slug):
    begin = slug.split('to')[0]
    end = slug.split('to')[1]
    a = YearlyTable.objects.filter(index__range=[begin,end])
    serializer = api_serializer(a,many=True)
    return Response(serializer.data)


# Create your views here.

def showcharts(request):
    # ModelName.objects.values('Colum_name') To get list of column
    daytime = YearlyTable.objects.values('timestamp').order_by('timestamp')
    start = daytime[0]['timestamp']
    end = daytime[len(daytime) - 1]['timestamp']
    x = [time['timestamp'].strftime("%H:%M") for time in daytime]
    high = [numbers['high'] for numbers in YearlyTable.objects.values('high').order_by('timestamp')]
    low = [numbers['low'] for numbers in YearlyTable.objects.values('low').order_by('timestamp')]
    open = [numbers['open'] for numbers in YearlyTable.objects.values('open').order_by('timestamp')]
    close = [numbers['close'] for numbers in YearlyTable.objects.values('close').order_by('timestamp')]
    volume = [numbers['volume'] for numbers in YearlyTable.objects.values('volume').order_by('timestamp')]
    return render(request,'charts.html',{'x':json.dumps(x),'high':json.dumps(high),'low':json.dumps(low),
                                         'open':json.dumps(open),'close':json.dumps(close),'volume':json.dumps(volume),
                                         'start':start,'end':end})


def getdata(request):
    ''' To fetch data from api and storing it in our database'''
    TESTING = False

    if not TESTING:
        # ---------GET DATA FROM API---------
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"
        headers = {
            'x-rapidapi-key': "9571e09a0bmsh19d766352eb983ap1d5f95jsn2ab02e9bc8b8",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

        # ---XXX Date time format is unix based XXX---
        # Getting Data of the Day  on an interval of 5 min
        querystring = {"interval": "5m", "symbol": "AMRN", "range": "1d", "region": "US"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
    else:
        #----------GET DATA FROM JSON FILE
        pathofjson = 'Statistics/data-day.json'
        fp = open(pathofjson, 'r')
        data = json.load(fp)



    #---------- DROPING PREVIOUS DATA YEARLY ----------
    YearlyTable.objects.all().delete()
    # -----------CLEANING THE DATA AND EXTRACTING ROWS
    # Getting Time Data
    time = data["chart"]["result"][0]["timestamp"]
    col_names = list(data["chart"]["result"][0]["indicators"]["quote"][0].keys())
    dict_data = data["chart"]["result"][0]["indicators"]["quote"][0]
    # Creating Rows for database
    for i in range(0, len(time)):
        working_dict = {}
        working_dict['timestamp'] = time[i]
        for key in col_names:
            working_dict[key] = dict_data[key][i]
        print('Daywise',i,working_dict)
        row = YearlyTable()
        # row.timestamp = datetime.utcfromtimestamp(working_dict['timestamp']).strftime('%d-%m-%y %H:%M:%S')
        row.timestamp = datetime.utcfromtimestamp(working_dict['timestamp'])
        row.index = i + 1
        row.low = working_dict['low']
        row.close = working_dict['close']
        row.open = working_dict['open']
        row.volume = working_dict['volume']
        row.high = working_dict['high']
        row.save()

    return JsonResponse({'status': 'sucess'})
