import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


@api_view(['POST'])
def speech_to_text(request):
    headers = {
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }

    response = requests.post('https://asr.ulut.kg/api/receive_data', files={'audio': request.FILES['audio']},
                             headers=headers)

    if response.status_code != 200:
        return Response({'error': 'Ошибка при отправке данных на UlutSoft'}, status=response.status_code)

    if 'audio' in response.headers.get('Content-Type', ''):
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])

    return Response(response.json(), status=response.status_code)
