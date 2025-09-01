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
        docker_key_commands = [
            "sudo apt-get update",
            "sudo apt-get install ca-certificates curl",
            "sudo install -m 0755 -d /etc/apt/keyrings",
            "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
            "sudo chmod a+r /etc/apt/keyrings/docker.asc",
        ]
        print("Adding Docker's official GPGkey...")
        time.sleep(2)
        for commands in docker_key_commands:
            output, error = run_command(commands)
            if error:
                print("Error adding Docker's GPG key:", error, file=sys.stderr)
                sys.exit(1)
        print("Adding the repository to apt sources... ")
        repo_add_cmd = 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \\"${UBUNTU_CODENAME:-$VERSION_CODENAME}\\") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && sudo apt-get update'
        output, error = run_command(repo_add_cmd)
        if error:
            print("Error adding Docker repository:", error, file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
        print("Installing Docker Engine...")
        docker_install_cmd = "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
        output, error = run_command(docker_install_cmd)
        if error:
            print("Error installing Docker:", error, file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
        print("Docker installed successfully.")
        docker_version = "docker --version"
        time.sleep(2)
        output, error = run_command(docker_version)
        if error:
            print("Error checking Docker version:", error, file=sys.stderr)
            sys.exit(1)
        else:
            print("Docker version:", output.strip())
    else:
        print("Docker is installed:", output.strip())
        time.sleep(2)
        # proceed to install postgres
        print("Proceeding to create PostgreSQL database with Docker compose")
        time.sleep(2)
        print("creating the directory posgres in your home directory")
        time.sleep(2)
        home = run_command("echo $HOME")[0].strip()
        time.sleep(2)
        os.makedirs(f"{home}/postgres", exist_ok=True)
        posgres_user = input("Enter the Postgres username ")
        posgres_password = input("Enter the Postgres password ")
        posgres_db = input("Enter the Postgres database name ")
        mem_limit = input("Enter the memory limit for the Postgres container (e.g., 12g for 12GB) ")
        cpu_limit = input("Enter the CPU limit for the Postgres container (e.g., 3.5 for 3.5 CPUs) ")
        time.sleep(2)
        print("Creating the docker-compose.yml file...")
        time.sleep(2)
        docker_compose_content = f"""services:
  pg:
    image: postgres:16
    container_name: pg16
    restart: unless-stopped

    # Bind to all interfaces so LAN clients can reach it
    ports:
      - "0.0.0.0:5432:5432"

    environment:
      POSTGRES_USER: {posgres_user}            # <-- your DB username
      POSTGRES_PASSWORD: {posgres_password}  # <-- pick a strong password
      POSTGRES_DB: {posgres_db}              # optional; defaults to POSTGRES_USER
      POSTGRES_INITDB_ARGS: "--data-checksums"
      LAN_SUBNET: 192.168.1.0/24    # <-- your LAN CIDR for pg_hba; adjust as needed

    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d:ro

    mem_limit: {mem_limit}
    cpus: "{cpu_limit}"
    stop_grace_period: 120s

    command:
      - postgres
      - -c
      - listen_addresses=*
      - -c
      - shared_buffers=2GB
      - -c
      - effective_cache_size=10GB
      - -c
      - work_mem=128MB
      - -c
      - maintenance_work_mem=512MB
      - -c
      - wal_compression=on
      - -c
      - max_wal_size=4GB
      - -c
      - checkpoint_timeout=15min
      - -c
      - autovacuum_naptime=20s
      - -c
      - autovacuum_vacuum_scale_factor=0.05
      - -c
      - autovacuum_analyze_scale_factor=0.02
      - -c
      - jit=on

    healthcheck:
      # escape $ so it reaches the container env intact
      test: ["CMD-SHELL","pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 10s
      timeout: 5s
      retries: 5
      """
        with open(f"{home}/postgres/docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        time.sleep(2)
        print("docker-compose.yml file created successfully.")
        time.sleep(2)
        print("Starting the PostgreSQL container...")
        time.sleep(2)
        os.chdir(f"{home}/postgres")
        output, error = run_command("sudo docker compose up -d")
        if error:
            print("Error starting PostgreSQL container:", error, file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
        print("PostgreSQL container started successfully.")
        time.sleep(2)
        print("Checking the status of the PostgreSQL container...")
        time.sleep(2)
        output, error = run_command("sudo docker ps -f name=pg16")
        if error:
            print("Error checking PostgreSQL container status:", error, file=sys.stderr)
            sys.exit(1)
        else:
            print("PostgreSQL container status:\n", output.strip())
        time.sleep(2)
        print("PostgreSQL setup complete. You can connect to the database using the provided credentials.")
