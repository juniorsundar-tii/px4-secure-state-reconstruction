cmake_minimum_required(VERSION 3.8)
project(px4_offboard_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(px4_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gz-transport13 REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
    "msg/TimestampedArray.msg"
    DEPENDENCIES std_msgs
)

# add_executable(offboard_control src/offboard_control.cpp)
# ament_target_dependencies(offboard_control rclcpp px4_msgs)
#
# add_executable(ekf_2 src/ekf_2.cpp)
# ament_target_dependencies(ekf_2 rclcpp px4_msgs)

add_executable(attacker src/attacker.cpp)
ament_target_dependencies(attacker rclcpp std_msgs px4_msgs)

# add_executable(square_velocity_motion src/square_velocity_motion.cpp)
# ament_target_dependencies(square_velocity_motion rclcpp std_msgs px4_msgs)
#
# add_executable(square_acceleration_motion src/square_acceleration_motion.cpp)
# ament_target_dependencies(square_acceleration_motion rclcpp std_msgs px4_msgs)

add_executable(sensor_matrix_downsampler src/sensor_matrix_downsampler.cpp)
ament_target_dependencies(sensor_matrix_downsampler rclcpp std_msgs px4_msgs)
# rosidl_target_interfaces(sensor_matrix_downsampler ${PROJECT_NAME} "rosidl_typesupport_cpp")
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(sensor_matrix_downsampler "${cpp_typesupport_target}")

add_executable(offboard_control_xvel src/offboard_control_xvel.cpp)
ament_target_dependencies(offboard_control_xvel rclcpp std_msgs px4_msgs)
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(offboard_control_xvel "${cpp_typesupport_target}")

# add_executable(gz_test src/gz_test.cpp)
# ament_target_dependencies(gz_test rclcpp std_msgs geometry_msgs px4_msgs gz-transport13)

install(TARGETS
    # offboard_control
    # ekf_2
    attacker
    # square_velocity_motion
    # square_acceleration_motion 
    sensor_matrix_downsampler
    offboard_control_xvel
    # gz_test
    DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
    launch
    DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
    find_package(ament_lint_auto REQUIRED)
    # the following line skips the linter which checks for copyrights
    # comment the line when a copyright and license is added to all source files
    set(ament_cmake_copyright_FOUND TRUE)
    # the following line skips cpplint (only works in a git repo)
    # comment the line when this package is in a git repo and when
    # a copyright and license is added to all source files
    set(ament_cmake_cpplint_FOUND TRUE)
    ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_export_include_directories(include)
ament_package()
