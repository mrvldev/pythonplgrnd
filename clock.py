import time

try:

    while True:
        current = time.strftime("%I:%M:%S %p")
        print(f" {current}", end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClock stopped.\n")