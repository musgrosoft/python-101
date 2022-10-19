import utime
from machine import Pin, PWM



class Attractor:
    def __init__(self, point=(0.,1.,1.05), dt=0.01, name="Attractor"):
        self.initial_state = point
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
        self.dt = dt
        self.name = name
        self.x_min = self.x
        self.y_min = self.y
        self.z_min = self.z
        self.x_max = self.x
        self.y_max = self.y
        self.z_max = self.z
        # arbitrary initial range values    
        self.x_range = 100
        self.y_range = 100
        self.z_range = 100
        
    # The range of values produced depends on the parameters and the
    # specifics of the equations. If we know the range, we can then
    # normalise coordinates for use when generating CV. This method
    # runs through a number of iterations to estimate ranges.
    def estimate_ranges(self,steps=100000):
    
        # Execute a number of steps to get upper and lower bounds. 
        for i in range(steps):
            self.step()
            
            self.x_max = max(self.x, self.x_max)
            self.y_max = max(self.y, self.y_max)
            self.z_max = max(self.z, self.z_max)
            self.x_min = min(self.x, self.x_min)
            self.y_min = min(self.y, self.y_min)
            self.z_min = min(self.z, self.z_min)

        self.x_range = self.x_max-self.x_min
        self.y_range = self.y_max-self.y_min
        self.z_range = self.z_max-self.z_min
        
        # Reset to initial parameters
        self.x = self.initial_state[0]
        self.y = self.initial_state[1]
        self.z = self.initial_state[2]
        

    def x_scaled(self):
        return (100.0 * (self.x - self.x_min))/self.x_range

    def y_scaled(self):
        return (100.0 * (self.y - self.y_min))/self.y_range

    def z_scaled(self):
        return (100.0 * (self.z - self.z_min))/self.z_range

    def __str__(self):
        return (f"{self.name:>16} ({self.x:2.2f},{self.y:2.2f},{self.z:2.2f})({self.x_scaled():2.2f},{self.y_scaled():2.2f},{self.z_scaled():2.2f})")
    
    def step(self):
        '''
        Update the point. This needs to be implemented in subclasses. 
        '''
        pass

'''
Implementation of a simple Lorenz Attractor, see 
https://en.wikipedia.org/wiki/Lorenz_system
Default uses well known values of s=10,r=28,b=2.667. 
'''
class Lorenz(Attractor):
    def __init__(self, point=(0.,1.,1.05), params=(10,28,2.667), dt=0.01):
        super().__init__(point, dt, "Lorenz")
        self.s = params[0]
        self.r = params[1]
        self.b = params[2]

    def step(self):
        '''
        Update the point.
        '''
        x_dot = self.s*(self.y - self.x)
        y_dot = self.r*self.x - self.y - self.x*self.z
        z_dot = self.x*self.y - self.b*self.z
        self.x += x_dot * self.dt
        self.y += y_dot * self.dt
        self.z += z_dot * self.dt
        
        
a = 0
#attractor = Attractor()
lorenz = Lorenz()
pwm = PWM(Pin(25))
pwm.freq(1000)

while True:
   
   print(f"{lorenz.x} , {lorenz.y} , {lorenz.z}")
   total = lorenz.x + lorenz.y + lorenz.z
   ledValue = 65025 * total / 100
   pwm.duty_u16(int(ledValue))
   lorenz.step()
   utime.sleep(0.1)
   a += 1
   
   
