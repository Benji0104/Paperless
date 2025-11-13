from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ..models import GoogleToken
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlencode
from django.contrib.auth.models import User
import json
import traceback
from django.http import JsonResponse
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 


# IMPORTANTE: Desactivar validación de orden de scopes
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


SCOPES = [  'openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/drive.metadata.readonly'
            ]

REDIRECT_URI = "http://localhost:8000/auth/callback"  

api_view(['POST'])
def register_google(request):

    """
    Aqui le digo, los permisos que necesito, quien soy yo (credentials.json) y a donde redirigir al user despues de que google le de los permisos
    """
    flow = Flow.from_client_secrets_file(
        "env/credentials.json", SCOPES
    )
    """
    esto me trae la url de autorizacion y el estado , y le muestar al usuario la pantalla de permisos de google
    """

    flow.redirect_uri = REDIRECT_URI  

    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'    
    ) 

    #guarda sesion
    request.session['oauth_state'] = state
    
    
    return redirect(authorization_url) #redirige a la url de autorizacion de google

#google llama asta funcion despues de que el usuario le da permisos
api_view(['POST'])
def google_callback(request):
    # Validar que existe el state
    state = request.session.get('oauth_state')
   
    
    try:
        # Crear el flujo con el mismo state
        flow = Flow.from_client_secrets_file(
            "env/credentials.json",
            SCOPES
            
        )

        flow.redirect_uri = REDIRECT_URI
        
        authorization_response = request.build_absolute_uri()
        
        # Intercambiar el código por tokens
        flow.fetch_token(authorization_response=authorization_response)
        

        creds = flow.credentials
        

        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        

        user_email = user_info.get('email')
        user_name = user_info.get('name', '')
        user_picture = user_info.get('picture', '')
        token_json = creds.to_json()
        
        user, _ = User.objects.get_or_create(
            email=user_email,
            defaults={'username': user_email.split('@')[0]}
        )

        refresh = RefreshToken.for_user(user)

        # Guardar en base de datos
        token_obj, created = GoogleToken.objects.update_or_create(
            email=user_email,
            defaults={
                'token': token_json,
                'name': user_name,
                'picture': user_picture
            }
        )
        
        # Limpiar sesión
        if 'oauth_state' in request.session:
            del request.session['oauth_state']
        
        # Guardar email en sesión
        request.session['user_email'] = user_email
        request.session.modified = True
        
        # REDIRIGIR AL FRONTEND con los datos en la URL
        params = urlencode({
            'success': 'true',
            'token': refresh,
            'email': user_email,
            'name': user_name,
            'picture': user_picture
        })
        
        return redirect(f'http://localhost:5173/validar?{params}')
        
    except Exception as e:
        print(f"Error en google_callback: {str(e)}")
        print(traceback.format_exc())
        
        # Redirigir con error
        params = urlencode({'error': str(e)})
        return redirect(f'http://localhost:5173/validar?{params}')


@api_view(['POST'])
@authentication_classes([])
def google_login(request):
    user_email = request.session.get('user_email')
    
    # Si ya hay token guardado, no redirigir a Google
    if user_email:
        token_obj = GoogleToken.objects.filter(email=user_email).first()
        if token_obj:
            creds = Credentials.from_authorized_user_info(json.loads(token_obj.token))
            if creds.valid:
                # El token sigue siendo válido, no hace falta pedir permisos
                return redirect('/inicio')  # o tu página principal

    # Si no hay token, inicia el flujo de autorización
    flow = Flow.from_client_secrets_file(
        'env/credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'  # puedes quitar esto si no quieres forzar permisos cada vez
    )

    request.session['oauth_state'] = state
    return redirect(authorization_url)

@api_view(['GET'])
@authentication_classes([])
def perfil(request):
    user_email = request.session.get('user_email')

    if not user_email:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)


    token_obj = GoogleToken.objects.filter(email=user_email).first()
    if not token_obj:
        return JsonResponse({'error': 'Token no encontrado'}, status=404)

    creds_info = json.loads(token_obj.token)
    creds = Credentials.from_authorized_user_info(creds_info)

    try:
        service = build('drive', 'v3', credentials=creds)

        about = service.about().get(fields="*").execute()
        
        profile_info = {
            'user': {
                'name': about.get('user', {}).get('displayName', 'N/A'),
                'email': about.get('user', {}).get('emailAddress', 'N/A'),
                'photo': about.get('user', {}).get('photoLink', 'N/A')
            },
            'storage': {
                'total': about.get('storageQuota', {}).get('limit', 0),
                'used': about.get('storageQuota', {}).get('usage', 0),
                'used_in_drive': about.get('storageQuota', {}).get('usageInDrive', 0)
            },
            'files_count': about.get('folderColorPalette', {}),
            'max_upload_size': about.get('maxUploadSize', 'N/A')
            }

        

        return Response({"perfil": profile_info })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

