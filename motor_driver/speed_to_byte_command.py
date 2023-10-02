

def speed_to_byte_command(speed):
    return int.to_bytes(speed, 4, 'little', signed=True)


print(speed_to_byte_command(9))

