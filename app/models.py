from app import db
from sqlalchemy.orm import Mapped, mapped_column


class Kachel(db.Model):
    __tablename__ = 'kacheln'

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str]
    link: Mapped[str]
    image: Mapped[str]
    background_color: Mapped[str]
