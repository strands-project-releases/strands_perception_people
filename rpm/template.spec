Name:           ros-hydro-bayes-people-tracker-logging
Version:        0.0.2
Release:        0%{?dist}
Summary:        ROS bayes_people_tracker_logging package

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/strands-project/strands_perception_people
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-bayes-people-tracker
Requires:       ros-hydro-camera-calibration
Requires:       ros-hydro-geometry-msgs
Requires:       ros-hydro-mdl-people-tracker
Requires:       ros-hydro-message-filters
Requires:       ros-hydro-message-runtime
Requires:       ros-hydro-mongodb-store
Requires:       ros-hydro-rospy
Requires:       ros-hydro-tf
Requires:       ros-hydro-upper-body-detector
BuildRequires:  ros-hydro-bayes-people-tracker
BuildRequires:  ros-hydro-camera-calibration
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-geometry-msgs
BuildRequires:  ros-hydro-mdl-people-tracker
BuildRequires:  ros-hydro-message-filters
BuildRequires:  ros-hydro-message-generation
BuildRequires:  ros-hydro-mongodb-store
BuildRequires:  ros-hydro-rospy
BuildRequires:  ros-hydro-tf
BuildRequires:  ros-hydro-upper-body-detector

%description
The bayes_people_tracker_logging package

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p build && cd build
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/hydro" \
        -DCMAKE_PREFIX_PATH="/opt/ros/hydro" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Sat Oct 18 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.2-0
- Autogenerated by Bloom

