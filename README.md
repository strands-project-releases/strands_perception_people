## Pedestrian Tracking
This package uses the data generated by ground_hog, visual_odometry und upper_body_detector to track people. It is also possible to omit the ground_hog detections.

### Run
Parameters:
* `load_params_from_file` _default = true_: `false` tries to read parameters from datacentre, `true` reads parameters from YAML file specified by `config_file`
* `config_file` _default = $(find mdl_people_tracker)/config/mdl_people_tracker.yaml_: The config file containing all the essential parameters. Only used if `load_params_from_file == true`.
* `machine` _default = localhost_: Determines on which machine this node should run.
* `user` _default = ""_: The user used for the ssh connection if machine is not localhost.
* `queue_size` _default = 20_: The synchronisation queue size
* `camera_namespace` _default = /head_xtion_: The camera namespace.
* `ground_plane` _default = /ground_plane_: The ground plane published by the upper_body_detector
* `ground_hog` _default = /groundHOG/detections_: The ground_hog detections
* `upper_body_detections` _default = /upper_body_detector/detections_: The upper_body_detector_detections
* `visual_odometry` _default = /visual_odometry/motion_matrix_: The visual_odometry data
* `pedestrain_array` _default = /mdl_people_tracker/people_array_: The resulting tracking data.
* `people_markers" default="/mdl_people_tracker/marker_array_: A visualisation array for rviz
* `people_poses" default = /mdl_people_tracker/pose_array_: A PoseArray of the detected people

rosrun:
```
rosrun mdl_people_tracker mdl_people_tracker [_parameter_name:=value]
```

roslaunch:
```
roslaunch mdl_people_tracker mdl_people_tracker_with_HOG.launch [parameter_name:=value]
```

To run the tracker without the groundHOG feture extraction running use:
```
rosrun mdl_people_tracker mdl_people_tracker _ground_hog:=""
```
or

```
roslaunch mdl_people_tracker mdl_people_tracker.launch [parameter_name:=value]
```
