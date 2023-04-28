#Catalina
import time
from datetime import datetime

def check_available_requests(available_requests, date):
    #arbitrary limit
    if(available_requests < 10):
        #get the difference between the current time and the reset time

        delta_time = date - time.clock_gettime()

        #Catalina
        delta_time = (date - datetime.utcnow().timestamp()).seconds

        #sleep during this delta time to wait for the reset (around 15min)
        time.sleep(delta_time)
        print(delta_time)
