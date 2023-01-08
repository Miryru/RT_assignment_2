#! /usr/bin/env python

import rospy
import math
import time
from assignment_2_2022.msg import Position_velocity


frequency= 1.0
last_printed=0



# Callback function for the info subscriber
def posvel(msg):
	
	global frequency,last_printed
	
	# Compute the period in ms (milliseconds)
	period = (1.0/frequency) * 1000
	
	# Get current time in ms
	current_time = time.time() * 1000
	
	
	if current_time - last_printed > period:
		
		# Get the desired position
		des_x = rospy.get_param("des_pos_x")
		des_y = rospy.get_param("des_pos_y")
		
		# Get the actual position
		x = msg.x
		y = msg.y
		
		# Compute the distance
		distance = math.dist([des_x, des_y], [x, y])
		
		# Compute the average speed
		average_speed = math.sqrt(msg.v_x**2 + msg.v_y**2)
		
		# print info
		print( "Distance between the desired position and the actual position: " ,distance)
		print( "Average speed: " ,average_speed)
		print()
		
		# Update last_printed
		last_printed = current_time
	

def main():
	
	global frequency
	
	# Initialize the node
	rospy.init_node('print_info')
	
	# Get the publishing frequency 
	frequency = rospy.get_param("frequency")
	
	# Subscriber for the position_velocity message
	sub_pos = rospy.Subscriber("/Position_velocity", Position_velocity, posvel)
	
	# Wait
	rospy.spin()
	
if __name__ == "__main__":
	main()	
