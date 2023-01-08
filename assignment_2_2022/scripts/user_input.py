#!/usr/bin/env python

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Position_velocity

 
def pub_values(msg):
	
	global pub
	# Get the position from the msg
	pos = msg.pose.pose.position
	
	# Get the twist from the msg
	velocity = msg.twist.twist.linear
	
	# Create custom message
	position_velocity = Position_velocity()
	
	#Assign the parameters of the custom message
	position_velocity.x=pos.x
	position_velocity.y=pos.y
	position_velocity.v_x=velocity.x
	position_velocity.v_y=velocity.y
	
	# Publish the custom message
	pub.publish(position_velocity)
	
def client():
	
    # Create the action client
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
    
    # Wait for the server 
    client.wait_for_server()

    while not rospy.is_shutdown():
	  
	  #Get the coordinates x,y from the user
      print("\nThis is a simple program which takes coordinates (x, y) and moves a robot to coordinates inside a virtual arena whith some obstacles")
      x_position = float(input("Set a target x: "))
      y_position = float(input("Set a target y: "))
   

	  # Create the goal postion
      goal = assignment_2_2022.msg.PlanningGoal()
      goal.target_pose.pose.position.x = x_position
      goal.target_pose.pose.position.y = y_position

	  # Send the goal to the server
      client.send_goal(goal)
      
      #If the user wants to cancel the goal
      #Give the user 5 seconds to cancel the goal
      print("Enten 'c' to cancel the goal:")
      input1 = select.select([sys.stdin], [], [], 5)[0]
      if input1:
        value = sys.stdin.readline().rstrip()
				  
		 
        if (value == "c"):
		  #Cancel the goal
          print("Goal cancelled.Robot stopped.")
          client.cancel_goal()


    

 


def main():
	#inizialize the node
    rospy.init_node('user_input')

	#global pub
    global pub
    
    #Publisher to send a msg with the velocity and the position parameters
    pub = rospy.Publisher("/Position_velocity", Position_velocity, queue_size = 1)
    
    #Subscriber to get from Odom the velocity and the position parameters
    sub_from_Odom=rospy.Subscriber("/odom",Odometry,pub_values)
    
    #calling the function client
    client()

if __name__ == '__main__':
    main()
