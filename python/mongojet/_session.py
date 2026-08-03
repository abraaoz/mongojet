from __future__ import annotations

from types import TracebackType
from typing import Any

from bson import CodecOptions

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from ._codec import Codec
from ._types import TransactionOptions


class ClientSession:
    def __init__(self, core_session: Any, codec_options: CodecOptions) -> None:
        self._core_session = core_session
        self._codec = Codec(options=codec_options)

    async def start_transaction(
        self,
        **options: Unpack[TransactionOptions],
    ) -> _TransactionContext:
        await self._core_session.start_transaction(self._codec.encode(options))
        return _TransactionContext(self)

    async def commit_transaction(self) -> None:
        await self._core_session.commit_transaction()

    async def abort_transaction(self) -> None:
        await self._core_session.abort_transaction()

    @property
    def core_session(self) -> Any:
        return self._core_session


class _TransactionContext:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # TODO: check if session in_transaction?  # noqa: FIX002
        if exc_val is None:
            await self._session.commit_transaction()
        else:
            await self._session.abort_transaction()
