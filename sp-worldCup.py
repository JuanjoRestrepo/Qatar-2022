from bs4 import BeautifulSoup
import requests
import pandas as pd

# Extraemos la data de todos los mundiales desde 1930 hasta 2018
# Haremos el Webscrapping para obtener estos datos con 'requests' y bs4
years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]

def get_matches(year):
  if year == '2022':
    web =  f'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
  else:
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

  response = requests.get(web)
  content = response.text #contenido html de la pagina
  soup = BeautifulSoup(content, 'lxml')

  matches = soup.find_all('div', class_='footballbox')

  home = []
  score = []
  away = []

  for game in matches:
      home.append(game.find('th', class_='fhome').get_text())
      score.append(game.find('th', class_='fscore').get_text())
      away.append(game.find('th', class_='faway').get_text())

  dict_football = {'home': home,
                  'score': score,
                  'away': away}

  df_football = pd.DataFrame(dict_football)
  df_football['year'] = year
  return df_football

# Data Historica de todos los mundiales realizados
#fifa = [get_matches(year) for year in years]
#df_fifa = pd.concat(fifa, ignore_index=True)
#df_fifa.to_csv('fifa_worldcup_historical_data.csv', index=False)

# Data del mundial Qatar 2022
#df_fixture = get_matches('2022')
#df_fixture = df_fixture
#df_fixture.to_csv('fifa_worldcup_fixture.csv', index=False)

df1990 = get_matches('1990')
df1990.to_csv('WC_1990.csv', index=False)