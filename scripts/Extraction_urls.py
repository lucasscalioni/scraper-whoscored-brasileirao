import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Caminhos e timestamp para o nome do arquivo
PATH_TO_DRIVER = r"C:"
BASE_URL = "https://www.whoscored.com"
OUTPUT_FOLDER = r"C"
timestamp = datetime.now().strftime('%d-%m-%y-%H-%M')
URLS_FILE = os.path.join(OUTPUT_FOLDER, f'match_urls_{timestamp}.txt')

# URL do site alvo
TARGET_URL = "https://br.whoscored.com/regions/31/tournaments/95/seasons/9428/brasil-brasileir%C3%A3o"#Brasileirao 2023

# Inicia o Edge WebDriver
service = Service(PATH_TO_DRIVER)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
time.sleep(2)

# Acessa a página principal
driver.get(TARGET_URL)
time.sleep(5)  # Ajuste esse tempo se necessário para garantir o carregamento completo

# Guarda a janela principal para depois retornar
main_window = driver.current_window_handle

# Conjunto para armazenar URLs já extraídas (já processadas)
extracted_urls = set()

# Função para extrair os links da página atual a partir dos ícones .svg
def extrair_links():
    icon_elements = driver.find_elements(By.XPATH, "//img[contains(@src, '.svg')]")
    links_page = []
    for icon in icon_elements:
        try:
            # Procura o elemento <a> ancestral da imagem
            a_tag = icon.find_element(By.XPATH, "./ancestor::a")
            if a_tag:
                href = a_tag.get_attribute("href")
                # Se for relativo, monta a URL completa
                if href and not href.startswith("http"):
                    href = BASE_URL + href
                if href and href not in links_page:
                    links_page.append(href)
        except Exception as e:
            print("Erro ao extrair link:", e)
    return links_page

# Abre o arquivo para escrita (substituindo o conteúdo existente)
with open(URLS_FILE, "w", encoding="utf-8") as file:
    previous_second_link = None  # Para comparar o segundo link de cada leva

    while True:
        # Extrai os links da página atual
        links = extrair_links()
        # Filtra somente os links que ainda não foram processados
        new_links = [link for link in links if link and (link not in extracted_urls)]
        
        if not new_links:
            print("Nenhum link novo encontrado nesta página. Encerrando loop.")
            break

        # Critério de parada: se o segundo link desta leva for igual ao da iteração anterior
        if len(new_links) >= 2:
            if previous_second_link == new_links[1]:
                print("Segundo link repetido da leva anterior. Encerrando loop.")
                break
            previous_second_link = new_links[1]
        
        # Processa cada link novo
        for link in new_links:
            try:
                # Abre o link em uma nova aba
                driver.execute_script("window.open(arguments[0]);", link)
                time.sleep(2)
                # Alterna para a aba recém-aberta
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)  # Aguarda o carregamento completo da nova página

                # Captura a URL completa da página atual e processa
                full_url = driver.current_url
                processed_url = full_url.replace("https://br.whoscored.com", "").strip()
                
                # Se não estiver vazia e ainda não tiver sido registrada, grava no arquivo
                if processed_url and processed_url not in extracted_urls:
                    file.write(processed_url + "\n")
                    file.flush()  # Força a escrita imediata
                    extracted_urls.add(processed_url)

                # Fecha a aba atual e retorna para a janela principal
                driver.close()
                driver.switch_to.window(main_window)
            except Exception as e:
                print("Erro ao processar link", link, ":", e)

        # Tenta clicar no botão para ir para a data anterior
        try:
            left_arrow = driver.find_element(By.ID, "dayChangeBtn-prev")
            if not left_arrow.is_enabled():
                print("Botão de data anterior desabilitado. Encerrando loop.")
                break
            left_arrow.click()
            time.sleep(5)  # Aguarda a página recarregar
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print("Não foi possível clicar no botão de data anterior. Encerrando loop.")
            break

# Encerra o navegador
driver.quit()
print("Extração concluída! URLs salvas em:", URLS_FILE)

# Lógica para apagar a primeira linha do arquivo gerado
with open(URLS_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

if lines:
    with open(URLS_FILE, "w", encoding="utf-8") as file:
        file.writelines(lines[1:])

print("Primeira linha removida do arquivo.")
