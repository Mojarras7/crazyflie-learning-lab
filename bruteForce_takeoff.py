"""
Test script for open-loop thrust takeoff without external position estimation.

IMPORTANT NOTES & WARNINGS:
1. Position Estimation (OptiTrack):
   The Crazyflie requires a position estimation system (such as an OptiTrack motion
   capture system or Flow deck) for stable, controlled autonomous flight.
   This script operates completely in open-loop mode; without OptiTrack feedback,
   the drone will drift unpredictably.

2. Throttle Safety Limits:
   NEVER set the throttle/thrust to maximum (65535). Max throttle is extremely
   aggressive and will cause the drone to shoot up violently into obstacles.
   Always keep thrust within a conservative range between 30000 and 45000
   (hover threshold is typically around 38000 - 42000).

3. Firmware Requirement:
   The Crazyflie must be flashed with our custom firmware. Newer official firmware
   versions do not accept these raw open-loop thrust setpoint commands due to
   stricter arming and commander checks.
"""

import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from config import URI, get_uri

# Conservative hover thrust range: 30000 - 45000.
# WARNING: NEVER set to maximum (65535)!
THRUST_HOVER = 38000


def brute_force_takeoff(scf):
    """
    Send raw thrust setpoints to perform an open-loop takeoff and landing.
    """
    commander = scf.cf.commander

    print("Starting open-loop thrust takeoff...")
    print(f"Applying conservative thrust: {THRUST_HOVER} (safe range: 30000 - 45000)")

    # Send setpoints for 3 seconds (30 iterations * 0.1s)
    # Roll: 0 deg, Pitch: 0 deg, Yaw rate: 0 deg/s
    for _ in range(30):
        commander.send_setpoint(0.0, 0.0, 0.0, THRUST_HOVER)
        time.sleep(0.1)

    # Land (zero thrust)
    print("Landing: Setting thrust to 0...")
    commander.send_setpoint(0.0, 0.0, 0.0, 0)
    time.sleep(0.5)


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    uri = get_uri()
    print(f"Connecting to {uri}...")
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        brute_force_takeoff(scf)
