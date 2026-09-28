"""
Shared configuration for Crazyflie test scripts.

Provides flexible and intuitive Crazyflie URI configuration.
Default channel is 80 (radio://0/80/2M/E7E7E7E7E7).
"""

import os
import sys

# -----------------------------------------------------------------------------
# Default Radio Settings
# Modify these values directly if you want to change the defaults across scripts:
# -----------------------------------------------------------------------------
RADIO_INTERFACE = 0
RADIO_CHANNEL = 80          # Default channel: 80
RADIO_DATARATE = "2M"       # Datarate: '250K', '1M', or '2M'
CRAZYFLIE_ADDRESS = "E7E7E7E7E7"


def build_uri(channel=None, address=None, interface=None, datarate=None):
    """
    Construct a Crazyflie radio URI from individual components.
    """
    ifce = RADIO_INTERFACE if interface is None else interface
    ch = RADIO_CHANNEL if channel is None else channel
    rate = RADIO_DATARATE if datarate is None else datarate
    addr = CRAZYFLIE_ADDRESS if address is None else address
    return f"radio://{ifce}/{ch}/{rate}/{addr}"


DEFAULT_URI = build_uri()


def get_uri(custom_default=None):
    """
    Resolve the Crazyflie URI with the following priority:

    1. Command-line argument:
       - Full URI:       python script.py radio://0/90/2M/E7E7E7E7E7
       - Flag --uri:     python script.py --uri radio://0/90/2M/E7E7E7E7E7
       - Channel shortcut: python script.py 90 (or --channel 90 / -c 90)
    2. Environment variables:
       - CRAZYFLIE_URI or CFLIB_URI (e.g. export CRAZYFLIE_URI="radio://...")
       - CRAZYFLIE_CHANNEL or CFLIB_CHANNEL (e.g. export CRAZYFLIE_CHANNEL=90)
    3. Default URI:
       - Defaults to channel 80 (radio://0/80/2M/E7E7E7E7E7) or custom_default.
    """
    fallback_uri = custom_default or DEFAULT_URI

    # 1. Parse CLI arguments
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        # Case A: Full radio URI provided as positional arg
        if arg.startswith("radio://"):
            return arg

        # Case B: --uri / -u flag
        if arg in ("--uri", "-u") and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--uri="):
            return arg.split("=", 1)[1]

        # Case C: --channel / -c flag
        if arg in ("--channel", "-c") and i + 1 < len(args):
            return build_uri(channel=args[i + 1])
        if arg.startswith("--channel="):
            return build_uri(channel=arg.split("=", 1)[1])

        # Case D: Channel number passed directly as positional arg (e.g., `python script.py 90`)
        if arg.isdigit() and 0 <= int(arg) <= 125:
            return build_uri(channel=int(arg))

    # 2. Check Environment Variables
    for env_uri in ("CRAZYFLIE_URI", "CFLIB_URI", "URI"):
        val = os.environ.get(env_uri)
        if val:
            return val

    for env_ch in ("CRAZYFLIE_CHANNEL", "CFLIB_CHANNEL"):
        val = os.environ.get(env_ch)
        if val and val.isdigit():
            return build_uri(channel=int(val))

    # 3. Fallback to default
    return fallback_uri


# Export URI evaluated at import time for backwards compatibility
URI = get_uri()
