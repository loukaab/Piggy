from teacher import PiggyParent
import random, sys, time


class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
    
    def waggle(self):
        """This makes the robot do the 'waggle' dance """
        # Robot 'waggles' 4 times
        for i in range(2):
            self.turn_to_deg(45)
            time.sleep(.5)
            self.stop()
            self.servo(1750)
            time.sleep(.5)
            self.stop()
            self.turn_by_deg(-90)
            time.sleep(.5)
            self.stop()
            self.servo(1250)
            time.sleep(.5)
            self.stop()

    def headshake(self):
        """Function that makes robot do the 'head shake' """
        # Robot shakes head 4 times
        for i in range(4):
            self.servo(1750)
            self.stop()
            self.servo(1250)
            self.stop()

    def loopy(self):
        """This function makes the robot do loop-dee-loops"""
        
        for s in range(2):
            self.turn_by_deg(350)
            self.turn_by_deg(-350)
        
            
            
    def moonwalk(self):
        self.turn_by_deg(-45)
        self.back()
        time.sleep(.75)
        self.stop()
        self.turn_by_deg(45)
        self.back()
        time.sleep(.75)
        self.stop()

    def macarena(self):
        for i in range(4):
            self.servo(1050)
            self.stop()
            time.sleep(.5)
            self.servo(1950)
            self.stop()
            time.sleep(.5)
            self.turn_by_deg(-45)
            self.stop()
            time.sleep(.5)
            self.turn_by_deg(90)
            self.stop()
            time.sleep(.5)
            self.turn_by_deg(450)

            

    def safe_to_dance(self):
        """360 distance check to see if surroundings are safe for movement"""
        
        for x in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True
                


    def dance(self):
        """A higher numbered algorithm to make robot dance"""
        
        # Check to see if surroundings are safe
        if not self.safe_to_dance():
            print("Are you trying to kill me?")
        else:
            print("Ya know what kid, I like you.")    

        # Calling other dance moves
        # Declare dance randomizer variable and function list
        rd = random.randint(0, 4)
        fun = [self.waggle, self.headshake, self.loopy, self.moonwalk, self.macarena]

        # Loop to make robot do random dance
        for m in range(3):
            fun[4]()
            rd = random.randint(0, 4)
        
        
        
        # print("I don't know how to dance. \nPlease give my programmer a zero.")
        

        




    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 15):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and determines obstacle count"""

        # Setting up magic variables
        found_something = False         # Trigger
        count = 0
        trigger_distance = 250

        # Writing down starting position for storage
        starting_position = self.get_heading()

        # Starting rotation for scanning
        self.right(primary=60, counter=60)

        # While loop for object scanning
        while self.get_heading() != starting_position:
            if self.read_distance() < trigger_distance and not found_something:
                found_something = True
                count += 1
                print("\n Found something!")
            elif self.read_distance() > trigger_distance and found_something:
                found_something = False
                print("\n Seems I have a clear view, resetting trigger")

        self.stop
        print("I found %d objects" % count)
        return count


    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        while True:
            
            while self.read_distance() > 250:
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.scan()

            # traversal
            # magic numbers for counters
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0

            # transversal itself, collects distance and ange data
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT:
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1

            # average distance data to find open side
            left_avg = left_total / left_count
            right_avg = right_total / right_count

            # Turns to side that is open
            if left_avg > right_avg:
                self.turn_by_deg(-45)
            else:
                self.turn_by_deg(45)


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
