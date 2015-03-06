#!/usr/bin/env python

import sys
import rospy
from human_trajectory.msg import Trajectories
from human_trajectory.trajectories import OfflineTrajectories
from human_trajectory.trajectories import OnlineTrajectories
from strands_navigation_msgs.msg import TopologicalMap
from mongodb_store.message_store import MessageStoreProxy


class TrajectoryPublisher(object):

    def __init__(self, name, interval, online):
        self.map_info = ''
        self._publish_interval = interval
        self.online = online
        self.counter = self.seq = 0

        rospy.loginfo("Connecting to mongodb...")
        self._store_client = MessageStoreProxy(collection="people_trajectory")
        rospy.loginfo("Connecting to topological_map...")
        self._sub = rospy.Subscriber(
            "/topological_map", TopologicalMap, self.map_callback, None, 10
        )
        rospy.loginfo("Creating human_trajectory/trajectories topic...")
        self._pub = rospy.Publisher(
            name+'/trajectories', Trajectories, queue_size=10
        )

        if online:
            self._publish_rate = rospy.Rate(1 / float(interval))
            self.trajs = OnlineTrajectories()
        else:
            self._publish_rate = rospy.Rate(1)
            self.trajs = OfflineTrajectories()

        rospy.loginfo("human_trajectory is ready...")

    # construct trajectories message header
    def _construct_header(self):
        trajs = Trajectories()
        self.seq += 1
        trajs.header.seq = self.seq
        trajs.header.stamp = rospy.Time.now()
        trajs.header.frame_id = '/map'
        return trajs

    # publish based on online data from people_tracker
    def _publish_online_data(self, incremental=False):
        from_time = None
        while not rospy.is_shutdown():
            trajs = self._construct_header()

            for uuid, traj in self.trajs.traj.items():
                if incremental and uuid in self.trajs._checked \
                        and self.trajs._checked[uuid]:
                    traj_msg = traj.get_trajectory_message(self._publish_interval)
                    trajs.trajectories.append(traj_msg)
                if uuid in self.trajs.complete:
                    if self.trajs.complete[uuid]:
                        traj_msg = traj.get_trajectory_message()
                        if not incremental:
                            trajs.trajectories.append(traj_msg)
                        meta = dict()
                        meta["map"] = self.map_info
                        meta["taken"] = "online"
                        self._store_client.insert(traj_msg, meta)
                        self.counter += 1
                        rospy.loginfo("Total trajectories: %d", self.counter)
                    del self.trajs.traj[uuid]
                    del self.trajs.complete[uuid]

            self._pub.publish(trajs)
            self._publish_rate.sleep()

    # publish based on offline data in mongodb
    def _publish_offline_data(self):
        start_time = self.trajs.start_secs
        while not rospy.is_shutdown():
            trajs = self._construct_header()

            for uuid, traj in self.trajs.traj.items():
                end_time = start_time + self._publish_interval
                traj_end = traj.humrobpose[-1][0].header.stamp.secs
                if traj_end <= end_time:
                    traj_msg = traj.get_trajectory_message()
                    trajs.trajectories.append(traj_msg)
                    if not self.trajs.from_people_trajectory:
                        meta = dict()
                        meta["map"] = self.map_info
                        meta["taken"] = "offline"
                        self._store_client.insert(traj_msg, meta)
                    del self.trajs.traj[uuid]

            start_time += self._publish_interval
            self.counter += len(trajs.trajectories)
            rospy.loginfo("Total trajectories: %d", self.counter)

            self._pub.publish(trajs)
            self._publish_rate.sleep()

    # get map info from topological navigation
    def map_callback(self, msg):
        self.map_info = msg.map
        self._sub.unregister()

    # publish as ros message or store human trajectories into mongodb
    # sort poses for each human, delete noisy trajectory
    def publish_trajectories(self, incremental):
        if self.online:
            self._publish_online_data(incremental)
        else:
            self._publish_offline_data()

if __name__ == '__main__':
    rospy.init_node('human_trajectories')

    if len(sys.argv) < 4:
        rospy.logerr("usage: trajectory publish_interval online/offline[1/0] complete/incremental[0/1]")
        sys.exit(2)

    tp = TrajectoryPublisher(
        rospy.get_name(),
        int(sys.argv[1]),
        int(sys.argv[2])
    )
    tp.publish_trajectories(int(sys.argv[3]))

    rospy.spin()
