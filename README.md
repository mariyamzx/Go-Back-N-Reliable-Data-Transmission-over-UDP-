# 📡 Go-Back-N Reliable Data Transmission over UDP

This project implements the **Go-Back-N (GBN)** protocol using **UDP sockets in Python**. It was developed as a semester project for the *Data Communication and Computer Networks* course at PIEAS.

The system simulates reliable data transfer over an unreliable protocol (UDP) by incorporating real-world network conditions such as **packet loss**, **corruption**, **ACK loss**, and **timeouts**.

---

## ✨ Features

- ✅ Go-Back-N protocol with sliding window
- 📬 Custom packet header including:
  - Sequence number
  - ACK flag
  - Corruption flag
  - CRC32 checksum
- 💡 Simulated network challenges:
  - Packet loss
  - ACK loss
  - Packet corruption
  - Timeout handling
  - Fast retransmission on 3 duplicate ACKs

---

## 📂 Project Files

.
├── client.py # Sender side implementation (GBN logic)
├── server.py # Receiver side logic (ACK responder)
├── Header.py # Header structure, checksum handling
├── report.pdf # Semester project report
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🚀 How to Run

> Run both client and server in **separate terminals**.

### 1. Run the server:
```bash
python server.py
2. Run the client:
bash
Copy
Edit
python client.py
The client will start sending 20 packets using the GBN protocol. Some packets and ACKs are intentionally dropped or corrupted to test reliability.

⚙️ Simulated Behavior
Lost packets: 4, 8, 19

Corrupted packets: 3, 12

Lost ACKs: 5, 10

Corrupted ACKs: 2, 6

These are hardcoded to simulate real-world network unreliability.

📘 Concepts Covered
Sliding Window Protocol (GBN)

CRC32 checksum for data validation

UDP socket programming

Timeout & retransmission logic

Duplicate ACK detection & fast retransmit

