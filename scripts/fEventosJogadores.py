import pandas as pd
import os
from glob import glob

# Caminho da pasta onde estão os arquivos data_*.csv
PASTA_RAW = r"C:\Users\Data\Data raw"
PASTA_SAIDA = r"C:\Users\Data\Tables"
ARQUIVOS_CSV = glob(os.path.join(PASTA_RAW, "data_*.csv"))
CAMINHO_SAIDA = os.path.join(PASTA_SAIDA, "fEventosJogadores.csv")

# Lista para armazenar todos os DataFrames
todos_df = []

# Colunas que precisam de tratamento numérico
colunas_float_virgula = ["PassAccuracy", "Rating"]

for caminho_csv in ARQUIVOS_CSV:
    df = pd.read_csv(caminho_csv)

    # Substituições e tratamento para conversão em float
    for coluna in colunas_float_virgula:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace("-", "", regex=False)             # remove traços
            .str.replace("Ótimo", "", regex=False)         # remove texto inesperado
            .str.replace(",", ".", regex=False)            # vírgula → ponto
            .str.extract(r"(\d+\.?\d*)")                   # extrai somente número (ex: "7.3")
        )
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0.0)

    # Tratamento de tipos numéricos
    colunas_numericas = [
        "Age", "Shots", "SoT", "KeyPasses", "AerialsWon", "Touches",
        "TackleWon", "Interception", "Clearance", "ShotBlocked", "Fouls",
        "PassCrossTotal", "PassCrossAccurate", "PassLongBallTotal",
        "PassLongBallAccurate", "PassThroughBallTotal", "PassThroughBallAccurate",
        "DribbleWon", "FoulGiven", "OffsideGiven", "Dispossessed", "Turnover"
    ]
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    # Conversão da data
    df["Data"] = pd.to_datetime(df["Data"], errors='coerce')

    # Criação dos identificadores
    df["IdJogador"] = df["Name"] + " - " + df["Time"]
    df["IdJogo"] = df.apply(
        lambda row: f"{row['Time']} x {row['Adversário']}" if str(row["Mandante"]).lower() == "true"
        else f"{row['Adversário']} x {row['Time']}",
        axis=1
    )
    df["ID"] = df["IdJogo"] + df["Data"].dt.year.astype(str)

    todos_df.append(df)

# Junta tudo em um único DataFrame
df_final = pd.concat(todos_df, ignore_index=True)

# Caminho de salvamento final
CAMINHO_SAIDA = os.path.join(PASTA_SAIDA, "fEventosJogadores.csv")
df_final.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

print(f"✅ fEventosJogadores.csv salvo com sucesso em:\n{CAMINHO_SAIDA}")
