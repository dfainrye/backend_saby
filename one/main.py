from services import appointments, create_appointment


# 1. Создание двух корректных записей
first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

print("Список записей:")
for appointment in appointments:
    print(appointment.client_name, appointment.time)

# Очищаем список для изолированной проверки ошибочных случаев
appointments.clear()

# 2. Проверка Задания 1: не заполнено имя клиента
no_correct_appointment = create_appointment("", 1, 1, "12:00")
print(len(appointments))

# 3. Проверка Задания 2: некорректное время (вне диапазона 08:00 - 20:00)
no_correct_time = create_appointment("Сидорова А.А.", 1, 1, "00:00")
print(len(appointments))
