import socket

from Header import (
    generate_crc32,
    validate_crc,
    retrieve_SeqNo,
    retrieve_AckFlag,
    make_data_packet,
    retrieve_CorruptionFlag,
    retrieve_data,
)

# ===== Server Setup =====
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 9010))
print("✅ UDP Server Listening on Port 9010...\n")

last_ack = -1

try:
    # try until the last packet from server is received
    while True:
        packet, addr = server_socket.recvfrom(1024)

        # if packet is not corrupted
        if validate_crc(packet):
            seq = retrieve_SeqNo(packet)
            is_corrupt = retrieve_CorruptionFlag(packet)
            is_ack = retrieve_AckFlag(packet)
            data = retrieve_data(packet)

            if is_ack:
                print(f"📥 Received unexpected ACK Packet {seq}, ignored")
                continue

            if is_corrupt:
                print(f"⚠️ Corruption flag set on Packet {seq}, discarding")
                continue

            # printing acks
            if seq == last_ack + 1:
                print(f"✅ Received Packet {seq} from {addr}: '{data}'")
                last_ack = seq
            else:
                print(f"❌ Out-of-order Packet {seq}, expected {last_ack + 1}")

            ack_packet = make_data_packet("", last_ack, is_ack=True)
            server_socket.sendto(ack_packet, addr)
            print(f"📤 Sent ACK {last_ack}\n")

        # if packet is corrupted
        else:
            print(f"❌ CRC failed — corrupted packet discarded")
            ack_packet = make_data_packet("", last_ack, is_ack=True)
            server_socket.sendto(ack_packet, addr)
            print(f"📤 Sent ACK {last_ack} (last known good)\n")

except KeyboardInterrupt:
    print("\n🛑 Server shutting down gracefully.")
finally:
    server_socket.close()