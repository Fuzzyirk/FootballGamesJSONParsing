import requests
from bs4 import BeautifulSoup
import time
import random
import json

URL = 'https://www.eurosport.ru/_ajax_/results_v8_5/results_teamsports_v8_5.zone?O2=1&langueid=15&domainid=144&mime=' \
      'text%2fxml&dropletid=160&sportid=22&revid=381&seasonid=333&SharedPageTheme=black&DeviceType=desktop&roundid={}'
season = {}


def get_html(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        print('не удалось подключиться')


def is_end(text):
    soup = BeautifulSoup(text, 'lxml')
    it_is_end = soup.find_all('div', class_='no-data-message')
    return len(it_is_end)


def write_json(data):
    with open("season.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def get_soup(text):
    soup = BeautifulSoup(text, 'lxml')
    matches = soup.find_all('div', class_='match')
    return matches


def get_dict(team_home, team_away, score, date):
    if team_home not in season:
        season[f'{team_home}'] = {f'{team_away}': {'Home': {'Score': score, 'Date': date}}}
        season[f'{team_away}'] = {f'{team_home}': {'Away': {'Score': score[::-1], 'Date': date}}}
    else:
        if team_away not in season[f'{team_home}']:
            season[f'{team_home}'][f'{team_away}'] = {'Home': {'Score': score, 'Date': date}}
            season[f'{team_away}'][f'{team_home}'] = {'Away': {'Score': score[::-1], 'Date': date}}
        else:
            season[f'{team_home}'][f'{team_away}']['Home'] = {'Score': score, 'Date': date}
            season[f'{team_away}'][f'{team_home}']['Away'] = {'Score': score[::-1], 'Date': date}


def get_matches(matches):
    for match in matches:
        teams = match.find_all('span', 'team__label')
        date = match.find_previous_sibling('div', class_='date-caption').text
        team_home = teams[0].text.strip()
        team_away = teams[1].text.strip()
        try:
            scores = match.find_all('div', class_='match__score-text')
            score = scores[0].text.strip() + '-' + scores[1].text.strip()
            print(team_home, ' - ', team_away, score, date)
        except Exception:
            score = ''
            match_time = match.find('div', class_='match__time')
            print(team_home, ' - ', team_away, match_time.text, date)
        get_dict(team_home, team_away, score, date)


def main():
    i = 5171
    while True:
        time.sleep(random.randint(1, 2))
        get_matches(get_soup(get_html(URL.format(str(i)))))
        if is_end(get_html(URL.format(str(i)))) != 0:
            print('Сезон окончен')
            break
        else:
            i += 1
            continue


if __name__ == '__main__':
    main()
    write_json(season)
