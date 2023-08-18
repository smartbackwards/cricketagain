import pandas as pd
import os
import json


batterList=[]
bowlerList=[]
batterRuns=[]
wides=[]
noballs=[]
legbyes=[]
byes=[]
misfieldTypes=[]
misfieldFielders=[]
wicketTypes=[]
wicketFielders=[]
nonBoundaries=[]
phases=[]
keepers=[]

def addToLists(delivery,phase,keeper):
    batterList.append(delivery["batter"])
    bowlerList.append(delivery["bowler"])
    batterRuns.append(delivery["runs"]["batter"])
    
    wd=0
    nb=0
    lb=0
    b=0
    if "extras" in delivery:
        wd = 0 if "wides" not in delivery["extras"] else delivery["extras"]["wides"] 
        nb = 0 if "noballs" not in delivery["extras"] else delivery["extras"]["noballs"]
        lb = 0 if "legbyes" not in delivery["extras"] else delivery["extras"]["legbyes"]
        b = 0 if "byes" not in delivery["extras"] else delivery["extras"]["byes"] 

    wides.append(wd)
    noballs.append(nb)
    legbyes.append(lb)
    byes.append(b)
    msft = "" if "misfield" not in delivery else delivery["misfield"]["type"]
    msff = "" if "misfield" not in delivery else delivery["misfield"]["fielders"][0]["name"]
    misfieldTypes.append(msft)
    misfieldFielders.append(msff)
    

    wktt = ""
    wktf = ""
    if "wickets" in delivery:
        wktt = delivery["wickets"][0]["kind"]
        if "fielders" in delivery["wickets"][0]:
            wktf = delivery["wickets"][0]["fielders"][0]["name"]

                                    


    wicketTypes.append(wktt)
    wicketFielders.append(wktf)
    nonboundary=""
    if "non_boundary" in delivery["runs"]:
        nonboundary="true"
    nonBoundaries.append(nonboundary)
    phases.append(phase+1)
    keepers.append(keeper)

def create_wk_dict():
    keeperDict={}
    f=open("keeperscaptains.csv","r")
    firstOne=True
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        series_id=line[5]+"/"+line[0]
        
        if series_id not in keeperDict:
            keeperDict[series_id]=[]
        if firstOne:
            tempdct = {line[2]:line[4]}
            firstOne=False
        else:
            tempdct[line[2]]=line[4]
            keeperDict[series_id].append(tempdct)
            tempdct={}
            firstOne=True
    return keeperDict
    f.close()

keeperDict = create_wk_dict()


for season in os.listdir("match-data"):
    for series in os.listdir(os.path.join("match-data", season)):
        gameNo=0
        for game in os.listdir(os.path.join("match-data",season,series)):
            f=os.path.join("match-data",season,series,game)
            jsonfile = open(f)
            data=json.load(jsonfile)
            jsonfile.close()
            
            seriesid = str(season)+"/"+str(series)
            teamList = data["info"]["teams"]

            
            for inning in data["innings"]:
                battingTeam = inning["team"]
                if battingTeam==teamList[0]:
                    bowlingTeam=teamList[1]
                else:
                    bowlingTeam=teamList[0]

                keeper = keeperDict[seriesid][gameNo][bowlingTeam]

                if "super_over" in inning:
                    phase=2
                    for over in inning["overs"]:
                        for delivery in over["deliveries"]:
                            addToLists(delivery,phase,keeper)
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

                            addToLists(delivery,phase,keeper)                            
                            
                            if justChanged:
                                if not (str(phaseBeginnings[phase])==str(overNo)+"."+str(deliveryNo)):
                                    print(f,phaseBeginnings[phase], str(overNo),str(deliveryNo))
                                justChanged=False
                            if str(phaseEndings[phase])==str(overNo)+"."+str(deliveryNo):
                                
                                phase+=1
                                justChanged=True


                            deliveryNo+=1
                        overNo+=1
            gameNo+=1
                        
#print(wicketFielders)
         
dfData = {
    "batters":batterList,
    "bowlers":bowlerList,
    "phase":phases,
    "runs":batterRuns,
    "wides":wides,
    "noballs":noballs,
    "legbyes":legbyes,
    "byes":byes,
    "misfield_type": misfieldTypes,
    "misfield_fielder":misfieldFielders,
    "wicket_type":wicketTypes,
    "wicket_fielder":wicketFielders,
    "non_boundary":nonBoundaries,
    "keepers":keepers
}

df = pd.DataFrame(dfData)
df.to_csv("deliveriesData.csv")
                        
                        