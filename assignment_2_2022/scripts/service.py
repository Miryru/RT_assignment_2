#! /usr/bin/env python

import rospy
from assignment_2_2022.srv import goal_srv, goal_srvResponse
import actionlib
import actionlib.msg
import assignment_2_2022.msg

# Variables to store how many times goals were cancelled or reached
cancelled = 0;
reached = 0;

# Callback for result subscriber
def result(msg):
	
	global cancelled, reached
	
	# Get the status of the result from the msg 
	stat = msg.status.status
	
	# If stat is 2, the goal was preempted
	if stat == 2:
		cancelled += 1
	# If stat is 3, the goal was reached
	elif stat == 3:
		reached += 1
		
# Service function
def get_data(req):
	
	global cancelled, reached
	
	# Return the response
	return goal_srvResponse(reached, cancelled)

def main():
	# Initialize the node
	rospy.init_node('service')
	
	# Create the service
	srv = rospy.Service('service', goal_srv, get_data)
	
	# Subscriber for the result of the goal
	sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, result)
	
	# Wait
	rospy.spin()
	
if __name__ == "__main__":
    main()
