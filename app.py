import streamlit as st
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="IA AUDITOR FISCAL", layout="wide")

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ======== ESTILO CSS BASEADO NA IMAGEM =========
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #021026, #000000);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-top: 80px;
            padding: 0 60px;
        }
        .left {
            width: 45%;
            text-align: left;
        }
        .left img {
            width: 90px;
            margin-bottom: 15px;
        }
        .badge {
            background-color: #000;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .ia-title {
            font-size: 60px;
            font-weight: 700;
            margin-top: 5px;
            margin-bottom: 25px;
        }
        .chat-title {
            font-size: 30px;
            font-weight: 700;
            color: white;
        }
        .chat-subtitle {
            font-size: 18px;
            color: #d9d9d9;
            margin-top: 5px;
        }
        .right {
            width: 48%;
            text-align: left;
        }
        .resposta-titulo {
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .resposta-titulo::before {
            content: '💬';
            color: #ff004f;
            font-size: 24px;
            margin-right: 10px;
        }
        .input-container {
            background-color: rgba(255,255,255,0.05);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
        }
        input[type="text"] {
            width: 80%;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #333;
            background-color: #0a1a33;
            color: white;
            font-size: 16px;
        }
        button {
            background-color: #003cff;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 14px 26px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-left: 10px;
        }
        button:hover {
            background-color: #002fcc;
        }
        .resposta {
            margin-top: 25px;
            color: white;
            font-size: 18px;
            line-height: 1.5;
        }
    </style>
""", unsafe_allow_html=True)

# ======== LAYOUT VISUAL IGUAL AO MODELO =========
st.markdown("""
<div class="container">
    <div class="left">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712101.png" alt="IA Head">
        <div class="badge">AUDITOR FISCAL</div>
        <div class="ia-title">IA</div>
        <div class="chat-title">Chat Inteligente com IA</div>
        <div class="chat-subtitle">Faça perguntas sobre seus documentos e receba respostas</div>
    </div>
    <div class="right">
        <div class="resposta-titulo">Resposta da IA:</div>
        <div class="input-container">
""", unsafe_allow_html=True)

# ======== CAMPO DE PERGUNTA E BOTÃO =========
col1, col2 = st.columns([4, 1])
with col1:
    pergunta = st.text_input("", placeholder="Digite sua pergunta...")
with col2:
    consultar = st.button("Consultar")

# ======== FUNÇÃO DE RESPOSTA =========
def responder_ia(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um auditor fiscal inteligente e objetivo. Responda com base em conhecimento contábil e tributário brasileiro."},
            {"role": "user", "content": pergunta}
        ],
        temperature=0.5,
        max_tokens=700
    )
    return resposta.choices[0].message.content.strip()

# ======== EXIBIR RESULTADO =========
if consultar and pergunta:
    with st.spinner("Consultando IA..."):
        try:
            resposta = responder_ia(pergunta)
            st.markdown(f"<div class='resposta'>{resposta}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro: {e}")

# Fechando o container principal
st.markdown("</div></div></div>", unsafe_allow_html=True)
