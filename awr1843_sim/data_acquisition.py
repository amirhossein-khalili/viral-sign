from typing import Optional
from .communication_interfaces import UARTInterface
from .data_place_holders import RawData


class DataAcquisition:
    def __init__(
        self, radar_data_uart: UARTInterface
    ):  # Assuming data comes over a UART
        self._radar_data_uart = radar_data_uart
        self._is_capturing = False
        print("DataAcquisition module initialized.")

    def start(self):
        self._is_capturing = True
        print("DataAcquisition: Capture started (simulated).")

    def stop(self):
        self._is_capturing = False
        print("DataAcquisition: Capture stopped (simulated).")

    def captureADC(self) -> Optional[RawData]:
        if not self._is_capturing:
            print("DataAcquisition: Not capturing. Call start() first.")
            return None

        print("DataAcquisition: Attempting to capture ADC data...")
        # Simulate reading a frame of data. The size depends on the config.
        # For now, let's assume a fixed size or a simple mechanism.
        # In a real system, you'd read from the data UART port until a full packet is received.
        # This often involves parsing a header to know the packet size.
        simulated_packet_size = 1024  # bytes, arbitrary for simulation
        packet_bytes = self._radar_data_uart.readDataPortPacket(simulated_packet_size)

        if packet_bytes:
            print(f"DataAcquisition: ADC data captured ({len(packet_bytes)} bytes).")
            return RawData(packet_bytes)
        else:
            print(
                "DataAcquisition: Failed to capture ADC data (simulated timeout or error)."
            )
            return None
