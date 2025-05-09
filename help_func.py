## Help functions for robot such as bumber button etc

bumper_names = ['LEFT', 'CENTER', 'RIGHT']
state_names = ['RELEASED', 'PRESSED']

button_num = ['Button 1', 'Button 2', 'Button 3']

class Security():
    def __init__(self):
        self.button_pressed = True # TODO change to FALSE
        self.bumper = False
        self.bumped2obst = False

    def bumper_cb(self, msg):
        """Bumber callback."""
        # msg.bumper stores the id of bumper 0:LEFT, 1:CENTER, 2:RIGHT
        bumper = bumper_names[msg.bumper]

        # msg.state stores the event 0:RELEASED, 1:PRESSED
        state = state_names[msg.state]

        # Print the event
        print('DEBUG: {} bumper {}'.format(bumper, state))
        if bumper == 1:
            self.bumper = True
            self.bumped2obst = True
        else:
            self.bumper = False 

    def button_cb(self, msg):
        """Button callback"""
        # msg.button stores the id of button
        butt = button_num[msg.button]

        # msg.state stores the event 0:RELEASED, 1:PRESSED
        state = state_names[msg.state]
        print('DEBUG: {} {}'.format(butt, state))
        self.button_pressed = True
