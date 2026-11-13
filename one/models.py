class Master:
    def __init__(self, master_id: int, name: str):
        self.master_id = master_id
        self.name = name


class Service:
    def __init__(self, service_id: int, title: str, price: int):
        self.service_id = service_id
        self.title = title
        self.price = price


class Appoinment:
    def __init__(
        self,
        appointment_id: int,
        client_name: str,
        master_id: int,
        service_id: int,
        time: str,
    ):
        self.id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time
