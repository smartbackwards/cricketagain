import os
import json

bigDictionary = {}
csvfile = open("playersCSV.csv")
for player in csvfile:
    player = player.rstrip("\n")
    player = player.split(",")
    if player[4]!="bat_role":
        bigDictionary[player[0]] = {
            "battingRole":player[4],
            "battingHand":player[5],
            "bowlingRole":player[7],
            "team":player[9],
            "battingAmounts": {
                "vsSpin": [0,0,0],
                "vsPace": [0,0,0]
            },
            "bowlingAmounts": {
                "vsRH": [0,0,0],
                "vsLH": [0,0,0]
            }
    }
csvfile.close()

def addToDictionaries(batter,bowler,phase):
    batterHand = bigDictionary[batter]["battingHand"]
    bowlerType = bigDictionary[bowler]["bowlingRole"]
    if batterHand=="right":
        bigDictionary[bowler]["bowlingAmounts"]["vsRH"][phase]+=1
    else:
        bigDictionary[bowler]["bowlingAmounts"]["vsLH"][phase]+=1
        
    if bowlerType=="spin":
        bigDictionary[batter]["battingAmounts"]["vsSpin"][phase]+=1
    else:
        bigDictionary[batter]["battingAmounts"]["vsPace"][phase]+=1



for season in os.listdir("match-data"):
    for series in os.listdir(os.path.join("match-data", season)):
        for game in os.listdir(os.path.join("match-data",season,series)):
            f=os.path.join("match-data",season,series,game)
            jsonfile = open(f)
            data=json.load(jsonfile)
            jsonfile.close()
            
            for inning in data["innings"]:
                if "super_over" in inning:
                    for over in inning["overs"]:
                        for delivery in over["deliveries"]:
                            batter = delivery["batter"]
                            bowler = delivery["bowler"]
                            addToDictionaries(batter,bowler,2)
                else:
                    phaseBeginnings=[]
                    phaseEndings=[]
                    for phase in inning["powerplays"]:
                        phaseBeginnings.append(phase["from"])
                        phaseEndings.append(phase["to"])
                    phase=0
                    overNo=0
                    justChanged=False
                    for over in inning["overs"]:
                        deliveryNo=1
                        for delivery in over["deliveries"]:
                            batter = delivery["batter"]
                            bowler = delivery["bowler"]
                            addToDictionaries(batter,bowler,phase)                            
                            
                            if justChanged:
                                if not (str(phaseBeginnings[phase])==str(overNo)+"."+str(deliveryNo)):
                                    print(f,phaseBeginnings[phase], str(overNo),str(deliveryNo))
                                justChanged=False
                            if str(phaseEndings[phase])==str(overNo)+"."+str(deliveryNo):
                                #print(phaseEndings[phase])
                                phase+=1
                                justChanged=True


                            deliveryNo+=1
                        overNo+=1
                        
amountFile = open("ballAmounts.csv","w")

                    
for player in bigDictionary:
    st=""
    st+=player+";"
    for thing in bigDictionary[player]:
        if thing=="bowlingAmounts" or thing=="battingAmounts":
            for splits in bigDictionary[player][thing]:
                for amount in bigDictionary[player][thing][splits]:
                    st+=str(amount)+";"
#                   print(bigDictionary[player][thing][splits][amount])
        else:
            st+=str(bigDictionary[player][thing])+";"
    st+="\n"
    amountFile.write(st)
#    print(player,bigDictionary[player])