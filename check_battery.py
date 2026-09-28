"""
Script for logging and checking the Crazyflie battery voltage and percentage.
"""

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from config import URI, get_uri


def calculate_battery_percentage(vbat):
    """
    Estimate 1-cell LiPo battery percentage from measured voltage.
    Typical 1S LiPo range: 3.3V (0%) to 4.2V (100%).
    """
    min_v = 3.3
    max_v = 4.2
    pct = (vbat - min_v) / (max_v - min_v) * 100.0
    return max(0.0, min(100.0, pct))


def get_battery_voltage(scf):
    """
    Log and print the battery voltage and calculated percentage.
    """
    # Create log configuration for pm.vbat (battery voltage)
    log_config = LogConfig(name="Battery", period_in_ms=100)
    log_config.add_variable("pm.vbat", "float")

    # Use SyncLogger to retrieve the log entry
    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]
            vbat = data["pm.vbat"]
            percentage = calculate_battery_percentage(vbat)

            print(f"Battery voltage: {vbat:.2f} V")
            print(f"Battery percentage: {percentage:.1f}%")

            # Check if battery is critically low
            if vbat < 3.4:
                print(f"Warning: Low battery ({percentage:.1f}%). Please recharge soon.")

            # Only need a single reading, then exit loop
            break


if __name__ == "__main__":
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    uri = get_uri()
    print(f"Connecting to {uri}...")
    try:
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
            get_battery_voltage(scf)
    except Exception as e:
        print(f"Error connecting or reading battery: {e}")
