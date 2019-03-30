# WordClock logic for Raspberry Pi
import time
import datetime
from wordclock import WordClock

def main():
    wc = WordClock()
    while True:
        wc.set_time(datetime.datetime.now())
        wc.display()
        wc.check_buttons()
        time.sleep(1)

if __name__ == "__main__":
    main()
