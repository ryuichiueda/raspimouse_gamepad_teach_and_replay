#!/usr/bin/env python
# Copyright 2017 Ryo Okazaki
# Copyright 2017 Ryuichi Ueda
# Released under the BSD License.

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from sensor_msgs.msg import Joy

class JoyTwist(object):
    def __init__(self):
        self._joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback, queue_size=1)
        self._twist_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self.level = 1

    def limitter(self, lvl):
	if lvl <= 0:	return 1
	if lvl >= 6: 	return 5
	return lvl

    def joy_callback(self, joy_msg):
        if joy_msg.buttons[7] == 1: self.level += 1
        if joy_msg.buttons[6] == 1: self.level -= 1
	self.level = self.limitter(self.level)

        if joy_msg.buttons[0] == 1:
            twist = Twist()
            twist.linear.x = joy_msg.axes[1] * 0.2 * self.level
            twist.angular.z = joy_msg.axes[0] * 3.14/32 * (self.level + 15)
            self._twist_pub.publish(twist)

	if joy_msg.axes[1] == joy_msg.axes[0] == 0:
	    self.level -= 1

if __name__ == '__main__':
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off', Trigger).call)
    rospy.ServiceProxy('/motor_on', Trigger).call()
    rospy.init_node('logicool_cmd_vel')
    logicool_cmd_vel = JoyTwist()
    rospy.spin()
