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
from django.urls import path
from app.views import page_test, salvar_projeto, basePDG, projectListView, perguntas_do_projeto, interagir_com_pergunta, pagina_pergunta, detalhes_do_projeto, pdgPerguntas_view
from accounts.views import register_view, logout_view, login_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Paginas Administrativas
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    # Paginas do PDG
    path('register/', register_view, name='register'),
    #path('PDG/', PDGView.as_view(), name='PDG'), # PDGView.as_view() foi substituido por projectListView.as_view()
    #paginas de teste
    path('1/', page_test, name='page_test'),
    path('PDG/', projectListView.as_view() , name='PDG'),
    path('basePDG/', basePDG, name='basePDG'),
    #path('projeto/<int:projeto_id>/', perguntas_do_projeto, name='perguntas_do_projeto'),
    #path('pergunta/<int:pergunta_id>/', perguntas_do_projeto, name='pagina_pergunta'),
    #
    # Lista as perguntas do projeto no frontend - Sidebar complementar do projeto
    #path('pergunta/<int:pergunta_id>/', page_test, name='pagina_pergunta'),  # Link para página de cada pergunta
    path('projeto/<int:projeto_id>/', detalhes_do_projeto, name='detalhes_do_projeto'),

    path('PDG_Pergunta/<int:projeto_id>/<int:pergunta_id>/', pdgPerguntas_view, name='pagina_pergunta'),
    path('detalhes_do_projeto/<int:projeto_id>/', detalhes_do_projeto, name='detalhes_do_projeto'),
    
    # Paginas de ação
    path('logout/', logout_view, name='logout'),
    path('salvar_projeto/', salvar_projeto, name='salvar_projeto'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
