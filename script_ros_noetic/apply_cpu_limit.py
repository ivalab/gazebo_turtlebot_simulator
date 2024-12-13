#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@file apply_cpu_limit.py
@author Yanwei Du (yanwei.du@gatech.edu)
@date 11-22-2024
@version 1.0
@license Copyright (c) 2024
@desc None
"""

import subprocess
import psutil
import time
import sys


def find_pid_by_name(name):
    """
    Find the PID of a process by its name.
    """
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if name in " ".join(proc.info["cmdline"]):
                return proc.info["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None


def find_process_by_name(process_name):
    """_summary_

    Args:
        process_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        output = subprocess.check_output(["pgrep", "-f", process_name]).decode("utf-8")
        pid_list = output.strip().split("\n")
        return [int(pid) for pid in pid_list]
    except subprocess.CalledProcessError:
        return None


def apply_cpulimit(pids, limit):
    """
    Apply cpulimit to a process by PID.

    Parameters:
        pid (int): Process ID to limit.
        limit (int): CPU usage limit in percentage.
    """
    try:
        for pid in pids:
            subprocess.run(["cpulimit", "--pid", str(pid), "--limit", str(limit), "--background"], check=True)
            print(f"Applied cpulimit: PID={pid}, Limit={limit}%")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply cpulimit: {e}")


def main(rosnode_name: str = ""):

    if rosnode_name == "":
        print("No rosnode name is specified!!! Quit!")
        return

    """_summary_"""
    # Find PID of the ROS node
    pid = None
    start_time = time.time()
    duration = 30.0  # seconds.
    while time.time() - start_time < duration:
        pid_list = find_process_by_name(rosnode_name)
        if pid_list is not None:
            for pid in pid_list:
                print(f"Found PID for {rosnode_name}: {pid}")
            break

        time.sleep(1)

    # Apply cpulimit
    if pid_list is None:
        print(f"Failed to find PID for ROS node: {rosnode_name}")
    else:
        apply_cpulimit(pid_list, 100 * 3)


if __name__ == "__main__":
    main(sys.argv[1])
