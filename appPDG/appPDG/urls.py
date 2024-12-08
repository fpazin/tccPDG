"""
URL configuration for appPDG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import salvar_projeto, basePDG, projectListView, detalhes_do_projeto, pdgPerguntas_view, salvar_resposta, enviar_mensagem, gerar_pdf, concluir_tarefa
from accounts.views import register_view, logout_view, login_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Paginas Administrativas
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    
    path('/', include('allauth.urls')),
    #path('/', include('appPDG.urls')),
    # Paginas do PDG
    path('register/', register_view, name='register'),
    #path('PDG/', PDGView.as_view(), name='PDG'), # PDGView.as_view() foi substituido por projectListView.as_view()
    #paginas de teste
    path('PDG/', projectListView.as_view() , name='PDG'),
    path('basePDG/', basePDG, name='basePDG'),
    # Ação de Salvar a Resposta que o usuário deu a uma pergunta - TextArea
    path('salvar_resposta/', salvar_resposta, name='salvar_resposta'),
    path("concluir_tarefa/<int:pergunta_id>/", concluir_tarefa, name="concluir_tarefa"),
    # Ação enviar mensagem para OpenAI
    path('enviar_mensagem/', enviar_mensagem, name='enviar_mensagem'),
    # Lista as perguntas do projeto no frontend - Sidebar complementar do projeto
    path('projeto/<int:projeto_id>/', detalhes_do_projeto, name='detalhes_do_projeto'),
    path('PDG_Pergunta/<int:projeto_id>/<int:pergunta_id>/', pdgPerguntas_view, name='pagina_pergunta'),
    path('detalhes_do_projeto/<int:projeto_id>/', detalhes_do_projeto, name='detalhes_do_projeto'),
    path('projeto/<int:projeto_id>/imprimir_pdf', gerar_pdf, name='imprimir_pdf'),
    # Paginas de ação
    path('logout/', logout_view, name='logout'),
    path('salvar_projeto/', salvar_projeto, name='salvar_projeto'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
