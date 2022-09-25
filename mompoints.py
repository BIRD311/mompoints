#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import json

def top10Points(rank):
    rank-=1
    points= [
            3000, #points = 100% of WR
            2250, #points = 75% of WR
            2040, #points = 68% of WR
            1830, #points = 61% of WR
            1710, #points = 57% of WR
            1590, #points = 53% of WR
            1515, #points = 50.5% of WR
            1440, #points = 48% of WR
            1365, #points = 45.5% of WR
            1290 #points = 43% of WR
    ]
    if(rank >= 10):
        return 0
    else:
        return points[rank]
def formularPoints(rank):
    A=50000
    B=49
    return round(A/(rank+B))
groups=4
def groupSize(group, completions):
    group -= 1
    E = [
            0.5,
            0.56,
            0.62,
            0.68
            ]
    SF = [
            1,
            1.5,
            2,
            2.5
            ]
            
    minSize = [
            10,
            45,
            125,
            250
            ]
    #print(SF[group], E[group], completions)
    if(group< 0 or group >= groups):
        return 0
    else:
        return max(SF[group] * pow(completions, E[group]), minSize[group])

def getGroup(rank,completions):
    lastGroupRank=10
    if(rank <=lastGroupRank):
        return 0
    for group in range(groups):
        group+=1
        lastGroupRank += groupSize(group, completions)
        #print("lastGroupRank",lastGroupRank)
        if(rank < lastGroupRank):
            return group
    return 0

def groupPoints(group):
    group-=1
    p = [
            600, #points = 20% of WR
            390, #points = 13% of WR
            210, #points = 7% of WR
            90, #points = 3% of WR
        ]
    if(group<0 or group > groups):
        return 0
    else:
        return p[group]
    
f = open("./surf_mesa_fix.json")
#f = open("./surf_lux.json")
#f = open("./surf_me.json")
#f = open("./surf_lost2.json")
#f = open("./surf_beyer.json")
print(f.name, "points")
data = f.read()
jsonDict = json.loads(data)
jsonDict = sorted(jsonDict, key = lambda x: (x["rank"]), reverse=False)
x=[]
y=[]
recs=[]
x.clear()
y.clear()
completions=len(jsonDict)
print(completions,"completions")
prevG = -1
#for rank in range(completions):
wr=0
prevRec=None
for rec in jsonDict:
    #rank+=1
    rank = rec["rank"]
    if(rank == 1):
        wr = rec["time"]
    x.append(rank)
    #print("rank", rank)
    t=top10Points(rank)
    #print("rank", rank)
    f=formularPoints(rank)
    #print("rank", rank)
    g = getGroup(rank, completions)
    if(rank< 10000):
        is1000 = rank % 1000 == 0
    else:
        is1000 = rank % 10000 == 0
    if(prevG != g 
       or rank == len(jsonDict)
       or is1000):
        if(not is1000 and prevRec != None):
            recs.append(prevRec)
        recs.append(rec)
    gp=groupPoints(g)
    #print("rank", rank)
    s=t+f+gp
    y.append(s)
    #print(t, f, g, "=", s)
    rec["points"]=s
    rec["group"]=g
    prevG = g
    prevRec=rec
print("------------------------")
for rec in recs:
    print("rank", rec["rank"], 
          "group", rec["group"], 
          "time","{:.3f}".format(rec["time"]), 
          "(+"+"{:.3f}".format(rec["time"]-wr)+")", 
          "points",rec["points"])
plt.style.use('dark_background')
plt.plot(x,y,marker='o')
plt.draw()
plt.pause(0.1)
plt.clf()
#sleep(1000)
print("end")
plt.plot(x,y,marker='o')
plt.show()
