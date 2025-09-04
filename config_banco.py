from telegram_solution import TelegramSend
from dotenv import load_dotenv
from datetime import datetime
import pyodbc
import os

load_dotenv()

erro = TelegramSend("Banco")

def registrar_log(certidao, sucesso):
    try:
        conexao = pyodbc.connect(
            rf"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_HOST')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASS')};")
        cursor = conexao.cursor()

        data_hoje = datetime.now().date()

        cursor.execute("""
            SELECT tentativas, resultado 
            FROM dbo.cnd_testes
            WHERE nome_certidao = ? 
              AND CAST(data_execucao AS DATE) = ?""", 
            (certidao, data_hoje))
        
        resultado_bd = cursor.fetchone()

        if resultado_bd:
            tentativas_atual, resultado_atual = resultado_bd
            nova_tentativa = tentativas_atual + 1
            # Se sucesso=1, atualiza para 1; senão mantém o que já estava
            novo_resultado = 1 if sucesso == 1 else resultado_atual

            cursor.execute("""
                UPDATE dbo.cnd_testes
                SET tentativas = ?, resultado = ?
                WHERE nome_certidao = ? 
                  AND CAST(data_execucao AS DATE) = ?""",
                (nova_tentativa, novo_resultado, certidao, data_hoje))
        else:
            data_execucao = datetime.now()
            cursor.execute("""
                INSERT INTO dbo.cnd_testes (nome_certidao, data_execucao, tentativas, resultado)
                VALUES (?, ?, ?, ?)""", 
                (certidao, data_execucao, 1, sucesso))

        conexao.commit()
        conexao.close()

    except Exception as e:
        itoken = os.getenv("ITOKEN_TELEGRAM")
        chat_id = os.getenv("CHAT_ID")
        print(f"[ERRO BANCO] {e}")
        print(f"[DEBUG] ITOKEN={itoken}, CHAT_ID={chat_id}")
        erro.telegram_bot(f"Erro ao registrar no banco: {e}", itoken, (chat_id) if chat_id else 0)


def pode_tentar(certidao, data_hoje):
    try:
        conexao = pyodbc.connect(
            rf"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_HOST')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASS')};")
        cursor = conexao.cursor()

        query = """
            SELECT COUNT(*) FROM dbo.cnd_testes
            WHERE nome_certidao = ?
            AND CAST(data_execucao AS DATE) = ?
            AND (
                resultado = 1 OR
                (tentativas >= 3 AND resultado = 0))"""
        cursor.execute(query, (certidao, data_hoje))
        resultado = cursor.fetchone()[0]
        conexao.close()
        return resultado < 1 

    except Exception as e:
        erro.telegram_bot(f"Erro ao consultar tentativas no banco: {e}", os.getenv("ITOKEN"), os.getenv("CHAT_ID"))
        print(f"Erro ao consultar tentativas no banco: {e}")
        return False

def exibir_status_certidao(certidao):
    try:
        conexao = pyodbc.connect(
            rf"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_HOST')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASS')};")
        cursor = conexao.cursor()

        data_hoje = datetime.now().date()
        cursor.execute("""
            SELECT tentativas, resultado FROM dbo.cnd_testes
            WHERE nome_certidao = ? AND CAST(data_execucao AS DATE) = ?""",
            (certidao, data_hoje))
        
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            tentativas, resultado = resultado
            status = "Sucesso" if resultado == 1 else "Falhou"
            msg = f"Certidão: {certidao}\n\nTentativas: {tentativas}\n\nResultado: {status}"
        else:
            msg = f"Nenhum registro encontrado para '{certidao}' hoje."

        print(msg)

    except Exception as e:
        erro_msg = f"Erro ao buscar status: {e}"
        print(erro_msg)
        erro.telegram_bot(erro_msg, os.getenv("ITOKEN_TELEGRAM"), os.getenv("CHAT_ID"))
