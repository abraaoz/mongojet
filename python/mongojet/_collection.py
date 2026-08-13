# ruff: noqa: A001,A002
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, cast

try:
    from typing import Unpack  # type:ignore[attr-defined]
except ImportError:
    from typing_extensions import Unpack

from bson import CodecOptions, ObjectId

from ._codec import Codec
from ._cursor import Cursor
from ._session import ClientSession
from ._types import (
    AggregateOptions,
    CountOptions,
    CreateIndexArgs,
    CreateIndexesResult,
    CreateIndexOptions,
    CreateIndexResult,
    DeleteOptions,
    DeleteResult,
    DistinctOptions,
    Document,
    DropCollectionOptions,
    DropIndexOptions,
    EstimatedCountOptions,
    FindOneAndDeleteOptions,
    FindOneAndReplaceOptions,
    FindOneAndUpdateOptions,
    FindOneOptions,
    FindOptions,
    IndexKeys,
    IndexModel,
    IndexModelDef,
    InsertManyOptions,
    InsertManyResult,
    InsertOneOptions,
    InsertOneResult,
    ListIndexesOptions,
    ReadConcern,
    ReadPreference,
    ReplaceOptions,
    UpdateOptions,
    UpdateResult,
    WriteConcern,
)

if TYPE_CHECKING:
    from ._database import Database
    from .mongojet import CoreCollection


# noinspection PyShadowingBuiltins
class Collection:
    def __init__(
        self,
        core_collection: CoreCollection,
        codec_options: CodecOptions,
        database: Database,
    ) -> None:
        self._database = database
        self._codec_options = codec_options
        self._codec = Codec(options=codec_options)
        self._core_collection = core_collection

    async def find_one(
        self,
        filter: Document | str | None = None,
        session: ClientSession | None = None,
        **options: Unpack[FindOneOptions],
    ) -> Document | None:
        if filter is not None and not isinstance(filter, Mapping):
            filter = {"_id": filter}

        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.find_one(filter, options)
        else:
            result = await self._core_collection.find_one_with_session(
                session.core_session,
                filter,
                options,
            )

        return self._codec.decode(result)

    async def find_one_and_update(
        self,
        filter: Document,
        update: Document | Sequence[Document],
        session: ClientSession | None = None,
        **options: Unpack[FindOneAndUpdateOptions],
    ) -> Document | None:
        filter = self._codec.encode(filter, optional=False)

        if isinstance(update, Sequence):
            update = [self._codec.encode(doc) for doc in update]  # type:ignore[misc]
        else:
            update = self._codec.encode(update, optional=False)  # type:ignore[assignment]

        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.find_one_and_update(
                filter,
                update,
                options,
            )
        else:
            result = await self._core_collection.find_one_and_update_with_session(
                session.core_session,
                filter,
                update,
                options,
            )

        return self._codec.decode(result)

    async def find_one_and_replace(
        self,
        filter: Document,
        replacement: Document,
        session: ClientSession | None = None,
        **options: Unpack[FindOneAndReplaceOptions],
    ) -> Document | None:
        filter = self._codec.encode(filter, optional=False)
        replacement = self._codec.encode(replacement, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.find_one_and_replace(
                filter,
                replacement,
                options,
            )
        else:
            result = await self._core_collection.find_one_and_replace_with_session(
                session.core_session,
                filter,
                replacement,
                options,
            )

        return self._codec.decode(result)

    async def find_one_and_delete(
        self,
        filter: Document,
        session: ClientSession | None = None,
        **options: Unpack[FindOneAndDeleteOptions],
    ) -> Document | None:
        filter = self._codec.encode(filter, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.find_one_and_delete(
                filter,
                options,
            )
        else:
            result = await self._core_collection.find_one_and_delete_with_session(
                session.core_session,
                filter,
                options,
            )

        return self._codec.decode(result)

    async def find(
        self,
        filter: Document | None = None,
        session: ClientSession | None = None,
        **options: Unpack[FindOptions],
    ) -> Cursor[Document]:
        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            cur = await self._core_collection.find(filter, options)
        else:
            cur = await self._core_collection.find_with_session(
                session.core_session,
                filter,
                options,
            )
        return Cursor(cur, codec_options=self._codec_options)

    async def find_many(
        self,
        filter: Document | None = None,
        session: ClientSession | None = None,
        **options: Unpack[FindOptions],
    ) -> list[Document]:
        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            data = await self._core_collection.find_many(filter, options)
        else:
            data = await self._core_collection.find_many_with_session(
                session.core_session,
                filter,
                options,
            )

        doc = self._codec.decode(data)
        return list(doc.values())

    async def aggregate(
        self,
        pipeline: Sequence[Document],
        session: ClientSession | None = None,
        **options: Unpack[AggregateOptions],
    ) -> Cursor[Document]:
        pipeline = [self._codec.encode(doc) for doc in pipeline]
        options = self._codec.encode(options)

        if session is None:
            cur = await self._core_collection.aggregate(pipeline, options)
        else:
            cur = await self._core_collection.aggregate_with_session(
                session.core_session,
                pipeline,
                options,
            )

        return Cursor(cur, codec_options=self._codec_options)

    async def update_one(
        self,
        filter: Document,
        update: Document | Sequence[Document],
        session: ClientSession | None = None,
        **options: Unpack[UpdateOptions],
    ) -> UpdateResult:
        filter = self._codec.encode(filter, optional=False)

        if isinstance(update, Sequence):
            update = [self._codec.encode(doc) for doc in update]  # type:ignore[misc]
        else:
            update = self._codec.encode(update, optional=False)  # type:ignore[assignment]

        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.update_one(
                filter,
                update,
                options,
            )
        else:
            result = await self._core_collection.update_one_with_session(
                session.core_session,
                filter,
                update,
                options,
            )
        return cast("UpdateResult", self._codec.decode(result))

    async def update_many(
        self,
        filter: Document,
        update: Document | Sequence[Document],
        session: ClientSession | None = None,
        **options: Unpack[UpdateOptions],
    ) -> UpdateResult:
        filter = self._codec.encode(filter, optional=False)

        if isinstance(update, Sequence):
            update = [self._codec.encode(doc) for doc in update]  # type:ignore[misc]
        else:
            update = self._codec.encode(update, optional=False)  # type:ignore[assignment]

        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.update_many(
                filter,
                update,
                options,
            )
        else:
            result = await self._core_collection.update_many_with_session(
                session.core_session,
                filter,
                update,
                options,
            )
        return cast("UpdateResult", self._codec.decode(result))

    async def insert_one(
        self,
        document: Document,
        session: ClientSession | None = None,
        **options: Unpack[InsertOneOptions],
    ) -> InsertOneResult:

        if "_id" not in document:
            document["_id"] = ObjectId()

        document = self._codec.encode(document, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.insert_one(
                document,
                options,
            )
        else:
            result = await self._core_collection.insert_one_with_session(
                session.core_session,
                document,
                options,
            )

        return cast("InsertOneResult", self._codec.decode(result))

    async def insert_many(
        self,
        documents: list[Document],
        session: ClientSession | None = None,
        **options: Unpack[InsertManyOptions],
    ) -> InsertManyResult:

        for document in documents:
            if "_id" not in document:
                document["_id"] = ObjectId()

        documents = [self._codec.encode(doc) for doc in documents]
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.insert_many(
                documents,
                options,
            )
        else:
            result = await self._core_collection.insert_many_with_session(
                session.core_session,
                documents,
                options,
            )

        return cast("InsertManyResult", self._codec.decode(result))

    async def replace_one(
        self,
        filter: Document,
        replacement: Document,
        session: ClientSession | None = None,
        **options: Unpack[ReplaceOptions],
    ) -> UpdateResult:
        filter = self._codec.encode(filter, optional=False)
        replacement = self._codec.encode(replacement, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.replace_one(
                filter,
                replacement,
                options,
            )
        else:
            result = await self._core_collection.replace_one_with_session(
                session.core_session,
                filter,
                replacement,
                options,
            )

        return cast("UpdateResult", self._codec.decode(result))

    async def delete_one(
        self,
        filter: Document,
        session: ClientSession | None = None,
        **options: Unpack[DeleteOptions],
    ) -> DeleteResult:
        filter = self._codec.encode(filter, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.delete_one(
                filter,
                options,
            )
        else:
            result = await self._core_collection.delete_one_with_session(
                session.core_session,
                filter,
                options,
            )

        return cast("DeleteResult", self._codec.decode(result))

    async def delete_many(
        self,
        filter: Document,
        session: ClientSession | None = None,
        **options: Unpack[DeleteOptions],
    ) -> DeleteResult:
        filter = self._codec.encode(filter, optional=False)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.delete_many(
                filter,
                options,
            )
        else:
            result = await self._core_collection.delete_many_with_session(
                session.core_session,
                filter,
                options,
            )

        return cast("DeleteResult", self._codec.decode(result))

    async def count_documents(
        self,
        filter: Document | None = None,
        session: ClientSession | None = None,
        **options: Unpack[CountOptions],
    ) -> int:
        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            result = await self._core_collection.count_documents(
                filter,
                options,
            )
        else:
            result = await self._core_collection.count_documents_with_session(
                session.core_session,
                filter,
                options,
            )

        return result

    async def estimated_document_count(
        self,
        **options: Unpack[EstimatedCountOptions],
    ) -> int:
        result = await self._core_collection.estimated_document_count(
            self._codec.encode(options),
        )
        return result

    async def distinct(
        self,
        field_name: str,
        filter: Document | None = None,
        session: ClientSession | None = None,
        **options: Unpack[DistinctOptions],
    ) -> list[Any]:
        filter = self._codec.encode(filter)
        options = self._codec.encode(options)

        if session is None:
            data = await self._core_collection.distinct(
                field_name,
                filter,
                options,
            )
        else:
            data = await self._core_collection.distinct_with_session(
                session.core_session,
                field_name,
                filter,
                options,
            )

        result = self._codec.decode(data)
        return result["values"]

    async def create_index(
        self,
        keys: IndexKeys,
        session: ClientSession | None = None,
        **kwargs: Unpack[CreateIndexArgs],
    ) -> CreateIndexResult:

        options: dict[str, Any] = {}
        if "maxTimeMS" in kwargs:
            options["maxTimeMS"] = int(kwargs.pop("maxTimeMS"))  # type: ignore[arg-type]
        if "comment" in kwargs:
            options["comment"] = kwargs.pop("comment")
        if "writeConcern" in kwargs:
            options["commitQuorum"] = kwargs.pop("commitQuorum")
        if "commitQuorum" in kwargs:
            options["commitQuorum"] = kwargs.pop("commitQuorum")

        model = IndexModel(keys, **kwargs)  # type: ignore[misc]

        if session is None:
            result = await self._core_collection.create_index(
                self._codec.encode(model.document),
                self._codec.encode(options),
            )
        else:
            result = await self._core_collection.create_index_with_session(
                session.core_session,
                self._codec.encode(model.document),
                self._codec.encode(options),
            )

        return cast("CreateIndexResult", self._codec.decode(result))

    async def create_indexes(
        self,
        indexes: Sequence[IndexModel],
        session: ClientSession | None = None,
        **kwargs: Unpack[CreateIndexOptions],
    ) -> CreateIndexesResult:

        indexes = [self._codec.encode(idx.document) for idx in indexes]
        options = self._codec.encode(kwargs)

        if session is None:
            result = await self._core_collection.create_indexes(
                indexes,
                options,
            )
        else:
            result = await self._core_collection.create_indexes_with_session(
                session.core_session,
                indexes,
                options,
            )

        return cast("CreateIndexesResult", self._codec.decode(result))

    async def drop_index(
        self,
        name: str,
        session: ClientSession | None = None,
        **kwargs: Unpack[DropIndexOptions],
    ) -> None:

        options = self._codec.encode(kwargs)

        if session is None:
            await self._core_collection.drop_index(
                name,
                options,
            )
        else:
            await self._core_collection.drop_index_with_session(
                session.core_session,
                name,
                options,
            )

    async def drop_indexes(
        self,
        session: ClientSession | None = None,
        **kwargs: Unpack[DropIndexOptions],
    ) -> None:

        options = self._codec.encode(kwargs)

        if session is None:
            await self._core_collection.drop_indexes(
                options,
            )
        else:
            await self._core_collection.drop_indexes_with_session(
                session.core_session,
                options,
            )

    async def list_indexes(
        self,
        session: ClientSession | None = None,
        **kwargs: Unpack[ListIndexesOptions],
    ) -> list[IndexModelDef]:

        options = self._codec.encode(kwargs)

        if session is None:
            docs = await self._core_collection.list_indexes(
                options,
            )
        else:
            docs = await self._core_collection.list_indexes_with_session(
                session.core_session,
                options,
            )

        return [cast("IndexModelDef", self._codec.decode(doc)) for doc in docs]

    async def drop(
        self,
        session: ClientSession | None = None,
        **kwargs: Unpack[DropCollectionOptions],
    ) -> None:

        options = self._codec.encode(kwargs)

        if session is None:
            await self._core_collection.drop(
                options,
            )
        else:
            await self._core_collection.drop_with_session(
                session.core_session,
                options,
            )

    @property
    def read_preference(self) -> ReadPreference | None:
        data = self._core_collection.read_preference()
        return cast("ReadPreference | None", self._codec.decode(data))

    @property
    def write_concern(self) -> WriteConcern | None:
        data = self._core_collection.write_concern()
        return cast("WriteConcern | None", self._codec.decode(data))

    @property
    def read_concern(self) -> ReadConcern | None:
        data = self._core_collection.read_concern()
        return cast("ReadConcern | None", self._codec.decode(data))

    @property
    def name(self) -> str:
        return self._core_collection.name

    @property
    def full_name(self) -> str:
        return self._core_collection.full_name

    @property
    def database(self) -> Database:
        return self._database
