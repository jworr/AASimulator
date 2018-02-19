#! /usr/bin/python

import random
from collections import Counter
from copy import deepcopy

import aa1941

SIDES = 6

random.seed(0)

def runSim(attacker, defender, runs):
	"""
	Simulates a battle a given number of times
	"""
	aWins = 0
	rounds = []
	aleft = []
	dleft = []

	print("Attacker! {} {}".format(len(attacker), attacker))
	print("Defender! {} {}".format(len(defender), defender))

	def avg(counts):
		return float(sum(counts))/runs

	#do the simulation the given number of runs
	for i in range(runs):
		aArmy = deepcopy(attacker)
		dArmy = deepcopy(defender)
		steps = 0

		#simulate one battle
		while not aArmy.isDefeated() and not dArmy.isDefeated() and \
		not aa1941.checkSpecialEnd(aArmy, dArmy):
			steps += 1
			aa1941.battleRound(aArmy, dArmy)

		#record the number of rounds
		rounds.append(steps)
		aleft.append(aArmy)
		dleft.append(dArmy)

		#record the win for the attacker
		if dArmy.isDefeated():
			aWins += 1

	#return the number of wins, the average number of rounds,
	#and the average number of remaining attacking/defending units
	return float(aWins)/runs, avg(rounds), avg(map(len,aleft)), \
	avg(map(len, dleft)), mostCommon(aleft), mostCommon(dleft)

def roll():
	"""
	Rolls a dice
	"""
	return random.randint(1, SIDES)

class Army(object):
	"""
	A collection of millitary units (also a navy)
	"""

	def __init__(self, units):
		"""
		Initializes the army with all the units
		units is a list of units
		"""
		#sort the units according to cost
		self.units = sorted(units, key=lambda u: u.cost)

	def doDamage(self, attack=True, canHurt=lambda u: True):
		"""
		Calculates damage rolls for all the units in the army
		"""
		#record the hits per unit type
		hits = {}
	
		#roll for each unit
		for unit in filter(canHurt, self.units):
			if unit.doDamage(attack):
				hits[unit.name] = hits.get(unit.name,0) + 1

		return sum(hits.values()), hits

	def takeDamage(self, hits, canHit=lambda u: True):
		"""
		Applies damage to the army, to the lower costing units first
		hits - the number of hits to apply
		canHit - a function that determines which units can be hit
		"""
		pre = lambda u: canHit(u) and (u.hits - u.damage) > 1

		#break the damage into two steps
		#soak damage
		soaked, details = self._takeDamage(hits, pre)

		#take regular damage
		hitCount, hitDetails = self._takeDamage(hits-soaked, canHit)

		#update the details of the damage
		hitDetails.update(details)

		return soaked + hitCount, hitDetails

	def _takeDamage(self, hits, canHit):
		"""
		Private method to apply damage
		"""
		damage = {}
		hitsTaken = 0

		#only damage those units can be hit
		toHit = filter(canHit, self.units)

		#apply damage to a subset of units
		for unit in toHit[:min(hits, len(toHit))]: 
			unit.takeDamage()
			hitsTaken += 1

			#if it is destroyed remove it
			if unit.isDestroyed():
				self.units.remove(unit)
				damage[unit.name] = damage.get(unit.name,0) + 1

		return hitsTaken, damage

	def isDefeated(self):
		"""
		Returns true if the army is defeated
		"""
		return len(self.units) == 0

	def __contains__(self, unitName):
		"""
		Checks if the army contains a unit with a given name
		"""
		for unit in self.units:
			if unit.name == unitName:
				return True
		return False

	def __repr__(self):
		if self.isDefeated():
			return "Defeated"
		else:
			#count the types of units
			counts = Counter(u for u in self.units)
			
			#sort by unit cost, the put each unit type on its own line
			return "\n".join(["{} x{}".format(u,c) 
			for u,c in sorted(counts.items(), key=lambda (u,c): u.cost)])

	def details(self):
		return "\n".join(str(u) for u in self.units)

	def __len__(self):
		return len(self.units)

	def __eq__(self, other):
		return Counter(self.units) == Counter(other.units)

	def __hash__(self):
		counts = Counter(self.units)
		return sum(u.cost*c for u,c in counts.items())

def buildUnit(name):
	"""
	Build a unit with the given name
	"""
	return Unit(name, *aa1941.UNITS[name])

class Unit(object):
	"""
	Represents one battlefield unit
	"""

	def __init__(self, name, attack, defense, cost, hits):
		self.attack = attack
		self.defense = defense
		self.name = name
		self.cost = cost
		self.hits = hits #number of hits the unit can take
		self.damage = 0

	def doDamage(self, attack):
		"""
		Rolls a die to do damage
		"""
		return roll() <= (self.attack if attack else self.defense)

	def takeDamage(self, hits=1):
		assert hits <= self.hits
		self.damage += hits

	def isDestroyed(self):
		return self.damage == self.hits

	def __repr__(self):
		return self.name

	def toString(self):
		return "{} A:{} D:{} H:{}".format(self.name, self.attack, self.defense, self.damage)

	def __eq__(self, o):
		return self.name == o.name

	def __hash__(self):
		return hash(self.name)

def mostCommon(armies):
	"""
	Returns the most common army
	"""
	common = [a for a,c in Counter(armies).most_common(2) if not a.isDefeated()]
	if len(common):
		return str(common.pop())
	else:
		return ""
