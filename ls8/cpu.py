"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.MDR = None
        self.MAR = None

    # should accept the address to read and return the value stored there.
    def ram_read(self, address):
        self.MDR = self.ram[address]
        return self.MDR

    # should accept a value to write, and the address to write it to.
    def ram_write(self,value, address):
        self.MAR = address
        self.ram[self.MAR] = value



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:

            with open(sys.argv[1]) as f:
                for line in f:
                    string_val = line.split("#")[0].strip()
                    if string_val == '':
                        continue
                    v = int(string_val, 2)
                    self.ram[address] = v
                    address += 1
        except:
            print("Need a valid second file arge")
            sys.exit()




    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # register PC, and store that result in IR
        IR = self.pc
        SP = 7
        self.register[SP] = 0xf4

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        halted = False

        while not halted:
            instruction = self.ram_read(IR)
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)

            if instruction == HLT:
                halted = True

            # 3 bit operation
            elif instruction == LDI:
                # where and what
                self.register[operand_a] = operand_b
                IR += 3

            # 3 bit operationn
            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                IR += 3

            #2 bit operation
            elif instruction == PUSH:
                # Decrement the SP
                self.register[SP] -= 1

                # Get register number
                reg_num = self.ram[IR + 1]

                # Get value out of the register
                val = self.register[reg_num]

                # Store value in memory at SP
                top_of_stack_addr = self.register[SP]
                self.ram[top_of_stack_addr] = val
                IR += 2

            # 2 bit operatoin
            elif instruction == POP:
                # Copy the value from the address pointed to by SP to the given register.
                # Get register number
                reg_num = self.ram[IR+1]
                # Copy the value out of register
                val = self.ram[self.register[SP]]
                # overwrite to given register
                self.register[reg_num] = val
                #Increment SP
                self.register[SP] += 1
                IR += 2

            # 2 bin operation
            elif instruction == PRN:
                data = self.register[operand_a]
                print(data)
                IR += 2

            else:
                print(f'unknown instruction {instruction} at address {self.pc}')
                sys.exit(1)
