import sys
import time
import serial
import serial.tools.list_ports as lp
from ctypes import windll

from pcr.constants.config import FILTER_WHEEL, SERVO_MOTOR, LED

# Filter wheel setting values definitions.
COARSE_SPEED            = FILTER_WHEEL["coarse_speed"]
FINE_SPEED              = FILTER_WHEEL["fine_speed"]
MAX_SPEED               = FILTER_WHEEL["max_speed"]
ACCEL = CAM_SETTINGS    = FILTER_WHEEL["accel"]
FILTER_POSITIONS        = FILTER_WHEEL["filter_position"]

# Servo(Opening/Closing) motor setting values definitions.
# Added 240130 YSH
LID_SERVO_POS       = SERVO_MOTOR["lid_heater"]
CHAMBER_SERVO_POS   = SERVO_MOTOR["chamber"]

# LED setting values definitions.
LED_PWMS = LED

def ports():
    return lp.comports()

def valid_ports():
    return [port.name for port in lp.comports() if port.vid == 0x239A and port.pid == 0x80CB]

class SerialTask:
    def __init__(self, serial_port='COM8'):
        try:
            self.ser = serial.Serial(serial_port)
        except:
            windll.user32.MessageBoxW(0, f"Cannot connect serial : {serial_port}", u"PCR Serial error", 0)
        
        #Set motor homming speed
        self.set_coarseSpeed(COARSE_SPEED)
        self.set_fineSpeed(FINE_SPEED)

        #Set motor move speed
        self.set_maxSpeed(MAX_SPEED)
        self.set_accel(ACCEL)
    
        self.go_home()
        print("home done")
        
    def _read_serial(self):
        rsp = self.ser.readline()
        
        if rsp[:2] == b'\xff\xff':
            return rsp[2:].decode().strip()
        
        return None

    def wait_done(self):
        while True:
            if self.ser.in_waiting > 0:
                rsp = self._read_serial()
                print(rsp)
                if rsp == 'done':
                    return
                
    def wait_done_servo(self, cmd, val):
        while True:
            if self.ser.in_waiting > 0:
                rl = self._read_serial()
                print(rl)
                # if rl == f'{cmd} done {val}':
                #     return
                
                # 240130 modified
                if rl == f"done {val}":
                    return
                
                print("done?")
    
    def flush(self):
        while self.ser.in_waiting > 0: # flush
            print(f"-- flush : {self.ser.readline()}")

    def set_coarseSpeed(self, speed):
        cmd = 'H '+str(int(speed)) + '\r\n'
        self.ser.write(cmd.encode())

    def set_fineSpeed(self, speed):
        cmd = 'S '+str(int(speed)) + '\r\n'
        self.ser.write(cmd.encode())

    def set_maxSpeed(self, speed):
        cmd = 'M '+str(int(speed)) + '\r\n'
        self.ser.write(cmd.encode())

    def set_currentPos(self, pos):
        cmd = 'C '+str(int(pos)) + '\r\n'
        self.ser.write(cmd.encode())

    def go_to(self, pos):
        cmd = 'N '+str(int(pos)) + '\r\n'
        self.ser.write(cmd.encode())
        time.sleep(0.002)
        self.wait_done()

    def stop(self):
        self.ser.write('E\r\n'.encode())

    def set_accel(self, acc):
        cmd = 'A '+str(int(acc)) + '\r\n'
        self.ser.write(cmd.encode())

    def go_home(self):
        print('send G')
        self.ser.write('G\r\n'.encode())
        time.sleep(0.002)
        self.wait_done()

    def get_coarseSpeed(self):
        self.ser.write('h\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())

    def get_fineSpeed(self):
        self.ser.write('s\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())

    def get_maxSpeed(self):
        self.ser.write('m\r\n'.encode())
        time.sleep(0.002)
        return float(self._read_serial())

    def get_currentPos(self):
        self.ser.write('c\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())

    def get_accel(self):
        self.ser.write('a\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())

    def isHome(self):
        self.ser.write('o\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())

    '''
    LEDs controll functions
    '''
    def set_LEDPwm(self, pwm):
        cmd = 'P '+str(int(pwm)) + '\r\n'
        print(f"--set_LEDPwm : {cmd}")
        self.ser.write(cmd.encode())

    def get_LEDPwm(self, pwm):
        self.ser.write('p\r\n'.encode())
        time.sleep(0.002)
        return int(self._read_serial())
    
    
    # TODO: Need implementations for servo motor control.
    '''
    Servo motor control.
    '''
    def lid_forward(self):
        print("lid_forward")
        self.ser.write(f"Y {LID_SERVO_POS['forward']}\r\n".encode())
        self.wait_done_servo('Y', LID_SERVO_POS['forward'])
        # time.sleep(5)

    
    def lid_backward(self):
        print("lid_backward")
        self.ser.write(f"Y {LID_SERVO_POS['backward']}\r\n".encode())
        self.wait_done_servo('Y', LID_SERVO_POS['backward'])
        
        # time.sleep(5)

    def chamber_backward(self):
        print("chamber_backward")
        self.ser.write(f"X {CHAMBER_SERVO_POS['backward']}\r\n".encode())
        self.wait_done_servo('X', CHAMBER_SERVO_POS['backward'])
        # time.sleep(5)

    def chamber_forward(self):
        print("chamber_forward")
        self.ser.write(f"X {CHAMBER_SERVO_POS['forward']}\r\n".encode())
        self.wait_done_servo('X', CHAMBER_SERVO_POS['forward'])
        
        
        # time.sleep(5)