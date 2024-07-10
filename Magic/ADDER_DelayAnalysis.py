import os
import subprocess

command = "ngspice ADDER_destination.cir"

# Clear the file
with open("ADDER_delays.txt", 'w') as fp3:
    pass

# Function to replace text in the circuit data
def replace_text(data, replacements):
    for search, replace in replacements.items():
        data = data.replace(search, replace)
    return data

# Delay Analysis for Sum bits
for i in range(0, 8):
    with open("ALU.cir", "r") as fp1:
        data = fp1.read()

    # Initial replacements
    replacements = {
        "* Select line S0": "VS0 S0 Gnd DC 0",
        "* Select line S1": "VS1 S1 Gnd DC 0",
        "* Operation": '''
run
quit
''',
    }

    if i < 4:
        s1 = 'A' + str(i)
        replacements.update({
            "* Supply for A3": "VA3 A3 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for A2": "VA2 A2 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for A1": "VA1 A1 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for A0": "VA0 A0 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for B3": "VB3 B3 Gnd DC 0",
            "* Supply for B2": "VB2 B2 Gnd DC 0",
            "* Supply for B1": "VB1 B1 Gnd DC 0",
            "* Supply for B0": "VB0 B0 Gnd DC 0",
        })
    else:
        s1 = 'B' + str(i - 4)
        replacements.update({
            "* Supply for A3": "VA3 A3 Gnd 0",
            "* Supply for A2": "VA2 A2 Gnd 0",
            "* Supply for A1": "VA1 A1 Gnd 0",
            "* Supply for A0": "VA0 A0 Gnd 0",
            "* Supply for B3": "VB3 B3 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for B2": "VB2 B2 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for B1": "VB1 B1 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
            "* Supply for B0": "VB0 B0 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)",
        })

    data = replace_text(data, replacements)

    for j in range(0, 4):
        s2 = 'OUT_AS' + str(j)

        with open("ADDER_destination.cir", "w") as fp2:
            mode1 = 'RISE'
            mode2 = 'RISE'
            mode3 = 'FALL'
            mode4 = 'FALL'

            search_text = "* Text to be Replaced"
            replace_with = f'''
.measure tran trise 
+ TRIG v({s1}) VAL = 'SUPPLY/2' {mode1} =1
+ TARG v({s2}) VAL = 'SUPPLY/2' {mode2} =1 

.measure tran tfall 
+ TRIG v({s1}) VAL = 'SUPPLY/2' {mode3} =1 
+ TARG v({s2}) VAL = 'SUPPLY/2' {mode4}=1

.measure tran tpd param = '(trise + tfall)/2' goal = 0
'''
            data = data.replace(search_text, replace_with)

            fp2.write(data)

        simulation = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if simulation.returncode == 0:
            output = simulation.stdout
        else:
            output = f"Command execution failed at i={i}, j={j}"

        output_lines = output.split('\n')
        if len(output_lines) >= 4:
            output = output_lines[-4]

        additional_text = f" for Input = {s1} and Output = {s2}\n"

        with open("ADDER_delays.txt", "a") as fp3:
            fp3.write(output + additional_text)

# Delay Analysis for Carry Bit:
for i in range(0, 8):
    with open("ALU.cir", "r") as fp1:
        data = fp1.read()

    # Initial replacements
    replacements = {
        "* Select line S0": "VS0 S0 Gnd DC 0",
        "* Select line S1": "VS1 S1 Gnd DC 0",
        "* Operation": '''
run
quit
''',
    }

    if i < 4:
        s1 = 'A' + str(i)
        replacements.update({
            "* Supply for A3": "VA3 A3 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 3 else "VA3 A3 Gnd DC 0",
            "* Supply for A2": "VA2 A2 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 2 else "VA2 A2 Gnd DC 0",
            "* Supply for A1": "VA1 A1 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 1 else "VA1 A1 Gnd DC 0",
            "* Supply for A0": "VA0 A0 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 0 else "VA0 A0 Gnd DC 0",
            "* Supply for B3": "VB3 B3 Gnd DC 1",
            "* Supply for B2": "VB2 B2 Gnd DC 1",
            "* Supply for B1": "VB1 B1 Gnd DC 1",
            "* Supply for B0": "VB0 B0 Gnd DC 1",
        })
    else:
        s1 = 'B' + str(i - 4)
        replacements.update({
            "* Supply for A3": "VA3 A3 Gnd DC 1",
            "* Supply for A2": "VA2 A2 Gnd DC 1",
            "* Supply for A1": "VA1 A1 Gnd DC 1",
            "* Supply for A0": "VA0 A0 Gnd DC 1",
            "* Supply for B3": "VB3 B3 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 7 else "VB3 B3 Gnd DC 0",
            "* Supply for B2": "VB2 B2 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 6 else "VB2 B2 Gnd DC 0",
            "* Supply for B1": "VB1 B1 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 5 else "VB1 B1 Gnd DC 0",
            "* Supply for B0": "VB0 B0 Gnd PULSE('SUPPLY' 0 0ns 100ps 100ps 10ns 20ns)" if i == 4 else "VB0 B0 Gnd DC 0",
        })

    data = replace_text(data, replacements)
    s2 = 'C'

    with open("ADDER_destination.cir", "w") as fp2:
        mode1 = 'RISE'
        mode2 = 'RISE'
        mode3 = 'FALL'
        mode4 = 'FALL'

        search_text = "* Text to be Replaced"
        replace_with = f'''
.measure tran trise 
+ TRIG v({s1}) VAL = 'SUPPLY/2' {mode1} =1
+ TARG v({s2}) VAL = 'SUPPLY/2' {mode2} =1 

.measure tran tfall 
+ TRIG v({s1}) VAL = 'SUPPLY/2' {mode3} =1 
+ TARG v({s2}) VAL = 'SUPPLY/2' {mode4}=1

.measure tran tpd param = '(trise + tfall)/2' goal = 0
'''
        data = data.replace(search_text, replace_with)

        fp2.write(data)

    simulation = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if simulation.returncode == 0:
        output = simulation.stdout
    else:
        output = f"Command execution failed at i={i}"

    output_lines = output.split('\n')
    if len(output_lines) >= 4:
        output = output_lines[-4]

    additional_text = f" for Input = {s1} and Output = {s2}\n"

    with open("ADDER_delays.txt", "a") as fp3:
        fp3.write(output + additional_text)
