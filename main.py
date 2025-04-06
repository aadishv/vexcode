import asyncio
import os
import signal
import subprocess
import sys
import time
from multiprocessing import Process


def run_server(server_port, server_directory=None):
    """Run the HTTP server in a separate process"""
    # Change to the specified directory if provided
    if server_directory:
        os.chdir(server_directory)

    # Start Python's built-in HTTP server
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(server_port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Handle signals to ensure clean shutdown
    def signal_handler(sig, frame):
        server_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Keep the process running
    server_process.wait()


def run_browser_script():
    """Run the browser script in a separate process"""
    # Import the async function from browser.py
    from browser import open_page_headless

    # Create and run the event loop for the async function
    asyncio.run(open_page_headless())


def run_server_and_browser(server_port=8080, server_directory=None):
    """
    Run an HTTP server and the browser script concurrently in separate processes.

    Args:
        server_port (int): Port for the HTTP server (default: 8080)
        server_directory (str): Directory to serve (default: current directory)

    Returns:
        tuple: (server_process, browser_process) - both are Process objects
    """
    # Create processes with top-level functions instead of nested functions
    server_process = Process(target=run_server, args=(server_port, server_directory))
    browser_process = Process(target=run_browser_script)

    # Start server process
    server_process.start()
    print(f"HTTP server started on port {server_port}")

    # Wait a moment to ensure the server is running
    time.sleep(2)

    # Start browser process
    browser_process.start()
    print(f"Browser process started")

    return server_process, browser_process


# Example usage
if __name__ == "__main__":
    # Run server on port 8080 and execute the browser script
    server_proc, browser_proc = run_server_and_browser(
        server_port=8080, server_directory="."
    )

    try:
        # Wait for both processes to complete
        browser_proc.join()  # Wait for browser first since it will finish
        server_proc.join()  # Then terminate the server
    except KeyboardInterrupt:
        print("Stopping processes...")
        browser_proc.terminate()
        server_proc.terminate()
        browser_proc.join()
        server_proc.join()
    finally:
        # Make sure to terminate the server when browser is done
        if server_proc.is_alive():
            server_proc.terminate()
            server_proc.join()
            print("Server process terminated")
