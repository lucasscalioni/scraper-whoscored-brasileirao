# ⚽ WhoScored Brasileirão Scraper – Player Stats Automation (2024 & 2025)

🚧 **Status:** In progress – data collection automated, dashboard in development

## 📌 Project Goal

This project aims to automate the collection of detailed player performance statistics from the Brazilian Série A (Brasileirão), using WhoScored.com as the data source. The goal is to structure the data in a format suitable for scouting analysis, performance tracking, and advanced visualization in Power BI.

## 🛠 Tools & Technologies

- Python
- Selenium + BeautifulSoup
- Pandas
- Power BI
- CSV / TXT file handling

## 📈 What’s been done so far

- ✅ Automated scraping of all available match URLs from Brasileirão 2024 (380+ games)
- ✅ Script for collecting player statistics per match (17,000+ rows)
- ✅ Dataset includes stats such as:
  - `Name`, `Age`, `Position`, `Shots`, `SoT`, `KeyPasses`, `PassAccuracy`, `AerialsWon`, `Touches`, `Rating`
  - `TackleWon`, `Interception`, `Clearance`, `ShotBlocked`, `Fouls`, `Dispossessed`, `Turnover`, etc.
  - Match context: `Opponent`, `Home/Away`, `Date`, `Minutes played`

## 📂 Project Structure (initial)

## 📊 Next Steps

- [ ] Enrich data with goals and assists
- [ ] Create robust player ID (to handle transfers, age changes, position swaps)
- [ ] Build interactive dashboards in Power BI
- [ ] Extend to team-level and match-level statistics
- [ ] Publish insights and visualizations

## 📎 Notes

> This is my first football analytics project and is part of my transition from general data analytics to sports data science.  
> I’m learning in public and sharing progress as I go — feedback is welcome!

## 📬 Contact

**Lucas Scalioni de Souza**  
[LinkedIn](https://www.linkedin.com/in/lucas-scalioni-de-souza-7b1537138)  
Email: lucasscalioni@gmail.com
