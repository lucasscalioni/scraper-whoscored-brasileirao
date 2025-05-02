# ⚽ WhoScored Brasileirão Scraper – ETL & Automação de Estatísticas de Jogadores e Partidas (2024 & 2025)

🚧 **Status:** Em progresso – Scraping finalizado para jogadores e eventos; estruturação, modelagem e refinamento do pipeline ETL em andamento.

---

## 🎯 Objetivo

Desenvolver um pipeline ETL completo para automatizar a **coleta, transformação e carregamento** de estatísticas detalhadas de partidas e jogadores da Série A do Campeonato Brasileiro (2024 e 2025), utilizando o site WhoScored como fonte principal.

**Pipeline ETL:**
- **Extração (Extract):** Coleta automatizada de dados brutos de partidas usando Python, Selenium e BeautifulSoup.
- **Transformação (Transform):** Limpeza, padronização e estruturação dos dados em um modelo dimensional (estilo estrela), com tabelas de fato e dimensão.
- **Carregamento (Load):** Geração de arquivos CSV prontos para análise no Power BI.

---

## 📦 Estrutura do Projeto

scraper-whoscored-brasileirao/
│
├── data/
│ ├── raw/ # Arquivos brutos extraídos com Selenium
│ └── tables/ # Arquivos tratados prontos para Power BI
│ ├── fEventosJogadores.csv
│ ├── fEventosPartida.csv
│ ├── dJogadores.csv
│ ├── dPartidas.csv
│ └── dTimes.csv # Feito manualmente
│
├── scripts/
│ ├── Extraction_urls.py
│ ├── Extraction_players_events_whoscored.py
│ ├── Extraction_match_events_whoscored.py
│ ├── fEventosJogadores.py
│ ├── fEventosPartidas.py
│ ├── dJogador.py
│ └── dPartidas.py
│
├── main.py # Orquestrador CLI do pipeline ETL
├── requirements.txt # Dependências do projeto
└── README.md

---

## 🛠 Ferramentas Utilizadas

- **Python 3.10+**
- `pandas`
- `selenium`
- `beautifulsoup4`
- `lxml`
- `Power BI` (para visualizações finais)

---

## 📊 Dados Já Coletados

### 🧍‍♂️ Estatísticas de Jogadores por Partida

Extraídas de mais de **400 partidas**, totalizando **+20.000 linhas** com os seguintes campos:

Name, Age, Position, Shots, SoT, KeyPasses, PassAccuracy, AerialsWon, Touches,
Rating, TackleWon, Interception, Clearance, ShotBlocked, Fouls, PassCrossTotal,
PassCrossAccurate, PassLongBallTotal, PassLongBallAccurate, PassThroughBallTotal,
PassThroughBallAccurate, DribbleWon, FoulGiven, OffsideGiven, Dispossessed,
Turnover, Time, Adversário, Data, Mandante

### 📅 Eventos Cronológicos por Partida

Cada linha representa um evento relevante (gol, assistência, cartão):

minuto, time, tipo, jogador, assist, placar_momento, descricao, Resultado, Data

---

## 🧩 Tabelas e Modelagem

### 🔹 Tabelas Geradas

| Tipo      | Nome                | Descrição                                                   |
|-----------|---------------------|--------------------------------------------------------------|
| Dimensão  | `dJogadores`        | Jogadores únicos por time + posição                          |
| Dimensão  | `dPartidas`         | Uma linha por time em cada partida, com placar e vencedor    |
| Fato      | `fEventosJogadores` | Ações de cada jogador por jogo (passes, chutes, defesa etc.) |
| Fato      | `fEventosPartida`   | Eventos importantes da partida (gols, assistências etc.)     |

### 🔐 Chaves Criadas

- `IdJogador`: Nome + Time
- `IdJogo`: Nome do confronto com ano
- `ID`: Composto (IdJogo + ano)

---

## 🚀 Pipeline ETL (modularizado via `main.py`)

### Comandos disponíveis:
---
python main.py --extrair-eventos        # Scraping da timeline de eventos (gols, assistências, cartões)
python main.py --extrair-jogadores      # Scraping das estatísticas dos jogadores
python main.py --eventos-partida        # Processamento e geração do fEventosPartida.csv
python main.py --eventos-jogadores      # Processamento e geração do fEventosJogadores.csv
python main.py --dpartidas              # Geração da tabela dPartidas.csv
python main.py --djogadores             # Atualização da tabela dJogadores.csv
## 📌 Próximos Passos

- [x] Finalizar scraping de todas as partidas disponíveis de 2024–2025
- [x] Criar pipeline de transformação por script (modularizado)
- [x] Criar `main.py` sequencial com orquestração por argumentos
- [ ] Adicionar métricas avançadas (xG, xA, passes decisivos, pressão, etc.)
- [ ] Adicionar dados do FBref ou Transfermarkt
- [ ] Criar visualizações públicas no Power BI
- [ ] Escalar o projeto com BigQuery + GCP Cloud Functions
- [ ] Criar agendamentos com Airflow ou Cloud Scheduler


📬 Contato
Lucas Scalioni de Souza
🔗 LinkedIn
📧 lucasscalioni@gmail.com
