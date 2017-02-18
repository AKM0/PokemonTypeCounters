KNOWN_TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", 
"GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
TYPE_CHART = {}

def parseInput (uI):
    args = uI.split(" ", 1)
    if len(args) == 2:
        commandType = args[0]
        commandType = commandType.lstrip()
        #print(commandType)
        pokemonTypes = args[1]
        #print(pokemonTypes)
        pokemonTypes = pokemonTypes.lstrip()
        pokemonTypes = pokemonTypes.split(",")
        
        cont = True
        for t in pokemonTypes: 
            if t not in KNOWN_TYPES:
                cont = False
                continue
        
        if (cont):
            if (commandType == "ATTACK" or commandType == "TACK" or 
            commandType == "ATT" or  commandType == "AT" or commandType == "A"):
                getAttack (pokemonTypes)
            elif (commandType or "DEFEND" or commandType == "DEF" 
            or commandType == "DE" or commandType == "D"):
                getDefense (pokemonTypes)
            else:
                throwError()
        else:
            throwError()
        
    else:
        throwError()
  
def getAttack(pT):
    print ("Attacking with: " + str(pT))
    good = "Strong against:\n"
    bad = "Weak against:\n"
    #ugly = "Immune to:\n" 
    for type in pT:
        strAndWk = TYPE_CHART.get(type) #strengths and weaknesses
        for saw in strAndWk:
            val = TYPE_CHART.get(type).get(saw)
            if val == 2.0:
                good = good + saw + ", "
            elif val == 0.5:
                bad = bad + saw + ", "
            #elif val == 0.0:
                #ugly = ugly + saw + ", "
            
           
    print (good)
    print (bad)
    #print (ugly)
    
      
def getDefense(pT):
    print ("Defending: " + str(pT))

def throwError ():
    print("")
    print("Error in command arguments.\nEnter in format:")
    print("[ATTACK|DEFEND|HELP|QUIT] [TYPE1, TYPE2, ETC.]")
    print("")

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
        for k in range(0, len(filteredLine)):
            typeImpactVals[KNOWN_TYPES[k]] = float(filteredLine[k])
        TYPE_CHART[KNOWN_TYPES[ln]] =  typeImpactVals
    

initChart()    
QUIT = False

while (not QUIT):
    userInput = input("> ")
    #format to uppercase, remove all leading and trailing whitespace
    userInput = userInput.upper()
    userInput = userInput.lstrip()
    
    if (userInput == "QUIT" or userInput == "Q"):
        QUIT = True
        continue
    if (userInput == "HELP" or userInput == "H"):
        throwError()
        continue
   
    parseInput(userInput)
