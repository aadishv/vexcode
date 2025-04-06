import subprocess
import time
import signal
import os
import sys
from multiprocessing import Process

def run_server_and_command(server_port=8000, command=None, server_directory=None):
    """
    Run an HTTP server and another command concurrently in separate processes.

    Args:
        server_port (int): Port for the HTTP server (default: 8000)
        command (str or list): Command to run in a separate process
        server_directory (str): Directory to serve (default: current directory)

    Returns:
        tuple: (server_process, command_process) - both are Process objects
    """
    def run_server():
        # Change to the specified directory if provided
        if server_directory:
            os.chdir(server_directory)

        # Start Python's built-in HTTP server
        server_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(server_port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Handle signals to ensure clean shutdown
        def signal_handler(sig, frame):
            server_process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Keep the process running
        server_process.wait()

    def run_command():
        if not command:
            return

        # Execute the provided command
        if isinstance(command, list):
            cmd_process = subprocess.Popen(command)
        else:
            cmd_process = subprocess.Popen(command, shell=True)

        cmd_process.wait()

    # Create processes
    server_process = Process(target=run_server)
    command_process = Process(target=run_command)

    # Start processes
    server_process.start()
    print(f"HTTP server started on port {server_port}")

    # Wait a moment to ensure the server is running
    time.sleep(1)

    command_process.start()
    print(f"Command process started")

    return server_process, command_process

# Example usage
if __name__ == "__main__":
    # Run server on port 8000 and execute a command
    server_proc, cmd_proc = run_server_and_command(
        server_port=8000,
        command=["python3", "browser.py"],
        server_directory="."
    )

    try:
        # Wait for both processes to complete
        server_proc.join()
        cmd_proc.join()
    except KeyboardInterrupt:
        print("Stopping processes...")
        server_proc.terminate()
        cmd_proc.terminate()
        server_proc.join()
        cmd_proc.join()
