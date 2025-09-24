#!/usr/bin/env python3
# imu_analyze.py
import rclpy, time, numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu
import argparse

class ImuAnalyzer(Node):
    def __init__(self, topic, duration):
        super().__init__('imu_analyzer')
        self.sub = self.create_subscription(Imu, topic, self.cb, 400)
        self.samples = []
        self.start = time.time()
        self.duration = duration
        self.get_logger().info(f'Collecting IMU on {topic} for {duration}s...')

    def cb(self, msg):
        if time.time() - self.start > self.duration:
            return
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        gx = msg.angular_velocity.x
        gy = msg.angular_velocity.y
        gz = msg.angular_velocity.z
        self.samples.append((ax,ay,az,gx,gy,gz))

    def report(self):
        if len(self.samples) == 0:
            self.get_logger().error('No samples collected.')
            return
        a = np.array(self.samples)[:,0:3]
        g = np.array(self.samples)[:,3:6]
        norms = np.linalg.norm(a, axis=1)
        dz = np.abs(np.diff(a[:,2])) if a.shape[0] > 1 else np.array([0.0])

        def fmt(x): return ', '.join([f'{v:.4f}' for v in x])

        self.get_logger().info(f'Samples: {len(self.samples)}')
        self.get_logger().info(f'acc mean (x,y,z): {fmt(a.mean(axis=0))}')
        self.get_logger().info(f'acc std  (x,y,z): {fmt(a.std(axis=0))}')
        self.get_logger().info(f'acc min  (x,y,z): {fmt(a.min(axis=0))}')
        self.get_logger().info(f'acc max  (x,y,z): {fmt(a.max(axis=0))}')
        self.get_logger().info(f'gyro mean (x,y,z): {fmt(g.mean(axis=0))}')
        self.get_logger().info(f'gyro std  (x,y,z): {fmt(g.std(axis=0))}')
        self.get_logger().info(f'acc norm mean/std/min/max: {np.mean(norms):.4f} / {np.std(norms):.4f} / {np.min(norms):.4f} / {np.max(norms):.4f}')
        self.get_logger().info(f'max z jump: {np.max(dz):.4f}')
        # unit guess
        mz = np.mean(a[:,2])
        if abs(mz - 1.0) < 0.3:
            self.get_logger().warn('Detected likely unit = g (≈1). Consider multiplying by 9.81 for m/s^2.')
        elif abs(np.mean(norms) - 9.81) < 1.0:
            self.get_logger().info('Detected likely unit = m/s^2 (norm close to 9.81).')
        else:
            self.get_logger().warn('Acceleration norm not close to 9.81; possible issues (vibration, bias, or parsing error).')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='/imu_raw')
    parser.add_argument('--dur', type=float, default=5.0)
    args = parser.parse_args()

    rclpy.init()
    node = ImuAnalyzer(args.topic, args.dur)
    try:
        timeout = time.time() + args.dur + 0.5
        while time.time() < timeout:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    node.report()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
