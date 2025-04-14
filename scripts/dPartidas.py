import pandas as pd
import os

# Caminho do arquivo de eventos
CAMINHO_EVENTOS = r"C:\Users\lucas\OneDrive\Documentos\Python\Futebol\Data\Data novo\fEventosPartida.csv"
df = pd.read_csv(CAMINHO_EVENTOS)

# Garantir colunas esperadas e consistência
df["Resultado"] = df["Resultado"].astype(str).str.strip().str.replace("–", "-").str.replace(" ", "")
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# Extrair gols mandante e visitante
gols_split = df["Resultado"].str.split("-", expand=True)
df["GolsMandante"] = pd.to_numeric(gols_split[0], errors="coerce").fillna(0).astype(int)
df["GolsVisitante"] = pd.to_numeric(gols_split[1], errors="coerce").fillna(0).astype(int)

# Extrair Jogo sem ano e times
df["JogoSemAno"] = df["Jogo"].str.extract(r"^(.*? x .*?)(?:\d{4})?$")[0]
df[["MandanteNome", "VisitanteNome"]] = df["JogoSemAno"].str.split(" x ", expand=True)

# Remover duplicatas por partida
partidas_unicas = df.drop_duplicates(subset=["JogoSemAno", "Data"]).copy()

# Gerar linhas longitudinais (uma para cada time por jogo)
linhas = []

for _, row in partidas_unicas.iterrows():
    ano = row["Data"].year
    idjogo = f"{row['JogoSemAno']}{ano}"

    # Mandante
    linhas.append({
        "Time": row["MandanteNome"],
        "Adversário": row["VisitanteNome"],
        "IdJogo": idjogo,
        "Jogo": row["JogoSemAno"],
        "Mandante": True,
        "Gols Feitos": row["GolsMandante"],
        "Gols Sofridos": row["GolsVisitante"],
        "Resultado": row["Resultado"],
        "Vencedor": (
            row["MandanteNome"] if row["GolsMandante"] > row["GolsVisitante"]
            else row["VisitanteNome"] if row["GolsVisitante"] > row["GolsMandante"]
            else "Empate"
        ),
        "Data": row["Data"]
    })

    # Visitante
    linhas.append({
        "Time": row["VisitanteNome"],
        "Adversário": row["MandanteNome"],
        "IdJogo": idjogo,
        "Jogo": row["JogoSemAno"],
        "Mandante": False,
        "Gols Feitos": row["GolsVisitante"],
        "Gols Sofridos": row["GolsMandante"],
        "Resultado": row["Resultado"],
        "Vencedor": (
            row["MandanteNome"] if row["GolsMandante"] > row["GolsVisitante"]
            else row["VisitanteNome"] if row["GolsVisitante"] > row["GolsMandante"]
            else "Empate"
        ),
        "Data": row["Data"]
    })

# Criar DataFrame final
df_dpartidas = pd.DataFrame(linhas)

# Salvar CSV
CAMINHO_SAIDA = os.path.join(os.path.dirname(CAMINHO_EVENTOS), "dPartidas.csv")
df_dpartidas.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

print(f"✅ dPartidas.csv criado com sucesso em:\n{CAMINHO_SAIDA}")
