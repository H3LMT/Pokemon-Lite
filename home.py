#Main file which has all the drawing and pygame aspects, this file is to be run, to run the project

"""
Sprites @ https://veekun.com/dex/downloads
MODES
0.   MAIN MENU
1.   INFO
2.   POKEDEX
2.1  Added
2.2  No Space
2.5  POKEMON INFO 
3.   PARTY
3.5  Party More Info
4.   BATTLE
"""
from typeData import *
from colors import *
import time
import random
import structs  
import requests
import numpy as np
import os
import sys, pygame

data = structs.data()
def init(data):
    data.currPokedex = []
    data.units = "imperial"
    data.currMove = [0, 0]
    data.currentPokemon = 1
    data.allPokemon = {}
    data.allMoves = {}
    data.dimension = 500
    data.width, data.height = data.dimension, data.dimension
    data.screen = pygame.display.set_mode((data.width, data.height))
    data.backHome = pygame.image.load("Media/background.jpeg")
    data.backHome = pygame.transform.scale(data.backHome, (data.width, data.height))
    data.batGround = pygame.image.load("Media/battleground.jpg")
    data.batGround = pygame.transform.scale(data.batGround, (data.width, data.height))
    data.pokemonMax = 151
    data.background = pygame.image.load("Media/pokedexBackground.jpeg")
    data.background = pygame.transform.scale(data.background, (data.width, data.height))
    data.samePokemon = False
    data.opposingSwitch = False
    data.isFaintedSwitch = False
    data.allOwnFainted = False
    data.skip = False
    data.inGame = False
    data.opposingParty = structs.party()
    data.partyIndex = 0
    data.switchMode = False
    data.switchIndex = 0
    data.partyMenu = False
    data.partyMenuIndex = 0
    data.selected = None
    data.missed = False
    data.notEffective = False
    data.veryEffective = False
    data.mode = 0
    data.start_time = time.time()
    data.currText = [0,0]
    data.battlemode = 0
    data.currParty = structs.party()
    data.oldParty = data.currParty.toArray()
    def setTypes():
        data.types = \
             [
            ['X', 'normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying',
             'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'],
            ['normal', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0.5', '0', '1', '1', '0.5', '1'],
            ['fire', '1', '0.5', '0.5', '1', '2', '2', '1', '1', '1', '1', '1', '2', '0.5', '1', '0.5', '1', '2', '1'],
            ['water', '1', '2', '0.5', '1', '0.5', '1', '1', '1', '2', '1', '1', '1', '2', '1', '0.5', '1', '1', '1'],
            ['electric', '1', '1', '2', '0.5', '0.5', '1', '1', '1', '0', '2', '1', '1', '1', '1', '0.5', '1', '1',
             '1'],
            ['grass', '1', '0.5', '2', '1', '0.5', '1', '1', '0.5', '2', '0.5', '1', '0.5', '2', '1', '0.5', '1', '0.5',
             '1'],
            ['ice', '1', '0.5', '0.5', '1', '2', '0.5', '1', '1', '2', '2', '1', '1', '1', '1', '2', '1', '0.5', '1'],
            ['fighting', '2', '1', '1', '1', '1', '2', '1', '0.5', '1', '0.5', '0.5', '0.5', '2', '0', '1', '2', '2',
             '0.5'],
            ['poison', '1', '1', '1', '1', '2', '1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '0',
             '2'],
            ['ground', '1', '2', '1', '2', '0.5', '1', '1', '2', '1', '0', '1', '0.5', '2', '1', '1', '1', '2', '1'],
            ['flying', '1', '1', '1', '0.5', '2', '1', '2', '1', '1', '1', '1', '2', '0.5', '1', '1', '1', '0.5', '1'],
            ['psychic', '1', '1', '1', '1', '1', '1', '2', '2', '1', '1', '0.5', '1', '1', '1', '1', '0', '0.5', '1'],
            ['bug', '1', '0.5', '1', '1', '2', '1', '0.5', '0.5', '1', '0.5', '2', '1', '1', '0.5', '1', '2', '0.5',
             '0.5'],
            ['rock', '1', '2', '1', '1', '1', '2', '0.5', '1', '0.5', '2', '1', '2', '1', '1', '1', '1', '0.5', '1'],
            ['ghost', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '1', '2', '1', '0.5', '1', '1'],
            ['dragon', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '1', '0.5', '0'],
            ['dark', '1', '1', '1', '1', '1', '1', '0.5', '1', '1', '1', '2', '1', '1', '2', '1', '0.5', '1', '0.5'],
            ['steel', '1', '0.5', '0.5', '0.5', '1', '2', '1', '1', '1', '1', '1', '1', '2', '1', '1', '1', '0.5', '2'],
            ['fairy', '1', '0.5', '1', '1', '1', '1', '2', '0.5', '1', '1', '1', '1', '1', '1', '2', '2', '0.5', '1']]
    setTypes()
init(data)

class Pokemon(pygame.sprite.Sprite):
    def __init__(self,number,information):
        pygame.sprite.Sprite.__init__(self)
        #load appropiate image
        self.fainted = False
        self.number = number
        if(number<20):
            #self.fainted=True
            pass
        self.image = pygame.image.load("Pokemon/Sprites/"+str(number)+".png")
        self.image_back = pygame.image.load("Pokemon/Sprites_Back/"+str(number)+".png")
        self.stats = information
        self.name = self.stats['name']
        self.x = data.width/2
        self.y = data.height/2
        self.rect = (self.x,self.y,self.image.get_size()[0],self.image.get_size()[1])
        #moves
        self.aMoves = []
        self.types = []
        for type in self.stats['types']:
            self.types.append(type['type']['name'])
        self.weakness = returnWeakness(self.types)
        for move in self.stats['moves']:
            self.aMoves.append(move['move']['name'])
        self.moves= ["---"]*4
        moveAdded = False
        def getMove(): #only physical and special right now
            randMove = random.choice(self.aMoves)
            if random.choice(self.aMoves) not in self.moves:
                if data.allMoves[randMove]['damage_class']['name']=='special' or data.allMoves[randMove]['damage_class']['name']=='physical':
                    if(data.allMoves[randMove]['power']!=None):
                        return randMove
            return getMove()
        amount = len(self.aMoves)
        if(amount>4):
            amount = 4
        if(self.number!=132):
            for i in range(amount):
                self.moves[i]=(getMove())
        else:
            self.moves[0] = self.aMoves[0]
        self.moves = set(self.moves)
        self.moves = list(self.moves)
        if(len(self.moves)<4):
            missingAmount = 4-len(self.moves)
            for i in range(missingAmount):
                self.moves.append("---")
        if(self.number == 132):
            self.moves = ["transform","---","---","---"]
        self.totalStat = 0
        self.level = 50
        statNames = ['Spd: ', 'Sp.Def: ', 'Sp.Atk: ', 'Def: ', 'Atk: ', 'HP: ']
        self.finalStats = {}
        for i in range(len(statNames) - 1, -1, -1):
            self.finalStats[statNames[i]] = self.stats['stats'][i]['base_stat']
        for key in self.finalStats:
            self.totalStat+=self.finalStats[key]
        desiredStat = 700
        level = int((desiredStat/self.totalStat-1)/.02+50)
        if (level > 100):
            level = 100
        elif (level < 1):
            level = 1
        for key in self.finalStats:
            self.finalStats[key]+=int(0.02*(level-50)*self.finalStats[key])
        self.finalStats['HP: ']=int(self.finalStats["HP: "]*1.0)
        self.totalStat = 0
        for key in self.finalStats:
            self.totalStat+=self.finalStats[key]
        self.level = level
        self.battleStats = {}
        for item in self.finalStats:
            self.battleStats[item] = self.finalStats[item]
    def __repr__(self):
        return self.stats['forms'][0]['name'].upper()
    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 20
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left
        self.rect = (self.x, self.y, self.image.get_size()[0], self.image.get_size()[1])

    def draw(self, surface,location,scale=1,back=False):
        if(back):
            self.image_back = pygame.transform.scale(self.image_back, (int(scale * data.width / 5.5), int(scale * data.height / 5.5)))
            surface.blit(self.image_back, (location[0], location[1]))
        else:
            self.image = pygame.transform.scale(self.image, (int(scale*data.width/5.5), int(scale*data.height/5.5)))
            surface.blit(self.image, (location[0], location[1]))

class Text(object):
    def __init__(self,text,location, size = 60,color = (0,0,0),topmode = False):
        self.location = location
        self.myfont = pygame.font.SysFont("default", int(size))
        self.label = self.myfont.render((text), 1, color)
        self.text_rect = self.label.get_rect(center=location)
        self.topmode = topmode
    def draw(self):
        if(self.topmode==False):
            data.screen.blit(self.label, self.text_rect)
        else:
            data.screen.blit(self.label,self.location)

class Button(object):
    #initializes button
    def __init__(self, x, y, color, text, textSize = 4, w = 0.25 * data.width, h = 0.1 * data.height,textbox = False):
        self.x = x-w/2
        self.y = y-h/2
        self.textbox = textbox
        self.highlight = False
        #set location of the rectangle which will be updated if needed
        self.rect = (self.x,self.y,w,h)
        self.color = color
        self.text = Text(text,(x,y),w/textSize)

    def handle_mouse(self):
        """#wait so that code doesnt mess up
        pygame.event.wait()"""
        pos = pygame.mouse.get_pos()
        isClicked = pygame.mouse.get_pressed()
        isClicked = isClicked[0]
        #check if clicked and within the button
        if(pos[0]>self.rect[0] and pos[0]<self.rect[2]+self.rect[0]\
            and pos[1]>self.rect[1] and pos[1]<self.rect[3]+self.rect[1]):
            if (isClicked):
                return True
            else:
                self.highlight = True
        else:
            self.highlight = False
        return False

    def draw(self):
        if(self.textbox):
            pygame.draw.rect(data.screen, color.white, self.rect)
            pygame.draw.rect(data.screen, self.color, self.rect, 4)
            self.text.draw()
        elif(self.highlight==False):
            pygame.draw.rect(data.screen, self.color,self.rect,2)
            self.text.draw()
        else:
            pygame.draw.rect(data.screen,color.lightRed,self.rect)
            pygame.draw.rect(data.screen, self.color, self.rect,4)
            self.text.draw()

class TextBox(object):
    def __init__(self,loc,w,h,blankColor):
        self.location = loc
        self.rect = (loc[0],loc[1],w,h)
        self.blankColor = blankColor
        self.typing = False
        self.indicator = ""
        self.text = ""

    def handle_mouse(self):
        pos = pygame.mouse.get_pos()
        isClicked = pygame.mouse.get_pressed()
        isClicked = isClicked[0]
        #check if clicked and within the button
        if(pos[0]>self.rect[0] and pos[0]<self.rect[2]+self.rect[0]\
            and pos[1]>self.rect[1] and pos[1]<self.rect[3]+self.rect[1]):
            if (isClicked):
                return True
        else:
            if(isClicked):
                return False
        return None

    def key_handle(self):
        for event in pygame.event.get():
            if(event.type==pygame.KEYDOWN):
                self.text+=event.unicode

    def draw(self):
        if(self.handle_mouse()):
            self.typing = True
        elif(self.handle_mouse()==False):
            self.typing = False
        if(self.typing):
            self.key_handle()
            pygame.draw.rect(data.screen,color.white, self.rect)
            if((time.time()-data.start_time)%1<0.65):
                self.indicator = "|"
            else:
                self.indicator = ""
            Text(self.text+self.indicator,(self.rect[0],self.rect[1]),size=self.rect[3]/2,color=color.black,topmode=True).draw()
        else:
            pygame.draw.rect(data.screen, self.blankColor, self.rect)
        pygame.draw.rect(data.screen, color.black, self.rect, int(data.width/150))

class pokedexEntry(Button):
    def draw(self,location,caught = False,center = False,health=False,healthString = ""):
        #location is location of text
        pygame.draw.rect(data.screen, self.color, self.rect)
        #self.text.text_rect = self.text.label.get_rect(x = location)
        if(center==False):
            data.screen.blit(self.text.label,(location[0],location[1]))
        else:
            labelRect = self.text.label.get_rect()
            data.screen.blit(self.text.label, (location[0]-labelRect[2]/2, location[1]-labelRect[3]/2))
        #draw pokeball
        if(caught):
            pokeball = pygame.image.load("media/pokeball.png")
            pokeball = pygame.transform.scale(pokeball,(int(1*self.rect[3]),int(1*self.rect[3])))
            imrect = pokeball.get_rect()
            data.screen.blit(pokeball,(self.rect[0]+self.rect[2]-imrect[2]-self.rect[2]/150,self.rect[1]+self.rect[3]-imrect[3]))
        if(health):
            myfont = pygame.font.SysFont("default", int(data.width/25))
            label = myfont.render(healthString, 1, color.black)
            imrect = label.get_rect()
            data.screen.blit(label, (self.rect[0] + self.rect[2] - imrect[2] - self.rect[2] / 150, self.rect[1] + self.rect[3] - imrect[3]))

def returnWeakness(types):
    if(len(types)==1):
        weak = []
        col = typeToIndex(types[0])+1
        for item in data.types:
            weak.append(item[col])
        return weak[1:]
    elif(len(types)==2):
        weak = [[],[]]
        for i in range(len(weak)):
            col=typeToIndex(types[i])+1
            for item in data.types:
                weak[i].append(item[col])
        newList = []
        for i in range(1,len(weak[0])):
            #if()
            newList.append(float(weak[0][i])*float(weak[1][i]))
        return (newList)

def toNumbers():
    array = []
    for pokemon in data.currParty.toArray():
        array.append(pokemon.stats['id'])
    return array

def calculateDamage(own,opposing,move):
    stab = 1
    rand = random.randint(85,101)
    rand /=100
    critical = 1
    moveType = move['type']['name']
    accuracy = move['accuracy']
    #accuracy = 10
    effectivness = opposing.weakness[typeToIndex(moveType)]
    print(effectivness,"efect")
    if(float(effectivness)>=2.0):
        data.veryEffective = True
    elif(float(effectivness)<1):
        data.notEffective = True
    types = own.types
    print (own.name,moveType,types)
    if(moveType in types):
        print("stab")
        stab = 1.5
    modifier = stab * critical  * rand * float(effectivness)
    print(modifier,"mod")
    if(move['power']==None):
        damage = 0
    else:
        reg = 5
        less = 10
        if(move['damage_class']['name']=='special'):
            damage = (((2*80/less+2)*move['power']*own.battleStats['Sp.Atk: ']/opposing.battleStats['Sp.Def: '])/50+2)*modifier
        if (move['damage_class']['name'] == 'physical'):
            damage = (((2 * 80/less + 2) * move['power'] * own.battleStats['Atk: '] / opposing.battleStats['Def: ']) / 50 + 2) * modifier
    rand = random.randint(1,101)

    if(accuracy ==None or accuracy=='null'):
        accuracy = 100
    print("rand", rand, "acc", accuracy)
    if(rand>accuracy):
        damage = 0
    print(damage, "dama")
    print(move['power'])
    print("move done")
    print("")
    return damage

def oldResetOpposingParty():
    size = data.currParty.len()
    data.opposingParty = structs.party()
    for i in range(size):
        satisfied = False
        pokemonToAdd = None
        while(satisfied == False):
            pokemonToAdd = random.choice(data.allPokemon)
            if(pokemonToAdd not in data.currParty.toArray() and pokemonToAdd not in data.opposingParty.toArray()):
                satisfied = True
        data.opposingParty.add(pokemonToAdd)

def resetOpposingParty():
    data.opposingParty = structs.party()
    possible = returnPossibleList()
    #print(possible)
    size = data.currParty.len()
    for i in range(size):
        data.opposingParty.add(random.choice(possible))

def returnPossibleList():
    cParty = data.currParty.toArray()
    oParty = data.opposingParty.toArray()
    possibleList = []
    for pokemon in data.allPokemon:
        if(data.allPokemon[pokemon] not in cParty and data.allPokemon[pokemon] not in oParty):
            possibleList.append(data.allPokemon[pokemon])
    return possibleList

def pyScreen():
    otherTurn = False
    ownPokemonOffset = 0
    opposingPokemonOffset = 0
    ownAttackDisplay = False
    opposingAttackDisplay = False
    won = False
    lose = False
    oldTime = 0
    firstIteration = True
    opposingCurrentMove = ""
    while True:
        timer = time.time()-data.start_time
        timeWait = 110
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                np.save("Pokemon/party.npy",toNumbers())
                np.save("Pokemon/data.units.npy",data.units)
                sys.exit()
        data.screen.fill(color.white)
        if(data.mode == 0): #Home
            data.screen.blit(data.backHome, data.backHome.get_rect())
            title = Text("Pokemon Lite",(data.width/2,data.height/4.5),data.width/6,color.black)
            title.draw()
            #Pokedex Button
            pdex = Button(data.width / 3, data.height / 2+data.height/6.25, color.black, "PokeDex")
            if(pdex.handle_mouse()):
                data.mode= 2
                continue
            pdex.draw()
            #Battle Simulator Button
            sim = Button(data.width-data.width/3, data.height / 2+data.height/6.25, color.black, "Battle Simulator",6)
            if (sim.handle_mouse()):
                data.mode= 4
                pygame.mixer.music.load('media/battle.mp3')
                pygame.mixer.music.play(-1)
                #ownAttackDisplay = True
                data.skip = False
                continue
            sim.draw()
            # Party Button
            party = Button(data.width / 3 , data.height / 1.5 + data.height / 6.25, color.black, "Party")
            if (party.handle_mouse()):
                data.mode= 3
                continue
            party.draw()
            #Info Button
            info = Button(data.width - data.width / 3, data.height / 1.5+data.height/6.25, color.black, "Info")
            if (info.handle_mouse()):
                data.mode= 1
                continue
            info.draw()
        elif(data.mode == 1): #Info
            data.screen.blit(data.backHome, data.backHome.get_rect())
            clicked = "Media/radio_clicked.png"
            unclicked = "Media/radio_unclicked.png"
            metric = pygame.image.load(clicked)
            #data.screen.blit(metric,(data.width/2,data.height/2))
            imperial = pygame.image.load(unclicked)
            if(data.units != "metric"):
                metric = pygame.image.load(unclicked)
                imperial = pygame.image.load(clicked)
            scaleRatio = 20
            metric = pygame.transform.scale(metric,(int(data.width/scaleRatio),int(data.height/scaleRatio)))
            imperial = pygame.transform.scale(imperial, (int(data.width /scaleRatio), int(data.height /scaleRatio)))
            data.screen.blit(metric,(0.05*data.width,0.9*data.height))
            data.screen.blit(imperial, (0.45 * data.width, 0.9 * data.height))
            Text("METRIC",(0.125*data.width,0.91*data.height),size=24,topmode = True).draw()
            Text("IMPERIAL", (0.525 * data.width, 0.91 * data.height),size=24, topmode=True).draw()
            #buttons click code
            pos = pygame.mouse.get_pos()
            isClicked = pygame.mouse.get_pressed()
            isClicked = isClicked[0]
            metRect = (0.05*data.width,0.9*data.height,metric.get_rect()[2],metric.get_rect()[3])
            impRect = (0.45 * data.width, 0.9 * data.height,imperial.get_rect()[2],imperial.get_rect()[3])
            if(isClicked==1 and pos[0]>metRect[0] and pos[0]<metRect[2]+metRect[0]\
                       and pos[1]>metRect[1] and pos[1]<metRect[3]+metRect[1]):
                data.units = "metric"
            elif(isClicked == 1 and pos[0] > impRect[0] and pos[0] < impRect[2] + impRect[0]\
                         and pos[1] > impRect[1] and pos[1] < impRect[3] + impRect[1]):
                data.units = "imperial"
            # Home Button
            home = Button(data.width / 9, data.height / 15, color.black, "Home", w=0.17 * data.width, h=0.06 * data.height)
            if (home.handle_mouse()):
                data.mode= 0
                continue
            home.draw()
            infoLabel = Text("INFO",(data.width/2,data.height/9),size = 55)
            infoLabel.draw()
            Text("- Press Return On A Pokemon For Options", (data.width/50, data.height / 5), size=32.5,topmode=True).draw()
            Text("- Press 'Z' To Add A Pokemon To Party", (data.width / 50, 1.4 * data.height / 5), size=32.5, topmode=True).draw()
            Text("- Press 'Delete' To Remove A Pokemon From", (data.width / 50, 1.8 * data.height / 5), size=32.5, topmode=True).draw()
            Text("  Party", (data.width / 50, 2.05 * data.height / 5), size=32.5,
                 topmode=True).draw()
            Text("- Use Arrow Keys In Battle To Choose Next", (data.width / 50, 2.45 * data.height / 5), size=32.5,
                 topmode=True).draw()
            Text("  Action", (data.width / 50, 2.7 * data.height / 5), size=32.5,
                 topmode=True).draw()
            Text("- Press 'Delete' To Go Back In a Menu", (data.width / 50, 3.1 * data.height / 5), size=32.5,
                 topmode=True).draw()
        elif (data.mode == 2): #Pokedex
            pokedex = pygame.image.load("Media/pokedex.png")
            # Home Button
            data.screen.blit(data.background,data.background.get_rect())
            data.screen.blit(pokedex,(data.width/2.6,data.height/15))
            home = Button(data.width / 9, data.height / 15, color.black, "Home",w= 0.17*data.width,h =0.06*data.height)
            if (home.handle_mouse()):
                data.mode= 0
                continue
            home.draw()
            #key code
            key = pygame.key.get_pressed()
            skip = 10
            if(data.samePokemon==False):
                if (data.currentPokemon < data.pokemonMax and key[pygame.K_DOWN]):
                    data.currentPokemon += 1
                    pygame.time.wait(timeWait)
                elif (data.currentPokemon > 1 and key[pygame.K_UP]):
                    pygame.time.wait(timeWait)
                    data.currentPokemon -= 1
                elif (data.currentPokemon <= data.pokemonMax-skip and key[pygame.K_RIGHT]):
                    data.currentPokemon += skip
                    pygame.time.wait(timeWait)
                elif (data.currentPokemon > skip and key[pygame.K_LEFT]):
                    data.currentPokemon -= skip
                    pygame.time.wait(timeWait)
                elif (key[pygame.K_RETURN]):
                   data.mode= 2.5
                   pygame.time.wait(timeWait)
            else:
                if((key[pygame.K_RETURN] or key[pygame.K_SPACE] or key[pygame.K_BACKSPACE] or key[pygame.K_UP] or key[pygame.K_DOWN]) and data.samePokemon):
                    data.samePokemon = False
                    pygame.time.wait(timeWait)
            #image
            data.allPokemon[data.currentPokemon].draw(data.screen,(data.width/7,data.height/4.5))
            pokemonArray = data.currParty.toArray()
            #draw party
            for i in range(len(pokemonArray)):
                image = pokemonArray[i].image
                scale = 8.5
                image = pygame.transform.scale(image,(int(data.width/scale),int(data.height/scale)))
                irect = image.get_rect()
                data.screen.blit(image,(data.width/2.35+(data.width/10)*i-irect[2]/2,data.height/2.6-irect[3]/2))
            #pokedex entries
            for i in range(6):
                name= ""
                pokemonExists = False
                if(data.currentPokemon+i-2>=1 and data.currentPokemon+i-2<=data.pokemonMax):
                    num = "%03d" % (data.currentPokemon+i-2,)
                    name = num+" "+str(data.allPokemon[int(data.currentPokemon+i-2)].stats['forms'][0]['name']).upper()
                    if(data.allPokemon[data.currentPokemon+i-2] in pokemonArray):
                        pokemonExists = True
                        #name += " X"*data.currParty.toArray().count(data.allPokemon[data.currentPokemon+i-2])
                if(i==2):
                    data.currPokedex.append(pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.yellow, name,w=0.9 * data.width,h=data.height / 15, textSize=10))
                else:
                    data.currPokedex.append(pokedexEntry(0.5*data.width,i*data.height/12+0.51*data.height,color.lightRed,name,w=0.9*data.width,h = data.height/15,textSize=10))
                if(name!="" and pokemonExists):
                    data.currPokedex[i].draw((data.currPokedex[i].x+0.025*data.currPokedex[i].rect[2],\
                                         data.currPokedex[i].y+(data.currPokedex[i].rect[3]-data.currPokedex[i].text.label.get_rect()[3])/0.8),caught = True)

                elif(name!=""):
                    data.currPokedex[i].draw((data.currPokedex[i].x + 0.025 * data.currPokedex[i].rect[2], \
                                         data.currPokedex[i].y + (data.currPokedex[i].rect[3] - data.currPokedex[i].text.label.get_rect()[3]) / 0.8))
            data.currPokedex = []
            if (key[pygame.K_z] and data.samePokemon==False):
                oldLen = len(pokemonArray)
                if(data.allPokemon[data.currentPokemon] in pokemonArray):
                    data.samePokemon = True
                elif (oldLen < 6):
                    data.currParty.add(data.allPokemon[data.currentPokemon])
                    data.mode = 2.1
                    continue
                else:
                    data.mode= 2.2
                    continue
            elif(key[pygame.K_BACKSPACE] and data.samePokemon==False):
                if(data.allPokemon[data.currentPokemon] in pokemonArray):
                    index = pokemonArray.index(data.allPokemon[data.currentPokemon])
                    data.currParty.remove(index)
                else:
                    data.mode = 0
                pygame.time.wait(timeWait)
            if(data.samePokemon):
                disp = Button(data.width / 2, data.height / 2, color.black, "Can't Add!", w=data.width / 2, h=data.width / 3, textbox=True)
                disp.draw()
            rectH = data.height/15
            offset = (data.currentPokemon-1)*(0.625*data.height-data.height/15)/(data.pokemonMax-1)
            pygame.draw.rect(data.screen,color.white,(0.965*data.width,0.35*data.height,0.025*data.width,0.625*data.height))
            pygame.draw.rect(data.screen,color.lightRed,(0.965*data.width,0.35*data.height+offset,0.025*data.width,rectH))
        elif (data.mode==2.1): #
            pokedex = pygame.image.load("Media/pokedex.png")
            # Home Button
            data.screen.blit(data.background, data.background.get_rect())
            data.screen.blit(pokedex, (data.width / 2.6, data.height / 15))
            home = Button(data.width / 9, data.height / 15, color.black, "Home", w=0.17 * data.width, h=0.06 * data.height)
            if (home.handle_mouse()):
                data.mode= 0
                continue
            home.draw()
            # key code
            key = pygame.key.get_pressed()
            # global data.currentPokemon
            if (key[pygame.K_RETURN] or key[pygame.K_SPACE] or key[pygame.K_BACKSPACE] or key[pygame.K_UP] or key[pygame.K_DOWN]):
                data.mode = 2
                pygame.time.wait(timeWait)
                continue
            # image
            data.allPokemon[data.currentPokemon].draw(data.screen, (data.width / 7, data.height / 4.5))
            pokemonArray = data.currParty.toArray()
            # draw party
            for i in range(len(pokemonArray)):
                image = pokemonArray[i].image
                scale = 8.5
                image = pygame.transform.scale(image, (int(data.width / scale), int(data.height / scale)))
                irect = image.get_rect()
                data.screen.blit(image, (data.width / 2.35 + (data.width / 10) * i - irect[2] / 2, data.height / 2.6 - irect[3] / 2))
            # pokedex entries
            for i in range(6):
                name = ""
                pokemonExists = False
                if (data.currentPokemon + i - 2 >= 1 and data.currentPokemon + i - 2 <= data.pokemonMax):
                    num = "%03d" % (data.currentPokemon + i - 2,)
                    name = num + " " + str(
                        data.allPokemon[int(data.currentPokemon + i - 2)].stats['forms'][0]['name']).upper()
                    if (data.allPokemon[data.currentPokemon + i - 2] in pokemonArray):
                        pokemonExists = True
                        # name += " X"*data.currParty.toArray().count(data.allPokemon[data.currentPokemon+i-2])
                if (i == 2):
                    data.currPokedex.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.yellow, name,
                                     w=0.9 * data.width, h=data.height / 15, textSize=10))
                else:
                    data.currPokedex.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.lightRed, name,
                                     w=0.9 * data.width, h=data.height / 15, textSize=10))
                if (name != "" and pokemonExists):
                    data.currPokedex[i].draw((data.currPokedex[i].x + 0.025 * data.currPokedex[i].rect[2], \
                                         data.currPokedex[i].y + (
                                         data.currPokedex[i].rect[3] - data.currPokedex[i].text.label.get_rect()[3]) / 0.8),
                                        caught=True)

                elif (name != ""):
                    data.currPokedex[i].draw((data.currPokedex[i].x + 0.025 * data.currPokedex[i].rect[2], \
                                         data.currPokedex[i].y + (
                                         data.currPokedex[i].rect[3] - data.currPokedex[i].text.label.get_rect()[3]) / 0.8))
            data.currPokedex = []
            disp = Button(data.width / 2, data.height / 2, color.black, "Added!", w=data.width / 2, h=data.width / 3,textbox=True)
            disp.draw()
            rectH = data.height / 15
            offset = (data.currentPokemon - 1) * (0.625 * data.height - data.height / 15) / (data.pokemonMax - 1)
            pygame.draw.rect(data.screen, color.white,
                             (0.965 * data.width, 0.35 * data.height, 0.025 * data.width, 0.625 * data.height))
            pygame.draw.rect(data.screen, color.lightRed,
                             (0.965 * data.width, 0.35 * data.height + offset, 0.025 * data.width, rectH))
        elif (data.mode==2.2): #
            pokedex = pygame.image.load("Media/pokedex.png")
            # Home Button
            data.screen.blit(data.background, data.background.get_rect())
            data.screen.blit(pokedex, (data.width / 2.6, data.height / 15))
            home = Button(data.width / 9, data.height / 15, color.black, "Home", w=0.17 * data.width, h=0.06 * data.height)
            if (home.handle_mouse()):
                data.mode= 0
                continue
            home.draw()
            # key code
            key = pygame.key.get_pressed()
            # global data.currentPokemon
            if(key[pygame.K_RETURN] or key[pygame.K_SPACE] or key[pygame.K_BACKSPACE] or key[pygame.K_UP] or key[pygame.K_DOWN]):
                data.mode= 2
                pygame.time.wait(timeWait)
                continue
            # image
            data.allPokemon[data.currentPokemon].draw(data.screen, (data.width / 7, data.height / 4.5))
            pokemonArray = data.currParty.toArray()
            # draw party
            for i in range(len(pokemonArray)):
                image = pokemonArray[i].image
                scale = 8.5
                image = pygame.transform.scale(image, (int(data.width / scale), int(data.height / scale)))
                irect = image.get_rect()
                data.screen.blit(image, (data.width / 2.35 + (data.width / 10) * i - irect[2] / 2, data.height / 2.6 - irect[3] / 2))
                # pokedex entries
            for i in range(6):
                name = ""
                pokemonExists = False
                if (data.currentPokemon + i - 2 >= 1 and data.currentPokemon + i - 2 <= data.pokemonMax):
                    num = "%03d" % (data.currentPokemon + i - 2,)
                    name = num + " " + str(
                        data.allPokemon[int(data.currentPokemon + i - 2)].stats['forms'][0]['name']).upper()
                    if (data.allPokemon[data.currentPokemon + i - 2] in pokemonArray):
                        pokemonExists = True
                        # name += " X"*data.currParty.toArray().count(data.allPokemon[data.currentPokemon+i-2])
                if (i == 2):
                    data.currPokedex.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.yellow, name,
                                     w=0.9 * data.width, h=data.height / 15, textSize=10))
                else:
                    data.currPokedex.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.lightRed, name,
                                     w=0.9 * data.width, h=data.height / 15, textSize=10))
                if (name != "" and pokemonExists):
                    data.currPokedex[i].draw((data.currPokedex[i].x + 0.025 * data.currPokedex[i].rect[2], \
                                         data.currPokedex[i].y + (
                                         data.currPokedex[i].rect[3] - data.currPokedex[i].text.label.get_rect()[3]) / 0.8),
                                        caught=True)

                elif (name != ""):
                    data.currPokedex[i].draw((data.currPokedex[i].x + 0.025 * data.currPokedex[i].rect[2], \
                                         data.currPokedex[i].y + (
                                         data.currPokedex[i].rect[3] - data.currPokedex[i].text.label.get_rect()[3]) / 0.8))
            data.currPokedex = []
            disp = Button(data.width / 2, data.height / 2, color.black, "No Space!", w=data.width / 2, h=data.width / 3,textbox=True)
            disp.draw()
            rectH = data.height / 15
            offset = (data.currentPokemon - 1) * (0.625 * data.height - data.height / 15) / (data.pokemonMax - 1)
            pygame.draw.rect(data.screen, color.white,
                             (0.965 * data.width, 0.35 * data.height, 0.025 * data.width, 0.625 * data.height))
            pygame.draw.rect(data.screen, color.lightRed,
                             (0.965 * data.width, 0.35 * data.height + offset, 0.025 * data.width, rectH))
        elif(data.mode==2.5): #Pokemon Info
            num = "%03d" % (data.currentPokemon ,)
            name = num + "  " + str(data.allPokemon[int(data.currentPokemon)].stats['forms'][0]['name']).upper()
            data.screen.blit(data.background, data.background.get_rect())
            #move between pokemon
            skip = 5
            if (data.currentPokemon < data.pokemonMax and key[pygame.K_DOWN]):
                data.currentPokemon += 1
                pygame.time.wait(timeWait+20)
            if (data.currentPokemon > 1 and key[pygame.K_UP]):
                pygame.time.wait(timeWait+20)
                data.currentPokemon -= 1
            if (data.currentPokemon <= data.pokemonMax - skip and key[pygame.K_RIGHT]):
                data.currentPokemon += skip
                pygame.time.wait(timeWait)
            if (data.currentPokemon > skip and key[pygame.K_LEFT]):
                data.currentPokemon -= skip
                pygame.time.wait(timeWait)
            if (key[pygame.K_RETURN]):
                data.mode= 2.5
            if(key[pygame.K_BACKSPACE]):
                data.mode= 2
                pygame.time.wait(50)
                continue
            # Back Button
            back = Button(data.width / 9, data.height / 15, color.black, "Back", w=0.17 * data.width, h=0.06 * data.height)
            if (back.handle_mouse()):
                data.mode= 2
                pygame.time.wait(50)
                continue
            back.draw()
            # image
            data.allPokemon[data.currentPokemon].draw(data.screen, (data.width / 7, data.height / 4.5))
            #pokemon name
            nameLabel = Text(name,(data.width*.65,data.height*0.1),size=50)
            nameLabel.draw()
            #types
            types = ""
            for type in data.allPokemon[data.currentPokemon].stats['types']:
                types+=str(type['type']['name'])+" | "
                pass
            types = types[:len(types)-3]
            typesLabel = Text(types.upper(),(data.width*.7,data.height*0.21),size = 35)
            typesLabel.draw()
            #data.height/weight
            if(data.units=='metric'):
                #data.height
                height = "Height: "+str(data.allPokemon[data.currentPokemon].stats['height']/10)+" METERS"
                Text(height.upper(),(data.width/2.4,data.height/2.8),size = 30,topmode=True).draw()
                # weight
                weight = "Weight: " + str(data.allPokemon[data.currentPokemon].stats['weight'] / 10) + " KG"
                Text(weight.upper(), (data.width / 2.4, data.height / 2.4), size=30, topmode=True).draw()
            else:
                # data.height
                num = "%0.2f" % (data.allPokemon[data.currentPokemon].stats['height']*3.28 / 10)
                height = "Height: " + num + " FEET"
                Text(height.upper(), (data.width / 2.4, data.height / 2.8), size=30, topmode=True).draw()
                # weight
                num = "%0.2f" % (data.allPokemon[data.currentPokemon].stats['weight']*2.2 / 10)
                weight = "Weight: " + num + " LBS"
                Text(weight.upper(), (data.width / 2.4, data.height / 2.4), size=30, topmode=True).draw()
            #abilities
            abilities = "ABILITIES: "
            for i in range(len(data.allPokemon[data.currentPokemon].stats['abilities'])-1,-1,-1):
                abilities+=data.allPokemon[data.currentPokemon].stats['abilities'][i]['ability']['name']
                if i!=0:
                    abilities+=" | "
            abilLabel = Text(abilities.upper(),(data.width/50,data.height/2),topmode=True,size = 24)
            abilLabel.draw()
            #Weakness
            weakList = data.allPokemon[data.currentPokemon].weakness
            weakText = ""
            for i in range(len(weakList)):
                if float(weakList[i])>=2.0:
                    weakText+=indexToType(i,True).upper()+"."+" | "
            weakLabel = Text("WEAKNESSES: "+weakText[:len(weakText)-2], (data.width / 50, data.height / 2 +data.height/15), topmode=True, size=24)
            weakLabel.draw()
            #STATS
            Text("BASE STATS:", (data.width / 50, data.height / 2 + data.height / 15+1.25*data.height/15), topmode=True, size=32.5).draw()
            statNames = ['Spd: ', 'Sp.Def: ', 'Sp.Atk: ', 'Def: ', 'Atk: ', 'HP: ']
            totalStat =0
            for i in range(len(statNames)-1,-1+3,-1):
                text = statNames[i]+str(data.allPokemon[data.currentPokemon].stats['stats'][i]['base_stat'])
                totalStat+=data.allPokemon[data.currentPokemon].stats['stats'][i]['base_stat']
                statlabel = Text(text,(data.width/12+(5-i)*data.width/3,data.height/2+3.25*data.height/15),topmode = True,size = 30)
                statlabel.draw()
            for i in range(len(statNames)-1-3,-1,-1):
                text = statNames[i]+str(data.allPokemon[data.currentPokemon].stats['stats'][i]['base_stat'])
                totalStat += data.allPokemon[data.currentPokemon].stats['stats'][i]['base_stat']
                statlabel = Text(text,(data.width/12+(5-(i+3))*data.width/3,data.height/2+4.25*data.height/15),topmode = True,size = 30)
                statlabel.draw()
            totalStat = "TOTAL: "+str(totalStat)
            Text(totalStat, (data.width / 2, data.height / 2 + data.height / 15 + 5 * data.height / 15), size=30).draw()
        elif(data.mode==3): #Party
            data.screen.blit(data.background, data.background.get_rect())
            if(data.inGame==False):
                # Home Button
                home = Button(data.width / 9, data.height / 15, color.black, "Home", w=0.17 * data.width, h=0.06 * data.height)
                if (home.handle_mouse()):
                    data.mode= 0
                    data.partyMenu = False
                    continue
                home.draw()
            else:
                # Home Button
                back = Button(data.width / 9, data.height / 15, color.black, "Back", w=0.17 * data.width, h=0.06 * data.height)
                if (back.handle_mouse()):
                    data.mode = 4
                    data.partyMenu = False
                    pygame.time.wait(timeWait)
                    continue
                back.draw()
            partyList = data.currParty.toArray()
            # draw party
            for i in range(len(partyList)):
                image = partyList[i].image
                scale = 8.5
                image = pygame.transform.scale(image, (int(data.width / scale), int(data.height / scale)))
                irect = image.get_rect()
                data.screen.blit(image, (data.width / 2.35 + (data.width / 10) * i - irect[2] / 2, data.height / 2.6 - irect[3] / 2))
            Text("PARTY", (2*data.width / 3, data.height / 7), size=70).draw()
            if(len(partyList)>0):
                partyList[data.partyIndex].draw(data.screen, (data.width / 7, data.height / 4.5))
            else:
                Text("NO POKEMON",(data.width/2,data.height/1.5),size=65).draw()
            drawParty = []
            key = pygame.key.get_pressed()
            if(data.partyMenu==False):
                if(key[pygame.K_RETURN] and data.switchMode==False):
                    data.partyMenu = True
                    pygame.time.wait(timeWait)
                    continue
                elif(key[pygame.K_RETURN] and data.switchMode and data.switchIndex!=data.partyIndex):
                    temp = data.currParty.get(data.switchIndex)
                    data.currParty.replace(data.switchIndex,data.currParty.get(data.partyIndex))
                    data.currParty.replace(data.partyIndex,temp)
                    data.switchIndex = 0
                    data.switchMode = False
                    data.oldParty = data.currParty.toArray()
                    pygame.time.wait(timeWait)
                elif(len(partyList)>0 and key[pygame.K_BACKSPACE] and data.switchMode==False and data.inGame==False):
                    data.currParty.remove(data.partyIndex)
                    data.partyIndex = 0
                    pygame.time.wait(timeWait)
                    continue
                elif (len(partyList) > 0 and key[pygame.K_BACKSPACE] and data.switchMode == False and data.inGame):
                    data.mode=4
                    pygame.time.wait(timeWait)
                    continue
                if (data.partyIndex < len(partyList)-1 and key[pygame.K_DOWN]):
                    data.partyIndex += 1
                    if(partyList[data.partyIndex].fainted and data.inGame):
                        data.partyIndex-=1
                    pygame.time.wait(timeWait)
                if (data.partyIndex > 0 and key[pygame.K_UP]):
                    data.partyIndex -= 1
                    if (partyList[data.partyIndex].fainted and data.inGame):
                        data.partyIndex += 1
                    pygame.time.wait(timeWait)
            #pokemon party
            for i in range(len(partyList)):
                num = "Lv."
                if (partyList[i].level != 100):
                    num += "%02d" % (partyList[i].level)
                else:
                    num += "%03d" % (partyList[i].level)
                name = num + " " + str(partyList[i].stats['forms'][0]['name']).upper()
                if(i == data.switchIndex and data.switchMode):
                    drawParty.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.green, name, w=0.9 * data.width,
                                     h=data.height / 15, textSize=10))
                elif (partyList[i].fainted and data.inGame):
                    drawParty.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.blue, name, w=0.9 * data.width,
                                     h=data.height / 15, textSize=10))
                elif (i == data.partyIndex):
                    drawParty.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.yellow, name, w=0.9 * data.width,
                                     h=data.height / 15, textSize=10))
                else:
                    drawParty.append(
                        pokedexEntry(0.5 * data.width, i * data.height / 12 + 0.51 * data.height, color.lightRed, name, w=0.9 * data.width,
                                     h=data.height / 15, textSize=10))
                if(data.inGame==False):
                    if (name != ""):
                        drawParty[i].draw((drawParty[i].x + 0.025 * drawParty[i].rect[2], \
                                             drawParty[i].y + (
                                             drawParty[i].rect[3] - drawParty[i].text.label.get_rect()[3]) / 0.8))
                else:
                    if (name != ""):
                        text = ""
                        if(partyList[i].fainted):
                            text = "FNT"
                        else:
                            text = "HP: "+str(partyList[i].battleStats["HP: "])+"/"+str(partyList[i].finalStats["HP: "])
                        drawParty[i].draw((drawParty[i].x + 0.025 * drawParty[i].rect[2], drawParty[i].y + (drawParty[i].rect[3] - drawParty[i].text.label.get_rect()[3]) / 0.8),health=True,healthString=text)
            if(data.partyMenu and data.switchMode==False):
                disp = Button(data.width / 2, data.height / 2, color.black,"", w=data.width / 2, h=data.width / 3, textbox=True)
                disp.draw()
                menuItems = ["SWITCH","INFO","DELETE"]
                if(data.inGame):
                    menuItems.pop()
                for i in range(len(menuItems)):
                    if(data.partyMenuIndex==i):
                        Text(menuItems[i],(0.57*data.width/2,data.height/2.8+i*data.height/15),size=40,color=color.red,topmode=True).draw()
                    else:
                        Text(menuItems[i], (0.57*data.width / 2, data.height / 2.8 + i * data.height / 15), size=40, color=color.black,topmode=True).draw()
                if(key[pygame.K_BACKSPACE]):
                    data.mode = 3
                    data.partyMenu = False
                    data.partyMenuIndex = 0
                    pygame.time.wait(timeWait)
                if(key[pygame.K_UP] and data.partyMenuIndex>0):
                    data.partyMenuIndex-=1
                    pygame.time.wait(timeWait)
                elif(key[pygame.K_DOWN] and data.partyMenuIndex<len(menuItems)-1):
                    data.partyMenuIndex+=1
                    pygame.time.wait(timeWait)
                if(key[pygame.K_RETURN]):
                    if(data.partyMenuIndex==1):
                        data.mode = 3.5
                    elif (len(partyList) > 0 and data.partyMenuIndex==2):
                        data.currParty.remove(data.partyIndex)
                        data.partyIndex = 0
                        data.partyMenu = False
                    elif(data.partyMenuIndex==0 and data.currParty.len()>1 and data.inGame==False):
                        data.switchMode = True
                        data.switchIndex = data.partyIndex
                        data.partyMenu = False
                    elif(data.partyMenuIndex==0 and data.currParty.len()>1 and data.inGame and data.partyIndex!=0 and data.isFaintedSwitch==False):
                        data.mode=4
                        temp = data.currParty.get(0)
                        data.currParty.replace(0, data.currParty.get(data.partyIndex))
                        data.currParty.replace(data.partyIndex, temp)
                        data.switchIndex = 0
                        data.partyIndex = 0
                        data.partyMenu=False
                        data.skip=True
                        opposingAttackDisplay = True
                    elif (data.partyMenuIndex == 0 and data.currParty.len() > 1 and data.inGame and data.partyIndex != 0 and data.isFaintedSwitch):
                        data.mode = 4
                        temp = data.currParty.get(0)
                        data.currParty.replace(0, data.currParty.get(data.partyIndex))
                        data.currParty.remove(data.partyIndex)
                        data.currParty.add(temp)
                        data.switchIndex = 0
                        data.partyIndex = 0
                        data.partyMenu = False
                        data.skip = False
                        opposingAttackDisplay = False
                        data.isFaintedSwitch = False
                        data.battlemode = 0
                    elif (data.partyMenuIndex == 0 and data.currParty.len() <= 1):
                        data.switchIndex = data.partyIndex
                        data.partyMenu = False
                    pygame.time.wait(timeWait)
        elif(data.mode==3.5):
            pkmn = data.currParty.toArray()[data.partyIndex]
            num= ""
            if(pkmn.level!=100):
                num = "%02d" % (pkmn.level)
            else:
                num = "%03d" % (pkmn.level)
            name = "Lv."+str(num) + "  " + str(pkmn.stats['forms'][0]['name']).upper()
            data.screen.blit(data.background, data.background.get_rect())
            if(key[pygame.K_BACKSPACE]):
                data.mode = 3
                pygame.time.wait(timeWait)
            # Back Button
            back = Button(data.width / 9, data.height / 15, color.black, "Back", w=0.17 * data.width, h=0.06 * data.height)
            if (back.handle_mouse()):
                data.mode= 3
                pygame.time.wait(50)
                continue
            back.draw()
            # image
            pkmn.draw(data.screen, (data.width / 7, data.height / 4.5))
            # pokemon name
            nameLabel = Text(name, (data.width * .625, data.height * 0.1), size=48)
            nameLabel.draw()
            # types
            types = ""
            for type in pkmn.stats['types']:
                types += str(type['type']['name']) + " | "
                pass
            types = types[:len(types) - 3]
            typesLabel = Text(types.upper(), (data.width * .7, data.height * 0.21), size=35)
            typesLabel.draw()
            # STATS
            Text("BATTLE STATS:", (data.width / 50, data.height / 2 + data.height / 15 + 1.25 * data.height / 15), topmode=True,
                 size=32.5).draw()
            statNames = ['Spd: ', 'Sp.Def: ', 'Sp.Atk: ', 'Def: ', 'Atk: ', 'HP: ']
            totalStat = 0
            for i in range(len(statNames) - 1, -1 + 3, -1):
                text = statNames[i] + str(pkmn.finalStats[statNames[i]])
                statlabel = Text(text, (data.width / 12 + (5 - i) * data.width / 3, data.height / 2 + 3.25 * data.height / 15),
                                 topmode=True, size=30)
                statlabel.draw()
            for i in range(len(statNames) - 1 - 3, -1, -1):
                text = statNames[i] + str(pkmn.finalStats[statNames[i]])
                statlabel = Text(text, (data.width / 12 + (5 - (i + 3)) * data.width / 3, data.height / 2 + 4.25 * data.height / 15),topmode=True, size=30)
                statlabel.draw()
            Text("TOTAL: "+str(pkmn.totalStat), (data.width / 2, data.height / 2 + data.height / 15 + 5 * data.height / 15), size=30).draw()
            #moves
            Text("MOVES:", (data.width / 10, data.height / 2 + 0.25 * data.height / 15), topmode=True,
                 size=40).draw()
            for i in range(len(pkmn.moves)):
                formattedMove = pkmn.moves[i].upper()
                formattedMove = formattedMove.replace("-"," ")
                moveBox = pokedexEntry(0.71*data.width,0.38*data.height+data.height/12*i,color.lightRed,formattedMove,w=data.width/2,h=data.height/15,textSize=8)
                moveBox.draw((0.71*data.width,0.38*data.height+data.height/12*i),center = True)
        elif(data.mode==4): #Battle Simulation
            data.screen.blit(data.batGround, data.batGround.get_rect())
            #Home Button
            home = Button(data.width / 9, data.height / 15, color.black, "Home", w=0.17 * data.width, h=0.06 * data.height)
            if (home.handle_mouse()):
                pygame.mixer.music.load('media/music.mp3')
                pygame.mixer.music.play(-1)
                data.mode = 0
                data.battlemode = 0
                other = None
                if(data.opposingParty.len()>0):
                    other = data.opposingParty.toArray()[0]
                    for item in other.finalStats:
                        other.battleStats[item] = other.finalStats[item]
                    for own in data.currParty.toArray():
                        for item in own.finalStats:
                            own.battleStats[item] = own.finalStats[item]
                        own.fainted = False
                    for other in data.opposingParty.toArray():
                        for item in other.finalStats:
                            other.battleStats[item] = other.finalStats[item]
                        other.fainted = False
                resetOpposingParty()
                data.skip = False
                data.inGame = False
                won = False
                lose = False
                ownAttackDisplay = False
                opposingAttackDisplay = False
                data.currParty = structs.party()
                for item in data.oldParty:
                    data.currParty.add(item)
                firstIteration = True
                data.opposingSwitch = False
                data.isFaintedSwitch = False
                data.allOwnFainted = False
                #data.
            home.draw()
            #Draw box
            pygame.draw.rect(data.screen,color.white,(0,0.75*data.height,data.width,0.25*data.height))
            pygame.draw.rect(data.screen, color.black, (0, 0.75 * data.height, data.width, 0.248*data.height),int(data.width/100))
            # Check if pokemon exist
            if (len(data.currParty.toArray()) < 1):
                Text("NO POKEMON", (data.width / 2, data.height / 2), size=65).draw()
            else:
                #Draw Pokemon
                ownPokemons = data.currParty.toArray()
                ownPokemon = data.currParty.toArray()[0]
                #check if all pokemons fainted
                ownPokemon.draw(data.screen,(data.width/15,data.height*0.475+ownPokemonOffset),scale=1.5,back=True)
                Text("Lv."+str(ownPokemon.level)+ " "+ownPokemon.name.upper(),(7*data.width/15,data.height*0.605),topmode=True,size = data.width/15).draw()
                #draw own health bar
                healthRatio = ownPokemon.battleStats["HP: "]/ownPokemon.finalStats["HP: "]
                boxcolor = color.green
                if(healthRatio<0.5 and healthRatio>0.1):
                    boxcolor = color.yellow
                if(healthRatio<=0.1):
                    boxcolor = color.red
                pygame.draw.rect(data.screen, color.white, (7*data.width/15,data.height*0.67,data.width*0.4,data.height*0.04))
                pygame.draw.rect(data.screen, boxcolor, (7*data.width/15, data.height*0.67, data.width*0.4*healthRatio, data.height*0.04))
                Text(str(ownPokemon.battleStats["HP: "]) + "/" + str(ownPokemon.finalStats["HP: "]),
                     (7.1 * data.width / 15, data.height * 0.675), topmode=True, size=data.width / 18).draw()
                #Other Pokemon
                otherPokemons = data.opposingParty.toArray()
                otherPokemon = data.opposingParty.toArray()[0]
                otherPokemon.draw(data.screen, (10*data.width / 15, data.height * 0.1+opposingPokemonOffset), scale=1.5)
                Text("Lv."+str(otherPokemon.level)+ " "+otherPokemon.name.upper(), (1 * data.width / 15,  data.height * 0.125), topmode=True, size=data.width / 15).draw()
                #Text("HP: " + str(otherPokemon.battleStats["HP: "])+"/"+str(otherPokemon.finalStats["HP: "]), (1 * data.width / 15, data.height * 0.2), topmode=True, size=data.width / 15).draw()
                healthRatio = otherPokemon.battleStats["HP: "] / otherPokemon.finalStats["HP: "]
                boxcolor = color.green
                if (healthRatio < 0.5 and healthRatio > 0.1):
                    boxcolor = color.yellow
                if (healthRatio <= 0.1):
                    boxcolor = color.red
                pygame.draw.rect(data.screen, color.white,
                                 (1 * data.width / 15, data.height * 0.18, data.width * 0.4, data.height * 0.04))
                pygame.draw.rect(data.screen, boxcolor, (
                1 * data.width / 15, data.height * 0.18, data.width * 0.4 * healthRatio, data.height * 0.04))
                Text(str(otherPokemon.battleStats["HP: "]) + "/" + str(otherPokemon.finalStats["HP: "]),
                     (1.1 * data.width / 15, data.height * 0.185), topmode=True, size=data.width / 18).draw()
                texts = []
                whoFirst = "own"
                satisfied = False
                moveDamage = {}
                for move in otherPokemon.moves:
                    if move!="---":
                        moveDamage[move] = calculateDamage(ownPokemon,otherPokemon,data.allMoves[move])
                otherMove = "---"
                for key in moveDamage:
                    if(otherMove=="---"):
                        otherMove=key
                    else:
                        if(moveDamage[key]>moveDamage[otherMove]):
                            otherMove=key
                if(otherPokemon.finalStats["Spd: "]>ownPokemon.finalStats["Spd: "]): whoFirst = "other"
                if(data.battlemode==0):
                    texts = [["ATTACK","POKEMON"],["RUN",""]]
                    for i in range(4):
                        if (data.currText[0] * 2 + data.currText[1] * 1 == i):
                            texts[i // 2][i % 2] = Text(texts[i//2][i%2], (
                            i % 2 * data.width / 2 + 0.05 * data.width, i // 2 * data.height / 9 + 0.8 * data.height), size=35,
                                                         color=color.red, topmode=True)
                        else:
                            texts[i // 2][i % 2] = Text(texts[i//2][i%2],
                                                         (i % 2 * data.width / 2 + 0.05 * data.width,
                                                          i // 2 * data.height / 9 + 0.8 * data.height), size=35,
                                                         color=color.black, topmode=True)
                if(data.battlemode==1):
                    # Moves
                    move2d = [["", ""], ["", ""]]
                    for i in range(len(ownPokemon.moves)):
                        updatedText = "---"
                        if(ownPokemon.moves[i]!="---"):
                            updatedText = ownPokemon.moves[i].upper().replace("-", " ")
                        if (data.currMove[0] * 2 + data.currMove[1] * 1 == i):
                            move2d[i // 2][i % 2] = Text(updatedText, (
                            i % 2 * data.width / 2 + 0.05 * data.width, i // 2 * data.height / 9 + 0.8 * data.height), size=35,
                                                         color=color.red, topmode=True)
                        else:
                            move2d[i // 2][i % 2] = Text(updatedText,
                                                         (i % 2 * data.width / 2 + 0.05 * data.width,
                                                          i // 2 * data.height / 9 + 0.8 * data.height), size=35,
                                                         color=color.black, topmode=True)
                    texts = move2d
                textTime = 1.5
                if(ownAttackDisplay == False and opposingAttackDisplay ==False):
                    for i in range(len(texts)):
                        for j in range(len(texts[0])):
                            texts[j][i].draw()
                    key = pygame.key.get_pressed()
                    if(otherTurn==False):
                        #key control
                        if(data.battlemode==1):
                            movement = [0,0]
                            if(key[pygame.K_RIGHT]):
                                if(data.currMove[1]!=1):
                                    data.currMove[1]+=1
                                    movement = [1,1]
                                pygame.time.wait(timeWait-10)
                            elif (key[pygame.K_LEFT]):
                                if (data.currMove[1] != 0):
                                    movement = [1,-1]
                                    data.currMove[1] -= 1
                                pygame.time.wait(timeWait-10)
                            elif (key[pygame.K_DOWN]):
                                if (data.currMove[0] != 1):
                                    movement = [0,1]
                                    data.currMove[0] += 1
                                pygame.time.wait(timeWait-10)
                            elif (key[pygame.K_UP]):
                                if (data.currMove[0] != 0):
                                    movement = [0,-1]
                                    data.currMove[0] -= 1
                                pygame.time.wait(timeWait-10)
                            elif(key[pygame.K_RETURN] and won==False and lose==False and whoFirst == "own"):
                                if (ownPokemon.moves[data.currMove[0] * 2 + data.currMove[1] * 1] != "---"):
                                    ownAttackDisplay = True
                                pygame.time.wait(timeWait)
                            elif (key[pygame.K_RETURN] and won == False and lose == False and whoFirst == "other" and opposingAttackDisplay == False):
                                if (ownPokemon.moves[data.currMove[0] * 2 + data.currMove[1] * 1] != "---"):
                                    opposingAttackDisplay = True
                                pygame.time.wait(timeWait)
                            elif(key[pygame.K_BACKSPACE] and won==False and lose==False):
                                data.battlemode = 0
                                pygame.time.wait(timeWait)
                        elif(data.battlemode==0 and won==False and lose==False):
                            if (key[pygame.K_RIGHT]):
                                if (data.currText[1] != 1 and data.currText!=[1,0]):
                                    data.currText[1] += 1
                                pygame.time.wait(timeWait - 10)
                            elif (key[pygame.K_LEFT]):
                                if (data.currText[1] != 0):
                                    data.currText[1] -= 1
                                pygame.time.wait(timeWait - 10)
                            elif (key[pygame.K_DOWN] and data.currText!=[0,1]):
                                if (data.currText[0] != 1):
                                    data.currText[0] += 1
                                pygame.time.wait(timeWait - 10)
                            elif (key[pygame.K_UP]):
                                if (data.currText[0] != 0):
                                    data.currText[0] -= 1
                                pygame.time.wait(timeWait - 10)
                            elif(key[pygame.K_RETURN]):
                                if(data.currText == [0,0]):
                                    data.battlemode = 1
                                elif(data.currText == [1,0]):
                                    pygame.mixer.music.load('media/music.mp3')
                                    pygame.mixer.music.play(-1)
                                    data.mode = 0
                                    data.battlemode = 0
                                    other = None
                                    if (data.opposingParty.len() > 0):
                                        other = data.opposingParty.toArray()[0]
                                        for item in other.finalStats:
                                            other.battleStats[item] = other.finalStats[item]
                                        for own in data.currParty.toArray():
                                            for item in own.finalStats:
                                                own.battleStats[item] = own.finalStats[item]
                                            own.fainted = False
                                        for other in data.opposingParty.toArray():
                                            for item in other.finalStats:
                                                other.battleStats[item] = other.finalStats[item]
                                            other.fainted = False
                                    resetOpposingParty()
                                    data.skip = False
                                    data.inGame = False
                                    won = False
                                    lose = False
                                    ownAttackDisplay = False
                                    opposingAttackDisplay = False
                                    data.currParty = structs.party()
                                    for item in data.oldParty:
                                        data.currParty.add(item)
                                    firstIteration = True
                                    data.opposingSwitch = False
                                    data.isFaintedSwitch = False
                                    data.allOwnFainted = False
                                    # data.
                                elif(data.currText == [0,1]):
                                    data.mode = 3
                                    data.inGame = True
                                pygame.time.wait(timeWait)
                elif(ownAttackDisplay == True):# and whoFirst == "own"):
                    if(firstIteration):
                        moveInfo = data.allMoves[ownPokemon.moves[data.currMove[0] * 2 + data.currMove[1] * 1]]
                        oldTime = timer
                        firstIteration=False
                        damage = calculateDamage(ownPokemon, otherPokemon, moveInfo)
                        otherPokemon.battleStats['HP: '] -= int(damage)
                        if(damage ==0):
                            data.missed = True
                        if (otherPokemon.battleStats['HP: '] <= 0):
                            otherPokemon.battleStats['HP: '] = 0
                            otherPokemon.fainted = True
                            for pkmn in otherPokemons:
                                if (pkmn.fainted == False):
                                    won = False
                            if (won == False):
                                data.opposingParty.add(otherPokemon)
                                data.opposingParty.remove(0)
                                data.opposingSwitch = True
                    if(timer-oldTime<textTime):
                        if(timer-oldTime<textTime/2):
                            ownPokemonOffset-=1
                            txt = data.allMoves[ownPokemon.moves[data.currMove[0] * 2 + data.currMove[1] * 1]]['name'].upper().replace(
                                "-", " ")
                            Text(ownPokemon.name.upper() + " USED " + txt, (data.width / 2, 0.875 * data.height), size=35).draw()
                        else:
                            ownPokemonOffset+=1
                            if ((data.veryEffective == True or data.notEffective == True) and data.missed == False):
                                effective = "super"
                                if (data.notEffective):
                                    effective = "not very"
                                Text("It's " + effective + " effective!", (data.width / 2, 0.875 * data.height),
                                     size=40).draw()
                            elif(data.missed):
                                Text(ownPokemon.name.upper() + " MISSED! ", (data.width / 2, 0.875 * data.height),
                                     size=40).draw()
                            else:
                                txt = data.allMoves[ownPokemon.moves[data.currMove[0] * 2 + data.currMove[1] * 1]][
                                    'name'].upper().replace("-", " ")
                                Text(ownPokemon.name.upper() + " USED " + txt, (data.width / 2, 0.875 * data.height),
                                     size=35).draw()
                    else:
                        ownPokemonOffset = 0
                        oldTime = 0
                        firstIteration = True
                        ownAttackDisplay = False
                        if(whoFirst=="own" and data.opposingSwitch==False):
                            opposingAttackDisplay = True
                        data.opposingSwitch = False
                        data.notEffective = False
                        data.veryEffective = False
                        data.battlemode = 0
                        data.missed =False
                elif (opposingAttackDisplay == True):# and whoFirst == "other"):
                    if (won):
                        opposingAttackDisplay = False
                    if (firstIteration):
                        if (data.skip):
                            pygame.time.wait(250)
                        opposingCurrentMove = otherMove
                        oldTime = timer
                        firstIteration = False
                        if (won == False and lose == False):
                            damage = calculateDamage(otherPokemon, ownPokemon, data.allMoves[otherMove])
                            ownPokemon.battleStats['HP: '] -= int(damage)
                            if(damage == 0):
                                data.missed = True
                            if(ownPokemon.battleStats['HP: ']<0):
                                ownPokemon.battleStats['HP: '] = 0
                    if (timer - oldTime < textTime):
                        if (timer - oldTime < textTime / 2):
                            txt = data.allMoves[opposingCurrentMove]['name'].upper().replace("-", " ")
                            Text(otherPokemon.name.upper() + " USED " + txt, (data.width / 2, 0.875 * data.height), size=40).draw()
                            opposingPokemonOffset -= 1
                        else:
                            if(data.notEffective == False and data.veryEffective == False and data.missed ==False):
                                txt = data.allMoves[opposingCurrentMove]['name'].upper().replace("-", " ")
                                Text(otherPokemon.name.upper() + " USED " + txt, (data.width / 2, 0.875 * data.height),
                                     size=40).draw()
                            elif(data.missed):
                                txt = data.allMoves[opposingCurrentMove]['name'].upper().replace("-", " ")
                                Text(otherPokemon.name.upper() + " MISSED! " , (data.width / 2, 0.875 * data.height),
                                     size=40).draw()
                            else:
                                eff = "super"
                                if (data.notEffective):
                                    eff = "not"
                                Text("It's " + eff + " effective!", (data.width / 2, 0.875 * data.height), size=40).draw()
                            opposingPokemonOffset += 1
                    else:
                        data.missed = False
                        data.veryEffective = False
                        data.notEffective = False
                        ownPokemonOffset = 0
                        oldTime = 0
                        firstIteration = True
                        opposingAttackDisplay = False
                        if(whoFirst == "other" and data.skip==False):
                            ownAttackDisplay = True
                        if (ownPokemon.battleStats['HP: '] <= 0):
                            firstIteration = True
                            ownAttackDisplay = False
                            ownPokemon.fainted = True
                            data.isFaintedSwitch = True
                            data.mode = 3
                            data.partyIndex = 1
                            data.inGame = True
                        data.skip = False
                if(won and ownAttackDisplay == False and opposingAttackDisplay == False):
                    disp = Button(data.width / 2, data.height / 2, color.black, "You Win", w=data.width / 2, h=data.width / 3, textbox=True)
                    disp.draw()
                    #key = pygame.key.get_pressed()
                elif (lose and ownAttackDisplay == False and opposingAttackDisplay == False):
                    disp = Button(data.width / 2, data.height / 2, color.black, "You Lose", w=data.width / 2, h=data.width / 3, textbox=True)
                    disp.draw()
                    #key = pygame.key.get_pressed()
                lose = True
                for pkmn in ownPokemons:
                    if (pkmn.fainted == False):
                        lose = False
                if(lose==True):
                    if(firstIteration):
                        pygame.mixer.music.load('media/lose.mp3')
                        pygame.mixer.music.play(-1)
                        firstIteration = False
                    data.mode = 4
                    data.partyIndex = 0
                    #opposingAttackDisplay = False
                    #ownAttackDisplay = False
                won = True
                for pkmn in otherPokemons:
                    if (pkmn.fainted == False):
                        won = False
                if (won == True):
                    if(firstIteration):
                        pygame.mixer.music.load('media/won.mp3')
                        pygame.mixer.music.play(-1)
                        firstIteration = False
                    data.mode = 4
                    data.partyIndex = 0
                    #opposingAttackDisplay = False
                    #ownAttackDisplay = False
        if(data.opposingParty.len()!=data.currParty.len()):
            resetOpposingParty()
            data.oldParty = data.currParty.toArray()
        pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("Pokemon Lite")
    def getData(data):
        # data.weaknessChart = pass
        # get moves
        def getMoves(data):
            moves = set()
            data.pokemonMax = 151
            for i in range(1, data.pokemonMax + 1):
                read_dictionary = np.load("Pokemon/Data/" + str(i) + ".npy").item()
                for move in read_dictionary['moves']:
                    moves.add(move['move']['name'])
            if (os.path.isdir("Pokemon/Moves") == False):
                print("missing folder")
                os.makedirs("Pokemon/Moves")
                for item in moves:
                    url = "http://pokeapi.co/api/v2/move/" + str(item)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        print(i)
                        data = response.json()
                        np.save("Pokemon/Data/" + str(i) + ".npy", data)
                    else:
                        print("failed")
                        exit(0)
            else:
                # if folder exists go through all the files inside and check if any is missing
                allExist = True
                missingFiles = []
                for item in moves:
                    if (os.path.exists("Pokemon/Moves/" + str(item) + ".npy") == False):
                        allExist = False
                        missingFiles.append(item)
                if (allExist == False):
                    for item in missingFiles:
                        url = "http://pokeapi.co/api/v2/move/" + str(item)
                        response = requests.get(url)
                        if (response.status_code == 200):
                            data = response.json()
                            np.save("Pokemon/Moves/" + str(item) + ".npy", data)
                        else:
                            print("failed")
                            exit(0)
            for move in moves:
                read_dictionary = np.load("Pokemon/Moves/" + str(move) + ".npy").item()
                data.allMoves[move] = read_dictionary
        getMoves(data)
        # check if pokemon folder exists
        # if no folder create one and run code to find all
        if (os.path.isdir("Pokemon/Data") == False):
            print("missing folder")
            os.makedirs("Pokemon/Data")
            for i in range(1, data.pokemonMax + 1):
                url = "http://pokeapi.co/api/v2/pokemon/" + str(i)
                response = requests.get(url)
                if (response.status_code == 200):
                    print(i)
                    data = response.json()
                    np.save("Pokemon/Data/" + str(i) + ".npy", data)
                else:
                    print("failed")
                    exit(0)
        else:
            # if folder exists go through all the files inside and check if any is missing
            allExist = True
            missingFiles = []
            for i in range(1, data.pokemonMax + 1):
                if (os.path.exists("Pokemon/Data/" + str(i) + ".npy") == False):
                    allExist = False
                    missingFiles.append(i)
            if (allExist == False):
                for item in missingFiles:
                    url = "http://pokeapi.co/api/v2/pokemon/" + str(item)
                    response = requests.get(url)
                    if (response.status_code == 200):
                        data = response.json()
                        np.save("Pokemon/Data/" + str(item) + ".npy", data)
                    else:
                        print("failed")
                        exit(0)
        # load in dictionaries and sprites for pokedex
        for i in range(1, data.pokemonMax + 1):
            read_dictionary = np.load("Pokemon/Data/" + str(i) + ".npy").item()
            data.allPokemon[i] = Pokemon(i, read_dictionary)
        # load in currentParty
        if (os.path.exists("Pokemon/party.npy")):
            numberList = np.load("Pokemon/party.npy")
            for pokemonNum in numberList:
                data.currParty.add(data.allPokemon[pokemonNum])
        # load data.units
        if (os.path.exists("Pokemon/data.units.npy")):
            data.units = np.load("Pokemon/data.units.npy")
    getData(data)
    data.oldParty =data.currParty.toArray()
    resetOpposingParty()
    pygame.mixer.music.load('media/music.mp3')
    pygame.mixer.music.play(-1)
    pyScreen()

main()






