import datetime
from sqlalchemy.sql import func
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///avito_base1.db")


class Base(DeclarativeBase):
    pass


class Avito(Base):
    __tablename__ = "avito_parser"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.item_id!r})"


def create_items(data: dict):
    '''Добавляем запись, если такая есть ловим искоючение'''
    try:
        with Session(engine) as session:
            items_avito = Avito(
                item_id=data['item_id'],
                name=data['name'],
                description=data['description'],
                link=data['link'],
                price=data['price'],
                city=data['city']
            )

            session.add(items_avito)
            session.commit()
    except Exception as err:
        print('--ERROR--', str(err))


def fetch_id(id_item):
    '''проверяем уникальность объявления в базе'''
    with Session(engine) as session:
        stmt = select(Avito).where(Avito.item_id == id_item)
        resp = session.scalar(stmt)
        if resp is None:
            print('[!] Нет такого объявления, значит добавляем')
            return True
        else:
            print('[+] Объявление уже есть в базе', resp)
            return False


def change_valid():
    '''Объявления меньше 5000 руб. и объявления больше 70 000 руб. нам не интересны'''
    with Session(engine) as session:
        stmt = select(Avito).where(Avito.price <= 5000)
        resp = session.scalars(stmt)
        for i in resp:
            print(i)


def main():
    Base.metadata.create_all(engine)
    change_valid()


if __name__ == '__main__':
    main()
