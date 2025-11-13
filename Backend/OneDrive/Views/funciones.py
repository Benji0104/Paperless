from googleapiclient.discovery import build
from rest_framework.response import Response
from google.oauth2.credentials import Credentials
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import json
from ..models import GoogleToken
from googleapiclient.http import MediaIoBaseDownload
from django.http import HttpResponse, StreamingHttpResponse
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import io
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
@authentication_classes([])
def get_user_credentials(request):

    user_email = request.session.get('user_email')
    print(user_email)
    if not user_email:
        return None, JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    # Buscar las credenciales en la base de datos
    token_obj = GoogleToken.objects.filter(email=user_email).first()
    if not token_obj:
        return None, JsonResponse({'error': 'Token no encontrado'}, status=404)
    
    try:
        creds_info = json.loads(token_obj.token)
        creds = Credentials.from_authorized_user_info(creds_info)
        return creds, None
    except Exception as e:
        return None, JsonResponse({'error': f'Error al procesar credenciales: {str(e)}'}, status=500)



@api_view(['GET'])
@authentication_classes([])
def listar_archivos(request):
    user_email = request.session.get('user_email')

    if not user_email:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    # Buscar las credenciales en la base de datos
    token_obj = GoogleToken.objects.filter(email=user_email).first()
    if not token_obj:
        return JsonResponse({'error': 'Token no encontrado'}, status=404)

    # Reconstruir las credenciales
    creds_info = json.loads(token_obj.token)
    creds = Credentials.from_authorized_user_info(creds_info)

    try:
        service = build('drive', 'v3', credentials=creds)

        query = "(mimeType='application/pdf' or mimeType='application/epub+zip') and trashed=false"

        results = (
            service.files()
            .list(
                q=query,
                fields="files(id, name, createdTime, modifiedTime, viewedByMeTime, thumbnailLink, mimeType, appProperties)",
                pageSize=20
            )
            .execute()
        )

        files = results.get("files", [])

        return Response({"archivos": files})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def leer_archivo_contenido(request, file_id):


    creds, error_response = get_user_credentials(request)
    if error_response:
        return error_response

    try:
        service = build('drive', 'v3', credentials=creds)


        file_metadata = service.files().get(
            fileId=file_id, 
            fields="mimeType, name"
        ).execute()
        
        file_mime_type = file_metadata.get('mimeType', 'application/octet-stream')
        file_name = file_metadata.get('name', 'file')
        
        # 2. Inicializar la descarga
        request_drive = service.files().get_media(fileId=file_id)
        
        # 3. Usar un buffer en memoria para guardar el archivo
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request_drive)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()


        # El buffer se llena con el contenido binario del archivo
        file_buffer.seek(0)
        file_content = file_buffer.read()

        
        response = HttpResponse(file_content, content_type=file_mime_type)
        
        print("Archivo descargado y leído con éxito.")
        return response

    except Exception as e:
        print(f"Error al descargar o leer el archivo: {str(e)}")
        return JsonResponse({'error': f"Error al descargar o leer el archivo: {str(e)}"}, status=500)