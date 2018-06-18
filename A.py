# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 20:57:31 2018

@author: luoming
"""
import numpy as np
from collections import deque

class AStar:
    def __init__(self):
        self.rows = 0   # 行数
        self.cols = 0   # 列数
        self.map = None
    
    def loadMap(self,fileName):
        self.map = np.loadtxt(fileName,dtype=np.int8,skiprows=1)
        self.rows,self.cols = self.map.shape

    
    def distBetween(self,current,neighbor):
        
        if (current[0] != neighbor[0]) and (current[1] != neighbor[1]):
            dist = 1.4
        else:
            dist = 1.0
        #print(current,neighbor,dist)
        return dist
            

    def heuristicEstimate(self,start,goal):
        
        dx,dy = abs(start[0]-goal[0]),abs(start[1]-goal[1])
        #h = dx + dy
        h = 0.4*min(dx , dy) + max(dx , dy)
        #h=0
        return h


    def neighborNodes(self,current):
        neighborList = []
        for (i,j) in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            tmp = (current[0]+i,current[1]+j)
            if 0 <= tmp[0] < self.rows  and  0 <= tmp[1] < self.cols:
                if self.map[tmp[0]][tmp[1]] == 1:
                    neighborList.append(tmp)
        return neighborList
    
    def reconstructPath(self,cameFrom,goal):
        path = deque()
        node = goal
        path.appendleft(node)
        while node in cameFrom:
            node = cameFrom[node]
            path.appendleft(node)
        return path
    
    def getLowest(self,openSet,fScore):
        lowest = float("inf")
        lowestNode = None
        for node in openSet:
            if fScore[node] < lowest:
                lowest = fScore[node]
                lowestNode = node
        return lowestNode

    def aStar(self,start,goal):
        cameFrom = {}
        openSet = set([start])
        closedSet = set()
        gScore = {}
        fScore = {}
        gScore[start] = 0
        fScore[start] = gScore[start] + self.heuristicEstimate(start,goal)
        while len(openSet) != 0:
            current = self.getLowest(openSet,fScore)
            print(current)
            if current == goal:
                self.c = cameFrom
                return self.reconstructPath(cameFrom,goal)
            openSet.remove(current)
            closedSet.add(current)
#            for neighbor in self.neighborNodes(current):
#                tentative_gScore = gScore[current] + self.distBetween(current,neighbor)
#                if neighbor in closedSet and tentative_gScore >= gScore[neighbor]:
#                    continue
#                #if (neighbor not in closedSet): 
#                if neighbor not in closedSet or tentative_gScore < gScore[neighbor]:
#                    cameFrom[neighbor] = current
#                    gScore[neighbor] = tentative_gScore
#                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor,goal)
#                    if neighbor not in openSet:
#                        openSet.add(neighbor)
            for neighbor in self.neighborNodes(current):
                tentative_gScore = gScore[current] + self.distBetween(current,neighbor)
                if neighbor in openSet and tentative_gScore < gScore[neighbor]:
                    openSet.remove(neighbor)
                if neighbor in closedSet and tentative_gScore < gScore[neighbor]:
                    closedSet.remove(neighbor)
                if neighbor not in openSet and neighbor not in closedSet:
                    openSet.add(neighbor)
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor,goal)
                   

    
    
if __name__ == "__main__":
    
    A = AStar()
    A.loadMap("test.txt")
    p = A.aStar((2,2),(3,17))
    amap = A.map[:]
    j = 50
    for i in p:
        amap[i[0]][i[1]] = j
        j += 1