# Importa el módulo de modelos de Django, que contiene las clases base
# para definir campos y tablas en la base de datos (CharField, EmailField, BooleanField, etc.).
from django.db import models

# Importa las clases necesarias para crear un modelo de usuario personalizado.
from django.contrib.auth.models import (
    AbstractBaseUser,  # Clase base para manejar autenticación y contraseñas.
    PermissionsMixin,  # Mezcla que agrega soporte de permisos, grupos e is_superuser.
    BaseUserManager    # Clase base para definir un manager personalizado de usuarios.
)
# ===========================
# MANAGER PERSONALIZADO
# ===========================
class CustomUserManager(BaseUserManager):
    """Manager para el modelo de usuario personalizado."""

    # Método para crear un usuario normal
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario normal.
        Parámetros:
        - email: identificador único para el login.
        - password: contraseña (se guardará encriptada).
        - extra_fields: campos adicionales opcionales.
        """
        # Validamos que se haya pasado un email
        if not email:
            raise ValueError('El email es un campo obligatorio')

        # Normalizamos el email (ejemplo: convierte MAYÚSCULAS en minúsculas)
        email = self.normalize_email(email)

        # Creamos una instancia del modelo de usuario con los datos recibidos
        user = self.model(email=email, **extra_fields)

        # Encriptamos la contraseña antes de guardarla
        user.set_password(password)

        # Guardamos el usuario en la base de datos
        user.save(using=self._db)
        return user

    # Método para crear un superusuario
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos de administrador.
        Parámetros:
        - email: identificador único para login.
        - password: contraseña encriptada.
        - extra_fields: cualquier campo adicional.
        """
        # Forzamos estos campos a True porque son obligatorios para un superusuario
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_active'] = True

        # Usamos create_user para reutilizar la lógica y guardar el usuario
        return self.create_user(email, password, **extra_fields)
# ===========================
# MODELO PERSONALIZADO DE USUARIO
# ===========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado:
    - Usa 'email' como identificador único para el inicio de sesión.
    - Reemplaza al modelo de usuario predeterminado de Django.
    """

    # Campo de email (único y obligatorio), será el "username"
    email = models.EmailField(unique=True, null=False, blank=False)

    # Nombre del usuario (puede quedar vacío si se permite)
    name = models.CharField(max_length=255, blank=True, null=True)

    # Campo booleano que indica si el usuario puede entrar al panel de administración
    is_staff = models.BooleanField(default=False)

    # Campo booleano que indica si el usuario está activo (sirve para suspender cuentas)
    is_active = models.BooleanField(default=True)

    # Asignamos el manager personalizado definido arriba
    objects = CustomUserManager()

    # Definimos qué campo se usará como "username" en el login (aquí el email)
    USERNAME_FIELD = 'email'

    # Campos adicionales que se pedirán al crear un superusuario con 'createsuperuser'
    REQUIRED_FIELDS = ['name']

    # Configuración de metadatos para el modelo
    class Meta:
        # Nombre singular que se verá en el admin
        verbose_name = "Usuario"
        # Nombre plural que se verá en el admin
        verbose_name_plural = "Usuarios"

    # Método que devuelve cómo se representará el usuario en texto (ejemplo: en el admin o en consola)
    def __str__(self):
        return self.email

