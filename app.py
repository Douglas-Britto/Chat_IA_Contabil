import streamlit as st
from openai import OpenAI

# ===================== CONFIGURAÇÃO =====================
st.set_page_config(page_title="Auditor Fiscal IA", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===================== ESTILO VISUAL =====================
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #020c1b, #001f3f);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .titulo-principal {
            font-size: 48px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        }
        .subtitulo {
            font-size: 24px;
            color: #ff004c;
            font-weight: bold;
        }
        .descricao {
            font-size: 18px;
            margin-top: 20px;
            color: #ccc;
        }
        .caixa-chat {
            background-color: #0d2348;
            border-radius: 10px;
            padding: 30px;
            color: white;
            box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.1);
        }
        .input-box {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            border-radius: 8px;
            border: 1px solid #0056b3;
            background-color: #001f3f;
            color: white;
        }
        .botao {
            background-color: #0056b3;
            color: white;
            border: none;
            padding: 14px 24px;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
        }
        .botao:hover {
            background-color: #0077ff;
        }
        .resposta-ia {
            margin-top: 20px;
            background-color: #001a33;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== LAYOUT =====================
col1, col2 = st.columns(2)

with col1:
    st.image("Chat_IA_Docs_graficos/logo/logo.png", width=160)
    st.markdown("<div class='subtitulo'>AUDITOR FISCAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='titulo-principal'>IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitulo'>💬 Chat Inteligente com IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='descricao'>Faça perguntas sobre seus documentos e receba respostas inteligentes com análise fiscal automatizada.</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='color:white;'>💬 Resposta da IA:</h2>", unsafe_allow_html=True)
    st.markdown("<div class='caixa-chat'>", unsafe_allow_html=True)
    pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual o impacto do faturamento de 500 mil no CMV?")
    enviar = st.button("Consultar", key="consultar", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===================== FUNÇÃO DE RESPOSTA =====================
def responder_ia(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um auditor fiscal especialista em interpretar relatórios e documentos financeiros. Responda de forma clara, profissional e explicativa."},
            {"role": "user", "content": pergunta}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return resposta.choices[0].message.content

# ===================== LÓGICA =====================
if enviar and pergunta.strip():
    with st.spinner("Gerando resposta da IA..."):
        resposta = responder_ia(pergunta)
        st.markdown(f"<div class='resposta-ia'>{resposta}</div>", unsafe_allow_html=True)
