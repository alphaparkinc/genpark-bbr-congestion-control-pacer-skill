class BBRCongestionControl:
    """
    BBR Congestion Control engine estimating Bottleneck Bandwidth (BtlBw)
    and Round-Trip Propagation Time (RTprop).
    """
    def __init__(self):
        self.state = "STARTUP"
        self.btlbw = 100.0
        self.rtprop = 0.05
        self.pacing_gain = 2.89
        self.cwnd_gain = 2.89

    def on_ack(self, delivery_rate, rtt_sample):
        if delivery_rate > self.btlbw:
            self.btlbw = delivery_rate
        if rtt_sample < self.rtprop or self.rtprop == 0:
            self.rtprop = rtt_sample

        if self.state == "STARTUP" and delivery_rate >= 1.25 * self.btlbw:
            self.state = "DRAIN"
            self.pacing_gain = 0.35
        elif self.state == "DRAIN":
            self.state = "PROBE_BW"
            self.pacing_gain = 1.0

        bdp = self.btlbw * self.rtprop
        pacing_rate = self.btlbw * self.pacing_gain
        cwnd = max(4.0, bdp * self.cwnd_gain)
        return {"state": self.state, "bdp": bdp, "pacing_rate": pacing_rate, "cwnd": cwnd}
