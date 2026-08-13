from __future__ import annotations

from collections import deque
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, TypeVar

from bson import CodecOptions

try:
    from typing import Self  # type:ignore[attr-defined]
except ImportError:
    from typing_extensions import Self

from ._codec import Codec

if TYPE_CHECKING:
    from .mongojet import CoreBatchCursor, CoreSessionBatchCursor

T = TypeVar("T")


class Cursor(AsyncIterator[T]):
    def __init__(
        self,
        core_cursor: CoreBatchCursor | CoreSessionBatchCursor,
        codec_options: CodecOptions,
    ) -> None:
        self._core_cursor = core_cursor
        self._codec = Codec(options=codec_options)
        self._buff: deque[T] = deque()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        if not self._buff:
            data: bytes = await self._core_cursor.next_batch()
            if not data:
                raise StopAsyncIteration

            # "empty" mongodb document is a sequence of bytes
            # b'\x05\x00\x00\x00\x00'
            # that decodes into empty dict
            # bson.encode({}) == b'\x05\x00\x00\x00\x00'
            # bson.decode(b'\x05\x00\x00\x00\x00') == {}
            doc = self._codec.decode(data)
            if not doc:
                raise StopAsyncIteration

            self._buff.extend(list(doc.values()))

        return self._buff.popleft()

    async def to_list(self, length: int | None = None) -> list[T]:
        if length is not None:
            raise ValueError(
                "Only None value is supported for partial compatibility with Motor API"
            )
        data = await self._core_cursor.collect()
        doc = self._codec.decode(data)
        if not doc:
            return []

        return list(doc.values())
