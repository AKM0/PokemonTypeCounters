#This script aids the user in pokemon battles by providing 
#the user the best pokemon types for defense and offense agaisnt other types
#programmed by AKM 
#February 17, 2017 - 

#cross platform library used to color console output
from colorama import init, Fore, Back, Style 

#all aliases for attack and defend commands
KNOWN_ATTACK = ["ATTACK" , "TACK", "TAC", "TAK", "ATT", "ATK", "ATC", "AT", "A"] 
KNOWN_DEFEND = ["DEFEND", "FEND", "FEN", "END", "DEF", "DE", "D"]
#18 known pokemon types mirror order of https://img.pokemondb.net/images/typechart.png
KNOWN_TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", 
"GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
#Type:Color dictionary containing unique color codes for all pokemon types
TYPE_COLORS = {} 
#Matrix like structure (dictionary of dictionary) type to type damage values (0.0, 0.5, 1, 2.0)
TYPE_DAMAGE_CHART = {}


#further format user input to determine command types and pokemon types
def parseInput (userInput):
    args = userInput.split(" ", 1) #separate command type from pokemon types
    if len(args) == 2:
        #process command type argument and pokemone types
        commandType = args[0]
        commandType = commandType.strip()
        pokemonTypes = args[1]
        pokemonTypes = pokemonTypes.strip()
        pokemonTypes = pokemonTypes.split(",")
        
        #cycle through types to ensure real types, format types
        cont = True
        for k in range(0, len(pokemonTypes)): 
            pokemonTypes[k] = pokemonTypes[k].strip()
            if pokemonTypes[k] not in KNOWN_TYPES:
                cont = False
                throwWarning(3) #unknown pokemon type
                break
        
        if (cont):
            if (commandType in KNOWN_ATTACK):
                getAttack (pokemonTypes) 
            elif (commandType in KNOWN_DEFEND):
                getDefense (pokemonTypes)
            else:
                throwWarning(1) #command not of type Attack or Defend
    else:
        throwWarning(2) #command type and pokemon types not separeated by space

#prints types assuming types are of user's attacking pokemon
def getAttack(pokemonTypes):
    #render type color strings
    argTypes = printTypes(pokemonTypes)
    print ("Attacking type(s): " + argTypes)
    goodTypes = [] #holds types argTypes is effective against
    badTypes = [] #opposite above
    uglyTypes = [] #types which take no damage
    
    #cycle through all values and sort dmgVals != 1 onto respective lists
    for type in pokemonTypes:
        dmgDict = TYPE_DAMAGE_CHART.get(type)
        for dmgVal in dmgDict:
            dmgMultip = TYPE_DAMAGE_CHART.get(type).get(dmgVal)
            if dmgMultip == 2.0:
                goodTypes.append(dmgVal)
            elif dmgMultip == 0.5:
                badTypes.append(dmgVal)
            elif dmgMultip == 0.0:
                uglyTypes.append(dmgVal)
    
    #remove types appended twice due to multiple argTypes
    goodTypes = list(set(goodTypes))
    badTypes = list(set(badTypes))
    uglyTypes = list (set(uglyTypes))
    
    #remove types present in bad and good because 0.5*2=1, type advantages nullified
    inBoth = []
    for gT in goodTypes: 
        if (gT in goodTypes) and (gT in badTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
        badTypes.remove(iB)
    inBoth = []
    #remove type from good if also immune 
    for gT in goodTypes:
        if (gT in goodTypes) and (gT in uglyTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
    
    print("Strong strong:\n" + printTypes(goodTypes) + Style.RESET_ALL)
    print("Weak against:\n" + printTypes(badTypes) + Style.RESET_ALL)
    print("Types immune:\n" + printTypes(uglyTypes) + Style.RESET_ALL)
    

#prints types assuming types are of the user's defending pokemon
def getDefense(pokemonTypes):
    #render type color strings
    argTypes = printTypes(pokemonTypes)
    print ("Defending type(s): " + argTypes)
    goodTypes = [] #holds type that argTypes is weak against
    badTypes = [] #opposite above
    bestTypes = [] #holds types that are immune to argTypes
    
    #cycle through all values and sort dmgVals != 1 onto respective lists
    for type in pokemonTypes:
        dmgDict = TYPE_DAMAGE_CHART.get(type)
        for dmgVal in dmgDict:
            dmgMultip = TYPE_DAMAGE_CHART.get(type).get(dmgVal)
            if dmgMultip == 0.5:
                goodTypes.append(dmgVal)
            elif dmgMultip == 2.0:
                badTypes.append(dmgVal)
            elif dmgMultip == 0.0:
                bestTypes.append(dmgVal)
    
    #remove types appended twice due to multiple argTypes
    goodTypes = list(set(goodTypes))
    badTypes = list(set(badTypes))
    bestTypes = list (set(bestTypes))
    
    #remove types present in bad and good because 0.5*2=1, type advantages nullified
    inBoth = []
    for gT in goodTypes: 
        if (gT in goodTypes) and (gT in badTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
        badTypes.remove(iB)
    #remove type from bad if it is immune to another type 
    inBoth = []
    for bT in badTypes:
        if (bT in badTypes) and (bT in bestTypes):
            inBoth.append(bT)
    for iB in inBoth:
        badTypes.remove(iB)
    
    print("Immune to:\n" + printTypes(bestTypes) + Style.RESET_ALL)
    print("Strong against:\n" + printTypes(goodTypes) + Style.RESET_ALL)
    print("Weak against:\n" + printTypes(badTypes) + Style.RESET_ALL)
    
    
#generate Gen-6 pokemon type damage matrix
def initDmgChart ():
    #read file of 18 by 18 matrix to populate dict of dict of dmg multipliers
    dmgMatrixFile = open("GEN_6.txt", 'r')
    ln = -1
    for line in dmgMatrixFile:
        ln = ln + 1
        #format line (remove whitespace, special characters, format to uppercase)
        filteredLine = line.strip()
        filteredLine = filteredLine.upper()
        filteredLine = filteredLine.split(" ")
        typeDmgVals = {} #initialize dictionary for particular type
        if (len(filteredLine) != 18):
            print ("Error in type matrix.")
            break
        for k in range(0, len(filteredLine)):
            typeDmgVals[KNOWN_TYPES[k]] = float(filteredLine[k])
        #add dictionary to super dictionary
        TYPE_DAMAGE_CHART[KNOWN_TYPES[ln]] =  typeDmgVals 
    dmgMatrixFile.close()

#throw particular warning or general messages depending on case
def throwWarning (case):
    print(Fore.RED)
    if case == 0: #0 = undefined error
        print("Error in command.\nEnter in format:")
        print("[ATTACK|DEFEND|HELP|QUIT] [TYPE1, TYPE2, ETC.]")
    elif case == 1: #1 = unknown command
        print("Unknown command type.\nKnown commands:\n[ATTACK|DEFEND|HELP|QUIT]")
        print("ATTACK command alias:\n" + ", ".join(KNOWN_ATTACK))
        print("DEFEND command alias:\n" + ", ".join(KNOWN_DEFEND))
    elif case == 2: #2 = incorrect argument formatting
        print("Incorrect arguments.\nCorrect formatting:")
        print("Separate command [ATTACK|DEFEND] and Pokemon types [TYPE1, TYPE2, ETC.] with space [ ].")
        print("Separate Pokemon types [TYPE1, TYPE2, ETC.] with commas [,].")
        print("Example:\nattack ice, water")
    elif case == 3: #3 = unknown pokemon types
        print("Unknown Pokemon type(s). Known types:")
        print(printTypes(KNOWN_TYPES))
    elif case == 4: #4 = help command 
        print("Use:\n[ATTACK|DEFEND|HELP|QUIT] [TYPE1, TYPE2, ETC.]")
        print("Examples:\ndefend ice, water\nd ice, water\nd fire, electric")
        print("attack flying, electric\na ground, rock\natk bug, grass")   
    else:
        print("Error in command.\nEnter in format:")
        print("[ATTACK|DEFEND|HELP|QUIT] [TYPE1, TYPE2, ETC.]")
    print(Style.RESET_ALL)
    
#generate colors for all types (as closely matching as possible)
def initTypeColors ():
    TYPE_COLORS["NORMAL"] = Style.RESET_ALL  + Fore.WHITE 
    TYPE_COLORS["FIRE"] = Style.RESET_ALL  + Fore.RED
    TYPE_COLORS["WATER"] = Style.RESET_ALL  + Fore.BLUE + Style.BRIGHT
    TYPE_COLORS["ELECTRIC"] = Style.RESET_ALL  + Fore.YELLOW + Style.BRIGHT
    TYPE_COLORS["GRASS"] = Style.RESET_ALL  + Fore.GREEN
    TYPE_COLORS["ICE"] = Style.RESET_ALL  + Fore.CYAN + Style.BRIGHT
    TYPE_COLORS["FIGHTING"] = Style.RESET_ALL  + Back.RED + Fore.WHITE 
    TYPE_COLORS["POISON"] = Style.RESET_ALL  + Fore.MAGENTA
    TYPE_COLORS["GROUND"] = Style.RESET_ALL  + Back.YELLOW 
    TYPE_COLORS["FLYING"] = Style.RESET_ALL  + Back.MAGENTA + Fore.WHITE
    TYPE_COLORS["PSYCHIC"] = Style.RESET_ALL  + Fore.MAGENTA + Style.BRIGHT
    TYPE_COLORS["BUG"] = Style.RESET_ALL  + Fore.GREEN + Style.BRIGHT
    TYPE_COLORS["ROCK"] = Style.RESET_ALL  + Fore.YELLOW
    TYPE_COLORS["GHOST"] = Style.RESET_ALL  + Back.MAGENTA + Fore.BLACK + Style.BRIGHT 
    TYPE_COLORS["DRAGON"] = Style.RESET_ALL  + Back.MAGENTA + Fore.BLACK
    TYPE_COLORS["DARK"] = Style.RESET_ALL + Back.WHITE + Fore.BLACK
    TYPE_COLORS["STEEL"] = Style.RESET_ALL  + Fore.BLACK + Style.BRIGHT
    TYPE_COLORS["FAIRY"] = Style.RESET_ALL  + Style.BRIGHT + Back.MAGENTA + Fore.WHITE 

#accepts list of pokemone types and formats them into a colorized string
def printTypes (pokeTypes):
    typeString = ""
    for t in pokeTypes:
        if t != pokeTypes[len(pokeTypes)-1]:
            typeString = typeString + TYPE_COLORS.get(t) + str(t) + Style.RESET_ALL + ", "
        else:
            typeString = typeString + TYPE_COLORS.get(t) + str(t) + Style.RESET_ALL
    return(typeString)
    
init() #initialize colorama
initTypeColors() #initialize Type:Color dictionary
initDmgChart() #initialize matrix of type to type damage values
#main loop
while (True):
    userInput = input(">")
    #format userinput (remove whitespace, special characters, format to uppercase)
    userInput = userInput.strip()
    userInput = " ".join(userInput.split())
    userInput = userInput.upper()
    
    if (userInput == "QUIT" or userInput == "Q"):
        break #quit
    elif (userInput == "HELP" or userInput == "H"):
        throwWarning(4) #provide help page for user
        continue
    elif (userInput == "CLEAR" or userInput == "C"):
        for i in range(0, 1000): #clear screen
            print ("\n\n\n\n\n")
        continue
   
    parseInput(userInput) #parse userInput further
