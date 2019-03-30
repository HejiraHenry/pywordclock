# WordClock logic for Raspberry Pi
import time
import sys
import datetime
from wordclock import WordClock

def main():
    wc = WordClock()
    now = datetime.datetime.now()
    while True:
        wc.set_time(now)
        now = now + datetime.timedelta(0,60)
        wc.display()
        wc.check_buttons()
        time.sleep(1)

if __name__ == "__main__":
    main()
