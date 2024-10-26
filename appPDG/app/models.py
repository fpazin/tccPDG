from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    resposta_texto = models.TextField(blank=True, null=True)  # Campo onde o usuário salvará a resposta gerada pela IA

    def __str__(self):
        return f'Resposta para: {self.pergunta.texto[:50]}'
