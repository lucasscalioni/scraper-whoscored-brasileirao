from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from datetime import datetime

# Caminhos
PATH_TO_DRIVER = r"C"
BASE_URL = "https://www.whoscored.com"
OUTPUT_FOLDER = r"C"
URLS_FILE = os.path.join(OUTPUT_FOLDER, 'match_urls.txt')

# Nome do arquivo com data e hora
timestamp = datetime.now().strftime('%d-%m-%y-%H-%M-%S')
SAVE_PATH = os.path.join(OUTPUT_FOLDER, f"data_{timestamp}.csv")

# Inicia o Edge WebDriver
service = Service(PATH_TO_DRIVER)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
time.sleep(2)

def get_team_players_summary(players_stats, date, defensive_stat_button, venue):
    player_list = []
    pos = []
    pos_meta_data = players_stats.find_all('span', {'class': 'player-meta-data'})
    for meta in pos_meta_data:
        if meta.text.strip().startswith(','):
            pos.append(meta.text.strip().split()[1])

    for i, player in enumerate(players_stats.find_all('span', {'class': 'iconize iconize-icon-left'})):
        record = {}
        record["Name"] = player.text
        age_text = players_stats.find_all('span', {'style': 'padding-left: 3px;'})[i].text
        record["Age"] = int(age_text) - (23 - int(date))
        record["Position"] = pos[i * 2]
        record["Shots"] = players_stats.find_all('td', {'class': 'ShotsTotal'})[i].text
        record["SoT"] = players_stats.find_all('td', {'class': 'ShotOnTarget'})[i].text
        record["KeyPasses"] = players_stats.find_all('td', {'class': 'KeyPassTotal'})[i].text
        record["PassAccuracy"] = players_stats.find_all('td', {'class': 'PassSuccessInMatch'})[i].text
        record["AerialsWon"] = players_stats.find_all('td', {'class': 'DuelAerialWon'})[i].text
        record["Touches"] = players_stats.find_all('td', {'class': 'Touches'})[i].text
        record["Rating"] = players_stats.find_all('td', {'class': 'rating'})[i].text
        player_list.append(record)

    # Estatísticas defensivas
    defensive_stat_button.click()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    defensive_stats = soup.find("div", {"id": f"statistics-table-{venue}-defensive"})

    for i in range(len(player_list)):
        player_list[i]["TackleWon"] = defensive_stats.find_all('td', {'class': 'TackleWonTotal'})[i].text
        player_list[i]["Interception"] = defensive_stats.find_all('td', {'class': 'InterceptionAll'})[i].text
        player_list[i]["Clearance"] = defensive_stats.find_all('td', {'class': 'ClearanceTotal'})[i].text
        player_list[i]["ShotBlocked"] = defensive_stats.find_all('td', {'class': 'ShotBlocked'})[i].text
        player_list[i]["Fouls"] = defensive_stats.find_all('td', {'class': 'FoulCommitted'})[i].text

    # Estatísticas da aba "Passes"
    try:
        passes_selector = f'a[href="#live-player-{venue}-passing"]'
        passes_tab = driver.find_element(By.CSS_SELECTOR, passes_selector)
        passes_tab.click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        passing_stats = soup.find("div", {"id": f"statistics-table-{venue}-passing"})

        for i in range(len(player_list)):
            player_list[i]["PassCrossTotal"] = passing_stats.find_all('td', {'class': 'PassCrossTotal'})[i].text
            player_list[i]["PassCrossAccurate"] = passing_stats.find_all('td', {'class': 'PassCrossAccurate'})[i].text
            player_list[i]["PassLongBallTotal"] = passing_stats.find_all('td', {'class': 'PassLongBallTotal'})[i].text
            player_list[i]["PassLongBallAccurate"] = passing_stats.find_all('td', {'class': 'PassLongBallAccurate'})[i].text
            player_list[i]["PassThroughBallTotal"] = passing_stats.find_all('td', {'class': 'PassThroughBallTotal'})[i].text
            player_list[i]["PassThroughBallAccurate"] = passing_stats.find_all('td', {'class': 'PassThroughBallAccurate'})[i].text
    except Exception as e:
        print(f"⚠️ Erro ao processar aba 'Passes' ({venue}): {e}")

    # Estatísticas da aba "Ofensivo"
    try:
        offensive_selector = f'a[href="#live-player-{venue}-offensive"]'
        offensive_tab = driver.find_element(By.CSS_SELECTOR, offensive_selector)
        offensive_tab.click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        offensive_stats = soup.find("div", {"id": f"statistics-table-{venue}-offensive"})

        for i in range(len(player_list)):
            player_list[i]["DribbleWon"] = offensive_stats.find_all('td', {'class': 'DribbleWon'})[i].text
            player_list[i]["FoulGiven"] = offensive_stats.find_all('td', {'class': 'FoulGiven'})[i].text
            player_list[i]["OffsideGiven"] = offensive_stats.find_all('td', {'class': 'OffsideGiven'})[i].text
            player_list[i]["Dispossessed"] = offensive_stats.find_all('td', {'class': 'Dispossessed'})[i].text
            player_list[i]["Turnover"] = offensive_stats.find_all('td', {'class': 'Turnover'})[i].text
    except Exception as e:
        print(f"⚠️ Erro ao processar aba 'Ofensivo' ({venue}): {e}")

    return player_list

# Scraping principal
players_data = []
cookie_flag = True

with open(URLS_FILE, 'r', encoding='utf-8') as file:
    matches_urls = [line.strip() for line in file.readlines() if line.strip()]

for match_url in matches_urls:
    driver.get(BASE_URL + match_url)
    time.sleep(3)

    if cookie_flag:
        try:
            driver.find_element(By.CLASS_NAME, "css-1wc0q5e").click()
            time.sleep(2)
        except:
            pass
        cookie_flag = False

    soup = BeautifulSoup(driver.page_source, "html.parser")
    match_header = soup.find("div", {"class": "match-header"})
    player_data = {
        "Date": match_header.find_all("dd")[-1].text.split()[-1],
        "HomeTeam": match_header.find_all("a")[0].text,
        "AwayTeam": match_header.find_all("a")[1].text,
    }

    driver.find_element(By.ID, "sub-sub-navigation").find_elements(By.TAG_NAME, "a")[1].click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    defensive_btns = driver.find_element(By.ID, "live-player-stats").find_elements(By.LINK_TEXT, "Defensive")

    player_data["home_players"] = get_team_players_summary(
        soup.find("div", {"id": "live-player-home-summary"}),
        player_data["Date"][-2:],
        defensive_btns[0],
        "home"
    )

    player_data["away_players"] = get_team_players_summary(
        soup.find("div", {"id": "live-player-away-summary"}),
        player_data["Date"][-2:],
        defensive_btns[1],
        "away"
    )

    players_data.append(player_data)

driver.quit()

# Junta todos os jogadores
all_players = []
for match in players_data:
    for player in match["home_players"]:
        player.update({
            "Time": match["HomeTeam"],
            "Adversário": match["AwayTeam"],
            "Data": match["Date"],
            "Mandante": True
        })
        all_players.append(player)

    for player in match["away_players"]:
        player.update({
            "Time": match["AwayTeam"],
            "Adversário": match["HomeTeam"],
            "Data": match["Date"],
            "Mandante": False
        })
        all_players.append(player)

# Salva o DataFrame
df = pd.DataFrame(all_players)
colunas_finais = [
    "Name", "Age", "Position", "Shots", "SoT", "KeyPasses", "PassAccuracy",
    "AerialsWon", "Touches", "Rating", "TackleWon", "Interception",
    "Clearance", "ShotBlocked", "Fouls",
    "PassCrossTotal", "PassCrossAccurate",
    "PassLongBallTotal", "PassLongBallAccurate",
    "PassThroughBallTotal", "PassThroughBallAccurate",
    "DribbleWon", "FoulGiven", "OffsideGiven", "Dispossessed", "Turnover",
    "Time", "Adversário", "Data", "Mandante"
]
df = df[colunas_finais]
df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")

print("✅ Arquivo CSV salvo com sucesso em:", SAVE_PATH)
