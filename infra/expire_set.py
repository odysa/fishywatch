from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Generic, TypeVar

_T = TypeVar("_T")


@dataclass
class SetItem(Generic[_T]):
    item: _T
    timestamp: datetime


class ExpireSet(Generic[_T]):
    item_dict: Dict[int, SetItem[_T]]
    limit: int
    expire_time: timedelta
    current: int

    def __init__(self, limit: int, expire_time: timedelta):
        self.item_dict = {}
        self.expire_time = expire_time
        self.limit = limit
        self.current = 0

    def add(self, item: _T):
        set_item: SetItem[_T] = SetItem(item=item, timestamp=datetime.now())
        self.item_dict[item] = set_item

        if len(self.item_dict) > self.limit:
            self.evict_expire()

    def evict_expire(self):
        expired_items = []
        for key, value in self.item_dict.items():
            add_time = value.timestamp
            current_time = datetime.now()
            if current_time - add_time >= self.expire_time:
                expired_items.append(key)

        for key in expired_items:
            del self.item_dict[key]

    def __contains__(self, item: _T) -> bool:
        return item in self.item_dict

    def __len__(self):
        return len(self.item_dict)

    def values(self) -> list[_T]:
        return [v.item for v in self.item_dict.values()]
