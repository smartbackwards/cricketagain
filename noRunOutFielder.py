import os
import json


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
                        if "wickets" in delivery:
                            wkttype=delivery["wickets"][0]["kind"]
                            if wkttype=="run out":
                                # print(delivery["wickets"][0])
                                if "fielders" not in delivery["wickets"][0]:
                                    print(f)
                                