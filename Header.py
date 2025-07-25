import zlib

#===== CRC + Header Utilities =====
#COMBINED
# calculate crc for header + databytes using zlib
def generate_crc32(data: bytes) -> int:
    return zlib.crc32(data)

# check if crc is corrupted or not
def validate_crc(packet: bytes) -> bool:
    header = packet[:3]  
    crc_from_packet = int.from_bytes(packet[3:7], 'big')
    data = packet[7:]
    return crc_from_packet == generate_crc32(header + data)

# combine data + header to make packet
def make_data_packet(data_str: str, seq_no: int, is_ack=False, corrupted=False) -> bytes:
    data_bytes = data_str.encode()
    seq_byte = seq_no.to_bytes(1, 'big')
    corrupt_flag = (1 if corrupted else 0).to_bytes(1, 'big')
    ack_flag = (1 if is_ack else 0).to_bytes(1, 'big')
    header_wo_crc = seq_byte + corrupt_flag + ack_flag
    crc = generate_crc32(header_wo_crc + data_bytes)
    crc_bytes = crc.to_bytes(4, 'big')
    return header_wo_crc + crc_bytes + data_bytes 

def retrieve_SeqNo(packet: bytes) -> int:
    return packet[0]

def retrieve_AckFlag(packet: bytes) -> int:
    return packet[2]


#SERVER
def retrieve_CorruptionFlag(packet: bytes) -> int:
    return packet[1]

def retrieve_data(packet: bytes) -> str:
    return packet[7:].decode('utf-8')


#CLIENT
# corrupting packet by applying xor operation to first byte of data
def induce_Corruption(packet: bytes) -> bytes:
    packet = bytearray(packet)
    if len(packet) > 7:
        packet[7] ^= 0xFF  
    packet[1] = 1  
    return bytes(packet)