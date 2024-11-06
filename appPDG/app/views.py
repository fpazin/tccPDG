from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Projeto, Pergunta, Resposta
from django.views import View
from django.views.generic import ListView
from appPDG.main import geracao_texto

# Create your views here.
# Região de Testes
def page_test(request):
    print(request.user.username)
    return render(request, 'pdg_test.html')

def basePDG(request):
    return render(request, 'pdg_base.html')

# Região do PDG - Produção
def pdgPerguntas_view(request, projeto_id, pergunta_id):
    projetos = Projeto.objects.filter(usuario=request.user)  # Ou o filtro adequado para os projetos
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    max_pergunta_id = Pergunta.objects.filter(projeto_id=projeto_id).order_by('-id').first().id
    return render(request, 'pdg_perguntas.html', {
        'projeto': Projeto.objects.get(id=projeto_id),
        'pergunta': pergunta,
        'projetos': projetos,
        'max_pergunta_id': max_pergunta_id,
    })

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


def detalhes_do_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    perguntas = projeto.perguntas.all()  # Todas as perguntas associadas ao projeto
    
    dados_perguntas = [
        {"id": pergunta.id, "texto": pergunta.texto, "link": f"/pergunta/{pergunta.id}/"}
        for pergunta in perguntas
    ]
    
    return JsonResponse({"projeto_nome": projeto.nome, "perguntas": dados_perguntas})

def salvar_resposta(request):
    if request.method == 'POST':
        resposta_texto = request.POST.get('resposta_texto')
        pergunta_id = request.POST.get('pergunta_id')
        projeto_id = request.POST.get('projeto_id')
        
        pergunta = Pergunta.objects.get(id=pergunta_id)
        projeto = Projeto.objects.get(id=projeto_id)
        
        # Salvar a resposta no banco de dados, vinculando tanto ao projeto quanto à pergunta
        resposta, created = Resposta.objects.update_or_create(
            projeto=projeto,
            pergunta=pergunta,
            defaults={'resposta_texto': resposta_texto}
        )
        
        return JsonResponse({'status': 'success', 'message': 'Resposta salva com sucesso!'})

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

# Região de OpenAI
def enviar_mensagem(request):
    if request.method == 'POST':
        mensagem_usuario = request.POST.get('mensagem')
        mensagens = [{'role': 'user', 'content': mensagem_usuario}]
        
        # Obtém a resposta da função geracao_texto
        resposta = geracao_texto(mensagens)
        
        return JsonResponse({'resposta': resposta})
    
    return JsonResponse({'error': 'Método não permitido.'}, status=405)