# --- Configuration Classes ---
class ProfileConfig:
    def __init__(
        self,
        profileId: int,
        freqStartGHz: float,
        freqEndGHz: float,  # Not in UML but essential for slope calculation
        idleTimeUsec: float,
        adcStartTimeUsec: float,
        rampSlopeMHzPerUsec: float,  # Often called rampEndTime or similar
        txPower: int = 0,  # Example additional param
        rxGain: int = 30,
    ):  # Example additional param
        self.profileId = profileId
        self.freqStartGHz = freqStartGHz
        self.freqEndGHz = freqEndGHz  # Added this for completeness
        self.idleTimeUsec = idleTimeUsec
        self.adcStartTimeUsec = adcStartTimeUsec
        self.rampSlopeMHzPerUsec = rampSlopeMHzPerUsec
        self.txPower = txPower
        self.rxGain = rxGain
        print(f"ProfileConfig {profileId} created.")

    def toCommandString(self) -> str:
        # This is a simplified representation of what a CLI command might look like
        return (
            f"profileCfg {self.profileId} {self.freqStartGHz:.2f} "
            f"{self.idleTimeUsec:.1f} {self.adcStartTimeUsec:.1f} "
            f"{(self.freqEndGHz - self.freqStartGHz) * 1000 / self.rampSlopeMHzPerUsec:.1f} "  # ADC Valid Samples Duration
            f"0 0 0 0 0 0 {self.txPower} 0 {self.rxGain} "  # Many params here
            f"{self.rampSlopeMHzPerUsec:.3f} 0 1"  # Slope, TX Start, Num ADC Samples (derived)
        )


class ChirpConfig:
    def __init__(
        self,
        chirpId: int,  # Not in TI CLI, but good for internal tracking
        profileId: int,
        startIdx: int,  # Corresponds to chirpStartIdx in TI CLI
        endIdx: int,  # Corresponds to chirpEndIdx in TI CLI
        txEnable: int = 1,  # Which TX to enable (TX1=1, TX2=2, TX3=4, TX1&TX3=5)
        idleTimeUsec: float = 0,  # Usually inherited from profile or 0
        adcStartTimeUsec: float = 0,
    ):  # Usually inherited from profile or 0
        self.chirpId = chirpId  # Our internal ID
        self.profileId = profileId
        self.startIdx = startIdx
        self.endIdx = endIdx
        self.txEnable = txEnable
        self.idleTimeUsec = idleTimeUsec  # Often part of profile, but can be overridden
        self.adcStartTimeUsec = adcStartTimeUsec  # Same as above
        print(f"ChirpConfig {chirpId} for profile {profileId} created.")

    def toCommandString(self) -> str:
        # Chirp config maps to 'chirpCfg' in TI's CLI
        # chirpCfg <startIdx> <endIdx> <profileId> <startFreqVar> <freqSlopeVar> <idleTime> <adcStartTime> <txEnable>
        return (
            f"chirpCfg {self.startIdx} {self.endIdx} {self.profileId} "
            f"0.0 0.0 {self.idleTimeUsec:.1f} {self.adcStartTimeUsec:.1f} {self.txEnable}"
        )


class FrameConfig:
    def __init__(
        self,
        frameId: int,  # Not in TI CLI, but good for internal tracking
        chirpStartIdx: int,
        chirpEndIdx: int,
        numLoops: int,  # Number of times to loop through chirps
        periodUsec: float,  # Frame periodicity
        numFrames: int = 0,  # 0 for infinite frames
        triggerSelect: int = 1,  # 1 for SW trigger
        triggerDelayUsec: float = 0,
    ):
        self.frameId = frameId
        self.chirpStartIdx = chirpStartIdx
        self.chirpEndIdx = chirpEndIdx
        self.numLoops = numLoops
        self.periodUsec = periodUsec
        self.numFrames = numFrames
        self.triggerSelect = triggerSelect
        self.triggerDelayUsec = triggerDelayUsec
        print(f"FrameConfig {frameId} created.")

    def toCommandString(self) -> str:
        # Frame config maps to 'frameCfg' in TI's CLI
        # frameCfg <chirpStartIdx> <chirpEndIdx> <numLoops> <numFrames> <framePeriodicity> <triggerSelect> <triggerDelay>
        return (
            f"frameCfg {self.chirpStartIdx} {self.chirpEndIdx} {self.numLoops} "
            f"{self.numFrames} {self.periodUsec / 1000:.3f} "  # Convert to ms for typical CLI
            f"{self.triggerSelect} {self.triggerDelayUsec:.1f} 0"  # Last 0 is for lowPowerCfg
        )
