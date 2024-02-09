from typing import Union, Dict, Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class HasUidFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        uids = re.findall(r"\b\d+", message.text)

        # Если юзернеймы есть, то передаем их в хэндлер
        if len(uids) > 0:
            return {"uids": uids}
        return False
