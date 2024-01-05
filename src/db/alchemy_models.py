from core.db_client import Base
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

 
class UserModel(Base):
    __tablename__ = "app_user"
    _table_args__ = {'extend_existing': True}

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)
    display_name = mapped_column(String, unique=False, nullable=True)
    enabled = mapped_column(Boolean, unique=False, default=True)
