from typing import List, Optional

from .calibration import Calibration
from .communication_interfaces import SPIInterface, UARTInterface
from .configs import ChirpConfig, FrameConfig, ProfileConfig
from .data_acquisition import DataAcquisition
from .data_place_holders import RawData
from .data_processing import DataProcessing


# --- Main Radar Class ---
class AWR1843Radar:
    def __init__(
        self,
        spi_mode: int = 0,
        spi_speed: int = 1000000,
        uart_port: str = "/dev/ttyUSB0",
        uart_baud: int = 115200,
        data_uart_port: str = "/dev/ttyUSB1",
        data_uart_baud: int = 921600,
    ):  # Common for data
        # Initialize interfaces
        self.spiInterface = SPIInterface(mode=spi_mode, speedHz=spi_speed)
        self.uartInterface = UARTInterface(port=uart_port, baudRate=uart_baud)
        # TI devices often use a separate UART for configuration and data
        # For simulation simplicity, we can reuse UARTInterface or create a distinct one if needed.
        # Let's assume data comes over a separate logical channel, handled by DataAcquisition
        self.dataUartInterface = UARTInterface(
            port=data_uart_port, baudRate=data_uart_baud
        )

        # Configuration storage
        self.profileConfig: Optional[ProfileConfig] = None
        self.chirpConfigs: List[ChirpConfig] = []
        self.frameConfig: Optional[FrameConfig] = None

        # State
        self.calibrated: bool = False
        self._powered_on: bool = False
        self._initialized: bool = False
        self._capturing: bool = False

        # Functional components
        self.calibration_module = Calibration(self.uartInterface)
        self.data_acquisition_module = DataAcquisition(
            self.dataUartInterface
        )  # Pass the data UART
        self.data_processing_module = DataProcessing()

        print("AWR1843Radar instance created.")

    def _send_config_command(self, command: str) -> bool:
        self.uartInterface.sendCommand(command)
        response = self.uartInterface.readResponse()
        if "Done" in response:  # Or check for specific success indicators
            print(f"Command '{command.split()[0]}...' successful.")
            return True
        else:
            print(
                f"Command '{command.split()[0]}...' failed or got unexpected response: {response}"
            )
            return False

    def powerOn(self) -> None:
        print("AWR1843Radar: Powering ON...")
        # In a real system, this might involve enabling a power supply or a reset sequence via SPI
        self.spiInterface._ensure_open()  # Simulate opening SPI for potential firmware load
        self.uartInterface._ensure_open()  # Open UART for commands
        self.dataUartInterface._ensure_open()  # Open Data UART
        # Simulate firmware download if applicable (often over SPI or UART)
        # self.spiInterface.transfer(b'\xde\xad\xbe\xef') # Example firmware chunk
        self._powered_on = True
        print("AWR1843Radar: Powered ON.")

    def initialize(self) -> bool:
        if not self._powered_on:
            print("AWR1843Radar: Cannot initialize. Radar is not powered on.")
            return False
        print("AWR1843Radar: Initializing...")
        # Initialization might involve sending some basic setup commands or checks
        # e.g., checking firmware version
        self.uartInterface.sendCommand("version")
        fw_version = self.uartInterface.readResponse()
        print(f"AWR1843Radar: Firmware version (simulated): {fw_version}")
        # For this simulation, just set a flag
        self._initialized = True
        print("AWR1843Radar: Initialized.")
        return True

    def configureProfile(self, p: ProfileConfig) -> bool:
        if not self._initialized:
            print("AWR1843Radar: Cannot configure profile. Radar not initialized.")
            return False
        print(f"AWR1843Radar: Configuring profile {p.profileId}...")
        self.profileConfig = p
        if self._send_config_command(p.toCommandString()):
            print(f"AWR1843Radar: Profile {p.profileId} configured.")
            return True
        else:
            print(f"AWR1843Radar: Failed to configure profile {p.profileId}.")
            self.profileConfig = None  # Revert on failure
            return False

    def configureChirps(self, chirps: List[ChirpConfig]) -> bool:
        if not self._initialized:
            print("AWR1843Radar: Cannot configure chirps. Radar not initialized.")
            return False
        if not self.profileConfig:
            print("AWR1843Radar: Profile must be configured before chirps.")
            return False

        print(f"AWR1843Radar: Configuring {len(chirps)} chirps...")
        temp_chirps = []
        all_successful = True
        for chirp in chirps:
            if chirp.profileId != self.profileConfig.profileId:
                print(
                    f"AWR1843Radar: Chirp {chirp.chirpId} profileId mismatch. Skipping."
                )
                all_successful = False
                continue
            if self._send_config_command(chirp.toCommandString()):
                temp_chirps.append(chirp)
                print(f"AWR1843Radar: Chirp {chirp.chirpId} configured.")
            else:
                print(f"AWR1843Radar: Failed to configure chirp {chirp.chirpId}.")
                all_successful = False
                break  # Stop on first failure for simplicity

        if all_successful:
            self.chirpConfigs = temp_chirps
            print(
                f"AWR1843Radar: All {len(self.chirpConfigs)} chirps configured successfully."
            )
            return True
        else:
            # Potentially revert successfully configured chirps in a real system
            print(f"AWR1843Radar: Chirp configuration failed or was partial.")
            return False

    def configureFrame(self, f: FrameConfig) -> bool:
        if not self._initialized:
            print("AWR1843Radar: Cannot configure frame. Radar not initialized.")
            return False
        if not self.chirpConfigs:
            print("AWR1843Radar: Chirps must be configured before frame.")
            return False
        # Validate chirp indices in frame config
        max_chirp_idx = max(c.endIdx for c in self.chirpConfigs)
        if f.chirpStartIdx > max_chirp_idx or f.chirpEndIdx > max_chirp_idx:
            print(
                f"AWR1843Radar: Frame chirp indices ({f.chirpStartIdx}-{f.chirpEndIdx}) out of bounds for configured chirps (max_idx={max_chirp_idx})."
            )
            return False

        print(f"AWR1843Radar: Configuring frame {f.frameId}...")
        self.frameConfig = f
        if self._send_config_command(f.toCommandString()):
            print(f"AWR1843Radar: Frame {f.frameId} configured.")
            return True
        else:
            print(f"AWR1843Radar: Failed to configure frame {f.frameId}.")
            self.frameConfig = None  # Revert on failure
            return False

    def calibrate(self) -> bool:
        if not self._initialized:
            print("AWR1843Radar: Cannot calibrate. Radar not initialized.")
            return False
        print("AWR1843Radar: Starting calibration process...")
        if self.calibration_module.performSelfCal():
            self.calibrated = True
            calib_data = self.calibration_module.getCalibData()
            print(
                f"AWR1843Radar: Calibration successful. Data: {calib_data.data if calib_data else 'N/A'}"
            )
            return True
        else:
            self.calibrated = False
            print("AWR1843Radar: Calibration failed.")
            return False

    def startCapture(self) -> bool:
        if not self._initialized:
            print("AWR1843Radar: Cannot start capture. Radar not initialized.")
            return False
        if not self.frameConfig:
            print("AWR1843Radar: Cannot start capture. Frame not configured.")
            return False
        # if not self.calibrated: # Some systems might require calibration first
        #     print("AWR1843Radar: Warning - starting capture without calibration.")

        print("AWR1843Radar: Starting capture...")
        if self._send_config_command("sensorStart"):
            self._capturing = True
            self.data_acquisition_module.start()
            print("AWR1843Radar: Capture started.")
            return True
        else:
            print("AWR1843Radar: Failed to start sensor/capture.")
            return False

    def stopCapture(self) -> None:
        if not self._capturing:
            print("AWR1843Radar: Capture not active.")
            return
        print("AWR1843Radar: Stopping capture...")
        self.data_acquisition_module.stop()  # Stop data acquisition first
        if self._send_config_command("sensorStop"):
            self._capturing = False
            print("AWR1843Radar: Capture stopped.")
        else:
            print("AWR1843Radar: Failed to stop sensor. Forcing capture flag off.")
            self._capturing = False  # Still update state

    def readData(self) -> Optional[RawData]:
        if not self._capturing:
            print("AWR1843Radar: Not capturing. Cannot read data.")
            return None
        print("AWR1843Radar: Reading data...")
        raw_data = self.data_acquisition_module.captureADC()
        if raw_data:
            print("AWR1843Radar: Data read successfully.")
        else:
            print("AWR1843Radar: Failed to read data.")
        return raw_data

    def powerOff(self):
        print("AWR1843Radar: Powering OFF...")
        if self._capturing:
            self.stopCapture()
        self.uartInterface.close()
        self.dataUartInterface.close()
        self.spiInterface.close()
        self._powered_on = False
        self._initialized = False
        self.calibrated = False
        print("AWR1843Radar: Powered OFF.")
