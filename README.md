# LCGBR: Challenge - News Content Collect and Store

Projeto desenvolvido para o Coding Challenge - Data Engineering da Lima Consulting Group. A aplicação realiza crawl de notícias do site The Guardian, limpa e estrutura os dados, armazena no Google BigQuery e disponibiliza uma API para busca por palavras-chave.

## Objetivo

Construir um backend que:

- Coleta artigos do The Guardian
- Limpa o conteúdo removendo publicidade, menus e elementos irrelevantes
- Armazena os dados estruturados no BigQuery
- Disponibiliza uma API para busca e recuperação dos artigos

## Estrutura do projeto

```
./
├── api/
│   └── main.py
├── config/
│   ├── .env
│   └── config.yaml
├── crawler/
│   ├── scrapy.cfg
│   └── the_guardian/
│       ├── __init__.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       ├── settings.py
│       └── spiders/
│           └── theguardian.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Como executar

### Pré-requisitos

- Python 3.9+
- Conta no Google Cloud Platform (GCP)
- BigQuery API habilitada no projeto GCP
- Google Cloud SDK instalado ([instruções](https://docs.cloud.google.com/sdk/docs/install-sdk))

### Execução

**1. Clonar o repositório**

```
git clone https://github.com/httpsemilly/news-crawler-lcgbr-test
```

**2. Criar e ativar ambiente virtual**

```
# Cria o ambiente
python -m venv venv

# Ativa no Windows
venv\Scripts\activate

# Ativa no Linux/Mac
source venv/bin/activate
```

**3. Instalar dependências**

```
pip install -r requirements.txt
```

**4. Configurar credenciais do GCP**

```
gcloud auth application-default login
```

**5. Rodar o crawler**

```
cd crawler
scrapy crawl theguardian
```

**6. Rodar a API**

```
cd ..
uvicorn api.main:app --reload
```

**Obs.:** A API estará disponível em http://127.0.0.1:8000.

## API

### Buscar artigos por palavra-chave

```
GET /articles?keyword={keyword}
```

**Exemplo**

```
GET /articles?keyword=iran
```

**Resposta**

```
[
  {
    "headline": "Article headline",
    "article_url": "https://www.theguardian.com/...",
    "author": ["Author Name"],
    "published_date": "2026-03-07 17:04:00",
    "category": "world",
    "standfirst": "Article summary"
  }
]
```

**Obs.:** A busca é realizada nos campos `headline` e `article_text`. O endpoint pode ser acessado de três formas:

- **Navegador** — acesse `http://127.0.0.1:8000/articles?keyword={keyword}` diretamente na barra de endereços
- **Swagger UI** — acesse `http://127.0.0.1:8000/docs` para uma interface interativa gerada automaticamente pelo FastAPI
- **Insomnia ou Postman** — para testes mais avançados de API

## Decisões técnicas

### Scrapy em vez de Requests + BeautifulSoup

O Scrapy foi escolhido por oferecer suporte nativo a requisições assíncronas, gerenciamento de filas de URLs, pipelines de processamento e respeito ao robots.txt, funcionalidades que teriam que ser implementadas manualmente com Requests + BeautifulSoup.

### The Guardian

O site foi escolhido por ter HTML bem estruturado e semântico, com atributos como data-gu-name e data-component que tornam a extração de dados confiável e menos suscetível a quebras por mudanças de layout.

### Filtragem de conteúdo

Liveblogs (`/live/`), podcasts (`/audio/`), galerias de fotos (`/gallery/` e `/picture/`), páginas informativas (`/info/`) e páginas de newsletter (`/sign-up`) foram excluídas do crawl por terem estrutura HTML diferente de artigos comuns, o que comprometeria a qualidade da extração.

### Application Default Credentials (ADC)
Em vez de usar um arquivo JSON de Service Account, optou-se pelo ADC via gcloud auth application-default login. Essa é a abordagem recomendada pelo Google por ser mais segura, já que não há arquivos de credenciais que possam ser expostos de forma acidental.

### Deduplicação
Antes de inserir cada artigo no BigQuery, o pipeline verifica se a `article_url` já existe na tabela. Isso evita duplicatas em execuções consecutivas do crawler.

## Autor

**Emilly Cavalcante**
- GitHub: [@httpsemilly](https://github.com/httpsemilly)
- LinkedIn: [Emilly Cavalcante](https://linkedin.com/in/emillycavalcante)
- Email: emilly.menezescs@gmail.com

> ✅ Status: Finalizado!
