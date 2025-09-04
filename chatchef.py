from openai import OpenAI
import pdfplumber
from dotenv import load_dotenv
import os
import easyocr

class ChatChef:
    def __init__(self, api_key, base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1", model="qwen-plus"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def ask_questions(self, context, questions):
        results = {}
        for question in questions:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um assistente que responde em português de forma direta e concisa. "
                                "Use apenas as informações do texto fornecido, sem explicações extras. "
                                "Se a resposta não existir, diga apenas: 'Não encontrado no texto.'"
                            )
                        },
                        {"role": "user", "content": f"Texto: {context}\n\nPergunta: {question}"}
                    ]
                )
                resposta = completion.choices[0].message.content.strip()
                results[question] = resposta
            except Exception as e:
                results[question] = f"Erro na extração: {str(e)}"
        return results
    
load_dotenv()
    
OPENIA_KEY=os.getenv("CHAVE_OPENIA")

chat = ChatChef(api_key=OPENIA_KEY)

def extrair_info_Divida_Ativa(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto_pdf = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    perguntas = [
        "Extraia apenas o número da certidão (somente os dígitos).",
        "Extraia apenas a data de emissão (formato dd/mm/aaaa).",
        "Extraia a validade da certidão."]

    respostas = chat.ask_questions(texto_pdf, perguntas)

    numero = respostas.get("Extraia apenas o número da certidão (somente os dígitos).", "Não encontrado")
    emissao = respostas.get("Extraia apenas a data de emissão (formato dd/mm/aaaa).", "Não encontrado")
    validade = respostas.get("Extraia a validade da certidão.", "Não encontrado")

    numero = numero.replace("O número da certidão é", "").replace("Número da Certidão é", "").strip(": .")
    emissao = emissao.replace("Data de emissão", "").strip(": .")
    validade = validade.replace("Validade", "").strip(": .")

    return {
        "numero": numero,
        "emissao": emissao,
        "validade": validade}

def ocr_transcrever_FGTS(file_path):
    try:
        reader = easyocr.Reader(['pt'])
        resultados = reader.readtext(file_path)

        if not resultados:
            return ""

        texto = "\n".join([res[1] for res in resultados])
        return texto
    except Exception as e:
        print(f"Erro no OCR com EasyOCR: {e}")
        return ""

def extrair_info_FGTS(texto):
    perguntas = [
        "Extraia apenas o número da certidão (somente os dígitos).",
        "Extraia a data em que foi obtida as informações (dd/mm/aaaa).",
        "Extraia apenas a validade (dd/mm/aaaa) a (dd/mm/aaaa)."]

    respostas = chat.ask_questions(texto, perguntas)

    numero = respostas.get("Extraia apenas o número da certidão (somente os dígitos).", "Não encontrado")
    emissao = respostas.get("Extraia a data em que foi obtida as informações (dd/mm/aaaa).", "Não encontrado")
    validade = respostas.get("Extraia apenas a validade (dd/mm/aaaa) a (dd/mm/aaaa).", "Não encontrado")

    numero = numero.replace("O número da certidão é", "").replace("Número da Certidão é", "").strip(": .")
    emissao = emissao.replace("Data de emissão", "").strip(": .")
    validade = validade.replace("Validade", "").strip(": .")

    return {"numero": numero, "emissao": emissao, "validade": validade}

def extrair_info_Trabalhista(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto_pdf = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    perguntas = [
        "Extraia apenas o número da certidão (somente os dígitos).",
        "Extraia apenas a data de emissão (formato dd/mm/aaaa).",
        "Extraia apenas a validade da certidão (formato dd/mm/aaaa)."]
    
    respostas = chat.ask_questions(texto_pdf, perguntas)

    numero = respostas.get("Extraia apenas o número da certidão (somente os dígitos).", "Não encontrado")
    emissao = respostas.get("Extraia apenas a data de emissão (formato dd/mm/aaaa).", "Não encontrado")
    validade = respostas.get("Extraia apenas a validade da certidão (formato dd/mm/aaaa).", "Não encontrado")

    numero = numero.replace("O número da certidão é", "").replace("Número da Certidão é", "").strip(": .")
    emissao = emissao.replace("Data de emissão", "").strip(": .")
    validade = validade.replace("Validade", "").strip(": .")

    return {
        "numero": numero,
        "emissao": emissao,
        "validade": validade}

def ocr_transcrever_Municipal(file_path):
    try:
        reader = easyocr.Reader(['pt'])
        resultados = reader.readtext(file_path)

        if not resultados:
            return ""

        texto = "\n".join([res[1] for res in resultados])
        return texto
    except Exception as e:
        print(f"Erro no OCR com EasyOCR: {e}")
        return ""

def extrair_info_Municipal(texto):
    perguntas = [
        "Extraia apenas a data que a Certidão foi emitida via internet (dd/mm/aaaa).",
        "Extraia apenas a validade (dd/mm/aaaa)."]

    respostas = chat.ask_questions(texto, perguntas)

    emissao = respostas.get("Extraia apenas a data que a Certidão foi emitida via internet (dd/mm/aaaa).", "Não encontrado")
    validade = respostas.get("Extraia apenas a validade (dd/mm/aaaa).", "Não encontrado")

    emissao = emissao.replace("Data de emissão", "").strip(": .")
    validade = validade.replace("Validade", "").strip(": .")

    return {"emissao": emissao, "validade": validade}

