import os
import json
import pandas as pd

df = pd.read_csv("deliveriesData.csv")
df = df[df.columns[1:]]

batters_df = pd.read_csv("playersCSV.csv")
batters_df.rename(columns = {'cricsheet_name':'batters',
                             'games':'bat_games',
                             'full name':'bat_full_name',
                             'team':'bat_team'
                             }, inplace = True)
batters_df = batters_df.drop(columns=['bowl_role_det', 'bowl_role', 'bowl_h','other'])

batdata_df = pd.merge(df,batters_df,on="batters")

bowlers_df = pd.read_csv("playersCSV.csv")
bowlers_df.rename(columns = {'cricsheet_name':'bowlers',
                             'games':'bwlr_games',
                             'full name':'bowl_full_name',
                             'team':'bowl_team'
                             }, inplace = True)
bowlers_df = bowlers_df.drop(columns=['bat_role_det', 'bat_role', 'bat_h','other'])

final_df = pd.merge(batdata_df,bowlers_df,on="bowlers")

def return_amounts(df_slice):  
    weight = len(df_slice)
    dots = len(df_slice.query("runs==0 and legbyes==0 and wides==0 and wicket_type.isnull() "))
    singles = len(df_slice.query("runs==1"))
    twos = len(df_slice.query("runs==2"))
    threes = len(df_slice.query("runs==3"))
    fours = len(df_slice.query("runs==4 and non_boundary.isnull()"))
    sixes = len(df_slice.query("runs==6 and non_boundary.isnull()"))
    
    non_bdry_fours = len(df_slice.query("runs==4 and not (non_boundary.isnull())"))
    non_bdry_sixes = len(df_slice.query("runs==6 and not (non_boundary.isnull())"))
    fives = len(df_slice.query("runs==5"))
    
    dots+=non_bdry_fours
    singles+=fives
    twos+=non_bdry_sixes
    
    total_catches = len(df_slice.query("wicket_type == 'caught' or wicket_type == 'caught and bowled' or misfield_type == 'caught'"))
    bowler_catches = len(df_slice.query("(wicket_type=='caught and bowled') or (misfield_type=='caught' and (misfield_fielder==bowlers))"))
    wk_catches = len(df_slice.query("(wicket_type=='caught' and wicket_fielder==keepers) or (misfield_type=='caught' and (misfield_fielder==keepers))"))
    field_catches = total_catches-bowler_catches-wk_catches
     
    total_runouts = len(df_slice.query("wicket_type == 'run out' or misfield_type == 'run out'"))
    bowler_runouts = len(df_slice.query("(wicket_type=='run out' and wicket_fielder==bowlers) or (misfield_type=='run out' and (misfield_fielder==bowlers))"))
    wk_runouts = len(df_slice.query("(wicket_type=='run out' and wicket_fielder==keepers) or (misfield_type=='run out' and (misfield_fielder==keepers))"))
    field_runouts = total_runouts-bowler_runouts-wk_runouts
    
    stumped = len(df_slice.query("wicket_type == 'stumped' or misfield_type == 'stumping'"))
    bowled = len(df_slice.query("wicket_type == 'bowled'"))
    lbw = len(df_slice.query("wicket_type == 'lbw'"))
    
    onelb = len(df_slice.query("legbyes==1"))
    fourlb = len(df_slice.query("legbyes==4"))
    twolb = len(df_slice.query("legbyes==2 or legbyes==3"))
    
    results_str = f"{weight},{dots},{singles},{twos},{threes},{fours},{sixes},{bowler_catches},{wk_catches},{field_catches},{bowler_runouts},{wk_runouts},{field_runouts},{stumped},{bowled},{lbw},{onelb},{twolb},{fourlb}"
    
    print(results_str)
    return results_str

def split_by_bowler_type(df_slice):
    vsPace = df_slice[df_slice["bowl_role"]=="pace"]
    vsSpin = df_slice[df_slice["bowl_role"]=="spin"]
    return [vsPace,vsSpin]

def split_into_phases(df_slice):
    phase_1 = df_slice[df_slice["phase"]==1]
    phase_2 = df_slice[df_slice["phase"]==2]
    phase_3 = df_slice[df_slice["phase"]==3]
    return [phase_1,phase_2,phase_3]

def get_batting_occurences_role(_filter, isAllrounder):
    if not isAllrounder:
        filtered_df = final_df[final_df["bat_role"]==_filter]
    else:
        filtered_df = final_df[final_df["bat_role_det"]==_filter]
    
    splits = []
    type_splits = split_by_bowler_type(filtered_df)
    for type_split in type_splits:
        phase_splits = split_into_phases(type_split)
        for phase_split in phase_splits:
            splits.append(phase_split)  
    for _split in splits:
        return_amounts(_split)
    
    
    
roles = ["batter", "Batting allrounder", "allrounder", "Bowling allrounder", "bowler"]
isAR = [False, True, False, True, False]
for i in range(len(roles)):
    print(roles[i])
    get_batting_occurences_role(roles[i],isAR[i])
# get_batting_occurences_role("batter",False)