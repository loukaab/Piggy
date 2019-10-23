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
            self.turn_by_deg(360)
            self.turn_by_deg(-360)
        
            
            
    def moonwalk(self):
        pass

    def macarena(self):
        pass

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
        rd = random.randint(0, 3)
        fun = [self.waggle, self.headshake, self.loopy]

        # Loop to make robot do random dance
        for m in range(3):
            fun[rd]()
            rd = random.randint(0, 3)
        
        
        
        # print("I don't know how to dance. \nPlease give my programmer a zero.")
        

        




    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        print("I can't count how many obstacles are around me. Please give my programmer a zero.")

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")



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
