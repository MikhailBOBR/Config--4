# Проект: Ассемблер и Интерпретатор

## Общее описание

Этот проект включает в себя два основных компонента: **ассемблер** и **интерпретатор**. Ассемблер компилирует исходные инструкции, представленные в XML формате, в бинарный формат. Интерпретатор выполняет эти бинарные инструкции, эмулируя работу с памятью и стеком, и записывает результат выполнения в XML лог.

## Функционал

### Файл `assembler.py`

1. **assemble_line(instruction)** — Преобразует одну инструкцию из XML в бинарный формат:
   - `LOAD_CONST`: Загружает константу в стек.
   - `READ_MEM`: Читает значение из памяти по индексу и помещает его в стек.
   - `WRITE_MEM`: Записывает значение из стека в память по индексу.
   - `ABS`: Вычисляет абсолютное значение верхнего элемента в стеке.

2. **assemble(input_file, output_bin, log_file)** — Преобразует все инструкции из XML файла в бинарный формат и записывает в файл. Лог выполнения сохраняется в XML файл.

3. **Тесты**:
   - `test_load_const()`: Проверяет корректность преобразования инструкции `LOAD_CONST`.
   - `test_read_mem()`: Проверяет корректность преобразования инструкции `READ_MEM`.
   - `test_write_mem()`: Проверяет корректность преобразования инструкции `WRITE_MEM`.
   - `test_abs()`: Проверяет корректность работы инструкции `ABS`.
    Чтобы запустить тестовую программу test_assembler.py: 
```bash
python test_assembler.py
```


### Файл `interpreter.py`

1. **execute_program(binary_file, memory_range)** — Загружает бинарный файл с инструкциями и выполняет их, эмулируя работу процессора:
   - `LOAD_CONST`: Загружает значение в стек.
   - `READ_MEM`: Читает значение из памяти и помещает в стек.
   - `WRITE_MEM`: Записывает значение из стека в память.
   - `ABS`: Применяет операцию абсолютного значения к верхнему элементу стека.

### Пример входных данных

#### Входной файл `input.xml`:

```xml
<program>
    <instruction opcode="LOAD_CONST" A="1" B="789"/>
    <instruction opcode="LOAD_CONST" A="2" B="-456"/>
    <instruction opcode="ABS"/>
    <instruction opcode="WRITE_MEM" A="3" B="50"/>
    <instruction opcode="READ_MEM" A="4" B="50"/>
</program>
```
Лог выполнения log.xml:
```xml
<log>
    <instruction raw="B8 00 00 00 15 03 00 00" mnemonic="LOAD_CONST A=1 B=789" />
    <instruction raw="B8 00 00 00 38 FE FF FF" mnemonic="LOAD_CONST A=2 B=-456" />
    <instruction raw="00" mnemonic="ABS value=456 abs_value=456" />
    <instruction raw="FD 00 00 32 00" mnemonic="WRITE_MEM A=3 B=50" />
    <instruction raw="74 00 00 32 00" mnemonic="READ_MEM A=4 B=50" />
</log>
```
Запуск программы
Компиляция в бинарный формат:

Для компиляции программы из XML файла в бинарный формат, используйте команду:

```bash
python assembler.py input.xml output.bin log.xml
```
input.xml — входной XML файл с исходными инструкциями.
output.bin — путь к выходному бинарному файлу.
log.xml — путь к файлу для логирования выполнения программы.

Выполнение программы:
Для выполнения программы из бинарного файла, используйте команду:
```bash
python interpreter.py output.bin "0-1023"
```
output.bin — путь к бинарному файлу с скомпилированными инструкциями.
memory_range — диапазон памяти, в котором будет происходить выполнение программы (например, "0-1023").

Пример логирования
После выполнения программы будет создан файл result.xml, который содержит лог всех выполненных операций, включая ошибки, если таковые возникнут, например, попытку работы с пустым стеком.

```xml
<result>
    <operation opcode="LOAD_CONST" A="1" B="789" />
    <operation opcode="LOAD_CONST" A="2" B="-456" />
    <operation opcode="ABS" value="456" abs_value="456" />
    <operation opcode="WRITE_MEM" A="3" B="50" value="456" />
    <operation opcode="READ_MEM" A="4" B="50" value="456" />
</result>
```
Требования
Python 3.6+
Стандартные библиотеки Python: struct, sys, xml.etree.ElementTree