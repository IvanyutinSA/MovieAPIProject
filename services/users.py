from sqlalchemy.orm import Session

import models
import schemas


def get_users(db: Session):
    return db.query(models.UserInDB).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserInDB).filter(
        models.UserInDB.id == user_id
    ).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.UserInDB).filter(
        models.UserInDB.name == username
    ).first()


def create_user(db: Session, user: schemas.UserToCreate):
    db_user = models.UserInDB(
        name=user.name,
        hashed_password=user.password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_users_favorite_film(db: Session, user_id: int, film_id: int):
    db_favorite_film = models.FavoriteFilmsInDB(
        user_id=user_id,
        film_id=film_id,
    )
    db.add(db_favorite_film)
    db.commit()
    db.refresh(db_favorite_film)
    return db_favorite_film


def add_users_favorite_actor(db: Session, user_id: int, actor_id: int):
    db_favorite_actor = models.FavoriteActorsInDB(
        user_id=user_id,
        actor_id=actor_id,
    )
    db.add(db_favorite_actor)
    db.commit()
    db.refresh(db_favorite_actor)
    return db_favorite_actor


def get_users_favorite_films(db: Session, user: schemas.User):
    films_id = db.query(models.FavoriteFilmsInDB).filter(
        models.FavoriteFilmsInDB.user_id == user.id
    ).all()

    films_id = list(map(lambda x: x.film_id, films_id))

    films = db.query(models.FilmInDB).filter(
        models.FilmInDB.id.in_(films_id)
    ).all()

    return films


def get_users_favorite_actors(db: Session, user: schemas.User):
    actors_id = [x.actor_id for x in db.query(models.FavoriteActorsInDB).filter(
        models.FavoriteActorsInDB.user_id == user.id
    ).all()]

    actors = db.query(models.FilmInDB).filter(
        models.FilmInDB.id.in_(actors_id)
    ).all()

    return actors
