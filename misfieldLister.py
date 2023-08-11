import os
import json
series = "2021-22/NEDAFG"

for match in os.listdir(series):
    f = os.path.join(series,match)
    jsonfile = open(f)
    print(f)
    data = json.load(jsonfile)
    for inning in data["innings"]:
        for over in inning["overs"]:
            for delivery in over["deliveries"]:
                if "misfield" in delivery:
                    print(inning["team"],over["over"],delivery["misfield"]["type"],delivery["misfield"]["fielders"][0]["name"])
    jsonfile.close()