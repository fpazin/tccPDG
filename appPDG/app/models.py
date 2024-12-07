from django.contrib.auth.models import User
from django.db import models

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="perguntas")  # Nova relação com Projeto
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    resposta_texto = models.TextField(blank=True, null=True)  # Campo para a resposta do usuário

    def __str__(self):
        return f'Resposta para: {self.pergunta.texto[:50]}'

from app.models import Pergunta
def criar_perguntas_padrao():
    perguntas_texto = [
        "Nome do Projeto", "Justificativa?", "Objetivo?", "Riscos, Restrições e Limitações prévias ou não do projeto?",
        "Quais são os requisitos?", "Definição Geral do Escopo?", "Quais são os entregáveis?", 
        "Critérios de aceitação dos entregáveis", "O que está fora do Escopo?", "Cronograma do Projeto", 
        "Orçamento preliminar do projeto", "Formação da Equipe", "Métodos de Comunicação?", 
        "Priorização dos métodos de comunicação", "Aquisições", "Benefícios do Projeto", 
        "Critérios de Sucesso do Projeto", "Estratégias do Controle de Qualidade", 
        "Em caso de Problema, o que fazer? Construção da Matriz RACI"
    ]
    for texto in perguntas_texto:
        Pergunta.objects.get_or_create(texto=texto)