import os
import json
import pandas as pd

kcFile = open("keeperscaptains.csv")
keeperDict = {} #{"Series":[[keeper1,keeper2],[keeper1,keeper2]]}

tempKeeper = {}
for line in kcFile:
    line = line.rstrip("\n")
    splitLine=line.split(",")
    seriesSlash = splitLine[5]+"/"+splitLine[0]
    if seriesSlash not in keeperDict:
        keeperDict[seriesSlash] = []

    
    if tempKeeper !={}:
        tempKeeper[splitLine[2]]=splitLine[4]
        keeperDict[seriesSlash].append(tempKeeper)
        tempKeeper={}
    else:
        tempKeeper[splitLine[2]]=splitLine[4]



fieldersDict = {}

catchCounter=0

datafolder = "match-data"
for season in os.listdir(datafolder):
    for series in os.listdir(os.path.join(datafolder,season)):
        gameCounter=0
        for game in os.listdir(os.path.join(datafolder,season,series)):
            f=os.path.join(datafolder,season,series,game)
            jsonfile=open(f)
            data = json.load(jsonfile)
            teamsPlaying = data["info"]["teams"]



            for inning in data["innings"]:
                if teamsPlaying[0]==inning["team"]:
                    bowlingTeam=teamsPlaying[1]
                else:
                    bowlingTeam=teamsPlaying[0]

                idString = season+"/"+series
                keeper = keeperDict[idString][gameCounter][bowlingTeam]
                if keeper not in data["info"]["players"][bowlingTeam]:
                    print(f"issue:{f}: {keeper} not found")
                for over in inning["overs"]:
                    for delivery in over["deliveries"]:
                        if "wickets" in delivery:
                            kind = delivery["wickets"][0]["kind"]
                            fielders = []
                            if "fielders" in delivery["wickets"][0]:
                                for fielder in delivery["wickets"][0]["fielders"]:
                                    fielders.append(fielder["name"])

                                for fielder in fielders:
                                    if fielder not in fieldersDict:
                                        fieldersDict[fielder] = {"caught":0,"caughtAndBowled":0,"runOut":0,"stumping":0,
                                                                 "wkCaught":0,"wkRunOut":0,"wkDropped":0,"wkMissedRunOut":0,
                                                                 "runOutAndBowled":0, "missedRunOutAndBowled":0,
                                                                 "dropped":0, "droppedAndBowled":0, "missedRunOut":0,"missedStumping":0}
                                    
                                    if kind=="caught":
                                        if fielder==keeper:
                                            fieldersDict[fielder]["wkCaught"]+=1
                                        else:
                                            fieldersDict[fielder]["caught"]+=1
                                    if kind=="caught and bowled":
                                        fieldersDict[fielder]["caughtAndBowled"]+=1
                                    if kind=="run out":
                                        if fielder==delivery["bowler"]:
                                            fieldersDict[fielder]["runOutAndBowled"]+=1
                                        elif fielder==keeper:
                                            fieldersDict[fielder]["wkRunOut"]+=1
                                        else:
                                            fieldersDict[fielder]["runOut"]+=1
                                    if kind=="stumped":
                                        if fielder!=keeper:
                                            print(f"non keeper stumping {f} wtf: {fielder}, {keeper}")
                                        fieldersDict[fielder]["stumping"]+=1

                

                        if "misfield" in delivery:
                            kind = delivery["misfield"]["type"]
                            fielder = delivery["misfield"]["fielders"][0]["name"]

                            if fielder not in fieldersDict:
                                fieldersDict[fielder] = {"caught":0,"caughtAndBowled":0,"runOut":0,"stumping":0,
                                                                 "wkCaught":0,"wkRunOut":0,"wkDropped":0,"wkMissedRunOut":0,
                                                                 "runOutAndBowled":0, "missedRunOutAndBowled":0,
                                                                 "dropped":0, "droppedAndBowled":0, "missedRunOut":0,"missedStumping":0}
                                
                            if kind == "caught":
                                if fielder == delivery["bowler"]:
                                    fieldersDict[fielder]["droppedAndBowled"]+=1
                                elif fielder == keeper:
                                    fieldersDict[fielder]["wkDropped"]+=1
                                else:
                                    fieldersDict[fielder]["dropped"]+=1
                            elif kind=="run out":
                                if fielder==delivery["bowler"]:
                                    fieldersDict[fielder]["missedRunOutAndBowled"]+=1
                                elif fielder==keeper:
                                    fieldersDict[fielder]["wkMissedRunOut"]+=1
                                else:
                                    fieldersDict[fielder]["missedRunOut"]+=1
                            elif kind=="stumping":
                                if fielder!=keeper:
                                    print(f"non keeper stumping {f} wtf: {fielder}")
                                fieldersDict[fielder]["missedStumping"]+=1

            gameCounter+=1
            jsonfile.close()

#print(fieldersDict)