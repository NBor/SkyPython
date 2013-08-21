'''
Created on 2013-06-09

@author: Neil
'''

from Controller import Controller
from ManualOrientationController import ManualOrientationController
from ZoomController import ZoomController

def create_controller_group():
    '''
    Creates an instance of a controller group and provides it
    with the necessary controllers to allow for manipulation
    of the appearance of the sky. This class is both a factory
    and a facade for the underlying controllers
    '''
    group = ControllerGroup()
    
#     group.addController(new LocationController(context));
#     group.sensorOrientationController = new SensorOrientationController(context);
#     group.addController(group.sensorOrientationController);
    group.manual_direction_controller = ManualOrientationController()
    group.add_controller(group.manual_direction_controller)
    group.zoom_controller = ZoomController()
    group.add_controller(group.zoom_controller)
#     group.teleportingController = new TeleportingController();
#     group.addController(group.teleportingController);
    group.set_auto_mode(True)

    return group

class ControllerGroup(Controller):
    '''
    Class which holds all the controllers and provides
    methods for using the controllers. This way there
    is one collection of controllers that can be used
    centrally.
    '''
    def set_enabled(self, enabled_bool):
        '''
        enables or disables all controllers
        '''
        for controller in self.controllers:
            controller.enabled = enabled_bool
            
    def set_model(self, m_model):
        '''
        Provides all controllers with access to the model.
        '''
        for controller in self.controllers:
            controller.model = m_model
            
        self.model = m_model
        self.model.auto_update_pointing = self.using_auto_mode 
        #self.model.set_clock(transitioning_clock)
        
    def go_time_travel(self, date):
        '''
        Switches to time-travel model and start with the supplied time.
        '''
        raise NotImplementedError("not finished time stuff")
        #transitioningClock.goTimeTravel(d);
        
    def get_current_speed_tag(self):
        '''
        Gets the id of the string used to display the current speed of time travel.
        '''
        #return timeTravelClock.getCurrentSpeedTag();
        raise NotImplementedError("not finished time stuff")
    
    def use_real_time(self):
        '''
        Sets the model back to using real time.
        '''
        #transitioningClock.returnToRealTime();
        raise NotImplementedError("not finished time stuff")
    
    def accelerate_time_travel(self):
        '''
        Increases the rate of time travel into the future (or decreases the rate of
        time travel into the past) if in time travel mode.
        '''
        #timeTravelClock.accelerateTimeTravel();
        raise NotImplementedError("not finished time stuff")
    
    def decelerate_time_travel(self):
        '''
        Decreases the rate of time travel into the future (or increases the rate of
        time travel into the past) if in time travel mode.
        '''
        #timeTravelClock.decelerateTimeTravel();
        raise NotImplementedError("not finished time stuff")
    
    def pause_time(self):
        '''
        Pauses time, if in time travel mode.
        '''
        #timeTravelClock.pauseTime();
        raise NotImplementedError("not finished time stuff")
    
    def set_auto_mode(self, enabled_bool):
        '''
        Sets auto mode (true) or manual mode (false).
        '''
        self.manual_direction_controller.enabled = (not enabled_bool)
        #sensorOrientationController.setEnabled(enabled_bool)
        if self.model != None:
            self.model.auto_update_pointing = enabled_bool
        self.using_auto_mode = enabled_bool
        
    def start(self):
        for controller in self.controllers:
            controller.start()
            
    def stop(self):
        for controller in self.controllers:
            controller.stop()
            
    def change_right_left(self, radians):
        '''
        Moves the pointing right and left.
        
        radians is the angular change in the pointing in radians (only
        accurate in the limit as radians tends to 0.)
        '''
        self.manual_direction_controller.change_right_left(radians)
    
    def change_up_down(self, radians):
        '''
        Moves the pointing up and down.
        
        radians is the angular change in the pointing in radians (only
        accurate in the limit as radians tends to 0.)
        '''
        self.manual_direction_controller.change_up_down(radians)
    
    def rotate(self, degrees):
        '''
        Rotates the view about the current center point.
        '''
        self.manual_direction_controller.rotate(degrees)
    
    def zoom_in(self):
        '''
        Zooms the user in.
        '''
        self.zoom_controller.zoom_in()
        
    def zoom_out(self):
        '''
        Zooms the user out.
        '''
        self.zoom_controller.zoom_out()
    
    def teleport(self, target):
        '''
        Sends the astronomer's pointing to the new target.
        takes the target the destination
        '''
        #teleportingController.teleport(target)
        raise NotImplementedError("Not done yet")
    
    def add_controller(self, controller):
        '''
        Adds a new controller to this group.
        '''
        self.controllers.append(controller)

    def zoom_by(self, ratio):
        '''
        Zoomz by a given ratio
        '''
        self.zoom_controller.zoom_by(ratio)

    def __init__(self):
        '''
        Constructor
        '''
        Controller.__init__(self)
        self.controllers = []
        self.zoom_controller = None
        self.manual_direction_controller = None
        self.sensor_orientation_controller = None
        #self.time_travel_clock = TimeTravelClock();
        #self.transitioning_clock = TransitioningCompositeClock(timeTravelClock, RealClock())
        self.teleporting_controller = None
        self.using_auto_mode = True
        