from datetime import datetime
import time


previous_error = 0
sum_error_y_position = 0
sum_error_angle_value = 0
old_y_position = 0
old_angle_value = 0
start_time = 0
end_time = 0
counter_pid = 0

def steering_wheel_controller(number_of_lanes:int, angle_value:int, y_position:int):
    global velocity, rotation_speed, sum_error, previous_error, old_angle_value, old_y_position,\
    start_time, end_time, counter_pid, sum_error_angle_value, sum_error_y_position
    
    Kp_y_position = 0.001
    Kp_angle_value = 0.003
    Ki = 0
    Kd = 0
    pgv_position = "center"
    # algorithm = "combination"
    algorithm = "high_speed"
    if counter_pid == 0:
        dt = 0
        start_time = datetime.now()
        counter_pid += 1

    else:
        end_time = datetime.now()
        timespan = (end_time - start_time)
        timespan_ms = timespan.total_seconds() *1000
        dt = timespan_ms


    if number_of_lanes != 1:
        # print(f'{number_of_lanes} lane(s) are detected. It has to be 1')
        print(f'Stopping point detected')
        velocity = 0.00
        rotation_speed = 0 
        
    else:
        if pgv_position == "front":
            if abs(y_position) <= 3:
                velocity = 0.03
                rotation_speed = 0 
            else:
                velocity = 0.03    
                # rotation_speed = - Kp * angle_value
                rotation_speed = Kp_y_position * y_position
        elif pgv_position == "center":
            if algorithm == "y_position":
                if abs(y_position) <= 3:
                    velocity = 0.015
                    rotation_speed = 0 
                else:
                    velocity = 0.015    
                    # rotation_speed = - Kp * angle_value
                    rotation_speed = Kp_y_position * y_position
            elif algorithm == "angle_value":
                if abs(angle_value) <= 3:
                    velocity = 0.03
                    rotation_speed = 0
                else:
                    velocity = 0
                    rotation_speed = Kp_angle_value * angle_value
            elif algorithm == "combination":
                if abs(angle_value) + abs(y_position) > 5:
                    # error_total = angle_value + y_position
                    velocity = 0.03
                    rotation_speed = Kp_angle_value * angle_value + Kp_y_position* y_position
                else:
                    velocity = 0.03
                    rotation_speed = 0
            elif algorithm == "high_speed":
                if abs(angle_value) + abs(y_position) > 5:
                    # error_total = angle_value + y_position
                    velocity = 0.1
                    Kp_angle_value = 0.01
                    Kp_y_position = 0.005
                    
                    Kd_angle_value = 0.01
                    Kd_y_position = 0.01
                    
                    
                    dt = 1
                    
                    Ki_angle_value = 0.0
                    Ki_y_position = 0.0
                    
                    p = Kp_angle_value * angle_value + Kp_y_position* y_position 
                    d_angle_value = angle_value - old_angle_value
                    d_y_position = y_position - old_y_position
                    d = Kd_angle_value * d_angle_value + Kd_y_position * d_y_position
                    
                    sum_error_angle_value = sum_error_angle_value + angle_value * dt
                    sum_error_y_position = sum_error_y_position + y_position * dt
                    
                    i_angle_value = Ki_angle_value * sum_error_angle_value 
                    i_y_position = Ki_y_position * sum_error_y_position 
                    i =  i_angle_value + i_y_position
                    rotation_speed = p + i + d
                    print(f"angle_value = {angle_value} \t y_position = {y_position}\trotation_speed= {rotation_speed:.4f}\t p = {p:.4f} \t d  = {d:.4f} \td_angle = {d_angle_value} \td_y_position =  {d_y_position}")

                    old_angle_value = angle_value
                    old_y_position = y_position
                
                else:
                    velocity = 0.1
                    rotation_speed = 0
                    # print(f"angle_value = {angle_value} y_position = {y_position}")
                    
    # print(f"velocity: {velocity} \t rotation_speed {rotation_speed}")

    # velocity = 0
    # rotation_speed = 0
    return velocity, rotation_speed

    # return -velocity, -rotation_speed
