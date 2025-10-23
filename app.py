import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="IA AUDITOR FISCAL", layout="wide")

# === ESTILO VISUAL ===
st.markdown("""
    <style>
        body {
            background-color: #0a1f3d;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .container {
            display: flex;
            flex-direction: row;
            height: 100vh;
        }
        .sidebar {
            background-color: #111;
            width: 35%;
            padding: 40px 30px;
        }
        .logo {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .title {
            font-size: 22px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .description {
            font-size: 16px;
            margin-bottom: 30px;
        }
        .main {
            background: linear-gradient(to bottom, #0a1f3d, #000);
            width: 65%;
            padding: 60px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .input-box {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            margin-bottom: 20px;
        }
        .button {
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
    st.image("logo.png", width=150)  # Caminho simplificado
    st.markdown("<div class='logo'>🧠 AUDITOR FISCAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Chat Inteligente com IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='description'>Faça perguntas sobre seus documentos e receba respostas.</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("📞 fiscal@empresa.com.br\n© 2025 Empresa Inteligente")

# === ÁREA PRINCIPAL ===
st.markdown("<h2 style='color:white;'>🧠 Resposta da IA:</h2>", unsafe_allow_html=True)

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:")

# Função para localizar gráfico por palavras-chave
def localizar_grafico(pergunta, pasta="."):  # Busca na pasta atual
    try:
        arquivos = os.listdir(pasta)
        palavras = pergunta.lower().split()
        for arquivo in arquivos:
            nome = arquivo.lower()
            if nome.endswith((".png", ".jpg", ".jpeg")):
                if all(palavra in nome for palavra in palavras):
                    return os.path.join(pasta, arquivo)
    except FileNotFoundError:
        st.error("⚠️ Pasta de gráficos não encontrada.")
    return None

# Quando o cliente envia uma pergunta
if pergunta:
    grafico = localizar_grafico(pergunta)

    if grafico:
        st.success("✅ Gráfico encontrado com base na sua pergunta:")
        st.image(grafico, caption="Gráfico relacionado à sua consulta")
    else:
        st.warning("Nenhum gráfico correspondente foi encontrado. A IA responderá com base nos documentos.")
