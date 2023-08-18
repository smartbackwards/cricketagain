""" 
batter:
[0,1,2,3,4,6]
W = bowled, lbw
CATCH! = WKc, c&b, c,
RUN OUT? = WKro, bro, ro,
STUMPED?
Extras: Leg byes

bowler:
[0,1,2,3,4,6]
W = bowled, lbw
CATCH! = WKc, c&b, c,
RUN OUT? = WKro, bro, ro,
STUMPED?
Extras: Wides,No balls

"""

import os
import json



bigDictionary = {}
csvfile = open("playersCSV.csv")
for player in csvfile:
    player = player.rstrip("\n")
    player = player.split(",")
    role = player[4]
    if player[3]=="Batting allrounder" or player[3]=="Bowling allrounder":
        role=player[3]
    if player[4]!="bat_role":
        bigDictionary[player[0]] = {
            "battingRole":role,
            "battingHand":player[5],
            "bowlingRole":player[7],
            "team":player[9],
            #0s,1s,2s,3s,4s,6s,catches,runouts,stumpeds,bld,lbw,1lb,2lb,4lb,undefined
            "BatVsSpin":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "BatVsPace":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            #0s,1s,2s,3s,4s,6s,catches,runouts,stumpeds,bld,lbw,wd,nb,byes,undefined
            "BowlVsRHB":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "BowlVsLHB":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    }

#
csvfile.close()

def addToList(delivery):
    batter = delivery["batter"]
    bowler = delivery["bowler"]
    bowlerType = bigDictionary[bowler]["bowlingRole"]
    batterHandedness = bigDictionary[batter]["battingHand"]
    
    if bowlerType=="spin":
        activeBattingList=bigDictionary[batter]["BatVsSpin"]
    else:
        activeBattingList=bigDictionary[batter]["BatVsPace"]
    
    if batterHandedness=="right":
        activeBowlingList=bigDictionary[bowler]["BowlVsRHB"]
    else:
        activeBowlingList=bigDictionary[bowler]["BowlVsLHB"]
    
    runs = delivery["runs"]["batter"]
    if "non_boundary" in delivery["runs"] or delivery["runs"]["batter"]==5:
        runs = runs-4
    
    batLists=[]
    bowlLists=[]
        
    if ("wickets" not in delivery) and ("misfield" not in delivery) and ("extras" not in delivery):
        if runs<6:
            batLists.append(runs)
            bowlLists.append(runs)
        else:
            batLists.append(5)
            bowlLists.append(5)
        
    
    if "wickets" in delivery:
        wkts = delivery["wickets"]
        for wkt in wkts:
            kind=wkt["kind"]
            if kind=="caught" or kind=="caught and bowled":
                batLists.append(6)
                bowlLists.append(6)            
            elif kind=="run out":
                batLists.append(7)
                bowlLists.append(7)
                if "extras" in delivery:
                    if "wides" in delivery["extras"]:
                        pass
                    else:
                        if runs<6:
                            batLists.append(runs)
                            bowlLists.append(runs)
                        else:
                            batLists.append(5)
                            bowlLists.append(5)          
                else:
                    if runs<6:
                        batLists.append(runs)
                        bowlLists.append(runs)
                    else:
                        batLists.append(5)
                        bowlLists.append(5)
            elif kind=="stumped":
                batLists.append(8)
                bowlLists.append(8)
            elif kind=="bowled":
                batLists.append(9)
                bowlLists.append(9)
            elif kind=="lbw":
                batLists.append(10)
                bowlLists.append(10)
            else:
                batLists.append(14)
                bowlLists.append(14)
    
    if "misfield" in delivery:
        kind = delivery["misfield"]["type"]
        if runs<6:
            batLists.append(runs)
            bowlLists.append(runs)
        else:
            batLists.append(5)
            bowlLists.append(5)
        if kind=="caught":
            batLists.append(6)
            bowlLists.append(6)
        elif kind=="run out":
            batLists.append(7)
            bowlLists.append(7)
        elif kind=="stumping":
            batLists.append(8)
            bowlLists.append(8)
    
    if "extras" in delivery:
        if "wides" in delivery["extras"]:
            bowlLists.append(11)
        elif "noballs" in delivery["extras"]:
            if runs<6:
                batLists.append(runs)
                bowlLists.append(runs)
            else:
                batLists.append(5)
                bowlLists.append(5)

            bowlLists.append(12)
        elif "byes" in delivery["extras"]:
            batLists.append(0)
            bowlLists.append(13)
        elif "legbyes" in delivery["extras"]:
            if delivery["extras"]["legbyes"]==1:
                batLists.append(11)
            elif delivery["extras"]["legbyes"]==4:
                batLists.append(12)
            else:
                batLists.append(13)
                

        
    for b in batLists:
        activeBattingList[b]+=1
    for b in bowlLists:
        activeBowlingList[b]+=1
        
    
        

fiveCounter=0
nonBoundary4Counter=0
nonBoundary6Counter=0

extraDictionary={
    "wides": {},
    "legbyes": {},
    "noballs": {},
    "byes": {}
}

def extraParser(delivery,_type):
    if _type in delivery["extras"]:
        runamount=str(delivery["extras"][_type])
        if runamount not in extraDictionary[_type]:
            extraDictionary[_type][runamount]=1
        else:
            extraDictionary[_type][runamount]+=1
    

for season in os.listdir("match-data"):
    for series in os.listdir(os.path.join("match-data", season)):
        for game in os.listdir(os.path.join("match-data",season,series)):
            f=os.path.join("match-data",season,series,game)
            jsonfile = open(f)
            data=json.load(jsonfile)
            jsonfile.close()
            
            for inning in data["innings"]:
                for over in inning["overs"]:
                    for delivery in over["deliveries"]:
                        addToList(delivery)
                        if "extras" in delivery:
                            extraParser(delivery,"legbyes")
                            extraParser(delivery,"wides")
                            extraParser(delivery,"byes")
                            extraParser(delivery,"noballs")
                                            
                        
                        if "non_boundary" in delivery["runs"]:
                            if delivery["runs"]["batter"]==4:
                                nonBoundary4Counter+=1
                            elif delivery["runs"]["batter"]==6:
                                nonBoundary6Counter+=1
                            else:
                                print(delivery["runs"]["batter"],"non boundary")
                        if delivery["runs"]["batter"]==5:
                            fiveCounter+=1
print(f"Fives: {fiveCounter}, non boundary 4s: {nonBoundary4Counter}, non boundary 6s: {nonBoundary6Counter}")

# for ex in extraDictionary:
#     print(ex, extraDictionary[ex])
rolePaceDict = {
    "batter": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Batting allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Bowling allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "bowler": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
}
roleSpinDict = {
    "batter": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Batting allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "Bowling allrounder": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "bowler": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
}

for bat in bigDictionary:
    _type = bigDictionary[bat]["battingRole"]
    for i in range(len(bigDictionary[bat]["BatVsSpin"])):
        roleSpinDict[_type][i]+=bigDictionary[bat]["BatVsSpin"][i]
        
    for i in range(len(bigDictionary[bat]["BatVsPace"])):
        rolePaceDict[_type][i]+=bigDictionary[bat]["BatVsPace"][i]

for x in roleSpinDict:
    print(roleSpinDict[x])