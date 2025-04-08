# ⚽ WhoScored Brasileirão Scraper – Automação de Estatísticas de Jogadores e Partidas (2024 & 2025)

🚧 **Status:** Em progresso – scraping finalizado para jogadores e eventos, estruturação e modelagem em andamento

---

## 🎯 Objetivo

Automatizar a coleta de estatísticas detalhadas de partidas e jogadores da Série A do Campeonato Brasileiro (2024 e 2025), utilizando o site WhoScored como fonte.  
O projeto visa construir uma **base estruturada de dados para análise de performance, scouting e inteligência tática**, com visualizações em Power BI.

---

## 🛠 Ferramentas Utilizadas

- **Python** (Selenium, BeautifulSoup, Pandas)
- **Power BI**
- **CSV/TXT** para ingestão de dados
- **GitHub** para versionamento e documentação

---

## 📊 Dados Já Coletados

### 🧍‍♂️ Estatísticas de Jogadores (por partida)

Extraídas de mais de **400 partidas**, totalizando **+17.000 linhas**:

Name, Age, Position, Shots, SoT, KeyPasses, PassAccuracy, AerialsWon, Touches, Rating, TackleWon, Interception, Clearance, ShotBlocked, Fouls, PassCrossTotal, PassCrossAccurate, PassLongBallTotal, PassLongBallAccurate, PassThroughBallTotal, PassThroughBallAccurate, DribbleWon, FoulGiven, OffsideGiven, Dispossessed, Turnover, Time, Adversário, Data, Mandante


---

### 📅 Cronologia de Eventos por Partida (timeline WhoScored)

Cada linha representa um evento como gol, assistência, cartão ou substituição:

minuto, time, tipo, jogador, assist, placar_momento, descricao, Resultado, Data


---

## 🧩 Estrutura e Modelagem (em andamento)

Antes de visualizar os dados no Power BI, o foco agora está em **estruturar corretamente o modelo dimensional**:

### 📁 Tabelas Fato e Dimensão

| Tipo        | Tabela                    | Objetivo                                 |
|-------------|---------------------------|-------------------------------------------|
| Dimensão    | `dJogador`                | Unificar nomes, idade, posição, time atual |
| Dimensão    | `dPartida`                | Criar um `MatchID` único por jogo         |
| Dimensão    | `dTime`                   | Criar um `TeamID` e metadados do clube    |
| Fato        | `fEstatisticasJogador`    | Métricas quantitativas por jogo           |
| Fato        | `fEventosPartida`         | Timeline de eventos em granularidade      |

---

### 🧠 IDs inteligentes planejados

- `PlayerID`: combinação de `nome`, `time`, `data de nascimento`, `posição` (para lidar com transferências e variações de nome)
- `MatchID`: hash ou concatenação de `data + mandante + visitante`
- `TeamID`: tabela única para normalizar os nomes dos times

---

## 📌 Próximos Passos

- [ ] Criar `dJogador`, `dTime`, `dPartida` com chaves limpas e únicas
- [ ] Tratar e padronizar nomes de jogadores
- [ ] Relacionar as tabelas Fato e Dimensão (modelo estrela)
- [ ] Cruzar com dados de outras fontes (FBref, Transfermarkt, StatsBomb)
- [ ] Montar dashboards em Power BI com análise tática e de performance

---

## 📎 Observações

> Este é meu primeiro projeto público de futebol analytics.  
> Estou estruturando um pipeline completo, desde o scraping até a modelagem analítica.  
> A documentação do processo faz parte da minha migração para a área de dados esportivos.  
> Feedbacks, colaborações e conexões são bem-vindas!

---

## 📬 Contato

**Lucas Scalioni de Souza**  
[LinkedIn](https://www.linkedin.com/in/lucas-scalioni-de-souza-7b1537138)  
📧 lucasscalioni@gmail.com
