from fastapi import FastAPI, HTTPException
from services import (
    masters,
    services,
    appointments,
    get_all_categories,
    get_category,
    get_master,
    get_service,
    create_appointment,
)

app = FastAPI()


# ===== Задание 1. Список категорий =====
@app.get("/categories")
def list_categories():
    return get_all_categories()


# ===== Задание 2. Информация по конкретной категории =====
@app.get("/categories/{category_id}")
def read_category(category_id: int):
    category = get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ===== Базовые эндпоинты из лекции =====
@app.get("/masters")
def list_masters():
    return [{"id": m.master_id, "name": m.name} for m in masters]


@app.get("/masters/{master_id}")
def read_master(master_id: int):
    master = get_master(master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return {"id": master.master_id, "name": master.name}


@app.get("/services")
def list_services():
    return [
        {
            "id": s.service_id,
            "title": s.title,
            "price": s.price,
            "categoryId": s.category_id,
        }
        for s in services
    ]


@app.get("/appointments")
def list_appointments():
    return [
        {
            "id": a.id,
            "client_name": a.client_name,
            "master_id": a.master_id,
            "service_id": a.service_id,
            "time": a.time,
        }
        for a in appointments
    ]


@app.post("/appointments", status_code=201)
def add_appointment(data: dict):
    required = ("client_name", "master_id", "service_id", "time")
    if any(field not in data for field in required):
        raise HTTPException(status_code=400, detail="Missing required fields")

    if not isinstance(data["master_id"], int) or isinstance(data["master_id"], bool):
        raise HTTPException(status_code=400, detail="master_id must be an integer")

    if not isinstance(data["service_id"], int) or isinstance(data["service_id"], bool):
        raise HTTPException(status_code=400, detail="service_id must be an integer")

    if get_master(data["master_id"]) is None:
        raise HTTPException(status_code=404, detail="Master not found")

    if get_service(data["service_id"]) is None:
        raise HTTPException(status_code=404, detail="Service not found")

    appointment = create_appointment(
        data["client_name"],
        data["master_id"],
        data["service_id"],
        data["time"],
    )
    if appointment is None:
        raise HTTPException(status_code=409, detail="Time is already occupied or invalid")

    return {
        "id": appointment.id,
        "client_name": appointment.client_name,
        "master_id": appointment.master_id,
        "service_id": appointment.service_id,
        "time": appointment.time,
    }
