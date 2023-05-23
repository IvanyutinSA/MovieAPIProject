from sqlalchemy.orm import Session

import models
import schemas


def add_actor(db: Session, actor: schemas.ActorToCreate):
    db_actor = models.ActorInDB(
        name=actor.name,
        info=actor.info,
    )

    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def get_actor_by_id(db: Session, actor_id: int):
    actor = db.query(models.ActorInDB).filter(
        models.ActorInDB.id == actor_id
    ).first()
    return actor


def add_actors_film(db: Session, actor_id: int, film_id: int):
    db_film_staff = models.FilmStaffInDB(
        actor_id=actor_id,
        film_id=film_id,
    )

    db.add(db_film_staff)
    db.commit()
    db.refresh(db_film_staff)

    return db_film_staff


def get_actors(db: Session):
    return db.query(models.ActorInDB).all()


def update_actor(db: Session, actor_id: int, new_actor: schemas.ActorToCreate):
    actor = get_actor_by_id(db, actor_id)
    actor.name = new_actor.name
    actor.info = new_actor.info
    db.commit()
    db.refresh(actor)
    return actor


def delete_actor(db: Session, actor_id: int):
    actor = db.query(models.ActorInDB).filter(
        models.ActorInDB.id == actor_id
    ).first()

    db.delete(actor)
    db.commit()
    return 'ok'
