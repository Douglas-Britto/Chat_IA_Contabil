import streamlit as st
import os
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Auditor Fiscal IA", layout="wide")

# Conexão com OpenAI via segredo do Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === Layout ===
st.title("🧠 Auditor Fiscal IA")
st.write("Faça perguntas sobre seus documentos e receba respostas com inteligência fiscal.")

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:", placeholder="Digite sua pergunta...")

# Função para ler arquivos da pasta local
def ler_arquivos(pasta="docs"):
    caminho = os.path.join(os.path.dirname(__file__), pasta)
    if not os.path.exists(caminho):
        st.error(f"Pasta '{pasta}' não encontrada.")
        return ""
    textos = []
    for arquivo in os.listdir(caminho):
        if arquivo.endswith(".txt"):
            with open(os.path.join(caminho, arquivo), "r", encoding="utf-8") as f:
                textos.append(f.read())
    return "\n".join(textos)

# Função para gerar resposta com IA
def responder_ia(pergunta, documentos):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um auditor fiscal inteligente. Use os documentos abaixo para responder com análise fiscal."},
            {"role": "user", "content": f"Documentos:\n{documentos}\n\nPergunta: {pergunta}"}
        ],
        temperature=0.7,
        max_tokens=700
    )
    return resposta.choices[0].message.content

# Execução principal
if pergunta:
    documentos = ler_arquivos()
    if documentos:
        resposta = responder_ia(pergunta, documentos)
        st.markdown(f"**Resposta da IA:**\n\n{resposta}")
    else:
        st.warning("⚠️ Nenhum conteúdo foi encontrado na pasta 'docs'.")
