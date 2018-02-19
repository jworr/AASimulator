#!/usr/bin/python

import battleSim as bs

from aa1941 import *

DAM = 1000
total = 0

testArmy = bs.Army([bs.buildUnit(SUB), bs.buildUnit(BAT)])
testArmy2 = bs.Army([bs.buildUnit(DEST), bs.buildUnit(DEST)])

for i in range(1000):
	damage, details = testArmy.doDamage()
	total += damage

print("Average damage {}, total hits {}".format(total/float(DAM), total))

applyDamage(testArmy2, testArmy, {DEST:1})
print(testArmy.details())

applyDamage(testArmy2, testArmy, {DEST:1})
print(testArmy.details())
"""
testArmy.takeDamage(1)
print(testArmy.details())

testArmy.takeDamage(1)
print(testArmy.details())

testArmy.takeDamage(1)
print(testArmy.details())

print(testArmy.isDefeated())
"""
