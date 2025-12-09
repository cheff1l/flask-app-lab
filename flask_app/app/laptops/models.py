from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime, timezone


class LaptopCategory(db.Model):
    __tablename__ = 'laptop_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)

    laptops: Mapped[List["Laptop"]] = relationship(back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<LaptopCategory {self.category_name}>'


class Laptop(db.Model):
    __tablename__ = 'laptops'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(db.String(100), nullable=False)
    model: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    category_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('laptop_categories.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    category: Mapped["LaptopCategory"] = relationship(back_populates="laptops")
    user: Mapped["User"] = relationship()

    def __repr__(self):
        return f'<Laptop {self.brand} {self.model}>'