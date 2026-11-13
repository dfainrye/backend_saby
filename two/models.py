class Category:
    def __init__(self, category_id: int, name: str, services_count: int):
        self.id = category_id
        self.name = name
        self.services_count = services_count


class Master:
    def __init__(self, master_id: int, name: str):
        self.master_id = master_id
        self.name = name


class Service:
    def __init__(self, service_id: int, title: str, price: int, category_id: int):
        self.service_id = service_id
        self.title = title
        self.price = price
        self.category_id = category_id


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
