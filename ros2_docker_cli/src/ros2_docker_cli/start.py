#!/usr/bin/env python3

import os
import subprocess
import argparse
import platform

def detect_distro():
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            data = f.read()
        if "ID=nixos" in data:
            return "nixos"
        elif "ID=ubuntu" in data:
            return "ubuntu"
    return "unknown"

def run_xhost(distro):
    if distro == "nixos":
        print("Detected NixOS, running xhost via nix-shell...")
        subprocess.run([
            "nix-shell", "-p", "xorg.xhost",
            "--run", "xhost +local:"
        ])
    elif distro == "ubuntu":
        print("Detected Ubuntu, running xhost directly...")
        subprocess.run(["xhost", "+local:"])
    else:
        raise RuntimeError("Unsupported or unknown Linux distribution.")

def build_docker_command(volumes, workspace):
    wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
    xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")

    base_command = [
        "docker", "run", "-it", "--rm",
        "--env=DISPLAY",
        "--env=QT_QPA_PLATFORM=xcb",
        "--env=QT_X11_NO_MITSHM=1",
        f"--env=WAYLAND_DISPLAY={wayland_display}",
        f"--env=XDG_RUNTIME_DIR={xdg_runtime_dir}",
        f"--volume=/tmp/.X11-unix:/tmp/.X11-unix:rw",
        f"--volume={xdg_runtime_dir}/{wayland_display}:/tmp/{wayland_display}:rw",
        "--ipc=host",
        "--name=ros",
        f"-w={workspace}",
    ]

    # Add user-specified volumes
    for vol in volumes:
        abs_path = os.path.abspath(vol)
        base_command.append(f"--volume={abs_path}:{abs_path}:rw")

    # Image and command
    base_command += ["jros:foxy", "/bin/bash"]

    return base_command

def main():
    parser = argparse.ArgumentParser(description="Run GUI-enabled Docker container.")
    parser.add_argument(
        "-v", "--volume", action="append", default=[],
        help="Additional volume to mount. Format: host_path (same path will be used in container)"
    )
    parser.add_argument(
        "-w", "--workspace", default="/home", type=str,
        help="Workspace to enter with"
    )
    args = parser.parse_args()

    distro = detect_distro()
    run_xhost(distro)

    docker_cmd = build_docker_command(args.volume, args.workspace)
    print("Running Docker with command:\n", " ".join(docker_cmd))
    subprocess.run(docker_cmd)

if __name__ == "__main__":
    main()

