#Generic Card Class
class Card:
	#Characteristics of a basic card include its name, effect, class, and picture directory
	def __init__(self, name, effect, cclass, pic):
		self.name = name
		self.effect = effect
		self.cclass = cclass
		self.pic = pic

#Class for Creature Cards
class CreatureCard(Card):
	#Includes same characteristics as a regular card but more
	def __init__(self, name, effect, cclass, pic, attack, defense, health, limit):
		super(name, effect, cclass, pic)
		self.attack = attack
		self.defense = defense
		self.health = health
		self.limit = limit

#Class for Enhancement Cards
class EnhancementCard(Card)
	def __init__(self, name, effect, cclass, pic, limit):
		super(name, effect, cclass, pic)
		self.limit = limit
