import struct
import sys
import xml.etree.ElementTree as ET

# Используем стек для хранения данных
stack = []

def assemble_line(instruction):
    global stack
    opcode = instruction.get('opcode')
    
    if opcode == 'LOAD_CONST':
        A = int(instruction.get('A'))
        B = int(instruction.get('B'))
        # Добавление значения в стек
        stack.append(B)
        # Генерация бинарного представления для команды LOAD_CONST
        return struct.pack('=B3xi', 0xB8 | (A << 4), B)
    
    elif opcode == 'READ_MEM':
        A = int(instruction.get('A'))
        B = int(instruction.get('B'))
        # Генерация бинарного представления для команды READ_MEM
        return struct.pack('=B2xH', 0x34 | (A << 4), B)
    
    elif opcode == 'WRITE_MEM':
        if stack:
            # Извлечение значения из стека
            value = stack.pop()
        else:
            value = 0  # Использование значения по умолчанию, если стек пуст
        A = int(instruction.get('A'))
        B = int(instruction.get('B'))
        # Генерация бинарного представления для команды WRITE_MEM
        return struct.pack('=B2xH', 0xFD | (A << 4), B)
    
    elif opcode == 'ABS':
        if stack:
            # Если стек не пуст, выполняем операцию
            value = stack.pop()
            abs_value = abs(value)
            stack.append(abs_value)
            return struct.pack('=B', 0x00)
        else:
            # Ошибка при пустом стеке
            raise ValueError("ABS attempted with empty stack")
    
    else:
        raise ValueError(f"Unknown opcode: {opcode}")

def assemble(input_file, output_bin, log_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    binary = b''  # Переменная для хранения бинарных данных
    log = ET.Element('log')

    # Проход по всем инструкциям в программе
    for instruction in root.findall('instruction'):
        try:
            binary_code = assemble_line(instruction)
            binary += binary_code
        except ValueError as e:
            error_entry = ET.SubElement(log, 'error')
            error_entry.set('message', str(e))
            continue

        # Создание лог-записи
        log_entry = ET.SubElement(log, 'instruction')
        log_entry.set('raw', ' '.join(f'{byte:02X}' for byte in binary_code))
        
        # Безопасно извлекаем атрибуты, проверяя наличие
        opcode = instruction.attrib.get('opcode', '')
        A = instruction.attrib.get('A', '')
        B = instruction.attrib.get('B', '')
        
        # Лог для команды ABS с учетом значений
        if opcode == 'ABS' and stack:
            value = stack[-1]  # Текущее значение в стеке
            abs_value = abs(value)
            log_entry.set('mnemonic', f'{opcode} value={value} abs_value={abs_value}')
        elif B:
            log_entry.set('mnemonic', f'{opcode} A={A} B={B}')
        else:
            log_entry.set('mnemonic', f'{opcode} A={A}')

    # Запись бинарного файла
    with open(output_bin, 'wb') as bin_file:
        bin_file.write(binary)

    # Запись лога в формате XML
    tree = ET.ElementTree(log)
    tree.write(log_file)

if __name__ == '__main__':
    input_file = sys.argv[1]  # XML файл с исходной программой
    output_bin = sys.argv[2]  # Путь к бинарному файлу
    log_file = sys.argv[3]    # Путь к файлу лога в формате XML

    assemble(input_file, output_bin, log_file)