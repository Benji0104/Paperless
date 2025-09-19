# Importamos las herramientas necesarias de Django.
from django.db import models
# Usamos settings.AUTH_USER_MODEL en lugar de importar directamente CustomUser.
# Esto hace que el código sea más flexible: si en el futuro cambias tu modelo de usuario,
# no tendrás que modificar este archivo.
from django.conf import settings


# ==============================
# MODELO: Category
# ==============================
class Category(models.Model):
    """
    Modelo para clasificar los documentos.
    Ejemplo de categorías: 'Actas', 'Facturas', 'Informes'.
    """
    # Nombre de la categoría, único para evitar duplicados.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # Muestra el nombre de la categoría en el admin y consola.
        return self.name


# ==============================
# MODELO: Document
# ==============================
class Document(models.Model):
    """
    Modelo principal para la gestión de documentos.
    Almacena la información de los archivos y su metadata asociada.
    """
    # Título del documento, obligatorio.
    title = models.CharField(max_length=255)
    # Descripción opcional para dar más detalles sobre el documento.
    description = models.TextField(blank=True, null=True)
    # Campo de archivo. 'upload_to' indica la carpeta dentro de MEDIA_ROOT (o S3 si configuras almacenamiento en la nube).
    file = models.FileField(upload_to='documents/')
    # Fecha y hora en que se creó el documento.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Fecha y hora en que el documento fue actualizado por última vez.
    updated_at = models.DateTimeField(auto_now=True)
    # Relación con el usuario que subió el documento.
    # Si el usuario se elimina, también se eliminan sus documentos (CASCADE).
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Relación con la categoría. Si la categoría se elimina, el campo queda en NULL.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # Representación del documento usando su título.
        return self.title


# ==============================
# MODELO: History
# ==============================
class History(models.Model):
    """
    Registro de las acciones que los usuarios realizan sobre los documentos.
    Importante para auditoría y seguridad.
    """
    # Opciones predefinidas para las acciones posibles.
    ACTION_CHOICES = (
        ('upload', 'Subida de documento'),
        ('download', 'Descarga de documento'),
        ('delete', 'Eliminación de documento'),
        ('update', 'Actualización de documento'),
    )

    # Tipo de acción realizada, restringido a las opciones definidas.
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    # Fecha y hora en que ocurrió la acción.
    action_date = models.DateTimeField(auto_now_add=True)
    # Usuario que realizó la acción. Si el usuario se elimina, también se borran sus registros.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Documento sobre el cual se realizó la acción.
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        # Representación legible del historial: "Usuario - Acción - Documento - Fecha".
        return f"{self.user} - {self.get_action_type_display()} - {self.document.title} - {self.action_date.strftime('%Y-%m-%d %H:%M')}"
