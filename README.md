# Projeto: [PDG - Project Documentation Generator]

## Descrição

Este é um projeto desenvolvido com Django para o backend, HTML e CSS para o frontend, utilizando designs criados no Figma e a integração com a API da OpenAI para recursos de inteligência artificial. O objetivo deste projeto é [descreva o objetivo principal do seu projeto].

## Funcionalidades

- Integração com a API da OpenAI para [descrever a funcionalidade específica]
- Frontend responsivo utilizando HTML e CSS
- Design elaborado no Figma e implementado no frontend
- [Outras funcionalidades relevantes]

## Tecnologias Utilizadas

- **Django**: Framework web para desenvolvimento do backend.
- **HTML/CSS**: Linguagens para estrutura e design do frontend.
- **Figma**: Ferramenta de design utilizada para prototipar a interface.
- **OpenAI API**: API para integração de modelos de IA no projeto.
- [Outras tecnologias ou ferramentas se aplicável]

## Requisitos

Antes de executar o projeto, certifique-se de que você tem os seguintes requisitos instalados:

- Python 3.x
- Django
- Pipenv (ou Virtualenv)
- Conta na OpenAI e chave de API
- [Outros requisitos, se houver]

## Instalação

1. Clone o repositório para sua máquina local - Em algum momento ele ficará público:

    ```bash
    git clone  https://github.com/fpazin/tccPDG.git
    ```

2. Entre na pasta do projeto:

    ```bash
    cd nome-do-projeto
    ```

3. Crie um ambiente virtual e ative-o:

    ```bash
    python -m venv venv
    source venv/bin/activate  # no Windows: venv\Scripts\activate
    ```

4. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

5. Crie um arquivo `.env` para configurar suas variáveis de ambiente:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    ```

6. Rode as migrações do banco de dados:

    ```bash
    python manage.py migrate
    ```

7. Inicie o servidor de desenvolvimento:

    ```bash
    python manage.py runserver
    ```

Agora o projeto estará rodando em `http://localhost:8000/`.

## Como Usar

Descreva aqui como os usuários podem interagir com o seu projeto. Por exemplo, explique como a integração com a API da OpenAI funciona, como o usuário pode acessar as diferentes páginas ou funcionalidades do projeto, etc.

## Estrutura do Projeto

```bash
nome-do-projeto/
│
├── manage.py                # Arquivo de gerenciamento do Django
├── nome_da_app/             # Aplicação principal do Django
│   ├── migrations/          # Arquivos de migração do banco de dados
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/           # Templates HTML
│   └── views.py             # Lógica das views do Django
├── static/                  # Arquivos estáticos compartilhados
├── templates/               # Templates HTML compartilhados
├── .env                     # Variáveis de ambiente
└── requirements.txt         # Dependências do projeto
