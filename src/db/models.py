from core.app_config import config
from core.db_client import sessionmanager
from core.helpers import Singleton
from db.alchemy_models import UserModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from core.logger import logger
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from core.enums import DBEngine

class AbstractBase(metaclass=Singleton):
    model = None

    def __init__(self) -> None:
        if not sessionmanager._sessionmaker:
            sessionmanager.init(config.DATABASE_URI)
            logger.debug("initialized model instance")

    async def _query(self, statement):
        logger.debug(f"perform db query exec:{statement}")
        async with sessionmanager.session() as session:
            try:
                result = await session.execute(statement)
            except IntegrityError as ex:
                logger.warning(f"malformed sql statement: {ex}")
                return []
            result_data = []
            for item in result:
                result_data.append(item[0])
            return result_data

    # updates require commits so
    async def _exec(self, statement):
        logger.debug(f"perform db data manipulation exec:{statement}")
        async with sessionmanager.session() as session:
            result = await session.execute(statement)
            await session.commit()
            logger.info(f"update affected {result.rowcount} rows.")
            return result

    def _parse_data(self, data: dict):
        # disallow updating primary key, even if attempted.
        data.pop("id", None)
        return {item: value for item, value in data.items() if item in self.columns}

    def _get_attr(self, attr):
        if not attr in self.columns:
            raise IntegrityError(f"field {attr} does not exist. avaialble fields are {self.columns}")
        return getattr(self.model, attr)

    # query data by single key:value filter
    async def get_item(self, attr, value=None):
        attr = self._get_attr(attr)
        statement = select(self.model).where(attr == value)
        return await self._query(statement)

    # create new object
    async def insert_item(self, **kwargs):
        statement = insert(self.model).values(**kwargs)
        # SQLite provided with python is an older version that doesn't support returning..
        if config.DB_ENGINE == DBEngine.POSTGRES.value:
            statement = statement.returning(*self.model_columns)
        result = await self._exec(statement)
        return result

    # update data by single key:value filter, with kwargs being the payload
    async def update_item(self, attr: int, value, **kwargs):
        attr = self._get_attr(attr)
        statement = update(self.model).where(attr == value).values(**kwargs)
        result = await self._exec(statement)
        return result

    # delete data by single key:value filter
    async def delete_item(self, attr: int, value):
        attr = self._get_attr(attr)
        statement = delete(self.model).where(attr == value)
        result = await self._exec(statement)
        return result

    async def get_item_by_id(self, item_id):
        result = await self.get_item("id", item_id)
        return result[0] if result else None

    async def create_item(self, **kwargs):
        create_data = self._parse_data(kwargs)
        result = await self.insert_item(**create_data)
        result_item = {"id": result.inserted_primary_key.id}
        result_item.update(result.last_inserted_params())
        return result_item

    async def update_item_by_id(self, item_id: int, **kwargs):
        update_data = self._parse_data(kwargs)
        return await self.update_item("id", item_id, **update_data)

    async def delete_item_by_id(self, item_id: int, **kwargs):
        update_data = self._parse_data(kwargs)
        return await self.delete_item("id", item_id, **update_data)



class User(AbstractBase):
    model = UserModel
    model_columns: ReadOnlyColumnCollection = model.__table__.columns
    columns: list = model.__table__.columns.keys()
