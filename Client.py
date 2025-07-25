import socket
import time

from Header import (
    generate_crc32,
    validate_crc,
    retrieve_SeqNo,
    retrieve_AckFlag,
    make_data_packet,
    induce_Corruption
)

IP = 'localhost'
PORT = 9010

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(4)

# ===== Header Display =====
print("🧾 Packet Header Format:")
print("┌────────────┬────────────────────┬──────────┬────────────┐")
print("│ Seq No (1) │ Corrupt Flag (1)   │ ACK (1)  │ CRC32 (4)  │")
print("└────────────┴────────────────────┴──────────┴────────────┘\n")

def wait_for_ack():
    try:
        packet, addr = client_socket.recvfrom(1024)
        return packet, addr
    except socket.timeout:
        return None, None

# ===== Go-Back-N Config =====
WINDOW_SIZE = 4
TOTAL_PACKETS = 20
base = 0
next_seq = 0

lost_packets = {4, 8, 19}
corrupt_packets = {3, 12}
lost_acks = {5, 10}
corrupt_acks = {2, 6}
l_ack = 1
c_ack = 1
dup_ack_count = 0
last_ack_received = -1

print("\n📤 Starting Go-Back-N Transmission\n")

while base < TOTAL_PACKETS:  # checks the starting index doesnot exceed total packets
    print(f"\n📍 Sliding Window: base={base}, next_seq={next_seq}, window=({base} → {min(base + WINDOW_SIZE - 1, TOTAL_PACKETS - 1)})")

    while next_seq < base + WINDOW_SIZE and next_seq < TOTAL_PACKETS:
        payload = f"Packet {next_seq}"
        packet = make_data_packet(payload, next_seq)

        if next_seq in lost_packets:
            print(f"🚫 Packet {next_seq} LOST — not sent")
            next_seq += 1
            continue

        if next_seq in corrupt_packets:
            print(f"💥 Packet {next_seq} CORRUPTED intentionally before sending")
            packet = induce_Corruption(packet)

        print(f"📦 Sending Packet {next_seq}: '{payload}'")
        client_socket.sendto(packet, (IP, PORT))
        next_seq += 1
 
#   waiting for server's response
    ack_packet, addr = wait_for_ack()
    # if packet is acked within time
    if ack_packet:
        if not validate_crc(ack_packet):
            print(f"💥 Received CORRUPTED ACK — ignored")
            continue

        ack_seq = retrieve_SeqNo(ack_packet)
        is_ack = retrieve_AckFlag(ack_packet)
        if not is_ack:
            print(f"⚠️ Received non-ACK packet unexpectedly — ignored")
            continue

        if ack_seq in lost_acks and l_ack == 1:
            print(f"🚫 Simulated LOSS of ACK {ack_seq}")
            l_ack = 0
            continue

        if ack_seq in corrupt_acks and c_ack == 1:
            print(f"💥 Simulated CORRUPTION of ACK {ack_seq}")
            ack_seq -= 1
            c_ack = 0

        print(f"📨 Received ACK {ack_seq} from server")

        if ack_seq == last_ack_received:
            dup_ack_count += 1
            print(f"⚠️  Duplicate ACK {ack_seq} (Count: {dup_ack_count})")

            if dup_ack_count == 3:
                print(f"🚀 Fast Retransmit Triggered for Packet {ack_seq + 1}")
                payload = f"Packet {ack_seq + 1}"
                packet = make_data_packet(payload, ack_seq + 1)
                client_socket.sendto(packet, (IP, PORT))
                print(f"🔁 Retransmitted Packet {ack_seq + 1} (Fast Retransmit)")
        else:
            dup_ack_count = 0
            last_ack_received = ack_seq

        if ack_seq >= base:
            print(f"✅ Sliding window moved from base={base} to base={ack_seq + 1}")
            base = ack_seq + 1
            
    # for timeout,        
    else:
        print(f"⏰ Timeout! No ACK received. Retransmitting packets from {base} to {next_seq - 1}")
        for seq in range(base, next_seq):
            payload = f"Packet {seq}"
            packet = make_data_packet(payload, seq)
            client_socket.sendto(packet, (IP, PORT))
            print(f"🔁 Retransmitted Packet {seq}")

print("\n🎉 All packets sent and acknowledged successfully. Transmission complete.\n")
client_socket.close()
