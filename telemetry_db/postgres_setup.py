#!/usr/bin/env python3

import os, sys, time
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
        time.sleep(2)

        # install docker for ubuntu
        print("Docker not found, installing Docker...")
        time.sleep(2)
        docker_keys = """sudo apt-get update sudo apt-get install ca-certificates curl sudo install -m 0755 -d /etc/apt/keyrings sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc sudo chmod a+r /etc/apt/keyrings/docker.asc"""
        print("Adding Docker's official GPGkey...")
        time.sleep(2)
        run_command(docker_keys)
        print("Adding the repository to apt sources... ")
        repo_add_cmd = """echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update"""
        run_command(repo_add_cmd)
        time.sleep(2)
        print("Installing Docker Engine...")
        docker_install_cmd = '''sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin'''
        run_command(docker_install_cmd)
        time.sleep(2)
        print("Docker installed successfully.")
    else:
        print("Docker is installed:", output.strip())
