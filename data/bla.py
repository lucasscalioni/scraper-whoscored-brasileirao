import os

# Diretório raiz do projeto
ROOT = os.path.join(os.getcwd(), "scraper-whoscored-brasileirao")

# Lista de subpastas que queremos garantir
folders = [
    "data/raw",
    "data/processed",
    "scripts",
    "dashboards"
]

# Criar cada pasta e um .gitkeep dentro
for folder in folders:
    path = os.path.join(ROOT, folder)
    os.makedirs(path, exist_ok=True)
    
    # Cria o arquivo .gitkeep para garantir versionamento
    gitkeep_path = os.path.join(path, ".gitkeep")
    with open(gitkeep_path, "w", encoding="utf-8") as f:
        f.write("")
    
    print(f"✅ Criado: {path} + .gitkeep")

print("\n📁 Estrutura criada com sucesso!")
