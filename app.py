import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt



st.set_page_config(page_title="Votação Nome da Bebê 👶", layout="centered")

ARQUIVO = "votos.csv"
VOTOS_MAXIMOS = 3

# -------------------------
# Controle de votos por sessão
# -------------------------
if "votos_restantes" not in st.session_state:
    st.session_state.votos_restantes = VOTOS_MAXIMOS

# -------------------------
# Inicialização dos dados
# -------------------------
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame({
        "nome": ["Olívia", "Beatriz", "Madalena"],
        "pontos": [0, 0, 0]
    })
    df.to_csv(ARQUIVO, index=False)
else:
    df = pd.read_csv(ARQUIVO)

if "ja_votou" not in st.session_state:
    st.session_state.ja_votou = False

st.title("👶 Votação para o nome da bebê")

#st.info(f"🗳️ Você ainda tem **{st.session_state.votos_restantes} voto(s)**")

# -------------------------
# Se acabaram os votos
# -------------------------
if st.session_state.votos_restantes <= 0:
    st.success("💖 Obrigado por participar! Você já utilizou todos os seus votos.")
    st.markdown("### 📊 Resultado parcial")
    st.table(df.sort_values("pontos", ascending=False))
    st.stop()

# -------------------------
# Adicionar novo nome
# -------------------------
with st.expander("➕ Sugerir um novo nome"):
    novo_nome = st.text_input("Digite o nome")
    if st.button("Adicionar nome"):
        if novo_nome.strip() != "" and novo_nome not in df["nome"].values:
            df.loc[len(df)] = [novo_nome, 0]
            df.to_csv(ARQUIVO, index=False)
            st.success("Nome adicionado!")
            st.rerun()
        else:
            st.warning("Nome inválido ou já existente.")

# -------------------------
# Votação
# -------------------------
nomes = df["nome"].tolist()

st.markdown("### 🥇🥈🥉 Ordene sua preferência")

primeiro = st.selectbox("🥇 Primeiro (3 pontos)", nomes)
segundo = st.selectbox(
    "🥈 Segundo (2 pontos)",
    [n for n in nomes if n != primeiro]
)
terceiro = st.selectbox(
    "🥉 Terceiro (1 ponto)",
    [n for n in nomes if n not in [primeiro, segundo]]
)

if st.button("✅ Confirmar voto"):
    df.loc[df["nome"] == primeiro, "pontos"] += 3
    df.loc[df["nome"] == segundo, "pontos"] += 2
    df.loc[df["nome"] == terceiro, "pontos"] += 1

    df.to_csv(ARQUIVO, index=False)

    st.session_state.votos_restantes -= 1
    st.session_state.ja_votou = True # marca que já votou

    st.success("Voto registrado com sucesso 💖")
    st.balloons()
    st.rerun()

# -------------------------
# Nuvem de nomes
# -------------------------

if st.session_state.ja_votou:
    st.markdown("---")
    st.markdown("### ☁️ Nuvem de nomes mais votados")

    frequencias = dict(zip(df["nome"], df["pontos"]))
    frequencias = {k: v for k, v in frequencias.items() if v > 0}

    if frequencias:
        wordcloud = WordCloud(
            font_path="verdana",
            width=800,
            height=400,
            background_color="#FFF0F5",
            colormap="Set2",
            prefer_horizontal=0.5
        ).generate_from_frequencies(frequencias)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Ainda não há votos suficientes para gerar a nuvem ☁️")