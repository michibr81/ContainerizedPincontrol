import json
import time

initialized = False
lockingPins = ""
pins =  ""
allPins = ""
onRaspi = False

def initialize(configJson, runOnRaspi = False ):

    onRaspi = runOnRaspi
    if onRaspi:
        print("Raspi Mode Enabled")
        import RPi.GPIO as GPIO   
    else:
        print("Raspi Mode Disabled") 

    global initialized
    global lockingPins
    global pins
    global allPins

    if initialized == False:

        print("start initialization")

        print("read configuration data")
        with open(configJson, 'r') as file:
            datastore = json.load(file)
            d = datastore["gpioPins"]
        
            lockingPins= d["lockingPins"]
            pins = d["pins"]

        print("configure board/pins")
        if onRaspi:
            GPIO.setmode(GPIO.BOARD)

        print("locking pins...")
        init(lockingPins)

        print("pins...")
        init(pins)

        allPins = lockingPins + pins

        initialized = False


def init(pinGroup):
    alreadyInitialized = []
    for pin in pinGroup:    

        if pin["number"] in alreadyInitialized:
            continue

        print(pin["name"] + ", PinNumber:" + str(pin["number"]) + ", " + pin["gpioType"] + ", Active:" + pin["activeLogic"])
        if pin["gpioType"] == "in":  
            print("GPIO.setup(pin[\"number\"],GPIO.IN)")              
            if onRaspi:
                GPIO.setup(pin["number"],GPIO.IN)
        else:
            print("GPIO.setup(pin[\"number\"],GPIO.OUT)")
            if onRaspi:
                GPIO.setup(pin["number"],GPIO.OUT)
        if pin["activeLogic"] == "high":  
            print("GPIO.output(pin[\"activeLogic\"],GPIO.LOW)")              
            if onRaspi:
                GPIO.output(pin["number"],GPIO.LOW)                
        else:
            print("GPIO.output(pin[\"activeLogic\"],GPIO.HIGH)")
            if onRaspi:
                GPIO.output(pin["number"],GPIO.HIGH)

        alreadyInitialized.append(pin["number"])


def controlPinByName(pinName):
    for pin in allPins:    
        if pin["name"].lower() == pinName.lower():
            print("set pin " + pin["name"] + " wait " + str(pin["timeToHold"]) + " seconds" + " and delay " + str(pin["delayTimeAfterHold"]) + " seconds")
        
            setPin(pin["number"],pin["activeLogic"])
            
            time.sleep(pin["timeToHold"])

            resetPin(pin["number"], pin["activeLogic"])

            time.sleep(pin["delayTimeAfterHold"])

            #return True
    
    return True



def controlPinByNameWithLocking(pinName):
    controlLockingPins()
    return controlPinByName(pinName)


def controlLockingPins():
    for pin in lockingPins:    
        controlPinByName(pin["name"])

def resetPin(number,activeLogic):
    print("reset pin " + str(number))
    if activeLogic == "high":  
        print("GPIO.output(" + str(number) +",GPIO.LOW)")             
        if onRaspi:
            GPIO.output(number,GPIO.LOW)                
    else:
        print("GPIO.output(" + str(number) +",GPIO.HIGH)")
        if onRaspi:
            GPIO.output(number,GPIO.HIGH)

def setPin(number,activeLogic):
    print("set pin " + str(number))
    if activeLogic == "high":  
        print("GPIO.output(" + str(number) +",GPIO.HIGH)")             
        if onRaspi:
            GPIO.output(number,GPIO.HIGH)                
    else:
        print("GPIO.output(" + str(number) +",GPIO.LOW)")
        if onRaspi:
            GPIO.output(number,GPIO.LOW)


initialize("shutterConfiguration.json",True)

#controlPinByNameWithLocking("AllShuttersUp")








