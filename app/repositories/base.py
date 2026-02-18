from app.config.database import Base


class BaseRepo:
    model_class: Base

    async def get_data_by_id(self):
        pass


    async def get_data_by_name(self):
        pass