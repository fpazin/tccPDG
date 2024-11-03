from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Projeto, Pergunta, Resposta
from django.views import View
from django.views.generic import ListView

# Create your views here.

def page_test(request):
    print(request.user.username)
    return render(request, 'pdg_test.html')

def basePDG(request):
    return render(request, 'pdg_base.html')

def pdgPerguntas_view(request, projeto_id, pergunta_id):
    projetos = Projeto.objects.filter(usuario=request.user)  # Ou o filtro adequado para os projetos
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    return render(request, 'pdg_perguntas.html', {
        'pergunta': pergunta,
        'projetos': projetos,
    })

# @method_decorator(login_required(login_url='login'), name='dispatch')
# def pdg_view(request):
#     return render(request, 'pdg.html')

# def salvar_projeto(request):
#     if request.method == 'POST':
#         projeto = Projeto()
#         projeto.nome = request.POST.get('nome')
#         projeto.descricao = request.POST.get('descricao')
#         projeto.save()
#         return redirect('PDG')
    
# def salvar_projeto(request):
#     if request.method == 'POST':
#         nome_projeto = request.POST.get('nome_projeto')
#         if nome_projeto:
#             # Cria o projeto
#             projeto = Projeto.objects.create(nome=nome_projeto, usuario=request.user)
            
#             # Associa todas as perguntas ao projeto criando respostas em branco
#             perguntas = Pergunta.objects.all()
#             for pergunta in perguntas:
#                 Resposta.objects.get_or_create(projeto=projeto, pergunta=pergunta, resposta_texto="")
            
#             # Retorna uma resposta para atualizar a lista de projetos no frontend
#             return JsonResponse({'projeto_id': projeto.id, 'nome_projeto': projeto.nome})

#         return JsonResponse({'error': 'Nome do projeto é obrigatório'}, status=400)

def salvar_projeto(request):
    if request.method == 'POST':
        nome_projeto = request.POST.get('nome_projeto')
        if nome_projeto:
            # Cria o projeto
            projeto = Projeto.objects.create(nome=nome_projeto, usuario=request.user)
            
            # Adiciona perguntas padrão ao novo projeto
            perguntas_texto = [
                "Nome do Projeto", "Justificativa?", "Objetivo?", "Riscos, Restrições e Limitações prévias ou não do projeto?",
                "Quais são os requisitos?", "Definição Geral do Escopo?", "Quais são os entregáveis?", 
                "Critérios de aceitação dos entregáveis", "O que está fora do Escopo?", "Cronograma do Projeto", 
                "Orçamento preliminar do projeto", "Formação da Equipe", "Métodos de Comunicação?", 
                "Priorização dos métodos de comunicação", "Aquisições", "Benefícios do Projeto", 
                "Critérios de Sucesso do Projeto", "Estratégias do Controle de Qualidade", 
                "Em caso de Problema, o que fazer? Construção da Matriz"
            ]
            
            for texto in perguntas_texto:
                Pergunta.objects.create(projeto=projeto, texto=texto)
            
            # Responder com ID do projeto e nome para frontend
            return JsonResponse({'projeto_id': projeto.id, 'nome_projeto': projeto.nome})

        return JsonResponse({'error': 'Nome do projeto é obrigatório'}, status=400)

class projectListView(ListView):
    model = Projeto
    template_name = 'pdg.html'
    context_object_name = 'projetos'
    paginate_by = 10

    def get_queryset(self):
        return Projeto.objects.filter(usuario=self.request.user).order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perguntas'] = Pergunta.objects.all()
        return context
    
def perguntas_do_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    perguntas = Pergunta.objects.values('texto')
    return JsonResponse({
        'projeto_nome': projeto.nome,
        'perguntas': list(perguntas)
    })

def interagir_com_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    return render(request, 'interacao_pergunta.html', {'pergunta': pergunta})

@login_required
def pagina_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    resposta, created = Resposta.objects.get_or_create(
        pergunta=pergunta,
        projeto=pergunta.projeto_set.filter(usuario=request.user).first()  # Associa ao projeto correto
    )

    if request.method == 'POST':
        resposta_texto = request.POST.get('resposta_texto')
        resposta.resposta_texto = resposta_texto
        resposta.save()
    
    projetos = Projeto.objects.filter(usuario=request.user)  # Para carregar na sidebar

    return render(request, 'pdg_perguntas.html', {
        'pergunta': pergunta,
        'resposta': resposta,
        'projetos': projetos,
    })

def criar_projeto(request):
    if request.method == 'POST':
        nome_do_projeto = request.POST.get('nome_projeto')
        projeto = Projeto.objects.create(nome=nome_do_projeto, usuario=request.user)

        # Carregar as perguntas padrão para o projeto
        perguntas_texto = [
            "Nome do Projeto", "Justificativa?", "Objetivo?", "Riscos, Restrições e Limitações prévias ou não do projeto?",
            "Quais são os requisitos?", "Definição Geral do Escopo?", "Quais são os entregáveis?", 
            "Critérios de aceitação dos entregáveis", "O que está fora do Escopo?", "Cronograma do Projeto", 
            "Orçamento preliminar do projeto", "Formação da Equipe", "Métodos de Comunicação?", 
            "Priorização dos métodos de comunicação", "Aquisições", "Benefícios do Projeto", 
            "Critérios de Sucesso do Projeto", "Estratégias do Controle de Qualidade", 
            "Em caso de Problema, o que fazer? Construção da Matriz"
        ]
        
        for texto in perguntas_texto:
            Pergunta.objects.create(projeto=projeto, texto=texto)

        return JsonResponse({"projeto_id": projeto.id, "nome_projeto": projeto.nome})

    
def detalhes_do_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    perguntas = projeto.perguntas.all()  # Todas as perguntas associadas ao projeto
    
    dados_perguntas = [
        {"id": pergunta.id, "texto": pergunta.texto, "link": f"/pergunta/{pergunta.id}/"}
        for pergunta in perguntas
    ]
    
    return JsonResponse({"projeto_nome": projeto.nome, "perguntas": dados_perguntas})
