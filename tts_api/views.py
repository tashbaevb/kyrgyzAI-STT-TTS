import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def text_to_speech(request):
    data = request.data
    data['speaker_id'] = 1

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }
    response = requests.post('http://tts.ulut.kg/api/tts', json=data, headers=headers)

    if response.status_code != 200:
        return Response({'error': 'Ошибка при отправке данных на другой backend'}, status=response.status_code)

    if 'audio' in response.headers.get('Content-Type', ''):
        print(response.headers['Content-Type'])
        return HttpResponse(response, content_type=response.headers['Content-Type'])

    return Response(response.json(), status=status.HTTP_200_OK)
