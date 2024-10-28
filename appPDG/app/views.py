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
    
def salvar_projeto(request):
    if request.method == "POST":
        nome_projeto = request.POST.get("nome_projeto")
        projeto = Projeto.objects.create(nome=nome_projeto, usuario=request.user)

        # Carregar as perguntas automaticamente para o projeto
        perguntas = Pergunta.objects.all()
        for pergunta in perguntas:
            Resposta.objects.create(projeto=projeto, pergunta=pergunta)

        return JsonResponse({"projeto_id": projeto.id, "nome_projeto": projeto.nome})
    return JsonResponse({"error": "Método não permitido"}, status=400)


def detalhes_do_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    respostas = projeto.respostas.all()  # Obter todas as respostas associadas ao projeto
    return render(request, 'detalhes_projeto.html', {'projeto': projeto, 'respostas': respostas})


class PDGView(View):
    template_name = 'pdg.html' # Nome do template que será renderizado

    @method_decorator(login_required(login_url='login'), name='dispatch') # Decorator para verificar se o usuário está logado
    def get(self, request):
        return render(request, self.template_name) 
    
class projectListView(ListView):
    model = Projeto
    template_name = 'pdg.html'
    context_object_name = 'projetos'
    paginate_by = 10

    def get_queryset(self):
        return Projeto.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perguntas'] = Pergunta.objects.all()
        return context