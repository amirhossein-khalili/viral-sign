from .data_place_holders import PointCloud, RawData, TargetList


class DataProcessing:
    def __init__(self):
        print("DataProcessing module initialized.")

    def parseRaw(self, raw: RawData) -> PointCloud:
        print(f"DataProcessing: Parsing RawData ({len(raw.data)} bytes)...")
        # Simulate parsing. This is where FFT, detection, etc., would happen.
        # For now, generate a dummy point cloud.
        num_points = (
            len(raw.data) // 16
        )  # Assuming 16 bytes per point (e.g., x,y,z,doppler as floats)
        points = []
        for i in range(num_points):
            # Dummy point data
            points.append(
                {
                    "x": i * 0.1,
                    "y": i * 0.05,
                    "z": 0,
                    "doppler": i * 0.01,
                    "snr": 10.0,
                    "noise": 1.0,
                }
            )
        print(
            f"DataProcessing: RawData parsed into PointCloud with {num_points} points."
        )
        return PointCloud(points)

    def applyCFAR(self, pc: PointCloud) -> TargetList:
        print(
            f"DataProcessing: Applying CFAR to PointCloud with {len(pc.points)} points..."
        )
        # Simulate CFAR filtering.
        # For now, let's assume CFAR keeps half the points as targets.
        targets = []
        for i, point in enumerate(pc.points):
            if i % 2 == 0:  # Arbitrary condition for simulation
                targets.append(
                    {
                        "id": i,
                        "position": (point["x"], point["y"], point["z"]),
                        "velocity": point["doppler"],
                    }
                )
        print(f"DataProcessing: CFAR applied. {len(targets)} targets identified.")
        return TargetList(targets)
