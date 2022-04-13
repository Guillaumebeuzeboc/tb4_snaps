import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    turtlebot4_navigation_dir = get_package_share_directory("turtlebot4_navigation")
    turtlebot4_bringup_dir = get_package_share_directory("turtlebot4_bringup")

    # Create the launch configuration variables
    map_yaml_file = LaunchConfiguration("map")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")

    map_yaml_arg = DeclareLaunchArgument(
        "map",
        default_value=os.path.join(turtlebot4_navigation_dir, "maps", "depot.yaml"),
        description="Full path to map yaml file to load",
    )
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock if true",
    )
    params_file_arg = DeclareLaunchArgument(
        "params_file",
        default_value=os.path.join(turtlebot4_navigation_dir, "config", "nav2.yaml"),
        description="Full path to the ROS2 parameters file to use for all launched nodes",
    )

    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot4_bringup_dir, "launch", "rplidar.launch.py")
        )
    )

    oakd_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot4_bringup_dir, "launch", "oakd.launch.py")
        )
    )

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot4_navigation_dir, "launch", "nav_bringup.launch.py")
        ),
        launch_arguments={
            "localization": "true",
            "slam": "off",
            "nav2": "true",
            "map_yaml_file": map_yaml_file,
            "use_sim_time": use_sim_time,
            "params_files": params_file,
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(map_yaml_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(params_file_arg)

    ld.add_action(rplidar_launch)
    ld.add_action(oakd_launch)
    ld.add_action(nav_launch)

    return ld
