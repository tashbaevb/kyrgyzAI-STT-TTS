import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from pydub import AudioSegment


def convert_to_mp3(audio_file):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Create the output file path with .mp3 extension
    output_file = os.path.splitext(audio_file.name)[0] + ".mp3"

    # Export the audio to MP3 format
    audio.export(output_file, format="mp3")

    return output_file


@api_view(['POST'])
def speech_to_text(request):
    # Check if 'audio' file is present in the request
    if 'audio' not in request.FILES:
        return Response({'error': 'No audio file provided in the request.'}, status=400)

    # Convert the uploaded audio file to MP3
    mp3_file = convert_to_mp3(request.FILES['audio'])

    headers = {
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }

    # Send the MP3 file to the UlutSoft API
    with open(mp3_file, 'rb') as f:
        response = requests.post('https://asr.ulut.kg/api/receive_data', files={'audio': f}, headers=headers)

    # Remove the temporary MP3 file
    os.remove(mp3_file)

    # Handle API response
    if response.status_code != 200:
        return Response({'error': 'Error sending data to UlutSoft API'}, status=response.status_code)

    if 'audio' in response.headers.get('Content-Type', ''):
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])

    return Response(response.json(), status=response.status_code)
