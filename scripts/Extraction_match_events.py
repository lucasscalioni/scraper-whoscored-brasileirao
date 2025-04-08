from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from datetime import datetime

# Caminhos fixos
PATH_TO_DRIVER = r"C:\Users\073907\Downloads\edgedriver_win64\msedgedriver.exe"
BASE_URL = "https://www.whoscored.com"
OUTPUT_FOLDER = r"C:\Users\073907\Downloads"
URLS_FILE = os.path.join(OUTPUT_FOLDER, "match_urls.txt")
timestamp = datetime.now().strftime('%d-%m-%y-%H-%M-%S')
SAVE_PATH = os.path.join(OUTPUT_FOLDER, f"eventos_{timestamp}.csv")

# Inicia WebDriver
service = Service(PATH_TO_DRIVER)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
time.sleep(2)

def get_match_events(driver):
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    team_cells = soup.find_all("td", class_="team")
    home_team = team_cells[0].text.strip()
    away_team = team_cells[1].text.strip()
    score = soup.find("td", class_="result").text.strip()
    match_date = soup.find("dt", text="Date:").find_next_sibling("dd").text.strip()

    timeline = soup.find("div", id="live-incidents")
    rows = timeline.find_all("tr")
    eventos = []

    for row in rows:
        minute_tag = row.find("span", class_="minute")
        if not minute_tag:
            continue
        minute = minute_tag.text.strip().replace("'", "")

        for side in ["home", "away"]:
            incident_td = row.find("td", class_=f"key-incident {side}-incident")
            if incident_td:
                incidents = incident_td.find_all("div", class_="match-centre-header-team-key-incident")
                for incident in incidents:
                    tipo = incident.get("data-type")
                    title = incident.get("title", "")
                    jogador = incident.find("a", class_="player-name")
                    jogador_nome = jogador.text.strip() if jogador else ""
                    assist = None
                    placar_momento = None

                    if tipo == "16":  # Gol
                        score_tag = incident.find("span", class_="current-score")
                        placar_momento = score_tag.text.strip("()") if score_tag else ""
                        previous = incident.find_previous_sibling("div")
                        if previous and previous.get("data-type") == "1":
                            assist_tag = previous.find("a", class_="player-name")
                            assist = assist_tag.text.strip() if assist_tag else ""

                    eventos.append({
                        "minuto": minute,
                        "time": home_team if side == "home" else away_team,
                        "tipo": tipo,
                        "jogador": jogador_nome,
                        "assist": assist,
                        "placar_momento": placar_momento,
                        "descricao": title,
                        "Resultado": score,
                        "Data": match_date
                    })

    return eventos

# Lê as URLs do arquivo
with open(URLS_FILE, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

todos_eventos = []

for relative_url in urls:
    full_url = BASE_URL + relative_url
    try:
        driver.get(full_url)
        eventos = get_match_events(driver)
        todos_eventos.extend(eventos)
        print(f"✅ Processado: {full_url}")
    except Exception as e:
        print(f"⚠️ Erro ao processar {full_url}: {e}")

driver.quit()

# Salva tudo em CSV
df_final = pd.DataFrame(todos_eventos)
df_final.to_csv(SAVE_PATH, index=False, encoding='utf-8-sig')
print(f"✅ Arquivo final salvo em: {SAVE_PATH}")
