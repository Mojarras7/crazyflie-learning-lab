"""
Simple script for connecting to the Crazyflie, verifying connection,
and sequentially testing each motor individually to provide physical feedback.
"""

import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from config import URI, get_uri


def test_motors(scf):
    """
    Test each motor individually using the motorPowerSet parameter group.
    """
    cf = scf.cf
    print("Connected to Crazyflie successfully.")
    print("Testing motors individually...")

    # Low PWM power value (~23% duty cycle) to gently spin the motor safely on the ground
    motor_power = 15000

    motors = [
        ("m1", "Motor 1 (M1 - Front Right)"),
        ("m2", "Motor 2 (M2 - Back Right)"),
        ("m3", "Motor 3 (M3 - Back Left)"),
        ("m4", "Motor 4 (M4 - Front Left)"),
    ]

    try:
        # Enable manual motor power control override
        cf.param.set_value("motorPowerSet.enable", "1")

        for motor_param, motor_label in motors:
            print(f"Spinning {motor_label}...")
            cf.param.set_value(f"motorPowerSet.{motor_param}", str(motor_power))
            time.sleep(1)
            cf.param.set_value(f"motorPowerSet.{motor_param}", "0")
            time.sleep(1)

        print("Motor test completed.")

    finally:
        # Ensure all motors are stopped and manual override is disabled
        for motor_param, _ in motors:
            cf.param.set_value(f"motorPowerSet.{motor_param}", "0")
        cf.param.set_value("motorPowerSet.enable", "0")

    time.sleep(0.5)
    print("Disconnecting from Crazyflie.")


if __name__ == "__main__":
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    uri = get_uri()
    print(f"Connecting to {uri}...")
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        test_motors(scf)
