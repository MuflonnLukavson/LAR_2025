## Help functions for robot such as bumber button etc

bumper_names = ['LEFT', 'CENTER', 'RIGHT']
state_names = ['RELEASED', 'PRESSED']

button_num = ['Button 1', 'Button 2', 'Button 3']


def bumper_cb(msg):
    """Bumber callback."""
    # msg.bumper stores the id of bumper 0:LEFT, 1:CENTER, 2:RIGHT
    bumper = bumper_names[msg.bumper]

    # msg.state stores the event 0:RELEASED, 1:PRESSED
    state = state_names[msg.state]

    # Print the event
    print('{} bumper {}'.format(bumper, state))

def button_cb(msg):
    """Button callback"""
    # msg.button stores the id of button
    butt = button_num[msg.button]

    # msg.state stores the event 0:RELEASED, 1:PRESSED
    state = state_names[msg.state]
    print('{} {}'.format(butt, state))
