import sys
import json
from client import BBRCongestionControl

def main():
    bbr = BBRCongestionControl()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "on_ack":
            res = bbr.on_ack(params.get("delivery_rate", 100.0), params.get("rtt_sample", 0.05))
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
