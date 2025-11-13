from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from ebooklib import epub
import fitz  # PyMuPDF
import os
import shutil
import time

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@api_view(['POST'])
@authentication_classes([]) 
def PDF(request):
    files = request.FILES.getlist('files') 
    if not files:
        return Response({"error": "No se recibieron archivos"}, status=400)

    resultados = []  # lista de resultados

    for pdf_file in files:
        if pdf_file.content_type != 'application/pdf':
            resultados.append({"error": f"{pdf_file.name} no es un PDF válido"})
            continue


        name_archivo = modify_filename(pdf_file.name, UPLOAD_DIR)
        pdf_path = os.path.join(UPLOAD_DIR, name_archivo)

        with open(pdf_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        try:
            reader = fitz.open(pdf_path)
            metadatos = reader.metadata or {}
            extracted_text = ""

            
            cover_page = reader[0]
            pix_portada = cover_page.get_pixmap()
            portada = pix_portada.tobytes("jpg")

            # Crear el epub
            book = epub.EpubBook()
            book.set_identifier(metadatos.get('id', 'unknown_id'))
            book.set_title(metadatos.get('title', 'Sin Título'))
            book.set_language('es')
            book.add_author(metadatos.get('author', 'Autor Desconocido'))
            book.set_cover("cover.jpg", portada)

            chapters = []
            for i, page in enumerate(reader):
                soup = BeautifulSoup(page.get_text("html"), "html.parser")
                for img in soup.find_all("img"):
                    img.decompose()

                cleaned_html = str(soup).strip()
                if not soup.get_text(strip=True):
                    continue

                chapter = epub.EpubHtml(
                    title=f'Página {i+1}',
                    file_name=f'page_{i+1}.xhtml',
                    lang='es'
                )
                chapter.content = cleaned_html
                book.add_item(chapter)
                chapters.append(chapter)

            book.spine = ["nav"] + chapters
            book.toc = tuple(chapters)

            epub_path = os.path.join(OUTPUT_DIR, name_archivo.replace('.pdf', '.epub'))
            epub.write_epub(epub_path, book, {})

            epub_filename = os.path.basename(epub_path)  # evita "outputs/outputs"
            epub_url = f"http://localhost:8000/outputs/{epub_filename}".replace("\\", "/")


            resultados.append({
                "archivo_pdf": name_archivo,
                "metadatos": metadatos,
                "text_preview": extracted_text[:500],
                "epub_path": epub_url
            })

        except Exception as e:
            resultados.append({
                "archivo_pdf": pdf_file.name,
                "error": str(e)
            })

    return Response({"resultados": resultados})


def modify_filename(original_filename, suffix):
    nombre, extension = os.path.splitext(original_filename)
    contador = 1
    nuevo_nombre = original_filename

    while os.path.exists(os.path.join(suffix, nuevo_nombre)):
        nuevo_nombre = f"{nombre} {contador}{extension}"
        contador += 1

    return nuevo_nombre

