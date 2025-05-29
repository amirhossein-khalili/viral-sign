# --- Example Usage ---
from .configs import ChirpConfig, FrameConfig, ProfileConfig
from .main import AWR1843Radar

if __name__ == "__main__":
    print("--- AWR1843 Radar Simulation Start ---")

    # Create a radar instance
    # Use dummy ports for simulation; these wouldn't connect to real hardware here
    radar = AWR1843Radar(uart_port="COM_CFG_SIM", data_uart_port="COM_DATA_SIM")

    # Power on and initialize
    radar.powerOn()
    if not radar.initialize():
        print("Failed to initialize radar. Exiting.")
        exit()

    # Define configurations
    profile0 = ProfileConfig(
        profileId=0,
        freqStartGHz=77.0,
        freqEndGHz=77.4,  # Example: 400MHz bandwidth
        idleTimeUsec=7.0,
        adcStartTimeUsec=5.0,
        rampSlopeMHzPerUsec=50.0,  # (77.4-77)*1000 / duration_us
        # If duration is e.g. 8us (400MHz/50MHz/us)
        txPower=3,
        rxGain=30,
    )

    chirp0 = ChirpConfig(
        chirpId=0, profileId=0, startIdx=0, endIdx=0, txEnable=1
    )  # TX1
    chirp1 = ChirpConfig(
        chirpId=1, profileId=0, startIdx=1, endIdx=1, txEnable=2
    )  # TX2 (if MIMO)

    # Note: TI's frameCfg chirpStartIdx and chirpEndIdx refer to the indices used in chirpCfg commands.
    # So if you define 2 chirps with startIdx=0, endIdx=0 and startIdx=1, endIdx=1 respectively,
    # your frame will use chirpStartIdx=0 and chirpEndIdx=1 to loop through both.
    frame0 = FrameConfig(
        frameId=0,
        chirpStartIdx=0,  # Use chirp defined with startIdx=0
        chirpEndIdx=1,  # Use chirp defined with startIdx=1 (loops from 0 to 1)
        numLoops=64,  # 64 doppler bins
        periodUsec=50000,  # 50ms frame rate -> 20 FPS
    )

    # Configure the radar
    if not radar.configureProfile(profile0):
        print("Profile configuration failed.")
        radar.powerOff()
        exit()

    if not radar.configureChirps([chirp0, chirp1]):
        print("Chirp configuration failed.")
        radar.powerOff()
        exit()

    if not radar.configureFrame(frame0):
        print("Frame configuration failed.")
        radar.powerOff()
        exit()

    if not radar.calibrate():
        print("Calibration failed. Continuing without...")
        # Depending on requirements, you might exit here

    # Start capturing data
    if not radar.startCapture():
        print("Failed to start capture.")
        radar.powerOff()
        exit()

    # Read a few frames of data (simulated)
    for i in range(3):
        print(f"\n--- Reading Frame {i+1} ---")
        raw_frame_data = radar.readData()
        if raw_frame_data:
            print(f"Received RawData with {len(raw_frame_data.data)} bytes.")
            # Process the data
            point_cloud = radar.data_processing_module.parseRaw(raw_frame_data)
            if point_cloud and point_cloud.points:
                print(
                    f"Processed into PointCloud with {len(point_cloud.points)} points."
                )
                targets = radar.data_processing_module.applyCFAR(point_cloud)
                print(f"CFAR resulted in {len(targets.targets)} targets.")
                if targets.targets:
                    print(f"First target (simulated): {targets.targets[0]}")
            else:
                print("No points in point cloud after parsing.")
        else:
            print("Failed to read data for this frame.")
            break  # Stop if data read fails

    # Stop capture and power off
    radar.stopCapture()
    radar.powerOff()

    print("\n--- AWR1843 Radar Simulation End ---")
