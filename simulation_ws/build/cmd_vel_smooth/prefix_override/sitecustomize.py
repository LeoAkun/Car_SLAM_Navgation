import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/akun/workspace/CAR/simulation_ws/install/cmd_vel_smooth'
