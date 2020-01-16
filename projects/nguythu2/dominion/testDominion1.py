# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 2020
@author: nguythu2
"""

import Dominion
import random
from collections import defaultdict
import testUtility

#Get player names
player_names = ["Annie","*Ben","*Carla"]

#number of curses and victory cards
#Here is the Test Case
nV= 1
nC = 0

box = testUtility.GetBoxes(nC)
supply_order = testUtility.FillSupplyOrder()

#Pick 10 cards from box to be in the supply.
random10 = testUtility.PickTen(box)

#Filling the supply
supply = testUtility.FillSupply(player_names, nV, nC, box, random10)

#initialize the trash
trash = []

#Costruct the Player objects
players = testUtility.CreatePlayerObjects(player_names)

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)

#Final score
dcs=Dominion.cardsummaries(players)
winstring = testUtility.FinalScore(dcs)
print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)