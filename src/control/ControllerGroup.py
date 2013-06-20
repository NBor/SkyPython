'''
Created on 2013-06-09

@author: Neil
'''

from Controller import Controller
from ManualOrientationController import ManualOrientationController
from ZoomController import ZoomController

def create_controller_group():
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
    classdocs
    '''
    def set_enabled(self, enabled_bool):
        for controller in self.controllers:
            controller.enabled = enabled_bool
            
    def set_model(self, m_model):
        for controller in self.controllers:
            controller.model = m_model
            
        self.model = m_model
        self.model.auto_update_pointing = self.using_auto_mode 
        #self.model.set_clock(transitioning_clock)
        
    # Switches to time-travel model and start with the supplied time.
    def go_time_travel(self, date):
        raise NotImplementedError("not finished time stuff")
        #transitioningClock.goTimeTravel(d);
        
    # Gets the id of the string used to display the current speed of time travel.
    def get_current_speed_tag(self):
        #return timeTravelClock.getCurrentSpeedTag();
        raise NotImplementedError("not finished time stuff")
    
    # Sets the model back to using real time.
    def use_real_time(self):
        #transitioningClock.returnToRealTime();
        raise NotImplementedError("not finished time stuff")
    
    # Increases the rate of time travel into the future (or decreases the rate of
    # time travel into the past) if in time travel mode.
    def accelerate_time_travel(self):
        #timeTravelClock.accelerateTimeTravel();
        raise NotImplementedError("not finished time stuff")
    
    # Decreases the rate of time travel into the future (or increases the rate of
    # time travel into the past) if in time travel mode.
    def decelerate_time_travel(self):
        #timeTravelClock.decelerateTimeTravel();
        raise NotImplementedError("not finished time stuff")
    
    # Pauses time, if in time travel mode.
    def pause_time(self):
        #timeTravelClock.pauseTime();
        raise NotImplementedError("not finished time stuff")
    
    # Sets auto mode (true) or manual mode (false).
    def set_auto_mode(self, enabled_bool):
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
            
    # Moves the pointing right and left.
    #
    # @param radians the angular change in the pointing in radians (only
    # accurate in the limit as radians tends to 0.)
    def change_right_left(self, radians):
        self.manual_direction_controller.change_right_left(radians)
    
    # Moves the pointing up and down.
    #
    # @param radians the angular change in the pointing in radians (only
    # accurate in the limit as radians tends to 0.)
    def change_up_down(self, radians):
        self.manual_direction_controller.change_up_down(radians)
    
    # Rotates the view about the current center point.
    def rotate(self, degrees):
        self.manual_direction_controller.rotate(degrees)
    
    # Zooms the user in.
    def zoom_in(self):
        self.zoom_controller.zoom_in()
        
    # Zooms the user out.
    def zoom_out(self):
        self.zoom_controller.zoom_out()
    
    # Sends the astronomer's pointing to the new target.
    # takes the target the destination
    def teleport(self, target):
        #teleportingController.teleport(target)
        raise NotImplementedError("Not done yet")
    
    # Adds a new controller to this group.
    def add_controller(self, controller):
        self.controllers.append(controller)

    def zoom_by(self, ratio):
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
        