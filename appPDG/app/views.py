from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Projeto, Pergunta, Resposta
from django.views import View
from django.views.generic import ListView
from appPDG.main import geracao_texto
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors, utils
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io, os, json

# Create your views here.
# Região de Testes

def basePDG(request):
    return render(request, 'pdg_base.html')

# Região do PDG - Produção
def pdgPerguntas_view(request, projeto_id, pergunta_id):
    projetos = Projeto.objects.filter(usuario=request.user)  # Ou o filtro adequado para os projetos
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    max_pergunta_id = Pergunta.objects.filter(projeto_id=projeto_id).order_by('-id').first().id

     # Obter a resposta específica para a pergunta, se existir
    resposta = Resposta.objects.filter(pergunta_id=pergunta_id, projeto_id=projeto_id).first()

    return render(request, 'pdg_perguntas.html', {
        'projeto': Projeto.objects.get(id=projeto_id),
        'pergunta': pergunta,
        'projetos': projetos,
        'resposta': resposta,
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
                "Em caso de Problema, o que fazer? Construção da Matriz RACI"
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

# Região de Impressão do PDF do Projeto
def gerar_pdf(request, projeto_id):
    # Obtenha o projeto, perguntas e respostas
    projeto = Projeto.objects.get(id=projeto_id)
    perguntas = Pergunta.objects.filter(projeto_id=projeto_id)
    respostas = {resposta.pergunta_id: resposta.resposta_texto for resposta in Resposta.objects.filter(projeto_id=projeto_id)}

    # Crie um buffer de bytes para o PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    for i, pergunta in enumerate(perguntas, start=1):
        # Reiniciar altura ao início de cada página
        altura_disponivel = altura - 2 * cm  # Altura inicial padrão para cada página
        
        # Cabeçalho do documento
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, altura_disponivel, "PDG – Project Documentation Generator")
        altura_disponivel -= 0.7 * cm  # Reduzir espaço após o cabeçalho
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, altura_disponivel, f"Nome do Projeto: {projeto.nome}")
        altura_disponivel -= 1.3 * cm  # Espaço para o logo e próximo conteúdo

        # Logo
        logo_path = os.path.join(settings.BASE_DIR, 'appPDG', 'static', 'images', 'imagemPDG4.png')
        c.drawImage(logo_path, largura - 5 * cm, altura_disponivel, width=3 * cm, height=2 * cm)
        altura_disponivel -= 2.5 * cm  # Espaço reservado para o logo

        # Linha de separação
        c.setLineWidth(0.5)  # Espessura da linha
        c.line(2 * cm, altura_disponivel + 1.5 * cm, largura - 2 * cm, altura_disponivel + 1.5 * cm)
        altura_disponivel -= 0.5 * cm  # Ajustar espaço após a linha

        # Pergunta e Resposta
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, altura_disponivel + 1 * cm, f"Tópico: {i}  “{pergunta.texto}”")
        altura_disponivel -= 1 * cm  # Espaço após o tópico

        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, altura_disponivel + 1 * cm, "Conteúdo Salvo:")
        altura_disponivel -= 1 * cm  # Espaço para o conteúdo

        # Conteúdo Justificado
        resposta_texto = respostas.get(pergunta.id)
        if not resposta_texto:  # Se a resposta for None ou vazia
            resposta_texto = "<Nenhum conteúdo foi registrado para este tópico...>"
        styles = getSampleStyleSheet()
        style_justified = styles['BodyText']
        style_justified.alignment = 4  # 4 indica justificação total

        # Criar o parágrafo justificado
        p = Paragraph(resposta_texto, style_justified)
        text_width = largura - 4 * cm

        # Verificar se há espaço na página atual
        needed_height = p.wrap(text_width, altura_disponivel)[1]
        if altura_disponivel - needed_height < 2 * cm:  # Se não couber, crie nova página
            c.showPage()
            altura_disponivel = altura - 2 * cm  # Reiniciar altura na nova página
            c.setFont("Helvetica-Bold", 14)
            c.drawString(2 * cm, altura_disponivel, "PDG – Project Documentation Generator")
            altura_disponivel -= 0.7 * cm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, altura_disponivel, f"Nome do Projeto: {projeto.nome}")
            altura_disponivel -= 1.3 * cm  # Ajustar para novo conteúdo
            c.setFont("Helvetica-Bold", 14)
            c.drawString(2 * cm, altura_disponivel, f"Tópico: {i}  “{pergunta.texto}”")
            altura_disponivel -= 1 * cm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, altura_disponivel, "Conteúdo Salvo:")
            altura_disponivel -= 1 * cm

        # Posicione o texto na página
        p.drawOn(c, 2 * cm, altura_disponivel - needed_height + 1.5 * cm)
        altura_disponivel -= needed_height + 3 * cm  # Ajuste para próximo conteúdo

        # Tabela de Aprovações
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, 5 * cm, "Aprovações")
        c.setFillColor(colors.lightgrey)
        c.rect(2 * cm, 4.5 * cm, largura - 4 * cm, 1 * cm, fill=True, stroke=False)
        c.setFillColor(colors.black)
        c.drawString(2.2 * cm, 4.8 * cm, "Participante")
        c.drawString(8 * cm, 4.8 * cm, "Nome")
        c.drawString(12 * cm, 4.8 * cm, "Assinatura")
        c.drawString(16 * cm, 4.8 * cm, "Data")

        # Linhas para assinaturas
        c.drawString(2.2 * cm, 3.8 * cm, "Patrocinador do Projeto")
        c.drawString(2.2 * cm, 2.3 * cm, "Gerente do Projeto")
        
        # Finalizar a página e criar uma nova para a próxima pergunta
        c.showPage()

    # Salvar o PDF no buffer
    c.save()
    buffer.seek(0)

    # Retornar o PDF como resposta HTTP
    return FileResponse(buffer, as_attachment=True, filename=f'Documentacao_Projeto_'+ projeto.nome +'.pdf')

# Concluir Pergunta/Tarefa

@csrf_exempt
def concluir_tarefa(request, pergunta_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pergunta = Pergunta.objects.get(id=pergunta_id)
            pergunta.concluida = data.get("concluida", False)
            pergunta.save()
            return JsonResponse({"status": "success", "message": "Tarefa concluída com sucesso!"})
        except Pergunta.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Pergunta não encontrada."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)



