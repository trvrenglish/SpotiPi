import random
import time
import sys

while True:
    noise_level = random.randint(50000, 150000)
    voltage = round(random.uniform(1, 2), 13)
    print(f"{noise_level} {voltage}")
    sys.stdout.flush()
