from sqlalchemy.orm import Session

import models
import schemas


def add_film_staff_actor(db: Session, actor_id: int, film_id: int):
    db_film_actor = models.FilmStaffInDB(
        actor_id=actor_id,
        film_id=film_id,
    )
    db.add(db_film_actor)
    db.commit()
    db.refresh(db_film_actor)
    return db_film_actor


def add_film(db: Session, film: schemas.FilmToCreate):
    db_film = models.FilmInDB(
        name=film.name,
        description=film.description,
        release_year=film.release_year,
    )
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def get_film_staff(db: Session, film_id: int):
    film_staff_id = [x.actor_id for x in db.query(models.FilmStaffInDB).filter(
        models.FilmStaffInDB.film_id == film_id
    ).all()]

    actors = db.query(models.ActorInDB).filter(
        models.ActorInDB.id.in_(film_staff_id)
    )

    return actors


def get_films_there_was_actor(db: Session, actor_id: int):
    films_id = [x.film_id for x in db.query(models.FilmStaffInDB).filter(
        models.FilmStaffInDB.actor_id == actor_id
    ).all()]

    films = db.query(models.FilmInDB).filter(
        models.FilmInDB.id.in_(films_id)
    ).all()

    return films


def get_films(db: Session):
    return db.query(models.FilmInDB).all()


def get_film_by_id(db: Session, film_id: int):
    return db.query(models.FilmInDB).filter(
        models.FilmInDB.id == film_id
    ).first()


def get_films_by_name(db: Session, film_name: str):
    return db.query(models.FilmInDB).filter(
        models.FilmInDB.name == film_name
    ).all()


def get_films_by_release_year(db: Session, year: int):
    return db.query(models.FilmInDB).filter(
        models.FilmInDB.release_year == year
    ).all()


def get_films_staff_by_id(db: Session, film_id: int):
    actors_id = db.query(models.FilmStaffInDB).filter(
        models.FilmStaffInDB.film_id == film_id
    )
    return db.query(models.ActorInDB).filter(
        models.ActorInDB.id in actors_id
    )


def update_film(db: Session, film_id: int, new_film: schemas.FilmToCreate):
    film = get_film_by_id(db, film_id)
    film.name = new_film.name
    film.description = new_film.description
    film.release_year = new_film.release_year
    db.commit()
    db.refresh(film)
    return film


def delete_film(db: Session, film_id: int):
    actor = get_film_by_id(db, film_id)
    db.delete(actor)
    db.commit()
    return 'ok'
