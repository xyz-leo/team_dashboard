from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from passlib.context import CryptContext

from app.core.database import Base


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    bcrypt__rounds=12  
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)

    # N:N relationship with Team via TeamMember table
    teams: Mapped[List["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Individual tasks
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # ----------------------------
    # Password utilities
    # ----------------------------
    def set_password(self, plain_password: str):
        """Hashes and sets the password."""
        MAX_BCRYPT_BYTES = 72
        password_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
        self.password_hash = pwd_context.hash(password_bytes)


    def verify_password(self, plain_password: str) -> bool:
        """Verifies a plain password against the stored hash."""
        return pwd_context.verify(plain_password, self.password_hash)
