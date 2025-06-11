import os
import sys
import rclpy
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    use_pcd = LaunchConfiguration('use_pcd', default=False)
    
    map_dir = LaunchConfiguration('map',default=os.path.join(get_package_share_directory('bearyx_navigation'), 'map_test.yaml'))
    
#======================== find map from terminal's input to decode ==========================
    n = len(sys.argv)
    if n >= 1:
        for i in range(n):
            map_arg = sys.argv[i]
            map_path = map_arg.split('=')
            if map_path[0] == "map:":
                if map_path[1] != "" and "~" in map_path[1] and "$HOME" not in map_path:
                    check_home = map_path[1].split('~')
                    map_dir = os.path.expanduser('~') + check_home[1]
                else:
                    map_dir = map_path[1]
#============================================================================================

    nav2_config_params_file = LaunchConfiguration('params_file', default=os.path.join(get_package_share_directory('bearyx_navigation'), 'config', 'bearyx_navigation.yaml'))
    nav2_pcd_config_params_file = LaunchConfiguration('params_file',default=os.path.join(get_package_share_directory('bearyx_navigation'), 'config', 'bearyx_pcd_navigation.yaml'))
    rviz_config_dir = os.path.join(get_package_share_directory('bearyx_navigation'),'rviz','bearyx_navigation.rviz')
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    
            
    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='Use simulation (Gazebo) clock if true'),
        
        DeclareLaunchArgument(
            name='map',
            default_value=map_dir,
            description='Navigation map path'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_launch_file_dir, '/localization_launch.py']),
                launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': nav2_config_params_file
            }.items()
        ),

        TimerAction(period=3.0, actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': nav2_config_params_file
            }.items(), condition=IfCondition(PythonExpression(["'",use_pcd,"' == 'False'"]))
        )]),
        
        TimerAction(period=3.0, actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': nav2_pcd_config_params_file
            }.items(), condition=IfCondition(PythonExpression(["'",use_pcd,"' == 'True'"]))
        )]),


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
