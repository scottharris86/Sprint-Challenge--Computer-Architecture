"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.flag = 0

    def load(self, file):
        """Load a program into memory."""
        address = 0
        with open(file) as f:
            for line in f:
                comment_split = line.split("#")
                n = comment_split[0].strip()

                if n == '':
                    continue
            
                x = int(n, 2)

                self.ram[address] = x
                address += 1
        

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
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            # flag = 00000LGE
            # flag = 0b00000000
            val1 = self.registers[reg_a]
            val2 = self.registers[reg_b]
            if val1 == val2:
                self.flag = 0b00000001
            elif val1 < val2:
                self.flag = 0b00000100
            else:
                self.flag = 0b00000010

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
        SP = 7
        self.registers[SP] = 244

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        running = True
        pc_count = 0
        pc = self.pc
        pc = 0
        fl = self.flag
        fl = 0

        while running:
            cmd = self.ram[pc]
            pc_count = ((cmd >> 6) & 0b11) + 1

            if cmd == LDI:
                the_register = self.ram[pc + 1]
                value = self.ram[pc +  2]
                self.registers[the_register] = value
                pc_count = 3

            elif cmd == HLT:
                running = False
                pc_count = 1

            elif cmd == PRN:
                the_register = self.ram[pc + 1]
                value = self.registers[the_register]
                print(value)
                pc_count = 2

            elif cmd == MUL:
                the_register1 = self.ram[pc + 1]
                the_register2 = self.ram[pc + 2]
                value1 = self.registers[the_register1]
                value2 = self.registers[the_register2]
                self.alu("MUL", the_register1, the_register2)
                pc_count = 3


             # PUSH
            elif cmd == PUSH:
                # setup
                reg_index = self.ram[pc + 1]
                val = self.registers[reg_index]

                # decrememt Stack Pointer
                self.registers[SP] -= 1

                # insert val on to the stack
                self.ram[self.registers[SP]] = val

                pc_count = 2

            # TODO: POP
            elif cmd == POP:
                # setup
                reg_index = self.ram[pc + 1]
                val = self.ram[self.registers[SP]]

                # take value from stack and put it in reg
                self.registers[reg_index] = val

                # increment Stack Pointer
                self.registers[SP] += 1

                pc_count = 2


            # CALL
            elif cmd == CALL:
                # push the return address on to the stack
                self.registers[SP] -= 1
                self.ram[self.registers[SP]] = pc + 2

                # Set the PC to the subroutines address
                reg = self.ram[pc + 1]
                pc = self.registers[reg]

                pc_count = 0

            # RET
            elif cmd == RET:
                # POP return address from stack to store in pc
                pc = self.ram[self.registers[SP]]
                self.registers[SP] += 1

                pc_count = 0

            elif cmd == CMP:
                the_register1 = self.ram[pc + 1]
                the_register2 = self.ram[pc + 2]
                value1 = self.registers[the_register1]
                value2 = self.registers[the_register2]
                self.alu("CMP", the_register1, the_register2)
                # print(self.flag)
                pc_count = 3

            # elif cmd == JMP:
            #     self.jump()

            elif cmd == JEQ:
                if self.flag == 1:
                    print("We JEQ'ed")
                    jump_to = self.ram[pc + 1]
                    self.jump(jump_to)

                    # pc_count = 0

            elif cmd == JNE:
                if self.flag != 1:
                    print("We JNE'ed")
                    jump_to = self.registers[self.ram[pc + 1]]
                    print(f"jump_to is {jump_to}")
                    self.jump(jump_to)

                    pc_count = 0

            pc += pc_count
            # print(f"PC is now: {pc}")


    def jump(self, somewhere):
        self.pc = somewhere
