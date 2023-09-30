from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///avito_base.db", echo=True)


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


def main():
    Base.metadata.create_all(engine)



if __name__ == '__main__':
    main()
