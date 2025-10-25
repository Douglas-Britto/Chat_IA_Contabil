import streamlit as st
import os
import pandas as pd
import pdfplumber
from PIL import Image
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

# Função para ler arquivos da raiz do projeto
def ler_arquivos(pasta="."):
    caminho = os.path.join(os.path.dirname(__file__), pasta)
    textos = []
    if not os.path.exists(caminho):
        st.error("📁 Nenhum diretório encontrado.")
        return ""
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

# Função para exibir gráfico solicitado
def mostrar_grafico_solicitado(pergunta, pasta="."):
    nome_grafico = pergunta.strip().lower()
    caminho = os.path.join(os.path.dirname(__file__), pasta)
    for arquivo in os.listdir(caminho):
        if arquivo.lower().endswith(".png") and nome_grafico in arquivo.lower():
            caminho_arquivo = os.path.join(caminho, arquivo)
            try:
                st.image(caminho_arquivo, caption=arquivo, use_container_width=True)
                return
            except Exception as e:
                st.warning(f"Erro ao exibir '{arquivo}': {e}")
                return
    # Se nenhum gráfico for encontrado
    st.info("📁 Nenhum gráfico correspondente foi encontrado.")

# Execução principal
if pergunta:
    documentos = ler_arquivos()
    if documentos:
        resposta = responder_ia(pergunta, documentos)
        st.markdown(f"**Resposta da IA:**\n\n{resposta}")
        st.session_state.historico.append((pergunta, resposta))
        mostrar_grafico_solicitado(pergunta)
    else:
        st.warning("⚠️ Nenhum conteúdo foi encontrado no diretório do projeto.")

# Histórico de perguntas
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### 🗂 Histórico de perguntas")
    for i, (q, r) in enumerate(reversed(st.session_state.historico), 1):
        st.markdown(f"**{i}. {q}**")
        st.markdown(f"{r}")
