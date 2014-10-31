#include "people_tracker/people_tracker.h"

PeopleTracker::PeopleTracker() :
    detect_seq(0),
    marker_seq(0)
{
    ros::NodeHandle n;

    listener = new tf::TransformListener();
    st = new SimpleTracking();

    startup_time = ros::Time::now().toSec();
    startup_time_str = num_to_str<double>(startup_time);

    // Declare variables that can be modified by launch file or command line.
    std::string pta_topic;
    std::string pub_topic;
    std::string pub_topic_pose;
    std::string pub_marker_topic;

    // Initialize node parameters from launch file or command line.
    // Use a private node handle so that multiple instances of the node can be run simultaneously
    // while using different parameters.
    ros::NodeHandle private_node_handle("~");
    private_node_handle.param("target_frame", target_frame, std::string("/base_link"));
    private_node_handle.param("people_array", pta_topic, std::string("/upper_body_detector/bounding_box_centres"));
    parseParams(private_node_handle);

    // Create a status callback.
    ros::SubscriberStatusCallback con_cb = boost::bind(&PeopleTracker::connectCallback, this, boost::ref(n));

    private_node_handle.param("positions", pub_topic, std::string("/people_tracker/positions"));
    pub_detect = n.advertise<bayes_people_tracker::PeopleTracker>(pub_topic.c_str(), 10, con_cb, con_cb);
    private_node_handle.param("pose", pub_topic_pose, std::string("/people_tracker/pose"));
    pub_pose = n.advertise<geometry_msgs::PoseStamped>(pub_topic_pose.c_str(), 10, con_cb, con_cb);
    private_node_handle.param("marker", pub_marker_topic, std::string("/people_tracker/marker_array"));
    pub_marker = n.advertise<visualization_msgs::MarkerArray>(pub_marker_topic.c_str(), 10, con_cb, con_cb);

    boost::thread tracking_thread(boost::bind(&PeopleTracker::trackingThread, this));

    ros::spin();
}

void PeopleTracker::parseParams(ros::NodeHandle n) {
    XmlRpc::XmlRpcValue detectors;
    n.getParam("detectors", detectors);
    ROS_ASSERT(detectors.getType() == XmlRpc::XmlRpcValue::TypeStruct);
    for(XmlRpc::XmlRpcValue::ValueStruct::const_iterator it = detectors.begin(); it != detectors.end(); ++it) {
        ROS_INFO_STREAM("Found detector: " << (std::string)(it->first) << " ==> " << detectors[it->first]);
        try {
            st->addDetectorModel(it->first,
                    detectors[it->first]["matching_algorithm"] == "NN" ? NN : detectors[it->first]["matching_algorithm"] == "NNJPDA" ? NNJPDA : throw(asso_exception()),
                    detectors[it->first]["noise_model"]["velocity"]["x"],
                    detectors[it->first]["noise_model"]["velocity"]["y"],
                    detectors[it->first]["noise_model"]["position"]["x"],
                    detectors[it->first]["noise_model"]["position"]["y"]);
        } catch (std::exception& e) {
            ROS_FATAL_STREAM(""
                    << e.what()
                    << " "
                    << detectors[it->first]["matching_algorithm"]
                    << " is not specified. Unable to add "
                    << (std::string)(it->first)
                    << " to the tracker. Please use either NN or NNJPDA as association algorithms."
            );
            continue;
        }
        ros::Subscriber sub;
        subscribers[std::pair<std::string, std::string>(it->first, detectors[it->first]["topic"])] = sub;
    }
}


void PeopleTracker::trackingThread() {
    ros::Rate fps(30);
    double time_sec = 0.0;
    while(ros::ok()) {
        std::map<long, geometry_msgs::Point> ppl = st->track(&time_sec);
        if(ppl.size()) {
            geometry_msgs::Point closest_person_point;
            std::vector<geometry_msgs::Point> tmp;
            std::vector<std::string> uuids;
            std::vector<double> distances;
            std::vector<double> angles;
            double min_dist = 10000.0d;
            double angle;

            for(std::map<long, geometry_msgs::Point>::const_iterator it = ppl.begin();
                it != ppl.end(); ++it) {
                tmp.push_back(it->second);
                uuids.push_back(generateUUID(startup_time_str, it->first));
                std::vector<double> polar = cartesianToPolar(it->second);
                distances.push_back(polar[0]);
                angles.push_back(polar[1]);

                //Find closest person and get distance and angle
                angle = polar[0] < min_dist ? polar[1] : angle;
                closest_person_point = polar[0] < min_dist ? it->second : closest_person_point;
                min_dist = polar[0] < min_dist ? polar[0] : min_dist;
            }

            if(pub_marker.getNumSubscribers())
                createVisualisation(tmp, pub_marker);
            publishDetections(time_sec, closest_person_point, tmp, uuids, distances, angles, min_dist, angle);
        }
        fps.sleep();
    }
}

void PeopleTracker::publishDetections(
        double time_sec,
        geometry_msgs::Point closest,
        std::vector<geometry_msgs::Point> ppl,
        std::vector<std::string> uuids,
        std::vector<double> distances,
        std::vector<double> angles,
        double min_dist,
        double angle) {
    bayes_people_tracker::PeopleTracker result;
    result.header.stamp.fromSec(time_sec);
    result.header.frame_id = target_frame;
    result.header.seq = ++detect_seq;
    for(int i = 0; i < ppl.size(); i++) {
        geometry_msgs::Pose pose;
        pose.position.x = ppl[i].x;
        pose.position.y = ppl[i].y;
        pose.position.z = ppl[i].z;
        //TODO: Get orientation from direction estimation
        pose.orientation.x = 0.0;
        pose.orientation.y = 0.0;
        pose.orientation.z = 0.0;
        pose.orientation.w = 1.0;
        result.poses.push_back(pose);
        ROS_DEBUG("publishDetections: Publishing detection: x: %f, y: %f, z: %f",
                  pose.position.x,
                  pose.position.y,
                  pose.position.z);
    }
    result.uuids = uuids;
    result.distances = distances;
    result.angles = angles;
    result.min_distance = min_dist;
    result.min_distance_angle = angle;
    publishDetections(result);

    geometry_msgs::PoseStamped pose;
    pose.header = result.header;
    pose.pose.position = closest;
    pose.pose.orientation.x = 0.0;
    pose.pose.orientation.y = 0.0;
    pose.pose.orientation.z = 0.0;
    pose.pose.orientation.w = 1.0;
    publishDetections(pose);
}

void PeopleTracker::publishDetections(bayes_people_tracker::PeopleTracker msg) {
    pub_detect.publish(msg);
}

void PeopleTracker::publishDetections(geometry_msgs::PoseStamped msg) {
    pub_pose.publish(msg);
}

void PeopleTracker::createVisualisation(std::vector<geometry_msgs::Point> points, ros::Publisher& pub) {
    ROS_DEBUG("Creating markers");
    visualization_msgs::MarkerArray marker_array;
    for(int i = 0; i < points.size(); i++) {

        geometry_msgs::Pose pose;
        pose.position.x = points[i].x;
        pose.position.y = points[i].y;
        pose.position.z = 0.6;
        pose.orientation.x = 0.0;
        pose.orientation.y = 0.0;
        pose.orientation.z = 0.0;
        pose.orientation.w = 1.0;
        std::vector<visualization_msgs::Marker> human = createHuman(i*10, pose);

        marker_array.markers.insert(marker_array.markers.begin(), human.begin(), human.end());
    }
    pub.publish(marker_array);
}

std::vector<double> PeopleTracker::cartesianToPolar(geometry_msgs::Point point) {
    ROS_DEBUG("cartesianToPolar: Cartesian point: x: %f, y: %f, z %f", point.x, point.y, point.z);
    std::vector<double> output;
    double dist = sqrt(pow(point.x,2) + pow(point.y,2));
    double angle = atan2(point.y, point.x);
    output.push_back(dist);
    output.push_back(angle);
    ROS_DEBUG("cartesianToPolar: Polar point: distance: %f, angle: %f", dist, angle);
    return output;
}

void PeopleTracker::detectorCallback(const geometry_msgs::PoseArray::ConstPtr &pta, std::string detector)
{
    // Publish an empty message to trigger callbacks even when there are no detections.
    // This can be used by nodes which might also want to know when there is no human detected.
    if(pta->poses.size() == 0) {
        bayes_people_tracker::PeopleTracker empty;
        empty.header.stamp = ros::Time::now();
        empty.header.frame_id = target_frame;
        empty.header.seq = ++detect_seq;
        publishDetections(empty);
        return;
    }

    geometry_msgs::PoseStamped closest_person;
    std::vector<geometry_msgs::Point> ppl;
    std::vector<int> ids;
    std::vector<std::string> uuids;
    std::vector<double> scores;
    std::vector<double> distances;
    std::vector<double> angles;
    double min_dist = 10000.0d;
    double angle;
    for(int i = 0; i < pta->poses.size(); i++) {
        geometry_msgs::Pose pt = pta->poses[i];

            //Create stamped pose for tf
            geometry_msgs::PoseStamped poseInCamCoords;
            geometry_msgs::PoseStamped poseInRobotCoords;
            geometry_msgs::PoseStamped poseInTargetCoords;
            poseInCamCoords.header = pta->header;
            poseInCamCoords.pose = pt;

            //Transform
            try {
                // Transform into robot coordinate system /base_link for the caluclation of relative distances and angles
                ROS_DEBUG("Transforming received position into %s coordinate system.", BASE_LINK);
                listener->waitForTransform(poseInCamCoords.header.frame_id, BASE_LINK, poseInCamCoords.header.stamp, ros::Duration(3.0));
                listener->transformPose(BASE_LINK, ros::Time(0), poseInCamCoords, poseInCamCoords.header.frame_id, poseInRobotCoords);

                // Transform into given traget frame. Default /map
                if(strcmp(target_frame.c_str(), BASE_LINK)) {
                    ROS_DEBUG("Transforming received position into %s coordinate system.", target_frame.c_str());
                    listener->waitForTransform(poseInCamCoords.header.frame_id, target_frame, poseInCamCoords.header.stamp, ros::Duration(3.0));
                    listener->transformPose(target_frame, ros::Time(0), poseInCamCoords, poseInCamCoords.header.frame_id, poseInTargetCoords);
                } else {
                    poseInTargetCoords = poseInRobotCoords;
                }
            }
            catch(tf::TransformException ex) {
                ROS_WARN("Failed transform: %s", ex.what());
                return;
            }

            poseInTargetCoords.pose.position.z = 0.0;
            poseInRobotCoords.pose.position.z = 0.0;

            ppl.push_back(poseInTargetCoords.pose.position);

    }
    if(ppl.size())
        st->addObservation(detector, ppl, pta->header.stamp.toSec());
}

// Connection callback that unsubscribes from the tracker if no one is subscribed.
void PeopleTracker::connectCallback(ros::NodeHandle &n) {
    bool loc = pub_detect.getNumSubscribers();
    bool markers = pub_marker.getNumSubscribers();
    bool test_markers = pub_marker.getNumSubscribers();
    std::map<std::pair<std::string, std::string>, ros::Subscriber>::const_iterator it;
    if(!loc && !markers && !test_markers) {
        ROS_DEBUG("Pedestrian Localisation: No subscribers. Unsubscribing.");
        for(it = subscribers.begin(); it != subscribers.end(); ++it)
            const_cast<ros::Subscriber&>(it->second).shutdown();
    } else {
        ROS_DEBUG("Pedestrian Localisation: New subscribers. Subscribing.");
        for(it = subscribers.begin(); it != subscribers.end(); ++it)
            subscribers[it->first] = n.subscribe<geometry_msgs::PoseArray>(it->first.second.c_str(), 10, boost::bind(&PeopleTracker::detectorCallback, this, _1, it->first.first));
    }
}

int main(int argc, char **argv)
{
    // Set up ROS.
    ros::init(argc, argv, "bayes_people_tracker");
    PeopleTracker* pl = new PeopleTracker();
    return 0;
}
