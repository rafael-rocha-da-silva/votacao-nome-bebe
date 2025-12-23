import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -------------------------
# Configurações da página
# -------------------------
st.set_page_config(page_title="Votação Nome da Bebê 👶", layout="centered")

ARQUIVO = "votos.csv"

# -------------------------
# Inicialização dos dados
# -------------------------
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame({
        "nome": ["Alice", "Helena", "Laura"],
        "pontos": [0, 0, 0]
    })
    df.to_csv(ARQUIVO, index=False)
else:
    df = pd.read_csv(ARQUIVO)

st.title("👶 Votação para o nome da bebê")

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
            #st.experimental_rerun()
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
    st.success("Voto registrado com sucesso 💖")
    st.balloons()
    #st.rerun()

# -------------------------
# Botão para mostrar a nuvem de palavras
# -------------------------
if st.button("☁️ Ver nuvem de nomes votados"):
    st.markdown("---")
    st.markdown("### ☁️ Nuvem de nomes mais votados")

    frequencias = dict(zip(df["nome"], df["pontos"]))
    frequencias = {k: v for k, v in frequencias.items() if v > 0}

    if frequencias:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="Pastel1",
            prefer_horizontal=0.9,
            font_path=None  # evita erro de fonte no Streamlit Cloud
        ).generate_from_frequencies(frequencias)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Ainda não há votos suficientes para gerar a nuvem ☁️")

