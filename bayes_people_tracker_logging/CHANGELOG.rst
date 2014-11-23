^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package bayes_people_tracker_logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.14 (2014-11-23)
-------------------
* Removing upped body detector and mdl people tracker from logging
  Those two are slowing down the logging and prevent logging if there is only detections via the leg detector.
* Contributors: Christian Dondrup

0.0.12 (2014-10-31)
-------------------

0.0.3 (2014-10-23)
------------------
* Added LICENSE files. Fixes `#101 <https://github.com/strands-project/strands_perception_people/issues/101>`_
* Contributors: Lucas Beyer

0.0.2 (2014-10-18)
------------------

0.0.1 (2014-10-18)
------------------
* Renamed strands_pedestrian_tracking to mdl_people_tracker
  This also includes renaming the messages and most of the parameters.
* Prepared bayes_people_tracker_logging for release
* Splitting utils package into seperate packages.
* Contributors: Christian Dondrup
