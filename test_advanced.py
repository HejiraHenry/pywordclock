# WordClock logic for Raspberry Pi
import time
import sys
import datetime
from wordclock import WordClock

def main():
    wc = WordClock()
    now = datetime.datetime.now()
    wc.set_time(now)
    ditl = 1440         # day in the life:  1440 minutes in a day
    while True:
        for i in range(ditl):
            wc.advance_time()
            wc.rotate_color()
            wc.display()
            time.sleep(1)

        for i in range(ditl):
            wc.decrement_time()
            wc.rotate_color()
            wc.display()
            time.sleep(1)


if __name__ == "__main__":
    main()
