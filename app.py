import streamlit as st
import os
from openai import OpenAI

# === CONFIGURAÇÃO GERAL ===
st.set_page_config(page_title="IA AUDITOR FISCAL", layout="wide")

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === ESTILO VISUAL GLOBAL ===
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #001a33, #000);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3, h4, h5 {
    color: white;
}
.chat-box {
    background-color: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(255,255,255,0.1);
}
.input-area {
    margin-top: 20px;
}
input[type="text"] {
    background-color: #001f3f;
    color: white !important;
    border: 1px solid #0056b3;
    border-radius: 8px;
    padding: 10px;
    width: 100%;
}
button[kind="primary"] {
    background-color: #0056b3 !important;
    color: white !important;
}
.logo-text {
    font-size: 22px;
    font-weight: bold;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# === LAYOUT ===
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.image("Logo.png", width=180)
    st.markdown("<div class='logo-text'>AUDITOR FISCAL</div>", unsafe_allow_html=True)
    st.markdown("<h1>IA</h1>", unsafe_allow_html=True)
    st.markdown("### 💬 Chat Inteligente com IA")
    st.write("Faça perguntas sobre seus documentos e receba respostas com análise fiscal inteligente.")

with col2:
    st.markdown("## 💡 Resposta da IA:")

    pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual o impacto de faturar 500 mil sobre o CMV?")
    st.write("")

    if pergunta:
        # Localizar textos relevantes (RAG)
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

        # Localizar gráficos
        def localizar_grafico(pergunta, pasta="."):
            arquivos = os.listdir(pasta)
            palavras = pergunta.lower().split()
            for arquivo in arquivos:
                nome = arquivo.lower()
                if nome.endswith((".png", ".jpg", ".jpeg")):
                    if all(palavra in nome for palavra in palavras):
                        return os.path.join(pasta, arquivo)
            return None

        documentos = localizar_textos(pergunta)
        grafico = localizar_grafico(pergunta)

        with st.spinner("A IA está analisando seus documentos..."):
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um auditor fiscal inteligente. Analise e explique com base nos documentos."},
                    {"role": "user", "content": f"Documentos:\n{documentos}\n\nPergunta: {pergunta}"}
                ],
                temperature=0.6,
                max_tokens=700
            )

        st.markdown(f"""
        <div class="chat-box">
        <p>{resposta.choices[0].message.content}</p>
        </div>
        """, unsafe_allow_html=True)

        if grafico:
            st.image(grafico, caption="Gráfico relacionado à consulta", use_column_width=True)

---

### ✅ O que este script faz
1. Deixa o **layout igual à imagem** (lado esquerdo com IA + título, lado direito com pergunta e resposta).  
2. A **IA responde de verdade** (usa `gpt-4o-mini` para respostas rápidas e baratas).  
3. Se houver **gráficos ou textos na pasta**, ele os usa como contexto.  
4. Usa **a chave API já configurada no Streamlit** (`st.secrets["OPENAI_API_KEY"]`).  

---

Quer que eu te mostre o passo a passo de **como colocar esse script na pasta certa e rodar localmente com o layout igual à imagem?**
