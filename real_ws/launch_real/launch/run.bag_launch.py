import launch, os, launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
from launch.event_handlers import OnProcessStart

def generate_launch_description():

    # 启动bag
    start_bag = launch.actions.ExecuteProcess(
        cwd="/home/akun/workspace/CAR",
        cmd = ['ros2','bag', 'play','rosbag2_2025_08_03-17_40_23'],
        output = "screen",
    )

    # 启动livox消息转换
    livox_custom_convert_pointcloud2 = launch_ros.actions.Node(
        package='convert_laser',
        executable='convert',
        output = 'screen' # 日志输出到屏幕
    )

    # 启动LIO-SAM
    start_LIO_SAM = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('lio_sam'),
            'launch',
            'run.launch.py'
        ))
    )

    # 依次启动
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(period=1.0, actions=[start_bag]),
        launch.actions.TimerAction(period=3.0, actions=[livox_custom_convert_pointcloud2]),
        launch.actions.TimerAction(period=6.0, actions=[start_LIO_SAM]),
    ])

    return launch.LaunchDescription([
        action_group
    ])

    