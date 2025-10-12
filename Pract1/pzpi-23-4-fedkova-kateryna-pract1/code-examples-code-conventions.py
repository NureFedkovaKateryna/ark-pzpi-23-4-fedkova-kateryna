# Поганий приклад

# Пакет
from CustomerAnalytics import GenerateReport

# Модуль
import MathUtils

# Функція
def AddNums():
    pass

# Змінна
FirstNumber = 1

# Константа
piNumber = 3.14

# Клас та метод
class online_course_platform:
    def EnrollStudentInCourse(self):
        pass


# Гарний приклад

# Пакет
from customeranalytics import generate_report

# Модуль
import math_utils


# Функція
def add_nums():
    pass


# Змінна
first_number = 1

# Константа
PI_NUMBER = 3.14


# Клас та метод
class OnlineCoursePlatform:
    def enroll_student_in_course(self):
        pass



# Поганий приклад
O = 2
l = 3

# Гарний приклад
first_number = 2
second_number = 3

# Поганий приклад
a = "Python Code-Conventions"
b, c = a.split()
print(f"{c}, {b}")

# Гарний приклад
lecture_title = "Python Code-Conventions"
language, topic = lecture_title.split()
print(f"{topic}, {language}")


# Поганий приклад
for number in range(0, 10):
# Ітерація по `number` десять разів та вивід на екран значення `number`.
    print(number)


# Гарний приклад
for number in range(0, 10):
    # Ітерація по `number` десять разів та вивід на екран значення `number`.
    print(number)


# Поганий приклад
a = "Python Code-Conventions"  # Presentation Title

# Гарний приклад
presentation_title = "Python Code-Conventions"



# Поганий приклад
def add_two_numbers(a, b):
    # додаємо a та b
    return a + b


# Гарний приклад
def add_two_numbers(a, b):
    """Add a to b."""
    return a + b


# Поганий приклад
class Dog:
    pass
class Cat:
    pass


# Гарний приклад
class Dog:
    pass


class Cat:
    pass


# Поганий приклад
class Dog:
    def eat(self):
        return None
    def bark(self):
        return None

class Cat:
    pass


# Гарний приклад
class Dog:
    def eat(self):
        return None
    
    def bark(self):
        return None


class Cat:
    pass



# Поганий приклад
def calculate_mean(numbers):
    sum_numbers = 0
    
    for number in numbers:
        sum_numbers = sum_numbers + number
    
    mean = sum_numbers / len(numbers)

    return mean


# Гарний приклад
def calculate_mean(numbers):
    sum_numbers = 0
    for number in numbers:
        sum_numbers = sum_numbers + number
    mean = sum_numbers / len(numbers)
    return mean



def add(first_number, second_number, 
        third_number, fourth_number, 
        fifth_number):
    return None


from package import example1, \
    example2, example3



# Поганий приклад
def data(a, b, c, d, e):
    result = (a + b + c) * (1 - d/100) + e
    print(result)


# Гарний приклад
from dataclasses import dataclass


@dataclass
class Order:
    items_total: float
    shipping_cost: float
    tax_rate: float
    discount_rate: float = 0.0


def calculate_final_price(order):
    """Обчислює фінальну ціну замовлення після знижки та податку."""
    subtotal = order.items_total - (order.items_total * order.discount_rate)
    taxed = subtotal * (1 + order.tax_rate)
    return taxed + order.shipping_cost




# Поганий приклад
foo = long_function_name(arg_one, arg_two,
    arg_three, arg_four)


def long_function_name(
    arg_one, arg_two, arg_three,
    arg_four):
    print(arg_one)


# Гарний приклад
foo = long_function_name(arg_one, arg_two,
                         arg_three, arg_four)


def long_function_name(
        arg_one, arg_two, arg_three,
        arg_four):
    print(arg_one)


# Поганий приклад
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Гарний приклад
if (this_is_one_thing
        and that_is_another_thing):
    do_something()


# Поганий приклад
my_list = [
    1, 2, 3,
    4, 5, 6,]

# Гарний приклад
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]

my_list = [
    1, 2, 3,
    4, 5, 6,
]
