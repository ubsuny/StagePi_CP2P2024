import serial
import time
import numpy as np

# from gpiozero.pins.native import NativeFactory
from gpiozero import LED
# factory = NativeFactory()

class E515():
    '''
    Control the piezo stage. Read feedback and write command.
    channel 1  ->  x,  left and right to the lens
    channel 2  ->  z,  up and down
    channel 3  ->  y,  back and forth along the optical path! Might not use this axis
    '''
    def __init__(self,port = '/dev/ttyUSB0',timeout=1, px_trig_pin=4,ln_trig_pin=5,fr_trig_pin=6,volt_threshold = 2, vthreshold=False):  
        # set up the port address and reading data timeout
        '''
        px_trig_pin -> pixel trigger pin number = 4, triggers when it starts to move to the next pixel
        ln_trig_pin -> line trigger pin number = 5, triggers when it starts a line
        fr_trig_pin -> frame trigger pin number = 6, triggers when it stats a frame
        vthreshold -> set True to enable voltage threshold to limit the volt offset, using a while loop, will slow down the piezo movement,
        !! now this only uses before a line or frame scan !!
        volt_threshold -> the voltage threshold value 
        '''
        px_trig_pin=4
        ln_trig_pin=5
        fr_trig_pin=6
        # setup the trigger 
        self.pxtrig = LED(px_trig_pin, pin_factory=factory)
        self.lntrig = LED(ln_trig_pin, pin_factory=factory)
        self.frtrig = LED(fr_trig_pin, pin_factory=factory)
        self.pxtrig.off()
        self.lntrig.off()
        self.frtrig.off()

        # set a endurance between get_pos and set_pos
        self.volt_threshold = volt_threshold
        self.vthreshold = vthreshold

        self.channel = [1,2,3] 		# it represents x,z,y axis
        self.ser = serial.Serial(port=port, baudrate=9600, timeout=timeout, xonxoff=True) 
        # xonxoff is data flow control, if one end is faster than the other one, it will stop transmission till both of them are ready
        self.volt_max = {}
        self.volt_min = {}
        self.volt_offs = {}
        self.writeln('DEV:CONT REM')	# enable to control device remotely
        for ch in self.channel:
            self.writeln('SOUR:VOLT:LIM:HIGH?')		# ??? set up the voltage limit?
            self.volt_max[ch] = float(self.readln())
            self.writeln('SOUR:VOLT:LIM:LOW?')		# ??? set up the voltage limit?
            self.volt_min[ch] = float(self.readln())
            self.writeln('SOUR:VOLT:OFFS?')		# ??? set up the voltage offset?
            self.volt_offs[ch] = float(self.readln())

    def readln(self):
        '''
        read lines until a '/n' encounters
        '''
        return self.ser.read_until()

    def writeln(self, cmd):
        '''
        cmd -> command input
        will write encoded command
        '''
        self.ser.write('{}\n'.format(cmd).encode('utf-8'))

    def close(self):
        '''
        switch to local control and close the port
        '''
        self.writeln('DEV:CONT LOC') 
        self.ser.close
        
    def volt_check(self, pos, channel):
        '''
        check if the voltage is in the range
        '''
        #channel = self.get_channel()
        if self.volt_min[channel] < pos <self.volt_max[channel]:
            pass
        else:
            raise ValueError('Input Voltage is out of the range. Please check the voltage limit.')
            
    def version(self):
        '''
        check the version
        '''
        self.writeln('*IDN?')  # query only
        return self.readln()

    def set_remote(self, rem=True):
        '''
        set it to remote mode
        '''
        if rem:
            print('all SERVO toggle switches have to be set to OFF on the device!!')
            self.writeln('DEV:CONT REM')
        else:
            self.writeln('DEV:CONT LOC')
     
    def get_pos_servo(self, channel=0):
        '''
        get the position using servo (pos signal)
        return: actual position in um
        '''
        if channel == 0:
            self.writeln('MEAS:POS?')
            return float(self.readln())
        elif channel in self.channel:
            self.set_channel(channel)
            self.writeln('MEAS:POS?')
            return float(self.readln())
        else:
            print('channel not available')


    def get_pos(self, channel=0):
        '''
        get the current channel position in voltage signal 
        '''
        if channel == 0: # current channel
            self.writeln('MEAS:VOLT?')
            return float(self.readln())
        elif channel in self.channel:  # switch to the input channel
            self.set_channel(channel)
            self.writeln('MEAS:VOLT?')
            return float(self.readln())
        else:
            print('channel not available')


    def set_pos(self, pos, channel=0):
        '''
        pos  ->  position in voltage, must be in the voltage range
        channel  ->  axis

        set the position at a channel using open-loop,
        where the input to the controller is interpreted 
        as voltage-setting commands and the signal 
        from the position sensor (if any) is not used 
        to refine the position attained
        '''
        
        if channel == 0:  # current channel
            self.writeln('SOUR:VOLT {:.2f}'.format(pos))

        elif channel in self.channel:
            self.set_channel(channel)  # switch to the input channel
            self.writeln('SOUR:VOLT {:.2f}'.format(pos))

        else:
            print('channel not available')
        

    def set_channel(self, channel):
        '''
        set the current channel, have to be 1 or 2 or 3
        channel 1  ->  x,  left and right to the lens
        channel 2  ->  z,  up and down
        channel 3  ->  y,  back and forth along the optical path! Might not use this axis
        '''
        if channel in self.channel:
            self.writeln('INST:SEL Ch{}'.format(channel))
        else:
            print('channel not available')

    def get_channel(self):
        '''
        get the current channel 
        '''
        self.writeln('INST:SEL?')
        return int(self.readln().decode('utf-8')[2])

    def get_servo(self, channel=0):
        '''
        read the current servo-status

        The servo-status corresponds with a 
        hardware switch in the servo-control module. 
        The switch is operated automatically: sending 
        a VOLT-branch command the switch is set to 
        servo-OFF, any POS-branch commands set servo-ON. 
        If the E-515 is set to local mode, the DEV:SERV? 
        query reflects theposition of the toggle switch 
        'open-loop' or 'closed-loop'.
        '''
        if channel == 0: # current channel
            self.writeln('DEV:SERV?')
            return self.readln()
        elif channel in self.channel:  # switch to the input channel
            self.set_channel(channel)
            self.writeln('DEV:SERV?')
            return self.readln()
        else:
            print('channel not available')
    
    def set_volt_threshold(self,threshold):
        self.volt_threshold = threshold
        
    def threshold(self, pos,channel=0):
        if self.vthreshold:
            while abs(self.get_pos(channel) - pos) > self.volt_threshold:
                pass

    def scanline(self,channel,poslist,dwell_time):
        '''
        scan input positions using open-loop (Voltage signal)
        channel  ->  scan axis (only 1 or 2 ; since 3 is the perpendicular axis)
        poslist  ->  position list (all in volt)
        yield: positions after each movement
        '''        
        # set the threshold for the start point
        #self.set_pos(poslist[0],channel)
        #self.threshold(poslist[0],channel)

        self.lntrig.on()
        time.sleep(.1)
        self.lntrig.off()

        for pos in poslist:
            self.set_pos(pos, channel)
            self.pxtrig.blink(on_time=0.05, off_time=0.05, n=1, background=True)
            #time.sleep(.1)
            #print("X: {}".format(pos))
            time.sleep(dwell_time)
            #self.pxtrig.off()
            #yield self.get_pos(1)  
            # use a generator so it won't return all the positions 

    def alt_scanline(self,channel,poslist,dwell_time):
        '''
        scan input positions using open-loop (Voltage signal)
        channel  ->  scan axis (only 1 or 2 ; since 3 is the perpendicular axis)
        poslist  ->  position list (all in volt)
        yield: positions after each movement
        '''        
        # set the threshold for the start point
        #self.set_pos(poslist[0],channel)
        #self.threshold(poslist[0],channel)

        self.set_pos(poslist[0], channel) # set pos first so we can use same channel afterweards
        self.lntrig.on()
        time.sleep(.1)
        self.lntrig.off()
        for pos in poslist:
            self.set_pos(pos, 0) # use zero for same channel
            print("X: {}".format(pos))
            self.pxtrig.on()
            time.sleep(.01)
            self.pxtrig.off()
            time.sleep(dwell_time)
            print("real X: {}".format(self.get_pos(0)))  
            # use a generator so it won't return all the positions 

    def scanframe(self, xpos, ypos, dwell_time=0.1, alt=False):
        '''
        scan in x&z axis (y axis is perpendicular to the lens), using volt signal
        xpos -> horizontal line list containing start stop and step size, channel 1
        ypos -> vertical line list containing start stop and step size, channel 2
        '''
        # setup scanning position arrays
        if dwell_time < 0.1 :
            raise Exception("Minimum Dwell time should be more than 100ms or chnge blink trigger function")
        xnumber = abs(xpos[1]-xpos[0]) / xpos[2] + 1
        ynumber = abs(ypos[1]-ypos[0]) / ypos[2] + 1
        yposs = np.linspace(ypos[0],ypos[1],int(ynumber))
        xposs = np.linspace(xpos[0],xpos[1],int(xnumber))
        
        # move to the start point
        self.set_pos(yposs[0], 3)
        #self.threshold(yposs[0],2)
        
        # start scanning
        self.frtrig.on()
        time.sleep(0.01)
        self.frtrig.off()
        
        for y in yposs:
            self.set_pos(y, 3)
            if alt==True:
                self.alt_scanline(1,xposs, dwell_time)
            else:
                self.scanline(1,xposs, dwell_time)
            print("Y: {}".format(y))
            print("real Y: {} ".format(self.get_pos(3)))

        # json cannot convert numpy arrays so make a list out of it instead
        return [xposs.tolist(), yposs.tolist()] 

    def farmerscanframe(self, xpos, ypos, dwell_time=0.1):
        '''
        scan in x&z axis (y axis is perpendicular to the lens), using volt signal
        xpos -> horizontal line list containing start stop and step size, channel 1
        ypos -> vertical line list containing start stop and step size, channel 2
        '''
        if dwell_time < 0.1 :
            raise Exception("Minimum Dwell time should be more than 100ms or chnge blink trigger function")
        
        # setup scanning position arrays
        xnumber = abs(xpos[1]-xpos[0]) / xpos[2] + 1
        ynumber = abs(ypos[1]-ypos[0]) / ypos[2] + 1
        yposs = np.linspace(ypos[0],ypos[1],int(ynumber))
        xposs = np.linspace(xpos[0],xpos[1],int(xnumber))
        
        # move to the start point
        #self.set_pos(yposs[0], 2)
        #self.threshold(yposs[0],2)
        
        # start scanning
        self.frtrig.on()
        #time.sleep(0.01)
        self.frtrig.off()
        # scan like the farmer is plowing the field
        for j,y in enumerate(yposs):
            self.set_pos(y, 3)
            print("Y: {}".format(y))
            if j % 2 != 0: # flip direction for every seconid line
                 self.scanline(1,np.flip(xposs), dwell_time)
            else:
                 self.scanline(1,xposs, dwell_time)
                 
            #yield self.get_pos(2)

        # frame scan ends
        self.frtrig.on()
        time.sleep(0.1)
        self.frtrig.off()
        # json cannot convert numpy arrays so make a list out of it instead
        return [xposs.tolist(), yposs.tolist()] 

    def get_error(self):
        '''
        reads the error number and error description of the oldest error occured (FIFO)
        return: "error_code", "error description" 
        '''
        self.writeln('SYST:ERR?')
        return self.readln()


  #  def scanline_servo(self,channel,start,stop,step):
'''
        scan input positions using closed-loop (Position signal),
        position sensor is used for refining the position
        ! use actual positions as input !
        
        channel  ->  scan axis
        start  ->  scanning start point
        stop  ->  scanning end point
        step  ->  scanning step size
        yield: positions after each movement

'''
'''            if channel in self.channel: 
                if (self.get_pos() - start) > 1.0: # check if start position is very far off, if so move there first
                    self.set_pos(start, channel)   # set the position
                    print("Moving to start postion: {}".format(start))
                    time.sleep(1.)   # print out the current position
                    print("new pos: {}".format(self.get_pos()))
                try:
                    # setup a position list, including the end point
                    poslist = np.concatenate((np.arange(start,stop,step),np.array([stop])))
                except:
                    raise ValueError('please input correct positions and step size')

                for pos in poslist:  # iterate the poslist
                    self.set_pos(pos, channel)
                    yield self.get_pos()  # yeild the current position

            else:  # doesn't have the channel
                print('channel not available')
'''
