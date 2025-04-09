# ⚽ WhoScored Brasileirão Scraper – ETL & Automação de Estatísticas de Jogadores e Partidas (2024 & 2025)

🚧 **Status:** Em progresso – Scraping finalizado para jogadores e eventos; estruturação, modelagem e refinamento do pipeline ETL em andamento

---

## 🎯 Objetivo

Desenvolver um pipeline ETL completo para automatizar a **coleta, transformação e carregamento** de estatísticas detalhadas de partidas e jogadores da Série A do Campeonato Brasileiro (2024 e 2025), utilizando o site WhoScored como fonte principal.

**Pipeline ETL:**
- **Extração (Extract):** Coletar dados brutos de mais de **400 partidas** (20.000+ linhas) utilizando Python, Selenium e BeautifulSoup.
- **Transformação (Transform):** Limpar, padronizar e estruturar os dados em um modelo dimensional (modelo estrela), criando tabelas de dimensão (dJogador, dPartida e dTime) e de fato (fEstatisticasJogador e fEventosPartida), com IDs inteligentes que garantem a integridade dos dados.
- **Carregamento (Load):** Integrar os dados transformados em dashboards interativos no Power BI para análises de performance, scouting e inteligência tática, permitindo otimizar os dados de futebol.

Embora o projeto esteja focado no Brasileirão para estabelecer uma base robusta, a lógica aplicada é versátil e pode ser facilmente adaptada para a maioria dos campeonatos e jogos disponíveis no WhoScored.

---

## 🛠 Ferramentas Utilizadas

- **Python** (Selenium, BeautifulSoup, Pandas)
- **Power BI**
- **CSV/TXT** para ingestão dos dados
- **GitHub** para versionamento e documentação

---

## 📊 Dados Já Coletados

### 🧍‍♂️ Estatísticas de Jogadores (por partida)

Extraídas de mais de **400 partidas**, totalizando **+20.000 linhas** de informações, com os seguintes campos:  
`Name, Age, Position, Shots, SoT, KeyPasses, PassAccuracy, AerialsWon, Touches, Rating, TackleWon, Interception, Clearance, ShotBlocked, Fouls, PassCrossTotal, PassCrossAccurate, PassLongBallTotal, PassLongBallAccurate, PassThroughBallTotal, PassThroughBallAccurate, DribbleWon, FoulGiven, OffsideGiven, Dispossessed, Turnover, Time, Adversário, Data, Mandante`

### 📅 Cronologia de Eventos por Partida (Timeline WhoScored)

Cada registro representa um evento (gol, assistência, cartão ou substituição) com os campos:  
`minuto, time, tipo, jogador, assist, placar_momento, descricao, Resultado, Data`

---

## 🧩 Estrutura e Modelagem (em andamento)

### 📁 Tabelas Fato e Dimensão

| Tipo           | Tabela                   | Objetivo                                                  |
|----------------|--------------------------|-----------------------------------------------------------|
| **Dimensão**   | `dJogador`               | Unificar dados dos jogadores (nome, idade, posição, time)   |
| **Dimensão**   | `dPartida`               | Criar um `MatchID` único para cada partida                |
| **Dimensão**   | `dTime`                  | Normalizar os nomes dos times e registrar metadados        |
| **Fato**       | `fEstatisticasJogador`   | Armazenar métricas quantitativas por jogo                 |
| **Fato**       | `fEventosPartida`        | Registrar a timeline detalhada dos eventos por partida     |

### 🧠 IDs Planejados

- **PlayerID:** Combinação única de `nome`, `time` e `posição`.
- **MatchID:** Criado a partir de um hash ou concatenação de `data`, `mandante`, `visitante` e `Resultado`.
- **TeamID:** Tabela única para normalizar os nomes dos times e seus metadados.

---

## 🚀 Pipeline ETL – Visão Geral

1. **Extração (Extract):**  
   - Dados coletados via scraping do site WhoScored utilizando Python, Selenium e BeautifulSoup.
2. **Transformação (Transform):**  
   - Os dados brutos são limpos e organizados em um modelo dimensional robusto, pronto para análises detalhadas.
3. **Carregamento (Load):**  
   - Dados transformados são integrados em dashboards interativos no Power BI para análise e visualização dos insights, permitindo aperfeiçoar a interpretação dos dados de futebol.

---

## 📌 Próximos Passos

- [ ] Criar as tabelas `dJogador`, `dTime` e `dPartida` com chaves únicas e padronizadas.
- [ ] Padronizar e limpar os nomes dos jogadores.
- [ ] Estabelecer as relações entre as tabelas Fato e Dimensão (modelo estrela).
- [ ] Integrar com dados de outras fontes (FBref, Transfermarkt, StatsBomb) para enriquecer a base.
- [ ] Refinar e expandir os dashboards no Power BI com análises táticas e de performance.

---

## 📎 Observações

> Este é meu primeiro projeto público de futebol analytics, que abrange desde a extração dos dados até a modelagem analítica completa.  
> A implementação do pipeline ETL organiza os dados de forma eficiente e agrega valor aos insights de performance e scouting.
> Embora o foco atual seja o Brasileirão, a lógica do pipeline é adaptável a uma ampla gama de campeonatos e jogos disponíveis no WhoScored.
> O projeto tem como meta, na fase de Carregamento, potencializar os dados para a criação de um BI completo e robusto.
> Feedbacks, colaborações e conexões são bem-vindos para aprimorar esta iniciativa.

---

## 📬 Contato

**Lucas Scalioni de Souza**  
[LinkedIn](https://www.linkedin.com/in/lucas-scalioni-de-souza-7b1537138)  
📧 lucasscalioni@gmail.com
