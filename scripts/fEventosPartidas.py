import pandas as pd
import os
from glob import glob

PASTA_DADOS = r"C:\Users\lucas\OneDrive\Documentos\Python\Futebol\Data\Data novo"
ARQUIVOS_EVENTOS = glob(os.path.join(PASTA_DADOS, "eventos_*.csv"))

eventos_df = []

for caminho_csv in ARQUIVOS_EVENTOS:
    df = pd.read_csv(caminho_csv)

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Ano"] = df["Data"].dt.year.astype(str)
    df["IdJogador"] = df["jogador"].astype(str) + " - " + df["time"].astype(str)

    df["Gols"] = df["descricao"].astype(str).str.startswith("GOAL!").astype(int)
    df["Own Goal"] = df["descricao"].astype(str).str.contains("OWN GOAL", case=False, na=False).astype(int)
    df["Assistência"] = df["assist"].fillna("").astype(str).str.strip().apply(lambda x: 1 if x else 0)
    df["Yellow Card"] = df["descricao"].astype(str).str.contains("yellow card", case=False, na=False).astype(int)
    df["Red Card"] = df["descricao"].astype(str).str.contains("red card", case=False, na=False).astype(int)

    df["Resultado"] = df["Resultado"].astype(str).str.strip().str.replace(" ", "").str.replace("–", "-")
    df["minuto"] = df["minuto"].astype(str)

    # 1. Extrair JogoBase de IdJogo (remove o ano final)
    df[["JogoBase", "AnoFinal"]] = df["IdJogo"].str.extract(r"^(.*?)(\d{4})?$")

    # 2. Tentar dividir mandante e visitante com validação
    split_jogo = df["JogoBase"].str.split(" x ", expand=True)
    if split_jogo.shape[1] != 2:
        print("⚠️ Atenção: houve erro ao dividir mandante x visitante. Verifique a coluna IdJogo.")
        continue  # pula este arquivo com problema

    df["MandanteNome"] = split_jogo[0].str.strip()
    df["VisitanteNome"] = split_jogo[1].str.strip()
    df["Mandante"] = df["time"].str.strip() == df["MandanteNome"]

    # 3. Separar o Resultado (com segurança)
    gols_split = df["Resultado"].str.split("-", expand=True)
    if gols_split.shape[1] == 2:
        df["GolsMandante"] = pd.to_numeric(gols_split[0], errors="coerce").fillna(0).astype(int)
        df["GolsVisitante"] = pd.to_numeric(gols_split[1], errors="coerce").fillna(0).astype(int)
    else:
        df["GolsMandante"] = 0
        df["GolsVisitante"] = 0

    # 4. Calcular SofreuGol com base em mandante
    df["SofreuGol"] = df.apply(
        lambda row: 1 if (row["Mandante"] and row["GolsVisitante"] > 0) or
                          (not row["Mandante"] and row["GolsMandante"] > 0) else 0,
        axis=1
    )

    # 5. Atualizar IdJogo final e limpeza
    df["Jogo"] = df["JogoBase"]
    df["IdJogo"] = df["JogoBase"] + df["Ano"]

    df.drop(columns=[
        "assist", "placar_momento", "descricao", "tipo",
        "MandanteNome", "VisitanteNome", "JogoBase", "AnoFinal",
        "GolsMandante", "GolsVisitante", "Ano"
    ], errors="ignore", inplace=True)

    eventos_df.append(df)

# Unir tudo e salvar
df_eventos_final = pd.concat(eventos_df, ignore_index=True)
CAMINHO_SAIDA = os.path.join(PASTA_DADOS, "fEventosPartida.csv")
df_eventos_final.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

print(f"✅ fEventosPartida.csv salvo com sucesso em:\n{CAMINHO_SAIDA}")
