"""
Script for logging IMU stabilizer variables from the Crazyflie.
Displays neatly formatted roll, pitch, and yaw data every 2 seconds.
"""

import logging

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from config import URI, get_uri

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def simple_log(scf, logconf):
    """
    Log and print stabilizer angles (roll, pitch, yaw) formatted to 2 decimal places.
    """
    print(f"\n{'Timestamp':<14} | {'Roll (deg)':<12} | {'Pitch (deg)':<12} | {'Yaw (deg)':<12}")
    print("-" * 58)

    with SyncLogger(scf, logconf) as logger:
        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]

            roll = data.get("stabilizer.roll", 0.0)
            pitch = data.get("stabilizer.pitch", 0.0)
            yaw = data.get("stabilizer.yaw", 0.0)

            print(f"{timestamp:>8} ms     | {roll:10.2f}   | {pitch:10.2f}   | {yaw:10.2f}")


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Configure logging at 2000 ms (every 2 seconds)
    lg_stab = LogConfig(name="Stabilizer", period_in_ms=2000)
    lg_stab.add_variable("stabilizer.roll", "float")
    lg_stab.add_variable("stabilizer.pitch", "float")
    lg_stab.add_variable("stabilizer.yaw", "float")

    uri = get_uri()
    print(f"Connecting to {uri}...")
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        simple_log(scf, lg_stab)
