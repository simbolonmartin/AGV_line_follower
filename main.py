import sys
import time
import threading

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

    counter_finding_no_line = 0
    print("t\tY\ttheta\tv\tw")

    try:
        start = time.time()
        while True:
            now = time.time()
            elapsed_time = now - start
            PGV.update_value()
            velocity, rotation_speed = steering_wheel_controller(
                PGV.number_of_lanes, PGV.angle_value, PGV.y_position
            )
            print(
                f"{elapsed_time:.2f}\t{PGV.y_position}\t{PGV.angle_value}\t{velocity:.2f}\t{rotation_speed:.2f}"
            )
            handle.go(velocity, rotation_speed)
            time.sleep(0.01)

            if velocity == 0:
                time.sleep(2)
                break

    except Exception as error:
        print(error)
    finally:
        handle.close_driver()
        handle.close_port()
