import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    # Get the directory of the slam_toolbox package
    slamtoolbox_file_path = os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')

    rviz_config_dir = os.path.join(get_package_share_directory('bearyx_navigation'),'rviz', 'bearyx_SlamToolBox_online_async.rviz')
                                   
    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slamtoolbox_file_path),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
                
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),

        TimerAction(
            period=5.0,  # Delay in seconds before starting the node
            actions=[
                Node(
                    package='bearyx_navigation',
                    executable='robot_position_tracking',
                    name='robot_position_tracking',
                    output='screen',
                    parameters=[{'use_sim_time': use_sim_time}]
                )
            ]
        ),

    ])
