# Conversor de PDF para Markdown (FastAPI + Docling)

Este projeto é uma API REST simples construída com **FastAPI** que utiliza a biblioteca **Docling** para converter documentos PDF em formato Markdown. A aplicação é totalmente containerizada usando Docker e Docker Compose para facilitar a execução e o deploy.

---

## 🚀 Funcionalidades

* **Conversão de PDF para Markdown:** Faz o upload de um arquivo PDF e recebe o conteúdo em formato Markdown.
* **API RESTful:** Expõe um endpoint `/convert_pdf_to_markdown/` para a conversão.
* **Containerizado:** Pronto para rodar com Docker Compose, garantindo um ambiente de execução isolado e consistente.

---

## 🛠️ Como Rodar o Projeto (com Docker Compose)

Siga os passos abaixo para executar a aplicação localmente usando Docker.

### Pré-requisitos

* **Docker** instalado
* **Docker Compose** instalado

### 1. Estrutura de Arquivos

Certifique-se de que seu projeto tenha a seguinte estrutura de arquivos (com o conteúdo fornecido na conversa anterior):

/seu-projeto/
├── docker-compose.yml
├── Dockerfile
├── main.py
└── requirements.txt

## 2. Construa e Suba os Containers

Com os 4 arquivos no diretório, abra um terminal e execute o seguinte comando:

```bash
docker-compose up -d --build
```

--build: Força o Docker a construir a imagem a partir do Dockerfile na primeira vez.

-d: Executa os containers em modo "detached" (em segundo plano).

3. Verifique a Execução
A API estará rodando e acessível em http://127.0.0.1:8080.

Você pode verificar os logs do container para garantir que tudo subiu corretamente:

```bash
docker-compose logs -f
```
---

📄 Como Usar a API
Para converter um arquivo PDF, você deve enviar uma requisição POST do tipo multipart/form-data para o endpoint /convert_pdf_to_markdown/.

O campo do formulário que contém o arquivo deve se chamar file.

Exemplo com cURL
Supondo que você tenha um arquivo chamado meu_documento.pdf no mesmo diretório onde você está executando o comando:

```bash
curl -X POST -F "file=@./meu_documento.pdf" [http://127.0.0.1:8080/convert_pdf_to_markdown/](http://127.0.0.1:8080/convert_pdf_to_markdown/)
```

```bash
# 1. Baixa o PDF da URL e salva como "sample.pdf"
curl -o sample.pdf "https://sample-files.com/downloads/documents/pdf/basic-text.pdf"

# 2. Envia o arquivo "sample.pdf" baixado para a sua API
curl -X POST -F "file=@./sample.pdf" http://127.0.0.1:8080/convert_pdf_to_markdown/
```


Resposta Esperada
A API retornará um objeto JSON contendo o texto extraído do PDF em formato Markdown:

```json
{
  "markdown": "## Título do Seu PDF\n\nEste é o conteúdo extraído...\n\n- Ponto 1\n- Ponto 2\n"
}
```

Em caso de erro (ex: enviar um arquivo que não é PDF), a API retornará um erro HTTP 400 ou 500 com os detalhes.

---

⏹️ Como Parar a Aplicação
Para parar e remover os containers, execute:

```bash
docker-compose down
```

