from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base, get_db
from models import Category, Service
from schemas import ServiceCreate, ServiceResponse


def seed_categories():
    with SessionLocal() as db:
        existing = db.scalar(select(Category.id).limit(1))
        if existing is None:
            initial_categories = [
                Category(id=1, name="Стрижки и укладки"),
                Category(id=2, name="Маникюр и педикюр"),
                Category(id=3, name="Брови и ресницы"),
                Category(id=4, name="Спа-процедуры"),
            ]
            db.add_all(initial_categories)
            db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_categories()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.scalars(select(Category)).all()
    return [{"id": c.id, "name": c.name} for c in categories]


@app.get("/services", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.scalars(select(Service)).all()


@app.post("/services", status_code=201, response_model=ServiceResponse)
def create_service(service_data: ServiceCreate, db: Session = Depends(get_db)):
    category = db.get(Category, service_data.categoryId)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    new_service = Service(
        category_id=service_data.categoryId,
        title=service_data.title,
        desc=service_data.desc,
        duration=service_data.duration,
        price=service_data.price,
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service
