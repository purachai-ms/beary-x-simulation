import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import TransformStamped, PoseStamped
import time

tf_buffer = None
robot_position_publisher = None

def get_transform():
    """Function to get the transform from 'map' to 'base_footprint' and publish it."""
    global tf_buffer, robot_position_publisher

    try:
        # Wait for the transform from "map" to "base_footprint"
        transform = tf_buffer.lookup_transform("map", "base_footprint", rclpy.time.Time() )

        # Extract translation (position)
        position = transform.transform.translation
        orientation = transform.transform.rotation

        # Publish the position
        robot_position_msg = PoseStamped()
        robot_position_msg.header.stamp = transform.header.stamp
        robot_position_msg.pose.position.x = position.x
        robot_position_msg.pose.position.y = position.y
        robot_position_msg.pose.position.z = position.z
        robot_position_msg.pose.orientation = orientation

        robot_position_publisher.publish(robot_position_msg)

        # print(
        #     f"Robot Position -> x: {position.x:.2f}, y: {position.y:.2f}, z: {position.z:.2f}"
        # )
        # print(
        #     f"Orientation (Quaternion) -> x: {orientation.x:.2f}, y: {orientation.y:.2f}, "
        #     f"z: {orientation.z:.2f}, w: {orientation.w:.2f}"
        # )

    except tf2_ros.LookupException as e:
        pass
        # print(f"Transform lookup failed: {e}")
    except tf2_ros.ExtrapolationException as e:
        pass
        # print(f"Extrapolation error: {e}")


def main():
    global tf_buffer, robot_position_publisher
    rclpy.init()
    node = rclpy.create_node('robot_position_node')
    robot_position_publisher = node.create_publisher(PoseStamped, '/robot_position', 10)

    # --- TF2 Setup ---
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer, node)
    node.create_timer(0.1, get_transform)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()