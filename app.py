import streamlit as st
import os
import pandas as pd
import pytesseract
from PIL import Image
import pdfplumber
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Auditor Fiscal IA", layout="wide")

# Conexão com OpenAI via segredo do Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Interface
st.title("🧠 Auditor Fiscal IA")
st.write("Este painel lê documentos e responde perguntas com inteligência artificial.")

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Quais impostos foram mencionados?")
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para ler arquivos da pasta
def ler_arquivos(pasta="Chat_IA_Contabil"):
    caminho = os.path.join(os.path.dirname(__file__), pasta)
    if not os.path.exists(caminho):
        st.error(f"Pasta '{pasta}' não encontrada.")
        return ""
    textos = []
    for arquivo in os.listdir(caminho):
        caminho_arquivo = os.path.join(caminho, arquivo)
        try:
            if arquivo.endswith(".txt"):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    textos.append(f.read())
            elif arquivo.endswith(".csv"):
                df = pd.read_csv(caminho_arquivo)
                textos.append(df.to_string())
            elif arquivo.endswith(".pdf"):
                with pdfplumber.open(caminho_arquivo) as pdf:
                    texto_pdf = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                    textos.append(texto_pdf)
            elif arquivo.endswith(".png"):
                imagem = Image.open(caminho_arquivo)
                texto_imagem = pytesseract.image_to_string(imagem)
                textos.append(texto_imagem)
        except Exception as e:
            st.warning(f"Erro ao ler '{arquivo}': {e}")
    return "\n".join(textos)

# Função para gerar resposta com IA
def responder_ia(pergunta, documentos):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um auditor fiscal inteligente. Use os documentos abaixo para responder com análise lógica e clara."},
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
        st.session_state.historico.append((pergunta, resposta))
    else:
        st.warning("⚠️ Nenhum conteúdo foi encontrado na pasta 'Chat_IA_Contabil'.")

# Histórico de perguntas
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### 🗂 Histórico de perguntas")
    for i, (q, r) in enumerate(reversed(st.session_state.historico), 1):
        st.markdown(f"**{i}. {q}**")
        st.markdown(f"{r}")
