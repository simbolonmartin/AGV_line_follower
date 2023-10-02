import sys
import time
sys.path.append("./controller")
sys.path.append("./motor_driver")
sys.path.append("./pgv_sensor")

from pid_controller import steering_wheel_controller
from motor_driver_lib import MotorCommunication
from read_write_serial_hex import PGVCommunication

if __name__ == "__main__":
    PGV = PGVCommunication()
    handle = MotorCommunication()
    handle.check_conn()
    handle.initialize_driver()
    # handle.go(0.03, 0)
    # time.sleep(2)
    # handle.go(0.03, -0.13)
    # time.sleep(3)
    # handle.go(0, 0)
    # time.sleep(3)
    # counter = 0
    counter_finding_no_line = 0
    try:
        while True:
            PGV.update_value()   
            velocity, rotation_speed = steering_wheel_controller(PGV.number_of_lanes, PGV.angle_value, PGV.y_position)
            print(f"y_position = {PGV.y_position:.2f} \t angle_value = {PGV.angle_value:.2f} \t velocity: {velocity:.2f} \trotation_speed:{rotation_speed:.2f}")
            handle.go(velocity, rotation_speed)
            if velocity == 0:
                time.sleep(2)
                break
            # print(counter)
            # counter+=1
            # if PGV.number_of_lanes == 0:
            #     counter_finding_no_line +=1
            #     if counter_finding_no_line >= 10:
            #         print("rotating")
            #         handle.go(0,0.03)
            #         time.sleep(51)
    except:
        pass
    finally:
        handle.close_driver()
        handle.close_port()
    
    # handle.close_driver()
    # handle.close_port()
