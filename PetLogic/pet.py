import threading
import time
import pdb


# Lock to prevent race conditions if other threads read/write these
lock = threading.Lock()

class Pet():
    def __init__(self):
        # Pet stats
        self.hunger = 50;      # 0 = full, 100 = starving
        self.health = 100;     # 0 = dead, 100 = healthy
        self.sleepiness = 0;   # 0 = wide awake, 100 = exhausted
        self.happiness = 80; # 0 = Depressed, 50 = content, 100 = happy
        # also want to add statuses
        self.age = 0; # add a age system
        self.status = "" # eg. sleep, playing etc...

        # use counters to track elapsed time for each stat
        self.last_hunger_update = time.time()
        self.last_happiness_update = time.time()
        self.last_sleep_update = time.time()
        self.last_age_update = time.time()
        
        # Lock to prevent race conditions if other threads read/write these
        self.lock = threading.Lock()


    def getHunger(self):
        return self.hunger

    def feed(self):
        self.hunger += 5

    def getHappiness(self):
        return self.happiness

    def play(self):
        self.happiness += 5
    
    def getSleep(self):
        return self.sleepiness

    def ToggleSleep(self):
        if self.status == "sleep":
            self.status = "awake"
        else:
            self.status = "sleep"

        print(f"LOG: pet is {self.status}\n")
            
    def runPet(self): # should be in a multithread        
        while True: 
            now = time.time()
            # Every 5 minutes hunger down by one
            if now - self.last_hunger_update >= 5 * 60:
                with self.lock:
                    self.hunger = min(self.hunger - 1, 100)
                self.last_hunger_update = now

            # Every 1 minute happiness goes down by 0.5
            if now - self.last_happiness_update >= 60:
                with self.lock:
                    self.happiness = max(self.happiness - 0.5, 0)
                self.last_happiness_update = now

            # if pet is asleep, sleepiness would go down periodically instead
            if self.status == "sleep":
                print("LOG:pet is asleep\n")
                if now - self.last_sleep_update >= 5 * 60: # 5 minutes
                    with self.lock:
                        self.sleepiness = max(self.sleepiness - 3, 0)
                    self.last_sleep_update = now
            elif self.status == "awake":
                # Every 5 minutes sleepiness goes up by 3
                if now - self.last_sleep_update >= 5 * 60:
                    with self.lock:
                        self.sleepiness = min(self.sleepiness + 3, 100)
                    self.last_sleep_update = now
            
            # print(f"current pet stat: hunger = {hunger}, happiness = {happiness}, sleep = {sleepiness}\n")

            time.sleep(1)  # sleep a bit so the loop doesn’t use 100% CPU