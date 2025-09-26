
from rest_framework.decorators import api_view
from rest_framework.response import Response

import fitz  # PyMuPDF
from ebooklib import epub
from PyPDF2 import PdfReader

import os # para manejar archivos y rutas


#este import es para eliminar os achivos 
import shutil # esto es mas para los archivos y carpetas
import time


# Directorios para subir y guardar archivos
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
EXPIRATION_TIME = 60 * 60 * 24 #es para limpiar dichas carpetas por tema espacio
os.makedirs(UPLOAD_DIR, exist_ok=True) # esto verifica si ya existe la carpeta, si no lo crea
os.makedirs(OUTPUT_DIR, exist_ok=True)

@api_view(['POST'])
def PDF (request):

    text = ""
    
    pdf_file = request.FILES.get('file') # obtener el archivo PDF del request
   

    #Primero generar nombre del archivo y luego guardar 
    name_archivo = modify_filename(pdf_file.name, UPLOAD_DIR) #modificar el nombre del archivo si ya existe
    pdf_path = os.path.join(UPLOAD_DIR, name_archivo) # ruta para guardar el archivo
    
    with open(pdf_path, 'wb+') as destination: #guardar el archivo subido
        for chunk in pdf_file.chunks():
            destination.write(chunk)
    
    try:
        
        reader = PdfReader(pdf_path)
        metadatos = reader.metadata or {}
        number_of_pages = len(reader.pages)
        #portada = reader.pages[0]
        page = reader.pages[0]
        
        for page in reader.pages:
            text += page.extract_text()

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
    return Response ({
        "metadatos" : metadatos, 
        #"portada" : portada,  
        "nombre_archivo": name_archivo,
        "number_of_pages": number_of_pages,
        "text": text
    }) 
    

#funcion para modificar el nombre del archivo
#devuelve el nombre modificado

def modify_filename(original_filename, suffix):
    nombre, extension = os.path.splitext(original_filename)
    contador = 1
    nuevo_nombre = original_filename

    while os.path.exists(os.path.join(suffix, nuevo_nombre)):
        nuevo_nombre = f"{nombre} {contador}{extension}"
        contador += 1

    
    return  nuevo_nombre

""" 
@api_view(['GET'])
def pdf_to_epub(pdf_path, output_path):
    # Abrir PDF
    doc = fitz.open(pdf_path)
    reader = PdfReader(pdf_path) # obtener metadatos

    # Crear libro EPUB
    book = epub.EpubBook()

    # Metadatos (título si existe)
    title = reader.metadata.get("/Title", "Documento PDF convertido")
    book.set_title(title)
    book.add_author("Conversor Automático")

    # Extraer portada de la primera página
    pix = doc[0].get_pixmap()
    cover_path = output_path.replace(".epub", "_cover.jpg")
    pix.save(cover_path)

    # Convertir portada a JPG y añadir como portada
    book.set_cover("cover.jpg", open(cover_path, "rb").read())

    # Recorrer páginas para extraer contenido
    for i, page in enumerate(doc):
        text = page.get_text("text")  # solo texto (evita imágenes de fondo)
        chapter = epub.EpubHtml(title=f"Página {i+1}", file_name=f"chap_{i+1}.xhtml", lang="es")
        chapter.content = f"<h2>Página {i+1}</h2><p>{text}</p>"
        book.add_item(chapter)

    # Definir spine (estructura de lectura)
    book.spine = ["nav"] + [item for item in book.items if isinstance(item, epub.EpubHtml)]

    # Añadir navegación
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Guardar EPUB
    epub.write_epub(output_path, book, {})

    return output_path


@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    # Guardar PDF subido
    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    epub_path = os.path.join(OUTPUT_DIR, f"{file_id}.epub")

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Convertir PDF a EPUB
    output_file = pdf_to_epub(pdf_path, epub_path)

    # Devolver archivo EPUB
    return FileResponse(output_file, filename="output.epub", media_type="application/epub+zip")


# esto es un extra despues lo veo   
#eliminar los archivos despues de 24 horas, 
def clean_folder(folder):
    
    now = time.time(), #el tiempo actual
    for filename in os.listdir(folder):  #recorre los archivos en la carpeta
        file_path = os.path.join(folder, filename) #determina la ruta completa del archivo
        if os.path.isfile(file_path): #verifica si es un archivo
            file_age = now - os.path.getmtime(file_path) #calcula la antiguedad del archivo
            if file_age > EXPIRATION_TIME: # si es mayor a 24 horas entonces se elimina
                os.remove(file_path)
                #print(f"🗑️ Eliminado: {file_path}")



def run_cleaner():
    clean_folder(UPLOAD_DIR)
    clean_folder(OUTPUT_DIR)
"""