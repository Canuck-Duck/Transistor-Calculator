from machine import Pin
import time

# Define pins
OE = Pin(17, Pin.OUT)  # Output Enable (active low)
WE = Pin(16, Pin.OUT)  # Write Enable (active low)

a0 = Pin(15, Pin.OUT)
a1 = Pin(14, Pin.OUT)
a2 = Pin(13, Pin.OUT)
a3 = Pin(12, Pin.OUT)
a4 = Pin(11, Pin.OUT)
a5 = Pin(10, Pin.OUT)
a6 = Pin(9, Pin.OUT)
a7 = Pin(8, Pin.OUT)

io0 = Pin(0, Pin.OUT)
io1 = Pin(1, Pin.OUT)
io2 = Pin(2, Pin.OUT)
io3 = Pin(3, Pin.OUT)
io4 = Pin(4, Pin.OUT)
io5 = Pin(5, Pin.OUT)
io6 = Pin(6, Pin.OUT)
io7 = Pin(7, Pin.OUT)

# Group pins
address_pins = [a0, a1, a2, a3, a4, a5, a6, a7]
io_pins = [io0, io1, io2, io3, io4, io5, io6, io7]

# Function to set address pins
def set_address(address):
    for i in range(8):  # 8 address pins
        address_pins[i].value((address >> i) & 1)

# Function to set data pins
def set_data(data):
    for i in range(8):  # 8 data pins
        io_pins[i].value((data >> i) & 1)
        #print(io_pins[i].value())

# Function to program (write) a byte to EEPROM
def write_byte(address, data):
    OE.high()
    time.sleep_us(100)
    set_address(address)
    set_data(data)
    
    time.sleep_us(10)
    # Write operation
    WE.off()  # Pull WE low to start write
    time.sleep_us(10)  # Delay to meet tWP (write pulse width, at least 100 ns)
    WE.on()   # Pull WE high to finish write
    
    # Hold time
    time.sleep_us(100)  # Delay for tAH (address hold time)

def read_byte(address):
    OE.low()
    time.sleep_us(10)
    # Set the address
    set_address(address)
  
    time.sleep(0.05)  # Small delay to stabilize the bus
    
    # Read data from IO pins
    data = 0
    for i in range(8):  # 8 data pins
        data |= (io_pins[i].value() << i)

    return data

def read_eeprom():
    OE.low()
    for pin in io_pins:
        pin.init(Pin.IN)
    print("Reading EEPROM...")
    for address in range(256):  # Assuming an 8-bit address space (256 bytes)
        data = read_byte(address)
        print(f"Address 0x{address:02X}: 0x{data:02X}")s
        time.sleep(0.05)
    OE.high()


# Example: Write a string to EEPROM
def program_eeprom(data):
    OE.low()
    print("Programming EEPROM...")
    for address, byte in enumerate(data):
        write_byte(address, byte)
        print(f"Programmed Address 0x{address:02X}: 0x{byte:02X}")
        time.sleep(0.05)  # Small delay between writes (depends on EEPROM specs)
def verify_and_write_eeprom(data):
    OE.low()
    print("Programming and verifying EEPROM...")
    for pin in io_pins:
        pin.init(Pin.IN)
    for address, byte in enumerate(data):
        current_data = read_byte(address)
        if current_data != byte:
            print(f"Mismatch at Address 0x{address:02X}: Expected 0x{byte:02X}, Found 0x{current_data:02X}")
            for pin in io_pins:
                pin.init(Pin.OUT)
            write_byte(address, byte)
            for pin in io_pins:
                pin.init(Pin.IN)
            print(f"Corrected Address 0x{address:02X}: 0x{byte:02X}")
        #else:
            #print(f"Address 0x{address:02X}: Data matches 0x{byte:02X}")
        time.sleep(0.05)  # Small delay between writes (depends on EEPROM specs)

# Initialize pins
WE.high()  # Keep WE high by default (disabled)
OE.low()

# data_1 is the data for the first EEPROM; it deals with the ones and the tens BDC
# data_2 is the data for the second EEPROM; it deals with the hundreds BDC
data_1 = [0X0, 0X1, 0X2, 0X3, 0X4, 0X5, 0X6, 0X7, 0X8, 0X9, 0X10, 0X11, 0X12, 0X13, 0X14, 0X15, 0X16, 0X17, 0X18, 0X19, 0X20, 0X21, 0X22, 0X23, 0X24, 0X25, 0X26, 0X27, 0X28, 0X29, 0X30, 0X31, 0X32, 0X33, 0X34, 0X35, 0X36, 0X37, 0X38, 0X39, 0X40, 0X41, 0X42, 0X43, 0X44, 0X45, 0X46, 0X47, 0X48, 0X49, 0X50, 0X51, 0X52, 0X53, 0X54, 0X55, 0X56, 0X57, 0X58, 0X59, 0X60, 0X61, 0X62, 0X63, 0X64, 0X65, 0X66, 0X67, 0X68, 0X69, 0X70, 0X71, 0X72, 0X73, 0X74, 0X75, 0X76, 0X77, 0X78, 0X79, 0X80, 0X81, 0X82, 0X83, 0X84, 0X85, 0X86, 0X87, 0X88, 0X89, 0X90, 0X91, 0X92, 0X93, 0X94, 0X95, 0X96, 0X97, 0X98, 0X99, 0X0, 0X1, 0X2, 0X3, 0X4, 0X5, 0X6, 0X7, 0X8, 0X9, 0X10, 0X11, 0X12, 0X13, 0X14, 0X15, 0X16, 0X17, 0X18, 0X19, 0X20, 0X21, 0X22, 0X23, 0X24, 0X25, 0X26, 0X27, 0X28, 0X29, 0X30, 0X31, 0X32, 0X33, 0X34, 0X35, 0X36, 0X37, 0X38, 0X39, 0X40, 0X41, 0X42, 0X43, 0X44, 0X45, 0X46, 0X47, 0X48, 0X49, 0X50, 0X51, 0X52, 0X53, 0X54, 0X55, 0X56, 0X57, 0X58, 0X59, 0X60, 0X61, 0X62, 0X63, 0X64, 0X65, 0X66, 0X67, 0X68, 0X69, 0X70, 0X71, 0X72, 0X73, 0X74, 0X75, 0X76, 0X77, 0X78, 0X79, 0X80, 0X81, 0X82, 0X83, 0X84, 0X85, 0X86, 0X87, 0X88, 0X89, 0X90, 0X91, 0X92, 0X93, 0X94, 0X95, 0X96, 0X97, 0X98, 0X99, 0X0, 0X1, 0X2, 0X3, 0X4, 0X5, 0X6, 0X7, 0X8, 0X9, 0X10, 0X11, 0X12, 0X13, 0X14, 0X15, 0X16, 0X17, 0X18, 0X19, 0X20, 0X21, 0X22, 0X23, 0X24, 0X25, 0X26, 0X27, 0X28, 0X29, 0X30, 0X31, 0X32, 0X33, 0X34, 0X35, 0X36, 0X37, 0X38, 0X39, 0X40, 0X41, 0X42, 0X43, 0X44, 0X45, 0X46, 0X47, 0X48, 0X49, 0X50, 0X51, 0X52, 0X53, 0X54, 0X55]
data_2 = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2]





#program_eeprom(data_2) # Programs the EEPROM

#verify_and_write_eeprom(data_2) # Checks if the EEPROM is correctly written

#read_eeprom() # Reads EEPROM