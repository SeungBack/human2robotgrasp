
```

ROS_NAMESPACE=azure1 roslaunch azure_kinect_ros_driver driver.launch color_resolution:=720P depth_mode:=WFOV_UNBINNED fps:=5

conda activate ros-py27 && rosrun human2robotgrasp handpose_estimator.py

ros && conda activate h2r-py37 && roscd human2robotgrasp && cd src/frankmocap && python handpose_client.py

```