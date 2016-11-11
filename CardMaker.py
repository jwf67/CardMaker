import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageFile
from PIL import ImageDraw
import textwrap
import os

#FONT PATH ON COMPUTER
FONT_PATH = "/usr/share/fonts/truetype/tlwg/Waree.ttf"
#Dinemsions of the card
WIDTH = 735
HEIGHT = 1029

#Where the name should be placed on the card
STARTNAME_X = 75
ENDNAME_X = 735
STARTNAME_Y = 25
ENDNAME_Y = 100

#Where the image should be placed on the card
IMAGE_X = 30
IMAGE_Y = 100

#Where the effect should be printed on the card
EFF_X = 35
EFF_Y = 720

#Where the attack, defense, and health should be printed in the Y direction
STARTSTAT_Y = 615
ENDSTAT_Y = 685

#Size of the different texts that are to be added
FONTSIZE_NAME = 50
FONTSIZE_EFFECT = 10
FONTSIZE_STATS = 25

#Generic Card Class
class Card(object):
	#Define font for the name and effect
	nameFont = ImageFont.truetype(FONT_PATH, FONTSIZE_NAME)
	effFont = ImageFont.truetype(FONT_PATH, FONTSIZE_EFFECT)

	#Characteristics of a basic card include its name, effect, class, and picture directory
	def __init__(self, name, effect, cclass, pic):
		self.name = name
		self.effect = effect
		self.cclass = cclass
		self.pic = pic

	#Print basic characteristics of the card
	def printCharacteristics(self):
		print self.name + "\n" + self.effect + "\n" + self.cclass

	#Add the name to the card
	def addNameToCard(self):
		defCard = Image.open("CardFronts/" + self.cclass + "_Prototype.png")
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.name, font = self.nameFont)
		
		print str(w) + "\n" + str(h)		

		nameFont = ImageFont.truetype(FONT_PATH, FONTSIZE_NAME)
		draw.text(((WIDTH-w)/2, (ENDNAME_Y-STARTNAME_Y-h)/2), self.name, (255, 255, 255), self.nameFont)
		defCard.save(self.name + '.png')

	#Add the picture of the creature to the card
	def addPicToCard(self):
		card = Image.open(self.name + '.png')
		image = Image.open(self.name + 'art.png')
		card.paste(image, (30,100))
		card.save(self.name + '.png')

	#Add the effect to the card
	def addEffectToCard(self):
		defCard = Image.open(self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		offset = EFF_Y
		for line in textwrap.wrap(self.effect, width = EFF_X):
			draw.text((35, offset), self.effect, (255, 255, 255), font = self.effFont)
			offset += self.nameFont.getsize(line)[1]
		defCard.save(self.name + '.png')
	
	#Generate the card in its entirety
	def generateCard(self):
		self.addNameToCard()
		self.addPicToCard()
		self.addEffectToCard()

#Class for Creature Cards
class CreatureCard(Card):

	#Includes same characteristics as a regular card but more
	def __init__(self, name, effect, cclass, pic, attack, defense, health, limit):
		super(CreatureCard, self).__init__(name, effect, cclass, pic)
		self.attack = str(attack)
		self.defense = str(defense)
		self.health = str(health)
		self.limit = str(limit)

	def addAttackToCard(self):
		defCard = Image.open(self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.attack, font = self.nameFont)

		draw.text(((WIDTH-w)/4, (ENDSTAT_Y+STARTSTAT_Y-h)/2), self.attack, (255, 255, 255), self.nameFont)
		defCard.save(self.name + '.png')

	def addDefenseToCard(self):
		defCard = Image.open(self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.defense, font = self.nameFont)

		draw.text(((WIDTH-w)/2, (ENDSTAT_Y+STARTSTAT_Y-h)/2), self.defense, (255, 255, 255), self.nameFont)
		defCard.save(self.name + '.png')

	def addHealthToCard(self):
		defCard = Image.open(self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.health, font = self.nameFont)

		draw.text(((WIDTH-w)*3/4, (ENDSTAT_Y+STARTSTAT_Y-h)/2), self.health, (255, 255, 255), self.nameFont)
		defCard.save(self.name + '.png')

	def generateCreatureCard(self):
		self.addNameToCard()
		#self.addPicToCard()
		self.addEffectToCard()
		self.addAttackToCard()
		self.addDefenseToCard()
		self.addHealthToCard()

#Class for Enhancement Cards
class EnhancementCard(Card):
	def __init__(self, name, effect, cclass, pic, limit):
		super(name, effect, cclass, pic)
		self.limit = limit

#Test 1
my_card = Card("Name", "This is the effect", "Standard", "Pictures not added yet.")
my_card.addNameToCard()
my_card.addEffectToCard()

#Test 2
my_creature = CreatureCard("Creature", "This creature has no effect", "Standard", "Pictures not added yet.", 10, 10, 10, 3)
my_creature.generateCreatureCard()
