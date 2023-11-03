rostopic pub -1 /mobile_base/commands/velocity geometry_msgs/Twist "linear:
  x: 1.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"

rostopic pub -1 /mobile_base/commands/velocity geometry_msgs/Twist "linear:
  x: -1.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"