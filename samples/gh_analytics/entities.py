from ...simpler import (
    DataEntity,
    Table,
)
from .sources import JaffleShopSource


class JaffleShopStores(DataEntity):
    """Stores in the Jaffle Shop dataset."""

    plural_name = "stores"
    properties = Table(JaffleShopSource, "stores").columns_as_properties()
