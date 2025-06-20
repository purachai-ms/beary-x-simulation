#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    launch_file_dir = os.path.join(get_package_share_directory('bearyx_gazebo'))

    world_file_name = 'bearyx_empty/beary_x.model'
    world = os.path.join(get_package_share_directory('bearyx_gazebo'),
                         'worlds', world_file_name)

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            ),
            launch_arguments={'world': world}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
            ),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/bearyx_robot_state_publisher_sim.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),

    ])
