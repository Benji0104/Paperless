from django.db import models

class GoogleToken(models.Model):
    email = models.EmailField(unique=True) 
    token = models.TextField()  
    name = models.CharField(max_length=255, blank=True)  
    picture = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): 
        return f"Token de {self.email}"
    
    class Meta:
        verbose_name = "Token de Google"
        verbose_name_plural = "Tokens de Google"
