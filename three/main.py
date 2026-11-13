from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base, get_db
from models import Master


def seed_masters():
    with SessionLocal() as db:
        existing = db.scalar(select(Master.id).limit(1))
        if existing is None:
            initial_masters = [
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ]
            db.add_all(initial_masters)
            db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_masters()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/masters")
def get_masters(
    specialization: str | None = None,
    db: Session = Depends(get_db),
):
    query = select(Master)
    if specialization:
        query = query.where(Master.specialization == specialization)

    masters = db.scalars(query).all()
    return [
        {
            "id": master.id,
            "name": master.name,
            "specialization": master.specialization,
        }
        for master in masters
    ]


@app.get("/masters/{master_id}")
def get_master(master_id: int, db: Session = Depends(get_db)):
    master = db.get(Master, master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")

    return {
        "id": master.id,
        "name": master.name,
        "specialization": master.specialization,
    }
