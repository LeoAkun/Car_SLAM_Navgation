import launch, os, launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

def generate_launch_description():

    # 启动IMU
    start_IMU = launch.actions.ExecuteProcess(
        cwd="/home/akun/workspace/CAR/yesense_ros2",
        cmd = ['bash','-c', 'source run.sh'],
        output = "screen",
    )

    # 启动livox
    start_livox = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('livox_ros_driver2'),
            'launch_ROS2',
            'msg_MID360_launch.py'
        ))
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

    

    return launch.LaunchDescription([
        start_IMU,
        start_livox,
        livox_custom_convert_pointcloud2,
        start_LIO_SAM
    ])

    