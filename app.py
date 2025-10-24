import streamlit as st
import os
import openai

# Configuração da página
st.set_page_config(page_title="IA AUDITOR FISCAL", layout="wide")

# Chave da OpenAI via Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === ESTILO VISUAL ===
st.markdown("""
    <style>
        body {
            background-color: #0a1f3d;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .sidebar {
            background-color: #111;
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
    st.image("Logo.png", width=150)
    st.markdown("<div class='logo'>🧠 AUDITOR FISCAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Chat Inteligente com IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='description'>Faça perguntas sobre seus documentos e receba respostas com análise fiscal inteligente.</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("📞 fiscal@empresa.com.br\n© 2025 Empresa Inteligente")

# === ÁREA PRINCIPAL ===
st.markdown("<h2 style='color:white;'>🧠 Resposta da IA:</h2>", unsafe_allow_html=True)

# Campo de pergunta
pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual o impacto de faturar 500 mil sobre o CMV?")

# Função para localizar gráfico por palavras-chave
def localizar_grafico(pergunta, pasta="."):
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

# Função para localizar textos relevantes
def localizar_textos(pergunta, pasta="."):
    textos = []
    palavras = pergunta.lower().split()
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            nome = arquivo.lower()
            if any(palavra in nome for palavra in palavras):
                with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
                    textos.append(f.read())
    return "\n".join(textos)

# Função para chamar a IA com RAG fiscal
def responder_ia(pergunta, documentos):
    prompt = [
        {"role": "system", "content": "Você é um auditor fiscal inteligente. Use os documentos abaixo para responder com análise, estimativas e raciocínio fiscal. Considere margens médias, regras tributárias e histórico de mercado."},
        {"role": "user", "content": f"Documentos:\n{documentos}\n\nPergunta: {pergunta}"}
    ]
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7,
        max_tokens=700
    )
    return resposta.choices[0].message["content"]

# Quando o cliente envia uma pergunta
if pergunta:
    grafico = localizar_grafico(pergunta)
    documentos = localizar_textos(pergunta)

    if grafico:
        st.success("✅ Gráfico encontrado com base na sua pergunta:")
        st.image(grafico, caption="Gráfico relacionado à sua consulta")
    else:
        st.info("🔍 Nenhum gráfico correspondente foi encontrado.")

    if documentos:
        resposta = responder_ia(pergunta, documentos)
        st.markdown(f"<div style='color:white;'>{resposta}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Nenhum documento relevante foi encontrado para análise.")
