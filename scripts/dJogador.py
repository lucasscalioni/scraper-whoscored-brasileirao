import os
import glob
import pandas as pd

# Caminho onde estão os arquivos data_*.csv
caminho = r"C:\Users"
arquivos_data = glob.glob(os.path.join(caminho, "data_*.csv"))
print("Arquivos encontrados:", arquivos_data)

lista_dfs = []

for arquivo in arquivos_data:
    try:
        df = pd.read_csv(arquivo, sep=',', encoding='utf-8-sig')
        print(f"Arquivo {arquivo}: {len(df)} registros lidos.")

        required_cols = ["Name", "Time", "Position"]
        if all(col in df.columns for col in required_cols):
            df["Name"] = df["Name"].astype(str).str.strip()
            df["Time"] = df["Time"].astype(str).str.strip()
            df["Position"] = df["Position"].astype(str).str.strip()

            # Cria o IdJogador com base em Nome + Time
            df["IdJogador"] = df["Name"] + " - " + df["Time"]

            lista_dfs.append(df[["Name", "Time", "Position", "IdJogador"]])
        else:
            print(f"⚠️ Colunas ausentes em {arquivo}: {df.columns.tolist()}")
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")

# Concatena todos os arquivos
dados = pd.concat(lista_dfs, ignore_index=True) if lista_dfs else pd.DataFrame(columns=["Name", "Time", "Position", "IdJogador"])
print("Total de registros lidos:", len(dados))

# Função de moda excluindo "Sub"
def get_mode_excluding_sub(serie):
    non_sub = serie[serie.str.lower().str.strip() != "sub"]
    return non_sub.mode().iloc[0] if not non_sub.mode().empty else ""

# Agrega por IdJogador apenas se houver repetições exatas
df_final = dados.groupby("IdJogador", as_index=False).agg({
    "Name": "first",
    "Time": "first",
    "Position": get_mode_excluding_sub
})

# Une com dJogadores.csv existente (se houver) e deduplica por IdJogador
arquivo_djogadores = os.path.join(caminho, "dJogadores.csv")
if os.path.exists(arquivo_djogadores):
    try:
        existentes = pd.read_csv(arquivo_djogadores, sep=',', encoding='utf-8-sig')
        print("Jogadores existentes:", len(existentes))
        combinados = pd.concat([existentes, df_final], ignore_index=True)
        df_final = combinados.drop_duplicates(subset="IdJogador", keep="first")
        print("Após combinar:", df_final.shape[0])
    except Exception as e:
        print(f"Erro ao combinar com dJogadores.csv existente: {e}")

# Salva arquivo final
try:
    df_final.to_csv(arquivo_djogadores, index=False, sep=',', encoding='utf-8-sig')
    print("✅ dJogadores.csv atualizado com sucesso!")
except Exception as e:
    print(f"Erro ao salvar dJogadores.csv: {e}")
