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
├── storage/
├── venv/
├── .gitignore
├── README.md
└── requirements.txt
```

## Como executar

### Pré-requisitos

- Python 3.8+
- Conta no Google Cloud Platform (GCP)
- BigQuery API habilitada no projeto GCP

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

## Autor

**Emilly Cavalcante**
- GitHub: [@httpsemilly](https://github.com/httpsemilly)
- LinkedIn: [Emilly Cavalcante](https://linkedin.com/in/emillycavalcante)
- Email: emilly.menezescs@gmail.com

> ✅ Status: Em desenvolvimento
> 📅 Última atualização: 06/03/2026
