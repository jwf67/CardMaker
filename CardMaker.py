import PIL
import sys
import textwrap
import os
import csv

from PIL import ImageFont
from PIL import Image
from PIL import ImageFile
from PIL import ImageDraw


#FONT PATH ON COMPUTER
FONT_PATH = "/usr/share/fonts/truetype/tlwg/Waree.ttf"

#Path to save card
CARD_PATH = "Cards/"

#Path to get card image
ART_PATH = "CardArt/"

#Path to get card front
FRONT_PATH = "CardFronts/"

#Path to cards list
CARDLIST_PATH = "CardList/"

#Dinemsions of the card
WIDTH = 735
HEIGHT = 1029

#Where the name should be placed on the card
STARTNAME_X = 75
ENDNAME_X = 660
STARTNAME_Y = 25
ENDNAME_Y = 100

#Where the image should be placed on the card
IMAGE_X = 30
IMAGE_Y = 100

#Where the effect should be printed on the card
EFF_X = 35
EFF_Y = 710

EFF_X_END = 700
EFF_Y_END = 994

#Where the attack, defense, and health should be printed in the Y direction
STARTSTAT_Y = 615

#Size of the different texts that are to be added
FONTSIZE_NAME = 50
FONTSIZE_EFFECT = 18
FONTSIZE_STATS = 40

#Generic Card Class
class Card(object):
	#Define font for the name and effect
	nameFont = ImageFont.truetype(FONT_PATH, FONTSIZE_NAME)
	effFont = ImageFont.truetype(FONT_PATH, FONTSIZE_EFFECT)

	#Characteristics of a basic card include its name, effect, and class
	def __init__(self, name, effect, cclass):
		self.name = name
		self.effect = effect
		self.cclass = cclass

	#Print basic characteristics of the card
	def printCharacteristics(self):
		print self.name + "\n" + self.effect + "\n" + self.cclass

	#Add the name to the card
	def addNameToCard(self):
		defCard = Image.open(FRONT_PATH + self.cclass + "_Prototype.png")
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.name, font = self.nameFont)
		nameFont = ImageFont.truetype(FONT_PATH, FONTSIZE_NAME)
		draw.text(((WIDTH-w)/2, (ENDNAME_Y-STARTNAME_Y-h)/2), self.name, (255, 255, 255), self.nameFont)
		defCard.save(CARD_PATH + self.name + '.png')

	#Add the picture of the creature to the card
	def addPicToCard(self):
		card = Image.open(CARD_PATH + self.name + '.png')
		image = Image.open(ART_PATH + self.name + '_art.png')
		image.paste(card, (0,0), mask = card)		
		image.save(CARD_PATH + self.name + '.png')

	#Add the effect to the card
	def addEffectToCard(self):
		defCard = Image.open(CARD_PATH + self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		offset = EFF_Y
		margin = 35		

		#Text from the previous line that should be added to the next line
		extra = "";

		#Want each line to be at most the size of the text box
		max_line_size = EFF_X_END - EFF_X
		for line in textwrap.wrap(self.effect, width = 30):
			print "HIT"
			analyzed_line = analyzeLine(extra + line, max_line_size, self.effFont)
			draw.text((margin, offset), analyzed_line[0], (255, 255, 255), font = self.effFont)
			offset += self.nameFont.getsize(line)[1]/2
			if offset > 1000:
				print "HIT" 
		defCard.save(CARD_PATH + self.name + '.png')
	
	#Generate the card in its entirety
	def generateCard(self):
		self.addNameToCard()
		self.addPicToCard()
		self.addEffectToCard()

#Take the current line and return the desired line resized and any extra content missing
def analyzeLine(line, max_size, font):
	result = ["", ""]
	for x in range(len(line), 0, -1):
		curr_line_size = font.getsize(line[:x])[0]
		print curr_line_size
		print max_size
		if curr_line_size <= max_size:
			result[0] = line[:x]
			result[1] = line[x:]
			print result
			return result
	return result
		

#Class for Creature Cards
class CreatureCard(Card):

	statFont = ImageFont.truetype(FONT_PATH, FONTSIZE_STATS)

	#Includes same characteristics as a regular card but more
	def __init__(self, name, effect, cclass, attack, defense, health, limit):
		super(CreatureCard, self).__init__(name, effect, cclass)
		self.attack = str(attack)
		self.defense = str(defense)
		self.health = str(health)
		self.limit = str(limit)

	def addAttackToCard(self):
		defCard = Image.open(CARD_PATH + self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.attack, font = self.statFont)

		draw.text(((WIDTH-w)/4, STARTSTAT_Y), self.attack, (255, 255, 255), font = self.statFont)
		defCard.save(CARD_PATH + self.name + '.png')

	def addDefenseToCard(self):
		defCard = Image.open(CARD_PATH + self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.defense, font = self.statFont)

		draw.text(((WIDTH-w)/2, STARTSTAT_Y), self.defense, (255, 255, 255), font = self.statFont)
		defCard.save(CARD_PATH + self.name + '.png')

	def addHealthToCard(self):
		defCard = Image.open(CARD_PATH + self.name + '.png')
		draw = ImageDraw.Draw(defCard)
		w, h = draw.textsize(self.health, font = self.statFont)

		draw.text(((WIDTH-w)*3/4, STARTSTAT_Y), self.health, (255, 255, 255), font = self.statFont)
		defCard.save(CARD_PATH + self.name + '.png')

	def generateCreatureCard(self):
		self.addNameToCard()
		self.addPicToCard()
		self.addEffectToCard()
		self.addAttackToCard()
		self.addDefenseToCard()
		self.addHealthToCard()

#Class for Enhancement Cards
class EnhancementCard(Card):
	def __init__(self, name, effect, cclass, limit):
		super(EnhancementCard, self).__init__(name, effect, cclass)
		self.limit = limit

	def generateEnhancementCard(self):
		self.addNameToCard()
		self.addPicToCard()
		self.addEffectToCard()

#Read csv file and make sure each line is being read
def readCardFile(fileName):
	cards = open(CARDLIST_PATH + fileName, 'r')
	for card in cards:
		s =  [stat.strip() for stat in card.split(',')]
		if s[7] == "Creature":
			thisCard = CreatureCard(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
			print "Generating valid creature card"
			thisCard.generateCreatureCard()
		elif s[7] == "Enhancement":
			thisCard = EnhancementCard(s[0], s[1], s[2], s[6])
			print "Generating valid enhancement card"			
			thisCard.generateEnhancementCard()
		else:
			print "No valid card printing."
			
#Execution at run time
print "STARTING CARD MAKER"

#Only looking for one argument - file name
print "COUNTING ARGUMENTS: " + str(len(sys.argv))
if len(sys.argv) > 1:
	print "TERMINATING - DO NOT NEED ANY ARGUMENTS"
	sys.exit()

#If a valid number of arguments exist continue
print "CONTINUING..."

fileName = "cards.csv"
readCardFile(fileName)


#Test 1
my_card = Card("Name", "This is the effect", "Standard")
my_card.addNameToCard()
my_card.addEffectToCard()

#Test 2
my_creature = CreatureCard("Creature", "This creature has no effect", "Standard", 10, 10, 10, 3)
my_creature.generateCreatureCard()
