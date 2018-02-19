
INF = "Infantry"
TANK = "Tank"
FGHT = "Fighter"
BOMB = "Bomber"
SUB = "Submarine"
DEST = "Destroyer"
AIR = "Aircraft Carrier"
BAT = "Battleship"

UNITS = { INF:(1, 2, 3, 1), TANK:(3, 3, 6, 1), FGHT:(3, 4, 10, 1), 
BOMB:(4, 1, 12, 1), SUB:(2, 1, 6, 1), DEST:(2, 2, 8, 1),
AIR:(1, 2, 12, 1), BAT:(4, 4, 16, 2)}

def everything(unit):
	return True

def isAircraft(unit):
	"""
	Returns True if the unit is an aircraft
	"""
	return unit.name == FGHT or unit.name == BOMB

def notAircraft(unit):
	"""
	Returns True if the unit is not an aircraft
	"""
	return not isAircraft(unit)

def isSub(unit):
	"""
	Returns True if the unit is a sub
	"""
	return unit.name == SUB

def notSub(unit):
	"""
	Returns true if the unit is not a sub
	"""
	return not isSub(unit)

def battleRound(attacker, defender):
	"""
	Does the pre-attack, subs may get a sneak attack
	"""
	aSneak = False
	dSneak = False

	#check for sneak attack
	if SUB in attacker and DEST not in defender:
		aHits, aDetails = attacker.doDamage(True, isSub)
		aSneak = True

	#check of other sides sneak attack
	if SUB in defender and DEST not in attacker:
		dHits, dDetails = defender.doDamage(False, isSub)
		dSneak = True

	#apply the sneak attack damage
	if aSneak:
		applyDamage(attacker, defender, aDetails)
	
	if dSneak:
		applyDamage(defender, attacker, dDetails)

	#do regular damage
	aHits, aDetails = attacker.doDamage(True, notSub if aSneak else everything)
	dHits, dDetails = defender.doDamage(False, notSub if dSneak else everything)

	#apply the damage
	applyDamage(attacker, defender, aDetails)
	applyDamage(defender, attacker, dDetails)

def applyDamage(damager, damagee, hits):
	"""
	Apply damage to the defending army based on the type of hits
	"""
	sub = hits.get(SUB,0)
	planes = hits.get(AIR,0) + hits.get(BOMB,0)
	done = 0
	allHits = 0
	damage = {}

	#if there is damage from subs, it cannot hit aircraft
	if sub > 0:
		done += sub
		sHits, sDetails = damagee.takeDamage(sub, notAircraft)
		allHits += sHits
		damage.update(sDetails)

	#if there is damage from aircraft and no destroyer, then aircraft
	#can only attack non-subs
	if planes > 0 and DEST not in damager:
		done += planes
		pHits, pDetails = damagee.takeDamage(planes, notSub)
		allHits += pHits
		damage.update(pDetails)

	#just do damage normally
	hits, details = damagee.takeDamage(sum(hits.values())-done)
	details.update(damage)

	return hits + allHits, details

def checkSpecialEnd(attacker, defender):
	def onlySubs(army):
		return len(army) == len(filter(isSub, army.units))

	def onlyPlanes(army):
		return len(army) == len(filter(isAircraft, army.units))
	
	return (onlySubs(attacker) and onlyPlanes(defender)) or\
	(onlySubs(defender) and onlyPlanes(attacker))
