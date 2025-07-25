
# Go-Back-N Reliable Data Transmission over UDP

This project implements the **Go-Back-N protocol** using **Python and UDP sockets** as part of my *Data Communication and Computer Networks* (DCCN) semester project.

## 💡 Features

- UDP-based client-server communication
- Go-Back-N ARQ protocol
- Custom packet header with:
  - Sequence number
  - ACK flag
  - Checksum
  - Corruption simulation
- Simulates:
  - Packet loss
  - ACK loss
  - Packet corruption
  - Timeouts and retransmissions

## 🗂️ File Structure

- `client.py`: Sender code implementing Go-Back-N logic
- `server.py`: Receiver code to validate and ACK packets
- `report.pdf`: Semester report explaining design and results

## ⚙️ How to Run

```bash
# Run server first
python server.py

# Then run client
python client.py
