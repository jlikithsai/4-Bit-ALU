arr = []
with open("ADDER_delays.txt", "r") as f:
    for lin in f.readlines():
        arr.append(lin + "for ADDER Circiut")

with open("SUBTRACTOR_delays.txt", "r") as f:
    for lin in f.readlines():
        arr.append(lin + "for SUBTRACTOR Circuit")

with open("Comparator_delays.txt", "r") as f:
    for lin in f.readlines():
        arr.append(lin+"for Comparator Circuit")

with open("AND_delays.txt", "r") as f:
    for lin in f.readlines():
        arr.append(lin + "for AND Circuit")
arr = []

def append_delays(filename, circuit_type):
    with open(filename, "r") as f:
        for lin in f.readlines():
            arr.append(lin.strip() + f" for {circuit_type} Circuit")

append_delays("ADDER_delays.txt", "ADDER")
append_delays("SUBTRACTOR_delays.txt", "SUBTRACTOR")
append_delays("Comparator_delays.txt", "Comparator")
append_delays("AND_delays.txt", "AND")

def extract_delay(line):
    parts = line.split()
    for part in parts:
        try:
            return float(part)
        except ValueError:
            continue
    return float('-inf')  # In case no float is found, return negative infinity

max_delay_line = max(arr, key=lambda x: extract_delay(x))
max_delay = extract_delay(max_delay_line)

# Assuming the delay is given in nanoseconds (ns)
max_delay_seconds = max_delay  # Convert nanoseconds to seconds
speed_hz = 1 / max_delay_seconds  # Frequency in Hz
speed_mhz = speed_hz * 1e-6  # Convert Hz to MHz

print(f"The line with the maximum delay is: {max_delay_line}")
print(f"The maximum delay is: {max_delay} ns")
print(f"The speed of the IC is: {speed_mhz} MHz")
