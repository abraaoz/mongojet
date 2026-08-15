# ruff: noqa: A001,A002
from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

try:
    from typing import Unpack  # type:ignore[attr-defined]
except ImportError:
    from typing_extensions import Unpack

from bson import CodecOptions

from ._codec import Codec
from ._collection import Collection
from ._cursor import Cursor
from ._gridfs import GridfsBucket
from ._types import (
    AggregateOptions,
    CollectionOptions,
    CollectionSpecification,
    CreateCollectionOptions,
    Document,
    DropDatabaseOptions,
    GridFsBucketOptions,
    ListCollectionsOptions,
    ReadConcern,
    ReadPreference,
    RunCommandOptions,
    WriteConcern,
)

if TYPE_CHECKING:
    from ._client import Client
    from ._session import ClientSession
    from .mongojet import CoreBatchCursor, CoreDatabase, CoreSessionBatchCursor


# noinspection PyShadowingBuiltins
class Database:
    def __init__(
        self,
        core_database: CoreDatabase,
        codec_options: CodecOptions,
        client: Client,
    ) -> None:
        self._client = client
        self._core_database = core_database
        self._codec = Codec(options=codec_options)
        self._codec_options = codec_options

    def get_collection(
        self,
        name: str,
        codec_options: CodecOptions | None = None,
        **options: Unpack[CollectionOptions],
    ) -> Collection:

        if options:
            core_collection = self._core_database.get_collection_with_options(
                name, self._codec.encode(options)
            )
        else:
            core_collection = self._core_database.get_collection(name)

        return Collection(
            core_collection,
            codec_options=codec_options or self._codec_options,
            database=self,
        )

    async def create_collection(
        self,
        name: str,
        session: ClientSession | None = None,
        **kwargs: Unpack[CreateCollectionOptions],
    ) -> None:

        options = self._codec.encode(kwargs)

        if session is None:
            await self._core_database.create_collection(
                name,
                options,
            )
        else:
            await self._core_database.create_collection_with_session(
                session.core_session,
                name,
                options,
            )

    async def list_collections(
        self,
        filter: Document | None = None,
        session: ClientSession | None = None,
        **options: Unpack[ListCollectionsOptions],
    ) -> Sequence[CollectionSpecification]:
        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_database.list_collections(filter, options)
        else:
            result = await self._core_database.list_collections_with_session(
                session.core_session,
                filter,
                options,
            )

        return [cast("CollectionSpecification", self._codec.decode(d)) for d in result]

    async def run_command(
        self,
        command: Document,
        session: ClientSession | None = None,
        **options: Unpack[RunCommandOptions],
    ) -> Document:
        command = self._codec.encode(command, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_database.run_command(command, options)
        else:
            result = await self._core_database.run_command_with_session(
                session.core_session,
                command,
                options,
            )

        return self._codec.decode(result)

    async def aggregate(
        self,
        pipeline: Sequence[Document],
        session: ClientSession | None = None,
        **options: Unpack[AggregateOptions],
    ) -> Cursor[Document]:
        pipeline = [self._codec.encode(doc) for doc in pipeline]
        options = self._codec.encode(options)

        cur: CoreBatchCursor | CoreSessionBatchCursor

        if session is None:
            cur = await self._core_database.aggregate(pipeline, options)
        else:
            cur = await self._core_database.aggregate_with_session(
                session.core_session,
                pipeline,
                options,
            )

        return Cursor(cur, codec_options=self._codec_options)

    def gridfs_bucket(
        self,
        **options: Unpack[GridFsBucketOptions],
    ) -> GridfsBucket:
        core_bucket = self._core_database.gridfs_bucket(self._codec.encode(options))
        return GridfsBucket(core_bucket=core_bucket, codec_options=self._codec_options)

    async def drop(
        self,
        session: ClientSession | None = None,
        **kwargs: Unpack[DropDatabaseOptions],
    ) -> None:
        options = self._codec.encode(kwargs)
        if session is None:
            await self._core_database.drop(
                options,
            )
        else:
            await self._core_database.drop_with_session(
                session.core_session,
                options,
            )

    @property
    def read_preference(self) -> ReadPreference | None:
        data = self._core_database.read_preference()
        return cast("ReadPreference | None", self._codec.decode(data))

    @property
    def write_concern(self) -> WriteConcern | None:
        data = self._core_database.write_concern()
        return cast("WriteConcern | None", self._codec.decode(data))

    @property
    def read_concern(self) -> ReadConcern | None:
        data = self._core_database.read_concern()
        return cast("ReadConcern | None", self._codec.decode(data))

    @property
    def name(self) -> str:
        return self._core_database.name

    @property
    def client(self) -> Client:
        return self._client

    def __getitem__(self, name: str) -> Collection:
        core_collection = self._core_database.get_collection(name)
        return Collection(
            core_collection,
            codec_options=self._codec_options,
            database=self,
        )

    def __getattr__(self, name: str) -> Collection:
        if name.startswith("_"):  # pragma: no cover
            raise AttributeError(
                f"Database has no attribute {name!r}. To access the {name}"
                f" collection, use database[{name!r}]."
            )
        return self.__getitem__(name)
