################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pykeyboard import PyKeyboard

k = PyKeyboard()
A_BUTTON = 'm'
B_BUTTON = 'n'
UP_BUTTON = 'w'
DOWN_BUTTON = 's'
LEFT_BUTTON = 'a'
RIGHT_BUTTON = 'd'
SELECT_BUTTON = 't'
START_BUTTON = 'y'
PUNCH_Z_VELOCITY = 500.0
HIGH_PUNCH_HEIGHT = 200.0
PUNCH_GRAB_STRENGTH = 0.5
BLOCK_GRAB_STRENGTH = 0.7
BLOCK_VELOCITY = 300.0
BLOCK_Z_RANGE = 0.3
DODGE_X_VELOCITY = 500.0
UPPERCUT_Y_VELOCITY = 1000.0
SELECT_CIRCLE_LENGTH = 2

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
	controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
	self.move = "none"
	self.previous_move = "none"
	self.keys_tapped = None

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def eval_hand(self, hand):
        if self.move != "none":
	    return
        if hand.palm_velocity.dot(Leap.Vector(0,1,0)) > UPPERCUT_Y_VELOCITY:
	    self.move = "uppercut"
	    return
        if hand.palm_velocity.dot(Leap.Vector(0,0,-1)) > PUNCH_Z_VELOCITY:
	    if hand.grab_strength > PUNCH_GRAB_STRENGTH:
		if hand.palm_position.y > HIGH_PUNCH_HEIGHT:
                    height_string = "high"
		else:
		    height_string = "low"
		if hand.is_left:
		    self.move = "left " + height_string + " punch"
		else:
		    self.move = "right " + height_string + " punch"
		return
	if hand.palm_velocity.dot(Leap.Vector(-1,0,0)) > DODGE_X_VELOCITY:
	    if hand.is_left:
		self.move = "left dodge"
        if hand.palm_velocity.dot(Leap.Vector(1,0,0)) > DODGE_X_VELOCITY:
	    if hand.is_right:
		self.move = "right dodge"

    def check_block(self, hands):
        if len(hands) == 2:
	    for h in hands:
	        if h.grab_strength < BLOCK_GRAB_STRENGTH:
		    return
		if h.palm_velocity.magnitude > BLOCK_VELOCITY:
		    return
		if h.palm_position.z < BLOCK_Z_RANGE:
		    return
            self.move = "block"

    def check_circle(self, frame):
	if len(frame.gestures()) > 0:
	    for g in frame.gestures():
                 if g.type == Leap.Gesture.TYPE_CIRCLE and CircleGesture(g).progress > SELECT_CIRCLE_LENGTH:
		    if g.hands[0].is_left:
		        self.move = "select"
		    else:
		        self.move = "start"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if not frame.hands.is_empty:
            # Get the first hand
	    self.previous_move = self.move
	    self.move = "none"
	    self.check_circle(frame)
            for h in frame.hands:
	        self.eval_hand(h)
	    if self.move == "none":
	        self.check_block(frame.hands)

        if self.keys_tapped != None:
	    self.counter = self.counter - 1
	    if self.counter > 0:
	        return
	    for l in self.keys_tapped:
	        k.release_key(l)
            self.keys_tapped = None

        tapped_keys = None
	if self.previous_move == "block" and self.move != "block":
	    k.release_key(DOWN_BUTTON)
	if self.move != "none" and self.previous_move == "none":
	    if self.move == "select":
	        tapped_keys = SELECT_BUTTON
            elif self.move == "start":
	        tapped_keys = START_BUTTON
	    elif self.move == "left low punch":
	        tapped_keys = B_BUTTON
	    elif self.move == "right low punch":
	        tapped_keys = A_BUTTON
	    elif self.move == "left high punch":
	        tapped_keys = B_BUTTON + UP_BUTTON
	    elif self.move == "right high punch":
	        tapped_keys = A_BUTTON + UP_BUTTON
	    elif self.move == "left dodge":
	        tapped_keys = LEFT_BUTTON
	    elif self.move == "right dodge":
	        tapped_keys = RIGHT_BUTTON
	    elif self.move == "uppercut":
	        tapped_keys = SELECT_BUTTON + START_BUTTON
	    elif self.move == "block":
	        if self.previous_move != "block":
		    k.press_key(DOWN_BUTTON)
	if tapped_keys != None:
	    for l in tapped_keys:
	        k.press_key(l)
	    self.keys_tapped = tapped_keys
	    self.counter = 5
	    # hold key for 2 frames

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
