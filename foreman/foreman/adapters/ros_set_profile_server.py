from rclpy.node import Node

from foreman.engine import ForemanEngine
from foreman_msgs.srv import SetProfile


class RosSetProfileServer:
    """ROS 2 service to set a named profile for Foreman Engine."""

    def __init__(self, node: Node, engine: ForemanEngine):
        self._node = node
        self._engine = engine
        self.logger_prefix = "Adapters.RosSetProfileServer:"
        # Using MutuallyExclusiveCallbackGroup
        # If a service is processing, we reject new service requests.
        self._srv = self._node.create_service(
            SetProfile,
            "foreman/set_profile",
            self._handle_set_profile,
            callback_group=self._node.callback_group_services,
        )

        self._node.get_logger().info(
            f"{self.logger_prefix} Service /foreman/set_profile is ready."
        )

    def _handle_set_profile(self, request, response):
        """Set the target system state."""
        profile_name = request.profile
        # TODO: demote some of these to DEBUG logs.
        self._node.get_logger().info(
            f"{self.logger_prefix} Received request for profile '{profile_name}'"
        )

        engine_response = self._engine.request_profile(profile_name)

        response.success = engine_response.success
        response.message = engine_response.message

        if not engine_response.success:
            self._node.get_logger().warning(f"{engine_response.message}")
        else:
            self._node.get_logger().info(f"{engine_response.message}")

        return response
