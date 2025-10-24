import streamlit as st
import os
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Auditor Fiscal IA", layout="wide")

# Conexão com OpenAI via segredo do Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === ESTILO VISUAL ===
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom, #0a1f3d, #000);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .sidebar .logo {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .sidebar .title {
            font-size: 22px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .sidebar .description {
            font-size: 16px;
            margin-bottom: 30px;
        }
        .input-box {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
            background-color: #001f3f;
            color: white;
        }
        .consultar-btn {
            background-color: #0056b3;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# === BARRA LATERAL ===
with st.sidebar:
    st.markdown("<div class='logo'>AUDITOR FISCAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>💬 Chat Inteligente com IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='description'>Faça perguntas sobre seus documentos e receba respostas com inteligência fiscal.</div>", unsafe_allow_html=True)
    st.markdown("📞 fiscal@empresa.com.br\n© 2025 Empresa Inteligente")

# === ÁREA PRINCIPAL ===
st.markdown("<h2 style='color:white;'>🧠 Resposta da IA:</h2>", unsafe_allow_html=True)

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:", placeholder="Digite sua pergunta...")

# Função para ler arquivos da pasta
def ler_arquivos(pasta="Chat_IA_Contabil"):
    textos = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
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

# Quando o usuário envia uma pergunta
if pergunta:
    documentos = ler_arquivos()
    if documentos:
        resposta = responder_ia(pergunta, documentos)
        st.markdown(f"<div style='color:white;'>{resposta}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Nenhum documento foi encontrado na pasta 'Chat_IA_Contabil'.")
