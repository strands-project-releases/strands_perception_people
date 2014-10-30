Name:           ros-indigo-upper-body-detector
Version:        0.0.11
Release:        0%{?dist}
Summary:        ROS upper_body_detector package

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/strands-project/strands_perception_people
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       qt-devel
Requires:       ros-indigo-cv-bridge
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-ground-plane-estimation
Requires:       ros-indigo-image-transport
Requires:       ros-indigo-message-filters
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-visualization-msgs
BuildRequires:  boost-devel
BuildRequires:  qt-devel
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cv-bridge
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-ground-plane-estimation
BuildRequires:  ros-indigo-image-transport
BuildRequires:  ros-indigo-message-filters
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-visualization-msgs

%description
The upper_body_detector package

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
* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.11-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.8-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.10-0
- Autogenerated by Bloom

* Thu Oct 30 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.9-0
- Autogenerated by Bloom

* Wed Oct 29 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.5-0
- Autogenerated by Bloom

* Wed Oct 29 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.7-0
- Autogenerated by Bloom

