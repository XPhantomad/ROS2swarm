#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Darby Lim
# Modified by Marian Begemann based on:
# https://discourse.ros.org/t/giving-a-turtlebot3-a-namespace-for-multi-robot-experiments/10756,
# at date 09.07.2020

import os
import argparse
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    #TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']
    turtle_namespace = LaunchConfiguration('turtle_namespace', default='robot_namespace_NOT_SET')
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    parser = argparse.ArgumentParser(description='Environment settings')
    parser.add_argument('-r', '--robot', type=str, default='waffle_pi',
                        help='The type of robot')
    args, unknown = parser.parse_known_args()
    robot = args.robot
    urdf_file_name = 'ugv_rover.urdf'

    print("urdf_file_name : {}".format(urdf_file_name))

    urdf = os.path.join(get_package_share_directory('ugv_description'), 'urdf', urdf_file_name)

    return LaunchDescription([
        DeclareLaunchArgument(
            'turtle_namespace',
            default_value=turtle_namespace,
            description='Use this as namespace for the turtlebot'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=[turtle_namespace],
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[urdf]),
    ])
