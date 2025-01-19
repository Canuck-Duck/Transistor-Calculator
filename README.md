# Transistor-Calculator
This is where I will store all of the KiCad files for the Transistor Calculator and its modules.


V0.1 has many problems with the schematic and the PCB design. First, the schematic contains a mistake with both XOR segments. A wire is supposed to go from the right resistor under Q10 to 5V and from the right resistor under Q14 to 5V. Also, the design of the PCB is flawed because it is hard to hand-solder. While designing this PCB, I was too focused on saving space, which should not have been the case for the first version. The input and output holes were too small to fit any regular-size wire. All of these problems were fixed in V0.3.

V0.3 fixed all of the problems mentioned but still has some. For example, there are no mounting holes, so I had to drill holes in the PBC for the standoffs to stack them. Also, the 5V and GND will run through the standoffs for the following versions to facilitate disassembly. The carry pins will also be on the same side as the imput since thats where it has to connect.
