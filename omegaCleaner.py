import os
import json

dir = "match-data/2023"

for series in os.listdir(dir):
    for game in os.listdir(os.path.join(dir,series)):
        f=os.path.join(dir,series,game)
        jsonfile=open(f)
        data = json.load(jsonfile)
        
        teams=[]
        for x in data["info"]["teams"]:
            teams.append(x)



        for inning in data["innings"]:

            battingTeam = inning["team"]

            if battingTeam==teams[0]:
                bowlingTeam=teams[1]
            else:
                bowlingTeam=teams[0]

            for over in inning["overs"]:
                for delivery in over["deliveries"]:
                    subFlag=False
                    fielder=""
                    if "misfield" in delivery:
                        fielder = delivery["misfield"]["fielders"][0]["name"]
                        if "substitute" in delivery["misfield"]["fielders"][0]:
                            subFlag=True

                    if fielder != "" and (not subFlag):
                        if fielder not in data["info"]["players"][bowlingTeam]:
                            print(f,fielder,bowlingTeam)
            



        jsonfile.close()