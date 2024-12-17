from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .database import Base
import enum

# Инициализация контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Определение перечисления для пола
class GenderEnum(enum.Enum):
    male = "Мужской"
    female = "Женский"

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    birth_date = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    language = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Метод для проверки пароля
    def verify_password(self, plain_password: str) -> bool:
        """
        Сравнивает хешированный пароль с введённым пользователем паролем.

        :param plain_password: Введённый пользователем пароль
        :return: True, если пароли совпадают, иначе False
        """
        return pwd_context.verify(plain_password, self.hashed_password)
