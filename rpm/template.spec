Name:           ros-indigo-bayes-people-tracker
Version:        0.0.5
Release:        0%{?dist}
Summary:        ROS bayes_people_tracker package

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/strands-project/strands_perception_people
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       ros-indigo-bayes-tracking
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-tf
Requires:       ros-indigo-visualization-msgs
BuildRequires:  boost-devel
BuildRequires:  ros-indigo-bayes-tracking
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-visualization-msgs

%description
The bayes_people_tracker package

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
* Wed Oct 29 2014 Christian Dondrup <cdondrup@lincoln.ac.uk> - 0.0.5-0
- Autogenerated by Bloom

