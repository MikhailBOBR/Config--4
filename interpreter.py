import struct
import sys
import xml.etree.ElementTree as ET

def execute_program(binary_file, memory_range):
    memory = [0] * 1024  # Допустим, у нас 1024 ячейки памяти
    stack = []
    result = ET.Element('result')

    with open(binary_file, 'rb') as f:
        while True:
            byte = f.read(1)  # Читаем 1 байт (код операции)
            if not byte:
                break  # Если данных нет, выходим из цикла
            opcode = ord(byte)

            # Обрабатываем команду LOAD_CONST (5 байтов)
            if opcode == 0xB8:  # LOAD_CONST
                data = f.read(4)  # Читаем 4 байта для B
                if len(data) < 4:
                    break  # Если данных недостаточно, выходим из цикла
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=I', data)[0]  # Извлекаем B
                stack.append(B)
                ET.SubElement(result, 'operation', {'opcode': 'LOAD_CONST', 'A': str(A), 'B': str(B)})

            # Обрабатываем команду READ_MEM (3 байта)
            elif opcode == 0x34:  # READ_MEM
                data = f.read(2)  # Читаем 2 байта для B
                if len(data) < 2:
                    break
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=H', data)[0]  # Извлекаем B
                value = memory[B]
                stack.append(value)
                ET.SubElement(result, 'operation', {'opcode': 'READ_MEM', 'A': str(A), 'B': str(B), 'value': str(value)})

            # Обрабатываем команду WRITE_MEM (3 байта)
            elif opcode == 0xFD:  # WRITE_MEM
                data = f.read(2)  # Читаем 2 байта для B
                if len(data) < 2:
                    break
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=H', data)[0]  # Извлекаем B
                
                # Проверка перед pop
                if stack:
                    value = stack.pop()
                    memory[B] = value
                    ET.SubElement(result, 'operation', {'opcode': 'WRITE_MEM', 'A': str(A), 'B': str(B), 'value': str(value)})
                else:
                    ET.SubElement(result, 'error', {'message': 'WRITE_MEM attempted with empty stack'})

            # Обрабатываем команду ABS (1 байт)
            elif opcode == 0x00:  # ABS
                if stack:
                    value = stack.pop()
                    abs_value = abs(value)
                    stack.append(abs_value)
                    ET.SubElement(result, 'operation', {'opcode': 'ABS', 'value': str(value), 'abs_value': str(abs_value)})
                else:
                    ET.SubElement(result, 'error', {'message': 'ABS attempted with empty stack'})


    # Запись результата в XML
    tree = ET.ElementTree(result)
    tree.write('result.xml')

if __name__ == '__main__':
    binary_file = sys.argv[1]  # Путь к бинарному файлу
    memory_range = sys.argv[2]  # Пример: "0-1023"
    execute_program(binary_file, memory_range)
# Пример обновления функции execute_program для предотвращения ошибок со стеком
def execute_program(binary_file, memory_range):
    memory = [0] * 1024  # Допустим, у нас 1024 ячейки памяти
    stack = []
    result = ET.Element('result')

    with open(binary_file, 'rb') as f:
        while True:
            byte = f.read(1)  # Читаем 1 байт (код операции)
            if not byte:
                break  # Если данных нет, выходим из цикла
            opcode = ord(byte)

            # Обрабатываем команду LOAD_CONST (5 байтов)
            if opcode == 0xB8:  # LOAD_CONST
                data = f.read(4)  # Читаем 4 байта для B
                if len(data) < 4:
                    break  # Если данных недостаточно, выходим из цикла
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=I', data)[0]  # Извлекаем B
                stack.append(B)
                ET.SubElement(result, 'operation', {'opcode': 'LOAD_CONST', 'A': str(A), 'B': str(B)})

            # Обрабатываем команду READ_MEM (3 байта)
            elif opcode == 0x34:  # READ_MEM
                data = f.read(2)  # Читаем 2 байта для B
                if len(data) < 2:
                    break
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=H', data)[0]  # Извлекаем B
                value = memory[B]
                stack.append(value)
                ET.SubElement(result, 'operation', {'opcode': 'READ_MEM', 'A': str(A), 'B': str(B), 'value': str(value)})

            # Обрабатываем команду WRITE_MEM (3 байта)
            elif opcode == 0xFD:  # WRITE_MEM
                data = f.read(2)  # Читаем 2 байта для B
                if len(data) < 2:
                    break
                A = (opcode & 0xF0) >> 4  # Извлекаем A из opcode
                B = struct.unpack('=H', data)[0]  # Извлекаем B
                
                # Проверка перед pop
                if stack:
                    value = stack.pop()
                    memory[B] = value
                    ET.SubElement(result, 'operation', {'opcode': 'WRITE_MEM', 'A': str(A), 'B': str(B), 'value': str(value)})
                else:
                    ET.SubElement(result, 'error', {'message': 'WRITE_MEM attempted with empty stack'})

            elif opcode == 0x00:  # ABS
                if stack:
                    value = stack.pop()
                    abs_value = abs(value)
                    stack.append(abs_value)
                    ET.SubElement(result, 'operation', {'opcode': 'ABS', 'value': str(value), 'abs_value': str(abs_value)})
                else:
                    # Игнорировать команду ABS, если стек пуст
                    ET.SubElement(result, 'error', {'message': 'ABS ignored due to empty stack'})
    # Запись результата в XML
    tree = ET.ElementTree(result)
    tree.write('result.xml')
