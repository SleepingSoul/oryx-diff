import requests
import json
import datetime
import re
from bs4 import BeautifulSoup


if __name__ == '__main__':
    russian_data = requests.get('https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html')

    soup = BeautifulSoup(russian_data.text, 'html.parser')

    tanks = soup.find_all('h3')[3]
    print(tanks)
    loss_dump = {'tanks': {}}
    lost_tanks_dump = loss_dump['tanks']
    list_of_tanks = tanks.next_sibling.next_sibling
    for tank_loss in list_of_tanks:
        tank_name = tank_loss.text.split(':')[0]
        #tank_name = tank_name[tank_name.find(' '):]
        losses = tank_loss.text[len(tank_name) + 2:].split('\xa0')

        overall_loss_number_str = str(re.findall(r'\d+', tank_name)[0])
        overall_loss_end = tank_name.find(overall_loss_number_str) + len(overall_loss_number_str)

        tank_name = tank_name[overall_loss_end + 1:]

        print(f'tank: {tank_name} losses: {losses}')
        lost_tanks_dump[tank_name] = losses

    now = datetime.datetime.utcnow()
    print(loss_dump)
    #with open(f'data_dumps/dump_{now.strftime("%m_%d_%Y_%H:%M:%S")}.json', 'w') as dump:
    with open('dump.json', 'w') as dump:
        json.dump(loss_dump, dump)
