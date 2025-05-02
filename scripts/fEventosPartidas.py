import pandas as pd
import os
from glob import glob
import re

# Caminhos
PASTA_DADOS_RAW = r"C:\Users\Data\Data raw"
PASTA_SAIDA = r"C:\Users\Data\Tables"
ARQUIVOS_EVENTOS = glob(os.path.join(PASTA_DADOS_RAW, "eventos_*.csv"))

eventos_df = []

for caminho_csv in ARQUIVOS_EVENTOS:
    df = pd.read_csv(caminho_csv)

    # Normalizações iniciais
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Ano"] = df["Data"].dt.year.astype(str)
    df["minuto"] = df["minuto"].astype(str).str.strip()
    df["jogador"] = df["jogador"].fillna("").astype(str).str.strip()
    df["time"] = df["time"].fillna("").astype(str).str.strip()
    df["descricao"] = df["descricao"].fillna("").astype(str).str.strip()
    df["assist"] = df["assist"].fillna("").astype(str).str.strip()
    df["Resultado"] = df["Resultado"].astype(str).str.strip().str.replace("–", "-").str.replace(" ", "")
    df["IdJogador"] = df["jogador"] + " - " + df["time"]

    # Eventos
    df["Gols"] = df["descricao"].str.startswith("GOAL!").astype(int)
    df["Own Goal"] = df["descricao"].str.contains("OWN GOAL!", case=False, na=False).astype(int)
    df["Assistência"] = df["descricao"].str.contains("assists a goal", case=False, na=False).astype(int)
    df["Yellow Card"] = df["descricao"].str.contains("yellow card", case=False, na=False).astype(int)
    df["Red Card"] = df["descricao"].str.contains("red card", case=False, na=False).astype(int)

    # Observações (para gols e assistências)
    def extrair_obs(texto):
        if "GOAL!" in texto or "assists a goal" in texto:
            match = re.search(r"\((.*?)\)", texto)
            return match.group(1) if match else ""
        return ""

    df["Observacao"] = df["descricao"].apply(extrair_obs)

    # Gerar Jogo, Mandante e SofreuGol
    df[["JogoBase", "AnoFinal"]] = df["IdJogo"].str.extract(r"^(.*?)(\d{4})?$")
    split_jogo = df["JogoBase"].str.split(" x ", expand=True)
    if split_jogo.shape[1] != 2:
        print(f"⚠️ Erro ao dividir mandante/visitante: {caminho_csv}")
        continue

    df["MandanteNome"] = split_jogo[0].str.strip()
    df["VisitanteNome"] = split_jogo[1].str.strip()
    df["Mandante"] = df["time"] == df["MandanteNome"]

    gols_split = df["Resultado"].str.split("-", expand=True)
    df["GolsMandante"] = pd.to_numeric(gols_split[0], errors="coerce").fillna(0).astype(int)
    df["GolsVisitante"] = pd.to_numeric(gols_split[1], errors="coerce").fillna(0).astype(int)

    df["SofreuGol"] = df.apply(
        lambda row: 1 if (row["Mandante"] and row["GolsVisitante"] > 0)
                     or (not row["Mandante"] and row["GolsMandante"] > 0)
                     else 0,
        axis=1
    )

    df["Jogo"] = df["JogoBase"]
    df["IdJogo"] = df["JogoBase"] + df["Ano"]

    # Limpeza final
    df.drop(columns=[
        "assist", "placar_momento", "descricao", "tipo",
        "MandanteNome", "VisitanteNome", "JogoBase", "AnoFinal",
        "GolsMandante", "GolsVisitante", "Ano"
    ], inplace=True, errors="ignore")

    eventos_df.append(df)

# Junta tudo
df_final = pd.concat(eventos_df, ignore_index=True)

# Reorganiza colunas
colunas_ordem = [
    "minuto", "time", "jogador", "Resultado", "Data", "IdJogo", "IdJogador",
    "Gols", "Own Goal", "Assistência", "Yellow Card", "Red Card",
    "Mandante", "SofreuGol", "Jogo", "Observacao"
]
df_final = df_final[colunas_ordem]

# Salva arquivo final
CAMINHO_SAIDA = os.path.join(PASTA_SAIDA, "fEventosPartida.csv")
df_final.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")
print(f"✅ fEventosPartida.csv atualizado com sucesso em:\n{CAMINHO_SAIDA}")
