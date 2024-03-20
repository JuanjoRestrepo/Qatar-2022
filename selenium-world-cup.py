from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

#path = 'C:\Users\Juan Jose Restrepo\Desktop\WC 2022\chromedriver-win64\chromedriver.exe'
path = 'chromedriver-win64\chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

def getMissingData(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    print(f'\nGetting the Matches of WC {year}')

    # NODO PADRE: CUBRE LOCAL Y VISITANTE: <tr itemprop="name"> <th class="fhome" itemprop="homeTeam" itemscope="" itemtype="http://schema.org/SportsTeam"><span itemprop="name"><a href="/wiki/Italy_national_football_team" title="Italy national football team">Italy</a><span class="flagicon">&nbsp;<span class="mw-image-border" typeof="mw:File"><span><img alt="" src="//upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/23px-Flag_of_Italy.svg.png" decoding="async" width="23" height="15" class="mw-file-element" srcset="//upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/35px-Flag_of_Italy.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/45px-Flag_of_Italy.svg.png 2x" data-file-width="1500" data-file-height="1000"></span></span></span></span></th><th class="fscore">0–0</th><th class="faway" itemprop="awayTeam" itemscope="" itemtype="http://schema.org/SportsTeam"><span itemprop="name"><span style="white-space:nowrap"><span class="flagicon"><span class="mw-image-border" typeof="mw:File"><span><img alt="" src="//upload.wikimedia.org/wikipedia/en/thumb/1/12/Flag_of_Poland.svg/23px-Flag_of_Poland.svg.png" decoding="async" width="23" height="14" class="mw-file-element" srcset="//upload.wikimedia.org/wikipedia/en/thumb/1/12/Flag_of_Poland.svg/35px-Flag_of_Poland.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/1/12/Flag_of_Poland.svg/46px-Flag_of_Poland.svg.png 2x" data-file-width="1280" data-file-height="800"></span></span>&nbsp;</span><a href="/wiki/Poland_national_football_team" title="Poland national football team">Poland</a></span></span></th></tr>
    # <th class="fhome" itemprop="homeTeam" itemscope="" itemtype="http://schema.org/SportsTeam"><span itemprop="name"><a href="/wiki/Italy_national_football_team" title="Italy national football team">Italy</a><span class="flagicon">&nbsp;<span class="mw-image-border" typeof="mw:File"><span><img alt="" src="//upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/23px-Flag_of_Italy.svg.png" decoding="async" width="23" height="15" class="mw-file-element" srcset="//upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/35px-Flag_of_Italy.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/45px-Flag_of_Italy.svg.png 2x" data-file-width="1500" data-file-height="1000"></span></span></span></span></th>

    #//th[@class="fhome"]/.. <th class="fhome" itemprop="homeTeam" itemscope="" itemtype="http://schema.org/SportsTeam"><span itemprop="name"><a href="/wiki/Brazil_national_football_team" title="Brazil national football team">Brazil</a><span class="flagicon">&nbsp;<span class="mw-image-border" typeof="mw:File"><span><img alt="" src="//upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flag_of_Brazil_%281968%E2%80%931992%29.svg/22px-Flag_of_Brazil_%281968%E2%80%931992%29.svg.png" decoding="async" width="22" height="15" class="mw-file-element" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flag_of_Brazil_%281968%E2%80%931992%29.svg/33px-Flag_of_Brazil_%281968%E2%80%931992%29.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Flag_of_Brazil_%281968%E2%80%931992%29.svg/43px-Flag_of_Brazil_%281968%E2%80%931992%29.svg.png 2x" data-file-width="720" data-file-height="504"></span></span></span></span></th>

    # Find all rows containing match information
    # obtenemos los partidos en la pagina web
    driver.get(web)
    matches = driver.find_elements(by='xpath', value='//th[@class="fhome"]/.. | //td[@align="right"]/.. | //td[@style="text-align:right;"]/..')

    # guardamos los datos de los partidos en las listas 
    home = []
    score = []
    away = []

    # Recorremos los partidos guardados para separarlos en local, visitante y resultado
    for match in matches:
        home.append(match.find_element(by='xpath', value='./th[1]').text)
        score.append(match.find_element(by='xpath', value='./th[2]').text)
        away.append(match.find_element(by='xpath', value='./th[3]').text)

    # Creamos un DataFrame a partir de las listas
    data = {'Home': home, 'Score': score, 'Away': away}
    df_football = pd.DataFrame(data)
    df_football['year'] = year
    time.sleep(2)
    
    return df_football



years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]

# Guardamos todos los df de los mundiales en una lista
fifa = [getMissingData(year) for year in years]
# Close the WebDriver
driver.quit()

# Juntamos todos los df en uno solo
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv('fifa_worldcup_missing_data.csv', index=False)

print('Web Scraping Done!')