import subprocess
import os
import getpass
import sys
import argparse

def build_docker_image(docker_path):
    """
    Builds a Docker image with the current user's UID, GID, and username
    as build arguments.

    Args:
        docker_path (str): The build context path for Docker.
    """
    try:
        # Get user info using Python's standard libraries
        uid = os.getuid()
        gid = os.getgid()
        uname = getpass.getuser()

        # Construct the command as a list of arguments
        command = [
            "docker", "build",
            "--build-arg", f"UID={uid}",
            "--build-arg", f"GID={gid}",
            "--build-arg", f"UNAME={uname}",
            "-t", "jros:foxy",
            docker_path  # Use the argument for the path
        ]
        
        print("---" * 10)
        print(f"🐍 Running Docker build command:")
        # Reconstruct the command string for clean printing
        print(f"   {' '.join(command)}")
        print("---" * 10)

        # Run the command, streaming the output to the console
        # check=True will raise an exception if the command fails
        process = subprocess.run(
            command,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        print("\n✅ Docker build completed successfully.")

    except FileNotFoundError:
        print("\n❌ Error: 'docker' command not found.")
        print("   Please ensure Docker is installed and that the 'docker' executable is in your system's PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Docker build failed with exit code {e.returncode}.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """Parses command-line arguments and initiates the Docker build."""
    parser = argparse.ArgumentParser(
        description="Builds a Docker image with user-specific build arguments."
    )
    parser.add_argument(
        "docker_path",
        nargs="?",
        default=".",
        help="Path to the Docker context (directory containing the Dockerfile). Defaults to the current directory."
    )
    args = parser.parse_args()
    
    build_docker_image(args.docker_path)

if __name__ == "__main__":
    main()
