#! /usr/bin/env python3

from jtop import jtop
import time
import pickle
import rospy
from std_msgs.msg import Float64

def get_resource_usage():
    with jtop() as jetson:
        if(jetson.ok()):
            stats = jetson.stats
            cpu_usage_list = [stats['CPU1'], stats['CPU2'], stats['CPU3'], stats['CPU4'], stats['CPU5'], stats['CPU6'], stats['CPU7'], stats['CPU8']]
            cpu_usage = sum(cpu_usage_list)/(100*len(cpu_usage_list))
            gpu_usage = stats['GPU']/100

    return cpu_usage, gpu_usage



def publish_resource_usage():
    pub_cpu = rospy.Publisher('resource_usage/cpu', Float64, queue_size=1)
    pub_gpu = rospy.Publisher('resource_usage/gpu', Float64, queue_size=1)
    rospy.init_node('resource_usage', anonymous=True)
    while not rospy.is_shutdown():
        cpu_usage, gpu_usage = get_resource_usage()
        pub_cpu.publish(cpu_usage)
        pub_gpu.publish(gpu_usage)


def main():
    try:
        publish_resource_usage()
    except rospy.ROSInterruptException:
        pass


if __name__ == "__main__":
    main()