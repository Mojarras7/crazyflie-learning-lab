"""
Utility script to scan for Crazyflie drones across radio interfaces.
Discovers active Crazyflies and prints their connection URIs.
"""

import sys
import cflib.crtp


def scan():
    print("=" * 60)
    print(" Crazyflie Radio Scanner")
    print("=" * 60)
    print("Initializing low-level Crazyflie drivers...")
    cflib.crtp.init_drivers(enable_debug_driver=False)

    print("Scanning radio channels for active Crazyflies...")
    available = cflib.crtp.scan_interfaces()

    if not available:
        print("\n[!] No Crazyflies found.")
        print("\nTroubleshooting tips:")
        print("  1. Make sure your Crazyflie is turned ON (LEDs blinking).")
        print("  2. Ensure the Crazyradio PA dongle is firmly connected to USB.")
        print("  3. Verify Linux USB permissions (plugdev group & udev rules).")
        print("  4. If the drone is connected via USB, check 'cfclient'.")
        return

    print(f"\n[+] Found {len(available)} Crazyflie(s):\n")
    for i, (uri, info) in enumerate(available, start=1):
        print(f"  {i}. URI: {uri}")
        if info:
            print(f"     Details: {info}")

    print("\n" + "-" * 60)
    first_uri = available[0][0]
    print("How to use this drone:")
    print(f"  - Direct run:     python HelloCrazy.py {first_uri}")
    print(f"  - Run by channel: python HelloCrazy.py {first_uri.split('/')[3]}")
    print("-" * 60)


if __name__ == "__main__":
    scan()
