# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 01:14:53 2019

@author: Kuro Azai
"""


from bs4 import BeautifulSoup
import urllib3
import re
http = urllib3.PoolManager()
urllib3.disable_warnings()


def opgg(user):
    url = 'https://euw.op.gg/summoner/userName='
    response = http.request('GET', url + user)
    soup = BeautifulSoup(response.data, "html.parser")

    Champ_Div = soup.find_all("div", class_="ChampionBox Ranked")
    Wins = soup.find_all("span", class_="wins")
    Losses = soup.find_all("span", class_="Losses")
    WinRatio = soup.find_all("span", class_="winratio")

    Champions = []
    for div in Champ_Div:
        for y in div:
            # print(y)
            Champ = re.findall('img alt="([^"]*)"', str(y))
            Win_Ratio = re.findall('title>([^"]*)%', str(y))

            # print(result, len(result))
            if len(Champ) != 0:
                Champions.append(Champ)
                print(Champ, Win_Ratio)

    results = [Champions, Wins, Losses, WinRatio]
    print(url + user)
    return results
