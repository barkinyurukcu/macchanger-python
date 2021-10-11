#!/usr/bin/env/ python
# Requires ifconfig
# Next Version: using "ip" command instead of "ifconfig"


import subprocess
import argparse
import re


def get_args():
    parser = argparse.ArgumentParser(prog="macchanger", description="A simple tool for changing MAC address.")
    parser.add_argument("-i", "--interface", dest="interface", help="Usage: -i interface")
    parser.add_argument("-m", "--mac", dest="new_mac", help="Usage: -m aa:bb:cc:dd:ee:ff")
    args = parser.parse_args()
    if not args.interface:
        parser.error("Please write a valid interface value.")
    elif not args.new_mac:
        parser.error("Please write a valid MAC address.")
    return args


def mac_change(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def find_mac(interface):
    mac_exist = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", subprocess.check_output(["ifconfig", interface]))
    if mac_exist:
        return mac_exist.group(0)
    else:
        return False


try:
    pre_mac = str(find_mac(get_args().interface))
    if find_mac(get_args().interface):
        if pre_mac != get_args().new_mac:
            print("Changing the MAC from " + pre_mac + " to " + get_args().new_mac + " for " + get_args().interface)
            mac_change(get_args().interface, get_args().new_mac)
            post_mac = str(find_mac(get_args().interface))
        else:
            print("MAC address value is the same. No action was taken.")
    else:
        print("No MAC address was found.")
except subprocess.CalledProcessError:
    print("Interface not found.")
