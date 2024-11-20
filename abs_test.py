# Программа для выполнения операции abs() поэлементно над вектором длины 5

def apply_abs_to_vector(vector):
    """
    Выполняет операцию abs() поэлементно над вектором и записывает результат в исходный вектор.
    
    :param vector: Список с 5 элементами.
    :return: Измененный вектор с примененной операцией abs() к каждому элементу.
    """
    for i in range(len(vector)):
        vector[i] = abs(vector[i])
    return vector

if __name__ == '__main__':
    # Исходный вектор
    vector = [-1, 2, -3, 4, -5]
    
    # Выводим исходный вектор
    print("Исходный вектор:", vector)
    
    # Применяем операцию abs() к каждому элементу
    result_vector = apply_abs_to_vector(vector)
    
    # Выводим результат
    print("Результат после применения abs():", result_vector)
