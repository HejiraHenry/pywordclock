# WordClock logic for Raspberry Pi
import time
import datetime
import board
import neopixel
import random
import RPi.GPIO as GPIO
from timechange import _linux_set_time
import random



class WordClock:

    def __init__ (self):

        # Initialize the NeoPixels
        pixel_pin = board.D18       # Connect NeoPixels to D10, D12, D18 or D21
        num_pixels = 125            # 11x11 matrix plus 4 dots
        ORDER = neopixel.RGB        # order of pixels RGB or GRB

        self.pixels = neopixel.NeoPixel(pixel_pin, num_pixels, \
            brightness=0.8, auto_write=False, pixel_order=ORDER)

        self.pixels.fill((0, 0, 0)) # Blank entire matrix
        self.pixels.show()


        # Initialize the Buttons
        self.color_button = 17
        self.time_forward_button = 22
        self.time_backward_button = 27

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.color_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.time_forward_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.time_backward_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initialize the Clock

        # Each word is a Tuple, consisting of the row, a string
        # mask of what lights should be on, and the word 
        self.phraseITS  = (0, "11100000000", "ITS") 
        self.phraseOCLOCK = (10, "00000111111","OCLOCK") 
        self.minuteA  = (0, "00001000000","A")
        self.minuteFIVE  = (2, "00000001111","FIVE")
        self.minuteTEN  = (1, "01110000000","TEN")
        self.minuteQUARTER = (1, "00001111111","QUARTER")
        self.minuteTWENTY = (2, "11111100000", "TWENTY")
        self.minuteTWENTYFIVE = (2, "11111101111","TWENTYFIVE")
        self.minuteHALF  = (0, "00000011110","HALF")
        self.minutePAST  = (3, "00000011110", "PAST")
        self.minuteTIL  = (3, "00011100000", "TIL")
        self.hourONE  = (9, "11100000000", "ONE")
        self.hourTWO  = (7, "00000000111", "TWO")
        self.hourTHREE  = (9, "00000011111", "THREE")
        self.hourFOUR  = (10, "11110000000", "FOUR")
        self.hourFIVE  = (7, "11110000000", "FIVE")
        self.hourSIX  = (9, "00011100000", "SIX")
        self.hourSEVEN  = (4, "01111100000", "SEVEN")
        self.hourEIGHT  = (8, "00000011111", "EIGHT")
        self.hourNINE  = (7, "00001111000", "NINE")
        self.hourTEN  = (6, "00000000111", "TEN")
        self.hourELEVEN  = (8, "11111100000", "ELEVEN")
        self.hourNOON  = (4, "00000001111", "NOON")
        self.hourMIDNIGHT = (6, "11111111000", "MIDNIGHT")
        self.dotONE  = (11, "10000000000", "*")
        self.dotTWO  = (11, "11000000000", "* *")
        self.dotTHREE = (11,"11100000000", "* * *")
        self.dotFOUR  = (11,"11110000000", "* * * *")
        self.NULL = (11, "00000000000", "")

        self.numCols = 11
        self.BLANK = (0, 0, 0)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.LIME = (0,255,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)
        self.CYAN = (0,255,255)
        self.MAGENTA = (255,0,255)
        self.SILVER = (192,192,192)
        self.GRAY = (128,128,128)
        self.MAROON = (128,0,0)
        self.OLIVE = (128,128,0)
        self.GREEN = (0,128,0)
        self.PURPLE = (128,0,128)
        self.TEAL = (0,128,128)
        self.NAVY = (0,0,128)
        self.USARMYGOLD = (255, 199, 44)
        self.CADETGRAY = (177, 179, 179)
        self.colors = [ self.WHITE, self.RED, self.LIME, self.USARMYGOLD,
            self.BLUE, self.YELLOW, self.CYAN, self.MAGENTA, self.SILVER, 
            self.GRAY, self.MAROON, self.OLIVE, self.GREEN, self.PURPLE, 
            self.TEAL, self.NAVY, self.CADETGRAY]
        self.color = self.WHITE
        
        self.time = datetime.datetime.strptime('Mar 16 1802  12:00PM', '%b %d %Y %I:%M%p')
        self.blackoutStart = datetime.datetime.strptime('23:00', '%H:%M').time()
        self.blackoutEnd = datetime.datetime.strptime('07:00', '%H:%M').time()


    # Our sole 'setter'
    def set_time(self, time):
        if (type(time) == type(self.time)):
            self.time = time

    # identify the right words for the current hour
    # Some simple pythonic logic, in lieu of a CASE or SWITCH statement
    def clock_hour(self, hour, minute):
        # logic for phrases like  'twenty-five til seven'
        if (minute > 34):
            hour = (hour + 1) % 24

        return {
            0: self.hourMIDNIGHT,
            1: self.hourONE,
            2: self.hourTWO,
            3: self.hourTHREE,
            4: self.hourFOUR,
            5: self.hourFIVE,
            6: self.hourSIX,
            7: self.hourSEVEN,
            8: self.hourEIGHT,
            9: self.hourNINE,
            10: self.hourTEN,
            11: self.hourELEVEN,
            12: self.hourNOON,
            13: self.hourONE,
            14: self.hourTWO,
            15: self.hourTHREE,
            16: self.hourFOUR,
            17: self.hourFIVE,
            18: self.hourSIX,
            19: self.hourSEVEN,
            20: self.hourEIGHT,
            21: self.hourNINE,
            22: self.hourTEN,
            23: self.hourELEVEN
            } [hour]

    # identify the right words for the current minute
    def clock_minute(self, minute):
        minute = minute // 5
        return {
            0: self.NULL,
            1: self.minuteFIVE,
            2: self.minuteTEN,
            3: self.minuteQUARTER,
            4: self.minuteTWENTY,
            5: self.minuteTWENTYFIVE,
            6: self.minuteHALF,
            7: self.minuteTWENTYFIVE,
            8: self.minuteTWENTY,
            9: self.minuteQUARTER,
            10: self.minuteTEN,
            11: self.minuteFIVE
        } [minute]
    
    # identify the right phrase before/after the bottom of the hour
    # top of the hour (e.g. 7:00 - 7:04) no words
    # five after til half past (e.g. 7:05 - 7:34) -> PAST
    # twentyfive til & later -> TIL
    # remember there are up to 4 dots for minutes

    def clock_phrase(self, minute):
        if ((minute < 35) & ( minute >= 5)):  # up to 'half past seven'
            return self.minutePAST
        elif (minute >= 35):
            return self.minuteTIL            # like 'twenty-five til seven'
        else:
            return self.NULL                 # top of the hour

    # return oclock when its appropriate
    def clock_time (self, hour, minute):
        # logic for phrases like  'twenty-five til seven'
        if (minute > 34):
            hour = (hour + 1) % 24
        if ((hour != 12) & ( hour != 0)):
            return self.phraseOCLOCK
        else:
            return self.NULL

    # 4 dots at the bottom
    def clock_dots(self, minute):
        numDots = minute % 5
        return {
            1: self.dotONE,
            2: self.dotTWO,
            3: self.dotTHREE,
            4: self.dotFOUR,
            0: self.NULL
        }[numDots]


    # Simple hack to account for the fact that I 
    # wired the matrix left to right back and forth
    def __serpentine(self, clockTuple):
        row = clockTuple[0]
        word = clockTuple[2]
        if ( int(row) % 2  == 0  ):
            mask = clockTuple[1][::-1]
        else:
            mask = clockTuple[1]
        return (row, mask, word)

    # create a list of the words
    def __clock_matrix(self):
        now = self.time
        led_matrix = []
        led_matrix.append(self.__serpentine(self.phraseITS))
        led_matrix.append(self.__serpentine(self.clock_minute(now.minute)))
        led_matrix.append(self.__serpentine(self.clock_phrase(now.minute)))
        led_matrix.append(self.__serpentine(self.clock_hour(now.hour, now.minute)))
        led_matrix.append(self.__serpentine(self.clock_time(now.hour, now.minute)))
        led_matrix.append(self.clock_dots(now.minute))
        return led_matrix
   

    def display(self):
        matrix = self.__clock_matrix()

        # Console output
        print("-------------------------------------")
        print(self.time.strftime("%H:%M:%S"), end='  |')
        for row in matrix:
            print(row[2], end=' ')
        print() 

        self.pixels.fill(self.BLANK)
        color = self.color
        now = datetime.datetime.now().time()
        
        # Blank out the screen during blackout times
        if ((now > self.blackoutStart) | (now < self.blackoutEnd)):
            color = self.BLANK
        
        
        for row in matrix:
            for column in range (0,self.numCols):
                if (row[1][column] == '1'):
                    num_pixel = (row[0] * self.numCols) + column
                    self.pixels[num_pixel] = color
        self.pixels.show()

    # Advance time -- move time forward a minute
    # Note:  will not work if systemd-timesyncd service is running
    def advance_time(self):
        now = self.time + datetime.timedelta(0,60)
        self.time = now
        _linux_set_time(now.timetuple())

    # Decrement time -- move time backward a minute
    # Note:  will not work if systemd-timesyncd service is running
    def decrement_time(self):
        now = self.time + datetime.timedelta(0,-60)
        self.time  = now
        _linux_set_time(now.timetuple())
    
    # Cycle through available colors
    # shift the color list by one, and pop the leftmost
    def rotate_color(self):
        self.colors = self.colors[1:] + self.colors[:1]
        self.color = self.colors[0]
       


    def check_buttons(self):
        button_state=GPIO.input(self.color_button)
        if button_state == False:
            self.rotate_color()
            time.sleep(0.2)

        button_state=GPIO.input(self.time_forward_button)
        if button_state == False:
            self.advance_time()
            time.sleep(0.2)

        button_state=GPIO.input(self.time_backward_button)
        if button_state == False:
            self.decrement_time()
            time.sleep(0.2)

