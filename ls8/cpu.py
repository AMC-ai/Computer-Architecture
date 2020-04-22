"""CPU functionality."""

import sys

# LDI: load "immediate", store a value in a register, or "set this register to this value".
LDI = 0b10000010
# PRN: a pseudo-instruction that prints the numeric value stored in a register.
PRN = 0b01000111
HLT = 0b00000001  # HLT: halt the CPU and exit the emulator.

# day 2
MUL = 0b10100010


class CPU:
    """Main CPU class."""
# day 1 Implement the CPU constructor , Add RAM functions ram_read() and ram_write()

    def __init__(self):
        # total CPU memory
        self.ram = [0] * 256
        # lambda CPU to print 8
        self.reg = [0] * 8  # r0 - r7
        # Program Counter, address of the currently executing instruction
        self.pc = 0

    # day 1 should accept the address to read and return the value stored there. The MAR contains the address that is being read or written to. MAR = address = location
    def ram_read(self, mar):
        return self.ram[mar]

    # day 1 should accept a value to write, and the address to write it to. The MDR contains the data that was read or the data to write. MDR = value
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # Later on, you might do further initialization here, e.g. setting the initial value of the stack pointer.

# day 2 Implement the load() function to load an .ls8 file given the filename passed in as an argument
    def load(self, file):
        """Load a program into memory."""

        try:
            with open(file) as f:

                address = 0
                for line in f:
                    # split the lines with comments
                    comments = line.strip().split('#')
                # take the first element of the line
                    strings = comments[0].strip()
                # skip empty lines
                    if strings == "":
                        continue
                # convert the line to an int
                    int_value = int(strings, 2)
                # save to memory
                    self.ram[address] = int_value
                # increment the address counter
                    address += 1
                # then close the file
                f.close()

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {file} not found")
            sys.exit(2)

# day 3 math and comparison

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

# day 1  Implement the core of run() # day 2 Implement a Multiply instruction (run mult.ls8)
    def run(self):
        # It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register. This can just be a local variable in run()
        while True:
            ir = self.ram[self.pc]
        # Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI). Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                # set the value of a register to an integer
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
                self.pc += 3
            elif ir == HLT:
                # exiting the system if HLT is encountered
                sys.exit(0)
            else:
                print(f"Something is not working, what did you forget?")
                sys.exit(1)
