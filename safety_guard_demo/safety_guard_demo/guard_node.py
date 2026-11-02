"""ROS 2 rclpy demonstration: proposal monitoring only, not brake actuation.

The guard is *NOT* an ASIL-rated safety mechanism. Clock health is set false
by default because ROS time alone doesn't prove synchronized capture clocks.
DO NOT connect this node's outputs to real vehicle actuators.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from adas_safety_interfaces.msg import FeatureProposal, GuardStatus
from .guard_logic import Proposal, ProposalGuard, Verdict

REASONS = {v: i for i, v in enumerate(Verdict)}

class GuardMonitorDemo(Node):
    def __init__(self):
        super().__init__('proposal_guard_demo')
        self.declare_parameter('clock_trusted_for_demo', False)
        qos = QoSProfile(history=HistoryPolicy.KEEP_LAST, depth=1,
                         reliability=ReliabilityPolicy.RELIABLE,
                         durability=DurabilityPolicy.VOLATILE)
        # Requested vs offered compatibility and actual DDS behavior must be tested.
        self.sub = self.create_subscription(FeatureProposal, '/demo/feature_proposal', self.on_proposal, qos)
        self.pub = self.create_publisher(GuardStatus, '/demo/guard_status', qos)
        self.guard = ProposalGuard()

    def on_proposal(self, msg):
        now = self.get_clock().now()
        sample_ns = int(msg.sensor_stamp.sec)*1_000_000_000 + int(msg.sensor_stamp.nanosec)
        proposal = Proposal(int(msg.sequence), sample_ns,
                            float(msg.requested_deceleration_mps2), float(msg.confidence), bool(msg.valid))
        # True only in a closed demo with validated clock assumptions. Not a safety clock monitor.
        ok_clock = bool(self.get_parameter('clock_trusted_for_demo').value)
        verdict = self.guard.check(proposal, now.nanoseconds, clock_trusted=ok_clock)
        out = GuardStatus(); out.decision_stamp=now.to_msg(); out.last_sequence=msg.sequence
        out.proposal_accepted=(verdict is Verdict.ACCEPT);out.reason_code=REASONS[verdict];out.diagnostic=verdict.value
        self.pub.publish(out)
        if verdict is not Verdict.ACCEPT:
            self.get_logger().warning(f'Proposal rejected: {verdict.value}')

def main():
    rclpy.init();n=GuardMonitorDemo()
    try:rclpy.spin(n)
    finally:n.destroy_node();rclpy.shutdown()

if __name__=='__main__':main()
