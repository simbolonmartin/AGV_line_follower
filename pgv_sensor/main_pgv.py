from read_write_serial_hex import PGVCommunication

velocity = 0
rotation_speed = 0 

if __name__ == "__main__":
    PGV = PGVCommunication()
    for a in range(0,5000):
        PGV.update_value()   #TODO: make this a thread?
        # print(f'number_of_lanes: {PGV.number_of_lanes} \t angle_value: {PGV.angle_value} \t y_position: {PGV.y_position} \t velocity: {velocity} \trotation_speed: {rotation_speed}')
        print(f'number_of_lanes: {PGV.number_of_lanes} \t angle_value: {PGV.angle_value} \t y_position: {PGV.y_position}')

        








