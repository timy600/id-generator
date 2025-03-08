import sys
import signal
from identity.generation import IDGenerator

filename = "tests/counters/token_restarting_counter.txt"

# Create IDGenerator instance
id_gen = IDGenerator(filename=filename)
while True:
    for _ in id_gen.generate_bulk(10):
        sys.stdout.write(f"{_}\n")

# # Handle graceful shutdown
# def handle_exit(signum, frame):
#     """Ensures the ID generator saves progress before exiting."""
#     print("\nShutting down gracefully...")
#     id_gen.close()  # Save counter before exiting
#     sys.exit(0)

# # Attach signal handlers for clean exit on Ctrl+C or termination
# signal.signal(signal.SIGINT, handle_exit)  # Ctrl+C
# signal.signal(signal.SIGTERM, handle_exit)  # Termination

# try:
#     while True:
#         for _ in id_gen.generate_bulk(10):
#             sys.stdout.write(f"{_}\n")
#             sys.stdout.flush()  # Ensure immediate output
# except Exception as e:
#     print(f"\nError encountered: {e}")
#     handle_exit(None, None)  # Ensure cleanup before exiting
