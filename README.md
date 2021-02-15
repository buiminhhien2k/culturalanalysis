# Cultural Index analysis
This project is inspired by from one of my studying assignment with Lapland University of Applied Science (my home university)

**Data and Sources:**
- `data/6-dimensions-for-website-2015-08-16.xls` aka *`culturalMetrics`* in code file, source: https://geerthofstede.com/research-and-vsm/dimension-data-matrix/
  - *Description*: containing 6 metrics indicate the culture of a countries [`pdi`,	`idv`,	`mas`,	`uai`,	`ltowvs`,	`ivr`]
- `data/commonBorderIntbyCountryandBorderingCountryA.csv` aka *`borderingCountry`* in code file, source: https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders
  - *Description*: listing all the adjacent/neighbouring countries of a country.
  
**Process:**
- fill the missing index in *`culturalMetrics`* by calculate the average index of the adjacent countries in *`borderingCountry`*
- then visualize data based on the total difference in cultural indexes

**Product:**
- You can choose your country and see the countries having the closest culture to your chosen one (Map shows all countries in the dataset and Table shows top 5 countries)
- You can change the color of the countries in the map.
- You can change the color of the background in the map.

**What I learn:**
- **Data manipulation methods** with DataFrame in Python Pandas.
- Dash and Plotly package to create an interactive web-based **dashboard**.
- **CSS** to beautify the website.

**How to use:**
- clone this remote to your local machine (Laptop/PC): ``
