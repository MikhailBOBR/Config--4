import struct
from assembler import COMMANDS

def run_tests():
    tests = [
        {
            "command": "LOAD_CONST",
            "args": (6, 40, 803),
            "expected": b"\x86\x8E\x0C\x00\x00\x00"
        },
        {
            "command": "READ_MEM",
            "args": (10, 28, 934),
            "expected": b"\xCA\x99\x0E\x00\x00\x00"
        },
        {
            "command": "WRITE_MEM",
            "args": (12, 46, 31, 60),
            "expected": b"\xEC\xFA\x78\x00\x00\x00"
        },
        {
            "command": "MODULO",
            "args": (14, 92, 42, 57, 33),
            "expected": b"\xCE\x55\xF3\x10\x00\x00"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        command = test["command"]
        args = test["args"]
        expected = test["expected"]

        opcode = COMMANDS[command]
        
        if command == "LOAD_CONST":
            # A + B + C -> Specific byte encoding logic
            data = struct.pack(">BHH", opcode, args[0] << 8 | args[1], args[2])
        elif command == "READ_MEM":
            # A + B + C -> Specific byte encoding logic
            data = struct.pack(">BHH", opcode, args[0] << 8 | args[1], args[2])
        elif command == "WRITE_MEM":
            # A + B + C + D -> Specific byte encoding logic
            data = struct.pack(">BHHB", opcode, args[0] << 8 | args[1], args[2], args[3])
        elif command == "MODULO":
            # A + B + C + D + E -> Specific byte encoding logic
            data = struct.pack(">BHHBB", opcode, args[0] << 8 | args[1], args[2], args[3], args[4])
        else:
            raise ValueError(f"Unknown command: {command}")
        
        assert data == expected, (
            f"Test {i} failed for {command}. "
            f"Expected: {expected.hex()}, Got: {data.hex()}"
        )
        print(f"Test {i} passed for {command}. Output: {data.hex()}")

if __name__ == "__main__":
    print("Running tests for assembler...")
    try:
        run_tests()
        print("All tests passed!")
    except AssertionError as e:
        print(e)


