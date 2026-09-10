from client import BBRCongestionControl

def main():
    print("=== Testing BBR Congestion Control Pacer ===")
    bbr = BBRCongestionControl()
    res = bbr.on_ack(delivery_rate=250.0, rtt_sample=0.04)
    print("BBR state:", res)
    assert res["bdp"] > 0
    assert res["cwnd"] >= 4.0
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
