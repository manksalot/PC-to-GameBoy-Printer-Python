def send_packet(arduino_obj, packet_TX):
    for byte in packet_TX:
        arduino_obj.write(bytes([byte]))
        arduino_obj.read(1)