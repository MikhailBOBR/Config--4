import struct
import xml.etree.ElementTree as ET
from assembler import assemble_line, stack

def test_load_const():
    instruction = ET.Element('instruction', opcode='LOAD_CONST', A='8', B='539')
    binary_code = assemble_line(instruction)
    expected_binary = struct.pack('=B3xi', 0xB8 | (8 << 4), 539)
    assert binary_code == expected_binary, f"Expected {expected_binary}, but got {binary_code}"
    print("Test LOAD_CONST passed")

def test_read_mem():
    instruction = ET.Element('instruction', opcode='READ_MEM', A='4', B='163')
    binary_code = assemble_line(instruction)
    expected_binary = struct.pack('=B2xH', 0x34 | (4 << 4), 163)
    assert binary_code == expected_binary, f"Expected {expected_binary}, but got {binary_code}"
    print("Test READ_MEM passed")

def test_write_mem():
    stack.append(671)
    instruction = ET.Element('instruction', opcode='WRITE_MEM', A='13', B='671')
    binary_code = assemble_line(instruction)
    expected_binary = struct.pack('=B2xH', 0xFD | (13 << 4), 671)
    assert binary_code == expected_binary, f"Expected {expected_binary}, but got {binary_code}"
    print("Test WRITE_MEM passed")

def test_abs():
    stack.append(-539)
    instruction = ET.Element('instruction', opcode='ABS')
    binary_code = assemble_line(instruction)
    expected_binary = struct.pack('=B', 0x00)
    assert binary_code == expected_binary, f"Expected {expected_binary}, but got {binary_code}"
    assert stack[-1] == 539, f"Expected stack top to be 539, but got {stack[-1]}"
    print("Test ABS passed")

if __name__ == '__main__':
    test_load_const()
    test_read_mem()
    test_write_mem()
    test_abs()
    print("\nAll tests passed successfully.")
