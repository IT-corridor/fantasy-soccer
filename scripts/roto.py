import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import csv

def read_csv(filename=None):
    with open('FanDuel-FIFA-2018-06-15-26260-players-list.csv') as f:
        return [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

def text2file(text):
    f = open('lineup.csv', 'a')
    f.write('%s\n'% text)
    f.close()


def main():
    dp = "https://www.rotowire.com/daily/soccer/optimizer.php"

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.2228.0 Safari/537.36'})

    r = session.get(dp)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")

        # soup = BeautifulSoup(html, "html.parser")

        table = soup.find("div", {"id":"rwo-poolbox"})
        player_rows = table.find("tbody", {"id":"players"})
        players = player_rows.find_all("tr")

        # keep track of total salary so we can get an average later
        tot_salary = 0

        # build a list of player dictionaries
        fwd_list = []
        mid_list = []
        def_list = []
        gk_list = []

        csv_fields = ['player_name', 'player_team', 'player_opp', 'player_pos', 'player_lineupslot', 'player_wo', 
                      'player_es', 'player_salary', 'player_points', 'player_value']
        with open('roto.csv', 'w') as f:
            result_csv = csv.DictWriter(f, fieldnames=csv_fields)
            result_csv.writeheader()            
            
            for player in players:
                player_dic = {}
                player_dic['player_name'] = player.find("td", {"class":"rwo-name"}).text.strip().replace('\n',' ')
                player_dic['player_team'] = player.find("td", {"class":"rwo-team"}).text
                player_dic['player_opp'] = player.find("td", {"class":"rwo-opp"}).text
                player_dic['player_pos'] = player.find("td", {"class":"rwo-pos"}).get('data-li')
                player_dic['player_lineupslot'] = player.find("td", {"class":"rwo-lineupslot"}).text
                player_dic['player_wo'] = float(player.find("td", {"class":"rwo-wo"}).get('data-wo').replace('%',''))
                player_dic['player_es'] = player.find("td", {"class":"rwo-es"}).get('data-es')
                player_dic['player_salary'] = int(player.find("td", {"class":"rwo-salary"}).get('data-salary').replace(",",""))
                player_dic['player_points'] = float(player.find("td", {"class":"rwo-points"}).get('data-points'))
                player_dic['player_value'] = float(player.find("td", {"class":"rwo-value"}).text)
                # only count them if points are greater than 0
                # if player_dic['player_points'] > 0:
                #     tot_salary += player_dic['player_salary']
                #     if player_dic['player_pos'] == 'F':
                #         fwd_list.append(player_dic)
                #     elif player_dic['player_pos'] == 'M':
                #         mid_list.append(player_dic)
                #     elif player_dic['player_pos'] == 'D':
                #         def_list.append(player_dic)
                #     elif player_dic['player_pos'] == 'GK':
                #         gk_list.append(player_dic)
                result_csv.writerow(player_dic)
        return
        average_salary = tot_salary/(len(fwd_list)+len(mid_list)+len(def_list)+len(gk_list))
        # forward from a good team so they get a lot of action
        sorted_fwd_list = sorted(fwd_list, key=lambda k: k['player_wo'], reverse=True)
        # mid should have a good all around mix
        sorted_mid_list = sorted(mid_list, key=lambda k: k['player_wo'], reverse=True)
        # defender from a not so good team so he gets a lot of action
        sorted_def_list = sorted(def_list, key=lambda k: k['player_wo'])
        # sort the goalie to the best value
        sorted_gk_list = sorted(gk_list, key=lambda k: k['player_value'], reverse=True)

        # need to fill 8 players
        # FWD, FWD, MID, MID, MID, DEF, DEF, GK
        # F = FWD
        # M = MID
        # D = DEF 
        # G = GK
        # 60,000 salary cap
        # 4 players max from 1 team

        # keep track of the lineup
        lineup = []
        # track the total salary
        salary=0
        # track the count of players on a team
        team_cnt = {}
        # keep count of the players
        fwd_cnt = 0
        mid_cnt = 0
        def_cnt = 0
        gk_cnt = 0
        # select some forwards
        for player in sorted_fwd_list:
            if fwd_cnt < 2:
                if player['player_salary']/average_salary < 1.2:
                    if player['player_team'] not in team_cnt:
                        team_cnt[player['player_team']] = 1
                    if team_cnt[player['player_team']] < 4:
                        team_cnt[player['player_team']] += 1
                        lineup.append(player)
                        salary += player['player_salary']
                        fwd_cnt += 1
        # select some mids
        for player in sorted_mid_list:
            if mid_cnt < 3:
                if player['player_salary']/average_salary < 1.2:
                    if player['player_team'] not in team_cnt:
                        team_cnt[player['player_team']] = 1
                    if team_cnt[player['player_team']] < 4:
                        team_cnt[player['player_team']] += 1
                        lineup.append(player)
                        salary += player['player_salary']
                        mid_cnt += 1
        # select some defenders
        for player in sorted_def_list:
            if def_cnt < 2:
                if player['player_salary']/average_salary < 1.2:
                    if player['player_team'] not in team_cnt:
                        team_cnt[player['player_team']] = 1
                    if team_cnt[player['player_team']] < 4:
                        team_cnt[player['player_team']] += 1
                        lineup.append(player)
                        salary += player['player_salary']
                        def_cnt += 1
        # select the goalie
        for player in sorted_gk_list:
            if gk_cnt < 1:
                if player['player_salary']/average_salary < 1.2:
                    if player['player_team'] not in team_cnt:
                        team_cnt[player['player_team']] = 1
                    if team_cnt[player['player_team']] < 4:
                        team_cnt[player['player_team']] += 1
                        lineup.append(player)
                        salary += player['player_salary']
                        gk_cnt += 1

        fd_dict = read_csv()

        output = ""
        for player in lineup:
            fdid = None
            print('%s (%s), %s, %s'% (player['player_name'], player['player_pos'], player['player_team'], player['player_opp']))
            # get the fanduel id
            name_list = player['player_name'].split(' ')
            for item in fd_dict:
                if player['player_name'] in item['Nickname']:
                    print(item['Id'])
                    fdid = item['Id']
                elif name_list[0] in item['First Name'] and name_list[-1] in item['Last Name']:
                    print(item['Id'])
                    fdid = item['Id']
            output += "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'\n"% (fdid,
            player['player_name'],
            player['player_team'],
            player['player_opp'],
            player['player_pos'],
            player['player_lineupslot'],
            player['player_wo'],
            player['player_es'],
            player['player_salary'],
            player['player_points'],
            player['player_value'])

        text2file(output)


main()
