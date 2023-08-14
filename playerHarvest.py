import os
import json

seasons = ["2019", "2019-20", "2020", "2020-21", "2021", "2021-22", "2022", "2022-23","2023"]

playerdict = {}

for season in seasons:
    for series in os.listdir(season):
        for game in os.listdir(os.path.join(season,series)):
            f=os.path.join(season,series,game)
            jsonfile=open(f)
            data = json.load(jsonfile)
            for team in data["info"]["players"]:
                if team not in playerdict:
                    playerdict[team]={}
                for player in data["info"]["players"][team]:
                    if player not in playerdict[team]:
                        playerdict[team][player]=1
                    else:
                        playerdict[team][player]+=1          
            
            jsonfile.close()
for team in playerdict:
    f=open("Players/"+str(team)+".txt", "w")
    for player in playerdict[team]:
        finalstr=player+";"+str(playerdict[team][player])+"\n"
        f.write(finalstr)    
    
    f.close()