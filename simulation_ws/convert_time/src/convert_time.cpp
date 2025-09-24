#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <sensor_msgs/msg/imu.hpp>

// 转换雷达，IMU时间，将仿真时间转换为真实时间
class Subscriber: public rclcpp::Node{
public:
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscriber_laser;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_laser;
    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr subscriber_imu;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_imu;
    
public:
    Subscriber(const std::string & node_name):Node(node_name){
        this->subscriber_laser = this->create_subscription<sensor_msgs::msg::PointCloud2>("/livox/pointcloud",
                10,
                std::bind(&Subscriber::callback_laser, this, std::placeholders::_1));
        this->publisher_laser = this->create_publisher<sensor_msgs::msg::PointCloud2>("/livox/pointcloud_simtime2realtime",10);
        this->subscriber_imu = this->create_subscription<sensor_msgs::msg::Imu>("/imu_raw",
                10,
                std::bind(&Subscriber::callback_imu, this, std::placeholders::_1));
        this->publisher_imu = this->create_publisher<sensor_msgs::msg::Imu>("/imu_raw_simtime2realtime",10);
    }

private:
    void callback_laser(sensor_msgs::msg::PointCloud2::SharedPtr cloud2)
    {
        // RCLCPP_INFO(this->get_logger(), "接收到laser\n");
        auto now = std::chrono::system_clock::now();  // 真实时间
        auto now_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(now);
        uint64_t ns_since_epoch = now_ns.time_since_epoch().count();       
        rclcpp::Time real_time(ns_since_epoch, RCL_SYSTEM_TIME);
        cloud2->header.stamp = real_time;
        publisher_laser->publish(*cloud2);
    }

    void callback_imu(sensor_msgs::msg::Imu::SharedPtr imu)
    {
        // RCLCPP_INFO(this->get_logger(), "接收到imu\n");
        auto now = std::chrono::system_clock::now();  // 真实时间
        auto now_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(now);
        uint64_t ns_since_epoch = now_ns.time_since_epoch().count();       
        rclcpp::Time real_time(ns_since_epoch, RCL_SYSTEM_TIME);
        imu->header.stamp = real_time;
        imu->linear_acceleration.z=9.85;
        publisher_imu->publish(*imu);
    }
};


int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto sub = std::make_shared<class Subscriber>("subscriber");
    rclcpp::spin(sub);
    rclcpp::shutdown();
    return 0;
    
}