#!/usr/bin/env python3

import os, sys
import subprocess


def run_command(command):
    """Run a shell command and return the result."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr


if __name__ == "__main__":

    # Check if docker is installed
    docker_check_cmd = "docker --version"
    output, error = run_command(docker_check_cmd)
    if error:
        print("Docker is not installed or not found in PATH.", file=sys.stderr)

        # install docker for ubuntu
        print("Docker not found, installing Docker...")
        docker_install_cmd = """sudo apt-get update sudo apt-get install ca-certificates curl sudo install -m 0755 -d /etc/apt/keyrings sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc sudo chmod a+r /etc/apt/keyrings/docker.asc"""
        print("Adding Docker's official GPGkey...")
        run_command(docker_install_cmd)

    else:
        print("Docker is installed:", output.strip())
