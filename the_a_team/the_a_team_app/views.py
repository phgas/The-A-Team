from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.decorators import api_view, parser_classes
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import datetime
import csv
import json
import time
import os
from .decorators import restrict_ip_address, require_api_key
from modules import main
from .models import APIKey
from django.db.models import F
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from rest_framework import status
import pandas as pd
import requests

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY')


REQUESTS_AMOUNT = {
    'free': '1000',
    'basic': '5000',
    'premium': '10000'
}


logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([FileUploadParser])
@require_api_key
def get_prediction(request):
    start_time = time.time()
    api_key_value = request.headers.get('X-API-Key')
    try:
        api_key_instance = APIKey.objects.get(key=api_key_value)
    except APIKey.DoesNotExist:
        return Response({'success': False, 'error': 'Invalid API Key'}, status=status.HTTP_401_UNAUTHORIZED)
    if api_key_instance.requests_left <= 0:
        if round(datetime.now().timestamp()) < api_key_instance.expiry:
            return Response({'success': False, 'error': f'Your Balance is empty: Try again after {datetime.fromtimestamp(api_key_instance.expiry).strftime("%Y-%m-%d %H:%M:%S")}'}, status=429)
        else:
            api_key_instance.requests_left = REQUESTS_AMOUNT[api_key_instance.subscription_type]
            api_key_instance.save()

    try:
        file_obj = request.FILES['file']
        if not file_obj.name.endswith('.csv'):
            return Response({'error': 'Uploaded file must be a CSV'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        is_valid_data, unseen_data_raw = main.read_prediction_data(file_obj)
        if is_valid_data:
            unseen_data_prepared = main.prepare_data(unseen_data_raw)
            model = main.read_existing_model(os.path.join('modules', 'ai4i2020_pycaret_model'))
            prediction = main.get_prediction(model, unseen_data_prepared)
            APIKey.objects.filter(key=api_key_value).update(
                requests_left=F('requests_left') - 1)
            return Response({'success': True, 'processing_time_ms': round((time.time() - start_time) * 1000, 2), 'data': prediction}, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': 'Invalid *.csv-data'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([FileUploadParser])
@require_api_key
def generate_new_model(request):
    start_time = time.time()
    api_key_value = request.headers.get('X-API-Key')
    try:
        api_key_instance = APIKey.objects.get(key=api_key_value)
    except APIKey.DoesNotExist:
        return Response({'success': False, 'error': 'Invalid API Key'}, status=status.HTTP_401_UNAUTHORIZED)
    if api_key_instance.requests_left <= 9:
        if round(datetime.now().timestamp()) < api_key_instance.expiry:
            return Response({'success': False, 'error': f'Your Balance is empty: Try again after {datetime.fromtimestamp(api_key_instance.expiry).strftime("%Y-%m-%d %H:%M:%S")}'}, status=429)
        else:
            api_key_instance.requests_left = REQUESTS_AMOUNT[api_key_instance.subscription_type]
            api_key_instance.save()

    try:
        file_obj = request.FILES['file']
        if not file_obj.name.endswith('.csv'):
            return Response({'error': 'Uploaded file must be a CSV'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        is_valid_data, training_data_raw = main.read_training_data(file_obj)
        if is_valid_data:
            training_data_prepared = main.prepare_data(training_data_raw)
            main.create_new_model(training_data_prepared, os.path.join('modules', 'ai4i2020_pycaret_model'))
            APIKey.objects.filter(key=api_key_value).update(
                requests_left=F('requests_left') - 10)
            return Response({'success': True, 'processing_time_ms': round((time.time() - start_time) * 1000, 2), 'data': 'Successfully generated new model'}, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': 'Invalid *.csv-data'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@restrict_ip_address
def generate_key(request):
    start_time = time.time()
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != SECRET_KEY:
        return Response({'success': False, 'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        subscription_type = data.get('subscription_type')
        if not email:
            return Response({'success': False, 'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        elif not subscription_type:
            return Response({'success': False, 'error': 'Subscription type is required!'}, status=status.HTTP_400_BAD_REQUEST)
        elif subscription_type not in REQUESTS_AMOUNT:
            return Response({'success': False, 'error': 'Subscription type is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'success': False, 'error': 'Request must be JSON'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    if APIKey.objects.filter(email=email).exists():
        return Response({'success': False, 'error': 'An API key for this email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

    api_key_instance = APIKey(
        email=email, is_active=True, subscription_type=subscription_type, requests_left=REQUESTS_AMOUNT[subscription_type], expiry=round((datetime.now()+timedelta(days=30)).timestamp()))
    api_key_instance.save()
    return Response({'success': True, 'processing_time_ms': round((time.time() - start_time) * 1000, 2), 'api_key': str(api_key_instance.key)}, status=status.HTTP_200_OK)


def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']
        data = pd.read_csv(file_obj)
        api_key = request.POST.get('api_key', '')
        operation = request.POST.get('operation', '')

        if operation == 'prediction':
            endpoint = 'http://127.0.0.1:8000/data/prediction'
        elif operation == 'model':
            endpoint = 'http://127.0.0.1:8000/data/model'
        else:
            return HttpResponse('Invalid operation.')

        headers = {
            'X-API-KEY': api_key,
            'Content-Disposition': 'attachment; filename="file.csv"'  # Assuming the API expects CSV data
        }

        csv_data = data.to_csv(index=False)
        response = requests.post(endpoint, headers=headers, data=csv_data)
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get('data', [])
            print(response_data)
            context = {
                'success': response_data.get('success', ''),
                'processing_time_ms': response_data.get('processing_time_ms', ''),
                'data': data,
                'failure_colors': ['Toolwear_FAILURE', 'Heat-Dissipation FAILURE', 'Power_FAILURE', 'Overstrain_FAILURE', 'Random_FAILURE']
            }
            return render(request, 'home.html', context)
        else:
            return HttpResponse(f'Failed to submit data. Status code: {response.status_code}')

    return render(request, 'home.html')