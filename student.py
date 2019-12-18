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
        self.LEFT_DEFAULT = 100
        self.RIGHT_DEFAULT = 100
        self.SAFE_DIST = 250
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        # self.fullcand[]
        

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
        menu = {"n": ("Autonomous Navigation", self.nav),
                "u": ("User Navigation", self.unav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "h": ("Hold position", self.hold_position),
                "v": ("Veer navigation", self.slither),
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
    
    def hold_position(self):
        startheading = self.get_heading()

        rsave = self.RIGHT_DEFAULT
        lsave = self.LEFT_DEFAULT
        self.LEFT_DEFAULT = 50
        self.RIGHT_DEFAULT = 50

        while True:
            if abs(startheading - self.get_heading()) > 15:
                self.turn_to_deg(startheading)

        self.LEFT_DEFAULT = lsave
        self.RIGHT_DEFAULT = rsave

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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 100):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def largescan(self):
        """Does a wide-ranged scan, and turns robot to hopefully open area"""
        for angle in range(self.MIDPOINT-500, self.MIDPOINT+500, 100):
            self.servo(angle)
            self.wide_scan_data[angle] = self.read_distance()

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

    def quick_check(self):
        # three quick checks
        for ang in range(self.MIDPOINT-150, self.MIDPOINT+151, 150):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False
        return True

    def turn(self, head):
        """Part of program that controls robot's turning function, takes in corner count var"""
        rt = 0
        rc = 0
        lt = 0
        lc = 0
        
        # obtaining distance data to calculate average distance
        for ang, dist in self.wide_scan_data.items():
            if ang < self.MIDPOINT:
                rt += dist
                rc += 1
            else:
                lt += dist
                lc += 1

        # average distance data to find open side
        la = lt / lc
        ra = rt / rc

        # Turns to side that is open
        if la > ra:
            self.turn_by_deg(-22)
            head -= 22

        else:
            self.turn_by_deg(22)
            head += 22

    def forw(self):
        self.fwd()
        time.sleep(.5)
        self.stop()
    
    def back(self):
        self.back()
        time.sleep(.5)
        self.stop()

    def lt(self):
        self.turn_by_deg(-22.5)
    
    def rt(self):
        self.turn_by_deg(22.5)

    def lasteffort(self, leave):
        self.turn_to_deg(leave)
        self.fwd()

    def fullcan(self):
        pass
        """
        for i in range(0, 361, 60):
            self.turn_to_deg(i)
            self.fullcand[i] = self.read_distance()
        
        self.turn_to_deg(i)
        """

    def unav(self):
        print("---------! USER NAVIGATION ACTIVATED !----------\n")
        

        while True:
            umenu = {"f": ("Forward", self.forw),
                    "b": ("Back", self.back),
                    "r": ("Right", self.rt),
                    "l": ("Left", self.lt)
                    }
            # loop and print the menu...
            for key in sorted(umenu.keys()):
                print(key + ":" + umenu[key][0])
            # store the user's answer
            ans = str.lower(input("Your selection: "))
            # activate the item selected
            umenu.get(ans, [None, self.quit])[1]()
    
    def slither(self): 
        """ Practive a smooth veer """
        # write down where we started
        starting_direction = self.get_heading()
        # start driving forward
        self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd()
        # throttle down the left motor
        for power in range(self.LEFT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
            print("throttling down left")

        # throttle up left
        for power in range(31, self.LEFT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
            print("throttling up left")

        # throttle down the right motor
        for power in range(self.RIGHT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
            print("throttling down right")

        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT

        # straighten out
        while self.get_heading() != starting_direction:
            # if I need to veer right
            if self.get_heading() < starting_direction:
                right_speed -= 10
                print("veer right")
            
            # if I need to veer left
            elif self.get_heading() > starting_direction:
                left_speed -= 10
                print("veer left")

            self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
            self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
            time.sleep(.1)

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        
        # these to values allow easier tracking direction to allow a turn bias
        starthead = 180
        currenthead = 180
        exitheading = self.get_heading()

        check = True
        # inital large scan to determine optimal first turn
        self.largescan()
        self.turn(starthead)

        # robot moves fowards until it detects a wall
        while True:
            cc = 0
            self.servo(self.MIDPOINT)
            if self.read_distance() < 1500:
                while self.quick_check():
                    self.fwd()
                    time.sleep(.01)
                self.stop()
                check = False
            else:
                self.fwd()
                time.sleep(1)
                self.stop()
            
            # if robot is facing wildly away from exit, turn towards exit
            if abs(starthead - currenthead) > 90 or self.read_distance() >= 1500:
                self.turn_to_deg(exitheading)
                currenthead = 180

            # traversal
            # magic numbers for counters
            
            while not check:
                self.scan()
                cc += 1
                left_total = 0
                left_count = 0
                right_total = 0
                right_count = 0

                # transversal itself, collects distance and angle data
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

                # if already turned 4 times then do 180 to get out of corner
                if cc >= 4:

                    self.turn_by_deg(90)
                    currenthead += 90
                    if self.quick_check() >= 250:
                        cc = 0
                        check = True

                    self.turn_by_deg(-180)
                    currenthead -= 180
                    if self.quick_check() >= 250:
                        cc = 0
                        check = True

                    self.lasteffort(exitheading)
                        
                    """
                    cc = 0
                    check = True
                    currenthead = 0
                    """    

                # Turns to side that is open with bias towards exit of maze
                elif left_avg > right_avg:
                    self.turn_by_deg(-45)
                    currenthead -= 45


                else:
                    self.turn_by_deg(45)
                    currenthead += 45
                    

                # checks if turned away from wall, if not, add 1 to turn checker and redoes turning protocal
                if self.read_distance() > self.SAFE_DIST:
                    check = True
                else:
                    cc += 1

                if currenthead < 0:
                    currenthead = abs(currenthead)

                

            
            


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
