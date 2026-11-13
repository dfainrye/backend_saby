from datetime import datetime
from models import Master, Service, Appoinment


masters: list[Master] = [
    Master(1, "Анна"),
    Master(2, "Иван"),
]

services: list[Service] = [
    Service(1, "Стрижка", 1500),
    Service(2, "Окрашивание", 3000),
]

appointments: list[Appoinment] = []


def get_master(master_id: int) -> Master | None:
    for master in masters:
        if master.master_id == master_id:
            return master
    return None


def get_service(service_id: int) -> Service | None:
    for service in services:
        if service.service_id == service_id:
            return service
    return None


def is_working_time(time_str: str) -> bool:
    try:
        parsed_time = datetime.strptime(time_str, "%H:%M").time()
    except (ValueError, TypeError):
        return False

    open_time = datetime.strptime("08:00", "%H:%M").time()
    close_time = datetime.strptime("20:00", "%H:%M").time()
    return open_time <= parsed_time <= close_time


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Appoinment | None:
    # Проверка заполненности всех полей (Задание 1)
    if (
        not client_name
        or not client_name.strip()
        or master_id is None
        or service_id is None
        or not time
        or not time.strip()
    ):
        return None

    clean_name = client_name.strip()
    clean_time = time.strip()

    # Проверка рабочих часов салона: с 08:00 до 20:00 (Задание 2)
    if not is_working_time(clean_time):
        return None

    master = get_master(master_id)
    service = get_service(service_id)
    if master is None or service is None:
        return None

    # Проверка, что на это время ещё нет записи
    for existing in appointments:
        if existing.time == clean_time:
            return None

    appointment = Appoinment(
        appointment_id=len(appointments) + 1,
        client_name=clean_name,
        master_id=master.master_id,
        service_id=service.service_id,
        time=clean_time,
    )
    appointments.append(appointment)
    return appointment
