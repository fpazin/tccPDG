from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Projeto, Pergunta, Resposta

# Create your views here.


def page_test(request):
    print(request.user.username)
    return render(request, 'page_test.html')

def pdg_view(request):
    return render(request, 'PDG.html')

@login_required
def criar_projeto(request):
    if request.method == 'POST':
        nome_do_projeto = request.POST.get('nome_do_projeto')
        projeto = Projeto.objects.create(nome=nome_do_projeto, usuario=request.user)

        # Carregar as perguntas automaticamente
        perguntas = Pergunta.objects.all()
        for pergunta in perguntas:
            Resposta.objects.create(projeto=projeto, pergunta=pergunta)

        return redirect('nome_da_pagina_do_projeto', projeto_id=projeto.id)
    return render(request, 'projeto.html')

@login_required
def detalhes_do_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    respostas = projeto.respostas.all()  # Obter todas as respostas associadas ao projeto
    return render(request, 'detalhes_projeto.html', {'projeto': projeto, 'respostas': respostas})