# Crazyflie Learning Lab

A lightweight collection of Python test scripts for interacting with the Bitcraze Crazyflie 2.X quadcopter using the official Crazyflie Python library (`cflib`).

---

## Installation & Requirements

Install dependencies using the included `requirements.txt`:

```bash
pip install -r requirements.txt
```

### USB Permissions (Linux)
To communicate with the Crazyradio PA dongle without root permissions, ensure your user is in the `plugdev` group and udev rules are installed:
```bash
sudo usermod -a -G plugdev $USER
```
See the [Bitcraze USB Permissions Guide](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/) for complete setup instructions.

---

## Configuration (`config.py`)

All scripts in this repository share a single configuration file ([config.py](config.py)) that defines the Crazyflie radio URI.

The URI follows this format:
```
radio://<radio_interface>/<radio_channel>/<radio_bandwidth>/<crazyflie_address>
```

- **radio_interface**: The Crazyradio dongle index (typically `0`).
- **radio_channel**: The radio frequency channel (e.g., `80`).
- **radio_bandwidth**: The transmission datarate (`250K`, `1M`, or `2M`).
- **crazyflie_address**: The 5-byte hex address of the Crazyflie (e.g., `E7E7E7E7E7`).

You can edit `URI` directly in `config.py`, or override it without modifying code via the `CRAZYFLIE_URI` environment variable:
```bash
export CRAZYFLIE_URI="radio://0/80/2M/E7E7E7E7E7"
```

### Checking Your Crazyflie Address & Channel via `cfclient`
If you do not know which address, channel, or datarate your Crazyflie is configured with, you can scan and inspect it using the official graphical client **`cfclient`** (Crazyflie PC Client):

- **Installation Guide**: [Install cfclient documentation](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/installation/install/)
- **Quick Install**:
  ```bash
  pip install cfclient
  ```
- Once installed, launch the GUI (`cfclient`), click **Scan** to locate your drone over the Crazyradio, or connect the Crazyflie via a micro-USB cable and open **Connect -> Configure 2.X** to view and modify its radio address and channel.

---

## Scripts Description

### 1. [HelloCrazy.py](HelloCrazy.py)
Tests basic communication with the Crazyflie. After establishing a synchronous connection (`SyncCrazyflie`), it sequentially spins each motor individually (M1 through M4) at low PWM power using the `motorPowerSet` parameter group, printing which motor is currently spinning in the terminal to provide physical feedback, then safely disconnects.

```bash
python HelloCrazy.py
```

### 2. [check_battery.py](check_battery.py)
Connects and reads the current battery voltage (`pm.vbat`) using the `SyncLogger` framework. It calculates and prints the battery percentage (based on a 1-cell LiPo curve: 3.3 V empty to 4.2 V full) and issues a warning if the voltage drops below the critical 3.4 V safety threshold.

```bash
python check_battery.py
```

### 3. [LoggerCrazy.py](LoggerCrazy.py)
Streams real-time IMU stabilization variables (`stabilizer.roll`, `stabilizer.pitch`, `stabilizer.yaw`). Data is formatted in an organized tabular view rounded to 2 decimal places and displayed every 2 seconds (`period_in_ms=2000`).

```bash
python LoggerCrazy.py
```

### 4. [bruteForce_takeoff.py](bruteForce_takeoff.py)
Performs an open-loop thrust setpoint test.

> **CRITICAL SAFETY WARNINGS**:
> - **Never set throttle to maximum (65535)**: Maximum throttle is extremely aggressive and will shoot the drone upward uncontrollably into ceilings or walls.
> - **Keep thrust within a conservative range**: Maintain thrust strictly between **30000 and 45000** (hover range is typically around 38000 - 42000).
> - **Position Estimation (OptiTrack)**: The Crazyflie cannot maintain stable position in open-loop mode. Without external position feedback (like OptiTrack), the drone will drift.
> - **Firmware Compatibility**: The drone **must be flashed with our custom firmware**. Newer official upstream firmware releases do not permit or accept these raw open-loop thrust setpoint commands due to arming and commander restrictions.

```bash
python bruteForce_takeoff.py
```

---

## OptiTrack Integration & Special Acknowledgments

Our setup does not use the official Bitcraze Flow deck. Instead, we achieve autonomous and stable flight by streaming 6DoF position and orientation estimation from an **OptiTrack** motion capture system.

We would like to extend our deepest gratitude and recognition to **Kevin Martinez** (GitHub: [**@Fairbrook**](https://github.com/Fairbrook)) and his work on:

- **Repository**: [https://github.com/covenant-tec](https://github.com/covenant-tec)
- **Key Projects**: `crazybridge`, `crazyflie-firmware`, `optitrack_client`, `crazybridge_interfaces`

Thanks to Kevin's open-source architecture, custom Crazyflie firmware modifications, and bridge packages, we have been able to reliably interface our Crazyflie drones with OptiTrack motion capture and achieve stable closed-loop flight without needing the official Flow deck. Thank you, Kevin, for making this possible!

---

## Author
Alejandro Mojarras - mojarrasalejandro@gmail.com

Project developed for the technical advancement and benefit of the **DroneOps** student group at **Tecnológico de Monterrey (ITESM), Campus Guadalajara**.

---

## Official Documentation Links

- [Bitcraze Official Website](https://www.bitcraze.io/)
- [Crazyflie Python Library (cflib) Documentation](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/)
- [Crazyflie 2.X Getting Started Guide](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/)
- [Crazyflie Logging and Parameter Framework](https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/functional-areas/logparam/)
- [Crazyradio PA Hardware Documentation](https://www.bitcraze.io/documentation/hardware/crazyradio/crazyradio-pa/)
- [Bitcraze GitHub Repositories](https://github.com/bitcraze)
