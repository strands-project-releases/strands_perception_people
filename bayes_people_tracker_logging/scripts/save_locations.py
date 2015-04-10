#!/usr/bin/env python

import rospy
from mongodb_store.message_store import MessageStoreProxy
from bayes_people_tracker.msg import PeopleTracker
#from mdl_people_tracker.msg import MdlPeopleTrackerArray, MdlPeopleTracker
#from upper_body_detector.msg import UpperBodyDetector
from topological_logging_manager.msg import LoggingManager
from bayes_people_tracker_logging.msg import PeopleTrackerLogging
from geometry_msgs.msg import Pose, PoseStamped
import message_filters
import tf


class SaveLocations():
    def __init__(self):
        rospy.logdebug("Intialising logging")
        self.robot_pose = Pose()
        self.tfl = tf.TransformListener()
        self.dataset_name = "tracks"
        self.target_frame = "/map"
        self.msg_store = MessageStoreProxy(collection="people_perception")

        manager_topic = rospy.get_param("~manager_topic", None)
        subs = [
            message_filters.Subscriber(
                "/people_tracker/positions",
            PeopleTracker
            )
        ]
        if manager_topic:
            subs += [message_filters.Subscriber(manager_topic, LoggingManager)]
        ts = message_filters.ApproximateTimeSynchronizer(
            subs,
            10,
            0.5
        )
        ts.registerCallback(self.people_callback)
        rospy.Subscriber(
            "/robot_pose",
            Pose,
            callback=self.pose_callback,
            queue_size=10
        )

    def transform(self, pose, target_frame):
        try:
            self.tfl.waitForTransform(
                target_frame,
                pose.header.frame_id,
                pose.header.stamp,
                rospy.Duration(3.0)
            )
            return self.tfl.transformPose(target_frame=target_frame, ps=pose)
        except (
            tf.Exception,
            tf.ConnectivityException,
            tf.LookupException,
            tf.ExtrapolationException
        ) as e:
            rospy.logwarn(e)
            return None

        return None

    def people_callback(self, pl, *mgr):
        if len(mgr) and not mgr[0].log:
            return

        if not len(pl.distances):
            return

        meta = {}
        meta["people"] = self.dataset_name
        rospy.logdebug(
            "Person detected. "
            "Logging to people_perception collection."
        )
        insert = PeopleTrackerLogging()
        insert.header = pl.header
        insert.uuids = pl.uuids
        for p in pl.poses:
            tp = self.transform(PoseStamped(header=pl.header, pose=p), self.target_frame)
            if tp:
                insert.people.append(tp)
        insert.robot = self.robot_pose
        insert.people_tracker = pl
        self.msg_store.insert(insert, meta)

    def pose_callback(self, pose):
        self.robot_pose = pose

if __name__ == '__main__':
    rospy.init_node('save_people_locations')
    sl = SaveLocations()
    rospy.spin()
