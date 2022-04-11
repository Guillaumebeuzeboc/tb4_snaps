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
    # Get the launch directory
    turtlebot4_navigation_dir = get_package_share_directory("turtlebot4_navigation")

    # Create the launch configuration variables
    namespace = LaunchConfiguration("namespace")
    use_namespace = LaunchConfiguration("use_namespace")
    localization = LaunchConfiguration("localization")
    slam = LaunchConfiguration("slam")
    nav2 = LaunchConfiguration("nav2")
    map_yaml_file = LaunchConfiguration("map")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    autostart = LaunchConfiguration("autostart")
    use_composition = LaunchConfiguration("use_composition")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "namespace", default_value="", description="Top-level namespace"
            ),
            DeclareLaunchArgument(
                "use_namespace",
                default_value="false",
                description="Whether to apply a namespace to the navigation stack",
            ),
            DeclareLaunchArgument(
                "slam",
                default_value="off",
                choices=["off", "sync", "async"],
                description="Whether to run a SLAM",
            ),
            DeclareLaunchArgument(
                "localization",
                default_value="true",
                choices=["true", "false"],
                description="Whether to run localization",
            ),
            DeclareLaunchArgument(
                "nav2", default_value="false", description="Whether to run Nav2"
            ),
            DeclareLaunchArgument(
                "map",
                default_value=os.path.join(
                    turtlebot4_navigation_dir, "maps", "depot.yaml"
                ),
                description="Full path to map yaml file to load",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use simulation (Gazebo) clock if true",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=os.path.join(
                    turtlebot4_navigation_dir, "config", "nav2.yaml"
                ),
                description="Full path to the ROS2 parameters file to use for all launched nodes",
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
                description="Automatically startup the nav2 stack",
            ),
            DeclareLaunchArgument(
                "use_composition",
                default_value="True",
                description="Whether to use composed bringup",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        turtlebot4_navigation_dir, "launch", "nav_bringup.launch.py"
                    )
                ),
                launch_arguments={
                    "namespace": namespace,
                    "use_namespace": use_namespace,
                    "localization": localization,
                    "slam": slam,
                    "nav2": nav2,
                    "map_yaml_file": map_yaml_file,
                    "use_sim_time": use_sim_time,
                    "params_files": params_file,
                    "autostart": autostart,
                    "use_composition": use_composition,
                }.items(),
            ),
        ]
    )
