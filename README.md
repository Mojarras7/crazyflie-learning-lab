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

## Configuration & Radio URI (`config.py`)

All scripts in this repository resolve the Crazyflie connection URI through a unified configuration file ([config.py](config.py)).

### Radio URI Structure
```
radio://<radio_interface>/<radio_channel>/<radio_bandwidth>/<crazyflie_address>
```
- **radio_interface**: The Crazyradio dongle index (`0`).
- **radio_channel**: Frequency channel (default: `80`).
- **radio_bandwidth**: Transmission datarate (`2M`, `1M`, or `250K`).
- **crazyflie_address**: 5-byte hex address (`E7E7E7E7E7`).

**Default URI**: `radio://0/80/2M/E7E7E7E7E7` (Channel 80).

---

### How to Change the URI (Multiple Intuitive Ways)

You can choose whichever method best fits your workflow:

#### 1. Command-Line Argument (Fastest & Most Intuitive)
You do not need to edit any code or set environment variables. Pass the URI or just the channel number directly when executing any script:

- **Pass only the channel** (keeps default address `E7E7E7E7E7` and datarate `2M`):
  ```bash
  python HelloCrazy.py 90
  ```
- **Pass the full URI**:
  ```bash
  python HelloCrazy.py radio://0/90/2M/E7E7E7E7E7
  ```
- **Using optional flags**:
  ```bash
  python HelloCrazy.py --channel 90
  python HelloCrazy.py --uri radio://0/90/2M/E7E7E7E7E7
  ```

#### 2. Auto-Detect via Scanner (`scan.py`)
If you do not know which channel or address your Crazyflie is using, run our lightweight scanner:
```bash
python scan.py
```
This scans all 2.4 GHz channels and lists all discovered Crazyflies along with their exact URIs and ready-to-run commands.

#### 3. Edit `config.py` Directly
If you prefer a permanent default for your setup, open [config.py](config.py) and simply edit the parameters:
```python
RADIO_CHANNEL = 80          # Change to your drone's channel (e.g. 90)
CRAZYFLIE_ADDRESS = "E7E7E7E7E7"
RADIO_INTERFACE = 0
RADIO_DATARATE = "2M"
```

#### 4. Environment Variables
You can also override the URI across an entire shell session:
```bash
# By full URI (both variable names are supported)
export CRAZYFLIE_URI="radio://0/90/2M/E7E7E7E7E7"
# or
export CFLIB_URI="radio://0/90/2M/E7E7E7E7E7"

# Or by channel number only:
export CRAZYFLIE_CHANNEL=90
```

#### 5. Inspecting via `cfclient` GUI (Alternative)
You can also view or reconfigure your drone's channel and address using the official Bitcraze client:
```bash
pip install cfclient
cfclient
```
Connect the Crazyflie via micro-USB and open **Connect -> Configure 2.X**.

---

## Scripts Description

### 1. [scan.py](scan.py)
Scans 2.4 GHz radio channels using the Crazyradio dongle and automatically discovers all active Crazyflies nearby. It prints their full URIs, channel numbers, and copy-paste commands to test them immediately without needing `cfclient`.

```bash
python scan.py
```

### 2. [HelloCrazy.py](HelloCrazy.py)
Tests basic communication with the Crazyflie. After establishing a synchronous connection (`SyncCrazyflie`), it sequentially spins each motor individually (M1 through M4) at low PWM power using the `motorPowerSet` parameter group, printing which motor is currently spinning in the terminal to provide physical feedback, then safely disconnects.

```bash
# Using default channel 80:
python HelloCrazy.py

# Or targeting a specific channel:
python HelloCrazy.py 90
```

### 3. [check_battery.py](check_battery.py)
Connects and reads the current battery voltage (`pm.vbat`) using the `SyncLogger` framework. It calculates and prints the battery percentage (based on a 1-cell LiPo curve: 3.3 V empty to 4.2 V full) and issues a warning if the voltage drops below the critical 3.4 V safety threshold.

```bash
python check_battery.py
```

### 4. [LoggerCrazy.py](LoggerCrazy.py)
Streams real-time IMU stabilization variables (`stabilizer.roll`, `stabilizer.pitch`, `stabilizer.yaw`). Data is formatted in an organized tabular view rounded to 2 decimal places and displayed every 2 seconds (`period_in_ms=2000`).

```bash
python LoggerCrazy.py
```

### 5. [bruteForce_takeoff.py](bruteForce_takeoff.py)
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
