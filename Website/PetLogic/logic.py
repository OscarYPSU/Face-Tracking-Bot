import threading
import time

# Lock to prevent race conditions if other threads read/write these
lock = threading.Lock()

# Pet stats
hunger = 50;      # 0 = full, 100 = starving
health = 100;     # 0 = dead, 100 = healthy
sleepiness = 0;   # 0 = wide awake, 100 = exhausted
happiness = 80; # 0 = Depressed, 50 = content, 100 = happy
# also want to add statuses
age = 0; # add a age system


# use counters to track elapsed time for each stat
last_hunger_update = time.time()
last_happiness_update = time.time()
last_sleep_update = time.time()
last_age_update = time.time()

def getHunger():
    print(f"getHunger:{hunger}\n")
    return hunger

def runPet(): # should be in a multithread
    global hunger, happiness, sleepiness, age, last_age_update, last_happiness_update, last_hunger_update, last_sleep_update
    
    while True: 
        now = time.time()
        # Every 5 minutes hunger goes up by 1
        if now - last_hunger_update >= 5 * 60:
            with lock:
                hunger = min(hunger + 1, 100)
            last_hunger_update = now

        # Every 1 minute happiness goes down by 0.5
        if now - last_happiness_update >= 60:
            with lock:
                happiness = max(happiness - 0.5, 0)
            last_happiness_update = now

        # Every 5 minutes sleepiness goes up by 3
        if now - last_sleep_update >= 5 * 60:
            with lock:
                sleepiness = min(sleepiness + 3, 100)
            last_sleep_update = now
        
        # print(f"current pet stat: hunger = {hunger}, happiness = {happiness}, sleep = {sleepiness}\n")

        time.sleep(1)  # sleep a bit so the loop doesn’t use 100% CPU