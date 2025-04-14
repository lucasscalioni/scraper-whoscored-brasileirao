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

```
scraper-whoscored-brasileirao/
│
├── data/                         # Os exemplos do GitHub não estão com todos os dados, são exemplos de output
│   ├── raw/                      # Arquivos brutos extraídos com Selenium
│   └── processed/                # Arquivos tratados prontos para Power BI
│       ├── fEventosJogadores.csv
│       ├── fEventosPartida.csv
│       ├── dJogadores.csv
│       └── dPartidas.csv
│       └── dTimes.csv #Feito manualmente
│
├── scripts/
│   ├── Extraction_urls.py                      # Extrai URLs de partidas por data
│   ├── Extraction_players_events_whoscored.py  # Extrai estatísticas dos jogadores (todas as abas)
│   ├── Extraction_match_events_whoscored.py    # Extrai eventos da timeline (gols, cartões, assistências)
│   ├── fEventosJogadores.py                    # Processa estatísticas e cria fEventosJogadores
│   ├── fEventosPartidas.py                     # Processa eventos e gera fEventosPartida
│   ├── dJogador.py                             # Cria tabela dJogadores com posição e time
│   └── dPartidas.py                            # Cria tabela por time em cada jogo (linha dupla por partida)
│
├── main.py               # (em construção) Pipeline sequencial com try/except
├── requirements.txt      # Dependências do projeto
└── README.md
```

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

```
Name, Age, Position, Shots, SoT, KeyPasses, PassAccuracy, AerialsWon, Touches,
Rating, TackleWon, Interception, Clearance, ShotBlocked, Fouls, PassCrossTotal,
PassCrossAccurate, PassLongBallTotal, PassLongBallAccurate, PassThroughBallTotal,
PassThroughBallAccurate, DribbleWon, FoulGiven, OffsideGiven, Dispossessed,
Turnover, Time, Adversário, Data, Mandante
```

### 📅 Eventos Cronológicos por Partida

Cada linha representa um evento relevante (gol, assistência, cartão):

```
minuto, time, tipo, jogador, assist, placar_momento, descricao, Resultado, Data
```

---

## 🧩 Tabelas e Modelagem

### 🔹 Tabelas Geradas

| Tipo        | Nome                  | Descrição                                                   |
|-------------|-----------------------|--------------------------------------------------------------|
| Dimensão    | `dJogadores`          | Jogadores únicos por time + posição                          |
| Dimensão    | `dPartidas`           | Uma linha por time em cada partida, com placar e vencedor    |
| Fato        | `fEventosJogadores`   | Ações de cada jogador por jogo (passes, chutes, defesa etc.) |
| Fato        | `fEventosPartida`     | Eventos importantes da partida (gols, assistências etc.)     |

### 🔐 Chaves Criadas

- `IdJogador`: Nome + Time
- `IdJogo`: Nome do confronto com ano
- `ID`: Composto (IdJogo + ano)

---

## 🚀 Pipeline ETL (em construção)

1. **Extração**
   - URLs de jogos
   - Estatísticas por jogador
   - Timeline de eventos

2. **Transformação**
   - Conversão de tipos, normalização de colunas
   - Criação de medidas (Gols por Jogo, Assistências por Jogo, Sofreu Gol etc.)

3. **Carga**
   - Salva os arquivos `.csv` prontos para leitura no Power BI

---

## 📌 Próximos Passos

- [x] Finalizar scraping de todas as partidas disponíveis de 2024–2025
- [x] Criar pipeline de transformação por script (já modularizado)
- [ ] Criar `main.py` sequencial
- [ ] Adicionar métricas avançadas (xG, xA, passes decisivos, pressão, etc.)
- [ ] Adicionar dados do FBref ou Transfermarkt no futuro
- [ ] Criar visualizações públicas no Power BI
- [ ] Extrair dados de outros campeonatos e outras temporadas do Brasileirão 

---

## 📬 Contato

**Lucas Scalioni de Souza**  
[LinkedIn](https://www.linkedin.com/in/lucas-scalioni-de-souza-7b1537138)  
📧 lucasscalioni@gmail.com
