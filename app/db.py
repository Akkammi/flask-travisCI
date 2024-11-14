from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="expenses")

    def __repr__(self):
        return f"Expense(title='{self.title}', amount={self.amount})"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    expenses: Mapped[list["Expense"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(username={self.username}"
