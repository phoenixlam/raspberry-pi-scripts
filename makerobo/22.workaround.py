# Because lirc is not working
import subprocess

# Start the irw process
process = subprocess.Popen(['irw'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print("Listening for IR signals...")

try:
    while True:
        line = process.stdout.readline()
        if line:
            # Parse and print the received IR command
            parts = line.strip().split()
            if len(parts) >= 3:
                hex_code = parts[0]
                key_name = parts[2]
                print(f"Received: {key_name} (code: {hex_code})")
except KeyboardInterrupt:
    print("\nStopped listening.")
finally:
    process.terminate()