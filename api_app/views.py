from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import os
import openai
import dotenv

dotenv.load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

@api_view(['POST'])
def get_answer(request):
    # Obtenemos el JSON enviado en el cuerpo de la solicitud
    data = request.data
    
    # Verificamos si el JSON contiene el rol y la pregunta
    if 'role' not in data or 'qestion' not in data:
        return Response({'error': 'El JSON debe contener el rol y la pregunta.'}, status=400)
    
    role = data['role']
    qestion = data['qestion']
    
    messages = [
        { 'role' : 'system', 'content' : role },
        { 'role' : 'user', 'content' : qestion }
    ]
    
    # Generamos la respuesta
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages, max_tokens=200)
    
    json_response = { 'response' : response.choices[0].message.content }
    
    # Devolvemos la respuesta
    return JsonResponse(json_response)