#! /usr/bin/python3

import rospy
import math
from turtlesim.msg import Pose
from turtlesim.msg import Pose as TurtlePose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist


class myNode:


	def __init__(self):
		rospy.init_node('turtle_stalker_node')

		rospy.wait_for_service('/spawn')
		spawn_func = rospy.ServiceProxy('/spawn',Spawn)
		spawn_func(1.0,1.0,0.0, 'turtle2')

		rospy.Subscriber('/turtle1/pose',TurtlePose,self.leader_pose_callback)
		rospy.Subscriber('/turtle2/pose',TurtlePose,self.stalker_pose_callback)		

		self.pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size = 10)
		
		self.rate = rospy.Rate(60)
		self.leader_pose = None
		self.stalker_pose = None
		
		
	def leader_pose_callback(self,data):
		self.leader_pose = data
		
	
	def stalker_pose_callback(self,data):
		self.stalker_pose = data
		
		
	def func(self):
		while not rospy.is_shutdown():
			if self.leader_pose and self.stalker_pose:
				self.speed = rospy.get_param('~speed', 1)
				dx = self.leader_pose.x - self.stalker_pose.x
				dy = self.leader_pose.y - self.stalker_pose.y
				angle = math.atan2(dy, dx)
				dist = math.sqrt(dx**2 + dy**2)
				
				move = Twist()
				move.linear.x = self.speed * dist
				move.angular.z = (angle - self.stalker_pose.theta) * 10.0
				self.pub.publish(move) 
			self.rate.sleep()
	
	
	def run(self):
		self.func()
		rospy.spin()	
		


if __name__ =='__main__':
	try:
		node = myNode()
		node.run()
	except rospy.ROSInterruptException:
		pass


