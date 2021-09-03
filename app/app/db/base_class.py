from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr  # type: ignore
from stringcase import snakecase  # type: ignore


@as_declarative()
class Base:
    id: Any
    __name__: str

    #
    @declared_attr
    def __tablename__(cls) -> str:
        """
        This generates __tablename__ automatically, mapping the class name to a snake-cased string.

        Example: class NewTableCreated(Base) would be converted to `SELECT * FROM new_table_created` through the ORM.

        This is completely optional, but helpful to enforce naming conventions programmatically.
        """
        return snakecase(cls.__name__)
