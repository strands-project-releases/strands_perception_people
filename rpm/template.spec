Name:           ros-indigo-bayes-people-tracker-logging
Version:        0.0.13
Release:        0%{?dist}
Summary:        ROS bayes_people_tracker_logging package

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/strands-project/strands_perception_people
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-bayes-people-tracker
Requires:       ros-indigo-camera-calibration
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-mdl-people-tracker
Requires:       ros-indigo-message-filters
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-mongodb-store
Requires:       ros-indigo-rospy
Requires:       ros-indigo-tf
Requires:       ros-indigo-upper-body-detector
BuildRequires:  ros-indigo-bayes-people-tracker
BuildRequires:  ros-indigo-camera-calibration
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-mdl-people-tracker
BuildRequires:  ros-indigo-message-filters
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-mongodb-store
BuildRequires:  ros-indigo-rospy
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-upper-body-detector

%description
The bayes_people_tracker_logging package

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p build && cd build
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Fri Oct 31 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.13-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.10-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.8-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.11-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.9-0
- Autogenerated by Bloom

* Wed Oct 29 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.5-0
- Autogenerated by Bloom

* Wed Oct 29 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.7-0
- Autogenerated by Bloom

