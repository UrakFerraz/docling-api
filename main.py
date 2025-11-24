import logging
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

# Imports específicos do Docling baseados no seu exemplo
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import ImageRefMode

app = FastAPI()

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)

# Configurações globais de imagem
IMAGE_RESOLUTION_SCALE = 2.0

@app.post("/convert_pdf_to_markdown/")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    temp_file_path = Path(f"./temp_{file.filename}")

    try:
        # 1. Salva o arquivo temporariamente
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # 2. Configura as opções do Pipeline (Habilita imagens)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True
        pipeline_options.generate_table_images = True  # Opcional: gera imagens das tabelas também

        # 3. Inicializa o Converter com as opções formatadas
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        # 4. Realiza a conversão
        _log.info(f"Iniciando conversão para: {temp_file_path}")
        conv_res = doc_converter.convert(str(temp_file_path))

        # 5. Exporta para Markdown com imagens EMBUTIDAS (Base64)
        # Usamos ImageRefMode.EMBEDDED para que a imagem venha dentro do JSON de resposta
        # ao invés de salvar arquivos soltos no servidor.
        markdown_output = conv_res.document.export_to_markdown(image_mode=ImageRefMode.EMBEDDED)

        # Remove o arquivo temporário
        temp_file_path.unlink()

        return {"markdown": markdown_output}

    except Exception as e:
        _log.error(f"Erro na conversão: {str(e)}")
        if temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")