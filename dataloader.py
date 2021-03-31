from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# install geckodriver
# https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path


def getNbaData(nba_urls: list):
    nba_data_list = list(map(lambda x: webScraper(x), nba_urls))
    data = dataProcessor(nba_data_list)
    fin = []
    for l in data:
        for sub_l in l:
            fin.append(sub_l)
            
    df = pd.DataFrame(data=fin, columns=['Season',
                                         'PlayerTeam',
                                         'GP',
                                         'W',
                                         'L',
                                         'Min',
                                         'DistFeet',
                                         'DistMiles',
                                         'DistMilesOff',
                                         'DistMilesDef',
                                         'AvgSpeed',
                                         'AvgSpeedOff',
                                         'AvgSpeedDef'])
    df.to_csv('./nba_stats.csv', encoding='utf-8',
              index=False, sep='|', header=True)
    return


def webScraper(url):
    print(url)
    # initialize web driver
    browser = webdriver.Firefox()

    # load the webpage
    browser.get(url)
    time.sleep(10)

    # modify webpage to all data
    select = Select(browser.find_element_by_class_name(
        'stats-table-pagination__select'))
    select.select_by_visible_text('All')

    # return table section
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = (soup.find('table', class_='table'))
    return table, str(url.split('https://www.nba.com/stats/players/speed-distance/?Season=')[1])[0:7]


def dataProcessor(data_list):

    def processingHelper(data_):
        data = data_[0]
        season = data_[1]
        cnt = 0
        year_data = []
        for i in list(str(data).split('<td class="player">')):
            cnt += 1
            if cnt == 1:
                continue
            else:
                name = str(i).split('Regular Season">')[1].replace('</a>', '')
                try:
                    name = str(' '.join(name.split(' ')[0:2]).split(
                        '<')[0]).strip('\n')
                except TypeError:
                    name = 'Unknown'
                iter_ = str(i).split('</td>')
                part_list = []
                if name == 'Unknown':
                    pass
                else:
                    for td in range(len(iter_)):
                        part_list.append(float(iter_[td][5:])) if ('-' not in iter_[td] and td not in [0, 1] and '</tr>' not in iter_[td] and len(iter_[td][5:]) > 0) else(
                            part_list.append(float(0)) if ('-' in iter_[td] and td not in [0, 1] and '</tr>' not in iter_[td] and len(iter_[td][5:]) > 0) else (
                                part_list.append(float(0)) if (td not in [0, 1] and '</tr>' not in iter_[td] and len(iter_[td][5:]) == 0) else None))
                    final_list = [season, name]
                    final_list.extend(part_list)
                    year_data.append(final_list)
        return year_data

    f_list = list(map(lambda x: processingHelper(x), data_list))
    output = f_list
    return output


if __name__ == '__main__':

    nba_urls = [
        'https://www.nba.com/stats/players/speed-distance/?Season=2020-21&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2019-20&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2018-19&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2017-18&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2016-17&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2015-16&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2014-15&SeasonType=Regular%20Season',
        'https://www.nba.com/stats/players/speed-distance/?Season=2013-14&SeasonType=Regular%20Season'
    ]

    getNbaData(nba_urls=nba_urls)
