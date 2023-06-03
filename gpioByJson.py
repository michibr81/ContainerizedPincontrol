import json
import time
import RPi.GPIO as GPIO
import sys

class gpioByJson:

    initialized = False
    lockingPins = ""
    pins =  ""
    allPins = ""
    dryRun = True
    alreadyInitialized = []

    def __init__(self, dryRun = True):
        self.dryRun = dryRun      

    def initialize(self, configJson):

        if self.initialized == False:

            print("start initialization")

            print("read configuration data")
            with open(configJson, 'r') as file:
                datastore = json.load(file)
                d = datastore["gpioPins"]
            
                self.lockingPins= d["lockingPins"]
                self.pins = d["pins"]

            print("configure board/pins")
            if not self.dryRun:
                GPIO.setmode(GPIO.BOARD)

            print("locking pins...")
            self.init(self.lockingPins)

            print("pins...")
            self.init(self.pins)

            self.allPins = self.lockingPins + self.pins
            initialized = False


    def init(self,pinGroup):
        
        for pin in pinGroup:    

            if pin["number"] in self.alreadyInitialized:
                continue

            print(pin["name"] + ", PinNumber:" + str(pin["number"]) + ", " + pin["gpioType"] + ", Active:" + pin["activeLogic"])
            if pin["gpioType"] == "in":  
                print("GPIO.setup(pin[\"number\"],GPIO.IN)")              
                if not self.dryRun:
                    GPIO.setup(pin["number"],GPIO.IN)
            else:
                print("GPIO.setup(pin[\"number\"],GPIO.OUT)")
                if not self.dryRun:
                    GPIO.setup(pin["number"],GPIO.OUT)
            if pin["activeLogic"] == "high":  
                print("GPIO.output(pin[\"activeLogic\"],GPIO.LOW)")              
                if not self.dryRun:
                    GPIO.output(pin["number"],GPIO.LOW)                
            else:
                print("GPIO.output(pin[\"activeLogic\"],GPIO.HIGH)")
                if not self.dryRun:
                    GPIO.output(pin["number"],GPIO.HIGH)

            self.alreadyInitialized.append(pin["number"])


    def controlPinByName(self,pinName):
        for pin in self.allPins:    
            if pin["name"].lower() == pinName.lower():
                print("set pin " + pin["name"] + " wait " + str(pin["timeToHold"]) + " seconds" + " and delay " + str(pin["delayTimeAfterHold"]) + " seconds")
            
                self.setPin(pin["number"],pin["activeLogic"])
                
                time.sleep(pin["timeToHold"])

                self.resetPin(pin["number"], pin["activeLogic"])

                time.sleep(pin["delayTimeAfterHold"])        
        return True



    def controlPinByNameWithLocking(self,pinName):
        self.controlLockingPins()
        return self.controlPinByName(pinName)


    def controlLockingPins(self):
        for pin in self.lockingPins:    
            self.controlPinByName(pin["name"])

    def resetPin(self,number,activeLogic):
        print("reset pin " + str(number))
        if activeLogic == "high":  
            print("GPIO.output(" + str(number) +",GPIO.LOW)")             
            if not self.dryRun:
                GPIO.output(number,GPIO.LOW)                
        else:
            print("GPIO.output(" + str(number) +",GPIO.HIGH)")
            if not self.dryRun:
                GPIO.output(number,GPIO.HIGH)

    def setPin(self,number,activeLogic):
        print("set pin " + str(number))
        if activeLogic == "high":  
            print("GPIO.output(" + str(number) +",GPIO.HIGH)")             
            if not self.dryRun:
                GPIO.output(number,GPIO.HIGH)                
        else:
            print("GPIO.output(" + str(number) +",GPIO.LOW)")
            if not self.dryRun:
                GPIO.output(number,GPIO.LOW)

if __name__ == '__main__':

    dryRun=False
    configFilePath = "shutterConfiguration.json"
    testControlPath = "OfficeShutterHalfDown"

    # if(len(sys.argv) <= 1):
    #     print(f'Take default')
    # else:
    #     print(f'Given args is {sys.argv[0]} second is {sys.argv[1]}')

    ctrl =  gpioByJson(dryRun=dryRun)
    ctrl.initialize(configFilePath)
    ctrl.controlPinByNameWithLocking(testControlPath)
