def add_checksum(input_data):
    checksum = sum(input_data[2:])
    LSB = checksum % 256
    MSB = (checksum - LSB) // 256 % 256
    return input_data + [LSB, MSB, 0, 0]