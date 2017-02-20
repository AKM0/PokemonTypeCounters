from colorama import init, Fore, Back, Style

KNOWN_ATTACK = ["ATTACK" , "TACK", "TAC", "TAK", "ATT", "ATK", "ATC", "AT", "A"]
KNOWN_DEFEND = ["DEFEND", "FEND", "FEN", "END", "DEF", "DE", "D"]
KNOWN_TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", 
"GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
TYPE_COLORS = {}
TYPE_CHART = {}


def parseInput (uI):
    args = uI.split(" ", 1)
    if len(args) == 2:
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
                throwError(3) #unknown pokemon type
                break
        
        if (cont):
            if (commandType in KNOWN_ATTACK):
                getAttack (pokemonTypes)
            elif (commandType in KNOWN_DEFEND):
                getDefense (pokemonTypes)
            else:
                throwError(1) #unknown command type
    else:
        throwError(2) #TODO, incorrect argument formatting
  
def getAttack(pokemonTypes):
    argTypes = printTypes(pokemonTypes)
    print ("Ally attacking with: " + argTypes)
    goodTypes = []
    badTypes = []
    uglyTypes = []
    
    for type in pokemonTypes:
        strAndWk = TYPE_CHART.get(type) #strengths and weaknesses
        for saw in strAndWk:
            val = TYPE_CHART.get(type).get(saw)
            if val == 2.0:
                goodTypes.append(saw)
            elif val == 0.5:
                badTypes.append(saw)
            elif val == 0.0:
                uglyTypes.append(saw)
    
    goodTypes = list(set(goodTypes))
    badTypes = list(set(badTypes))
    uglyTypes = list (set(uglyTypes))
    
    #remove types present in bad and good, AND good if also in immune
    inBoth = []
    for gT in goodTypes: 
        if (gT in goodTypes) and (gT in badTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
        badTypes.remove(iB)
    inBoth = []
    for gT in goodTypes:
        if (gT in goodTypes) and (gT in uglyTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
    
    print("Ally strong against:\n" + printTypes(goodTypes) + Style.RESET_ALL)
    print("Ally weak against:\n" + printTypes(badTypes) + Style.RESET_ALL)
    print("Foe immune to:\n" + printTypes(uglyTypes) + Style.RESET_ALL)
    
    
def getDefense(pokemonTypes):
    argTypes = printTypes(pokemonTypes)
    print ("Ally defending from: " + argTypes)
    goodTypes = []
    badTypes = []
    bestTypes = []
    
    for type in pokemonTypes:
        strAndWk = TYPE_CHART.get(type) #strengths and weaknesses
        for saw in strAndWk:
            val = TYPE_CHART.get(type).get(saw)
            if val == 0.5:
                goodTypes.append(saw)
            elif val == 2.0:
                badTypes.append(saw)
            elif val == 0.0:
                bestTypes.append(saw)
    
    goodTypes = list(set(goodTypes))
    badTypes = list(set(badTypes))
    bestTypes = list (set(bestTypes))
    
    #remove types present in bad and good, AND good if also in immune
    inBoth = []
    for gT in goodTypes: 
        if (gT in goodTypes) and (gT in badTypes):
            inBoth.append(gT)
    for iB in inBoth:
        goodTypes.remove(iB)
        badTypes.remove(iB)
    inBoth = []
    for bT in badTypes:
        if (bT in badTypes) and (bT in bestTypes):
            inBoth.append(gT)
    for iB in inBoth:
        badTypes.remove(iB)
    
    print("Ally immune to:\n" + printTypes(bestTypes) + Style.RESET_ALL)
    print("Ally strong against:\n" + printTypes(goodTypes) + Style.RESET_ALL)
    print("Ally weak against:\n" + printTypes(badTypes) + Style.RESET_ALL)
    
    
#generate gen 6 chart
def initChart ():
    file = open("GEN_6.txt", 'r')
    ln = -1 #line number
    for line in file:
        ln = ln + 1
        filteredLine = line.strip()
        filteredLine = line.upper()
        #print(filteredLine)
        filteredLine = line.split(" ")
        typeImpactVals = {}
        if (len(filteredLine) != 18):
            print ("Error in type matrix.")
            break
        for k in range(0, len(filteredLine)):
            typeImpactVals[KNOWN_TYPES[k]] = float(filteredLine[k])
        TYPE_CHART[KNOWN_TYPES[ln]] =  typeImpactVals
    file.close()
    
def throwError (case):
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
    
#generate known types and matching color representations
def initKnownTypes ():
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
    
def printTypes (types):
    typeString = ""
    for t in types:
        if t != types[len(types)-1]:
            typeString = typeString + TYPE_COLORS.get(t) + str(t) + Style.RESET_ALL + ", "
        else:
            typeString = typeString + TYPE_COLORS.get(t) + str(t) + Style.RESET_ALL
    return(typeString)
    
init() #init colorama
initKnownTypes()
initChart()    
QUIT = False

while (not QUIT):
    userInput = input(">")
    #format to uppercase, remove all leading and trailing whitespace
    userInput = userInput.strip()
    userInput = " ".join(userInput.split())
    userInput = userInput.upper()
    #print (userInput)
    
    if (userInput == "QUIT" or userInput == "Q"):
        QUIT = True
        continue
    elif (userInput == "HELP" or userInput == "H"):
        throwError(4) #TODO, help with example commands
        continue
    elif (userInput == "CLEAR" or userInput == "C"):
        for i in range(0, 1000):
            print ("\n\n\n\n\n")
        continue
   
    parseInput(userInput)
