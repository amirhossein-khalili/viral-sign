from typing import Optional


# --- Communication Interfaces (Simulated) ---
class SPIInterface:
    def __init__(self, mode: int = 0, speedHz: int = 1000000):
        self.mode = mode
        self.speedHz = speedHz
        self._is_open = False
        print(f"SPIInterface initialized: mode={mode}, speed={speedHz}Hz")

    def _ensure_open(self):
        if not self._is_open:
            # In a real scenario, this would open the SPI device
            self._is_open = True
            print("SPIInterface: Device opened.")

    def transfer(self, data_out: bytes) -> bytes:
        self._ensure_open()
        print(f"SPIInterface: Transferring {len(data_out)} bytes: {data_out.hex()}")
        # Simulate receiving data; for now, echo back or return predefined response
        data_in = b"\x00" * len(data_out)  # Dummy response
        print(f"SPIInterface: Received {len(data_in)} bytes: {data_in.hex()}")
        return data_in

    def close(self):
        if self._is_open:
            self._is_open = False
            print("SPIInterface: Device closed.")


class UARTInterface:
    def __init__(self, port: str, baudRate: int):
        self.port = port
        self.baudRate = baudRate
        self._is_open = False
        print(f"UARTInterface initialized: port={port}, baudrate={baudRate}")

    def _ensure_open(self):
        if not self._is_open:
            # In a real scenario, this would open the serial port
            self._is_open = True
            print(f"UARTInterface: Port {self.port} opened.")

    def sendCommand(self, cmd: str) -> None:
        self._ensure_open()
        print(f"UARTInterface: Sending command: '{cmd}'")
        # Simulate sending command
        # In a real scenario, you'd write cmd.encode() + b'\n' to the serial port

    def readResponse(self, timeout_sec: float = 1.0) -> str:
        self._ensure_open()
        # Simulate reading a response
        # This is highly simplified. Real UART involves reading until newline,
        # handling prompts, and timeouts.
        response = "Done"  # Generic success response
        print(f"UARTInterface: Reading response (simulated): '{response}'")
        return response

    def readDataPortPacket(
        self, expected_bytes: int, timeout_sec: float = 2.0
    ) -> Optional[bytes]:
        """Simulates reading a data packet from the radar's data UART port."""
        self._ensure_open()  # Assuming data port uses similar open/close logic
        print(f"UARTInterface (Data Port): Attempting to read {expected_bytes} bytes.")
        # Simulate some delay and data reception
        # In a real scenario, this would read from a separate data UART port.
        # For simulation, we can generate dummy data.
        if self._is_open:  # Simple check if radar is supposed to be sending data
            # Generate some dummy bytes, e.g., a simple pattern
            dummy_packet_data = bytes([i % 256 for i in range(expected_bytes)])
            print(
                f"UARTInterface (Data Port): Successfully read {len(dummy_packet_data)} dummy bytes."
            )
            return dummy_packet_data
        print(
            "UARTInterface (Data Port): Failed to read (simulated - port not ready or no data)."
        )
        return None

    def close(self):
        if self._is_open:
            self._is_open = False
            print(f"UARTInterface: Port {self.port} closed.")
