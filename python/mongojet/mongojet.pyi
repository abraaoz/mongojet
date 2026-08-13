# ruff: noqa: A002, N818
# A002: `filter` mirrors the parameter name the Rust methods declare (src/collection.rs).
# N818: the exception names mirror PyMongo's own, which is the point of them.
#
# Type stubs for the compiled Rust extension module (src/lib.rs).
#
# Every document, pipeline, options mapping and result crosses this boundary as BSON
# `bytes`: the Python layer encodes with `Codec.encode` before the call and decodes the
# answer with `Codec.decode`. That is why nothing here is typed as a mapping.
#
# Arguments are required, matching pyo3 0.29, where an `Option<T>` parameter without an
# explicit `#[pyo3(signature = ...)]` still has to be passed (as `None`).

from typing import final

@final
class CoreClient:
    @property
    def default_database_name(self) -> str | None: ...
    def get_default_database(self) -> CoreDatabase | None: ...
    def get_database(self, name: str) -> CoreDatabase: ...
    def get_database_with_options(self, name: str, options: bytes) -> CoreDatabase: ...
    async def start_session(self, options: bytes | None) -> CoreSession: ...
    async def shutdown(self) -> None: ...
    async def shutdown_immediate(self) -> None: ...

@final
class CoreDatabase:
    @property
    def name(self) -> str: ...
    def get_collection(self, name: str) -> CoreCollection: ...
    def get_collection_with_options(
        self,
        name: str,
        options: bytes,
    ) -> CoreCollection: ...
    def gridfs_bucket(self, options: bytes | None) -> CoreGridFsBucket: ...
    def read_preference(self) -> bytes | None: ...
    def write_concern(self) -> bytes | None: ...
    def read_concern(self) -> bytes | None: ...
    async def create_collection(self, name: str, options: bytes | None) -> None: ...
    async def create_collection_with_session(
        self,
        session: CoreSession,
        name: str,
        options: bytes | None,
    ) -> None: ...
    async def list_collections(
        self,
        filter: bytes | None,
        options: bytes | None,
    ) -> list[bytes]: ...
    async def list_collections_with_session(
        self,
        session: CoreSession,
        filter: bytes | None,
        options: bytes | None,
    ) -> list[bytes]: ...
    async def run_command(self, command: bytes, options: bytes | None) -> bytes: ...
    async def run_command_with_session(
        self,
        session: CoreSession,
        command: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def aggregate(
        self,
        pipeline: list[bytes],
        options: bytes | None,
    ) -> CoreBatchCursor: ...
    async def aggregate_with_session(
        self,
        session: CoreSession,
        pipeline: list[bytes],
        options: bytes | None,
    ) -> CoreSessionBatchCursor: ...
    async def drop(self, options: bytes | None) -> None: ...
    async def drop_with_session(
        self,
        session: CoreSession,
        options: bytes | None,
    ) -> None: ...

@final
class CoreCollection:
    @property
    def name(self) -> str: ...
    @property
    def full_name(self) -> str: ...
    def read_preference(self) -> bytes | None: ...
    def write_concern(self) -> bytes | None: ...
    def read_concern(self) -> bytes | None: ...
    async def find_one(
        self,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_with_session(
        self,
        session: CoreSession,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_update(
        self,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_update_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_replace(
        self,
        filter: bytes,
        replacement: bytes,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_replace_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        replacement: bytes,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_delete(
        self,
        filter: bytes,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find_one_and_delete_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        options: bytes | None,
    ) -> bytes | None: ...
    async def find(
        self,
        filter: bytes | None,
        options: bytes | None,
    ) -> CoreBatchCursor: ...
    async def find_with_session(
        self,
        session: CoreSession,
        filter: bytes | None,
        options: bytes | None,
    ) -> CoreSessionBatchCursor: ...
    async def find_many(
        self,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes: ...
    async def find_many_with_session(
        self,
        session: CoreSession,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes: ...
    async def aggregate(
        self,
        pipeline: list[bytes],
        options: bytes | None,
    ) -> CoreBatchCursor: ...
    async def aggregate_with_session(
        self,
        session: CoreSession,
        pipeline: list[bytes],
        options: bytes | None,
    ) -> CoreSessionBatchCursor: ...
    async def distinct(
        self,
        field_name: str,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes: ...
    async def distinct_with_session(
        self,
        session: CoreSession,
        field_name: str,
        filter: bytes | None,
        options: bytes | None,
    ) -> bytes: ...
    async def update_one(
        self,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def update_one_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def update_many(
        self,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def update_many_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        update: bytes | list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def replace_one(
        self,
        filter: bytes,
        replacement: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def replace_one_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        replacement: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def insert_one(self, document: bytes, options: bytes | None) -> bytes: ...
    async def insert_one_with_session(
        self,
        session: CoreSession,
        document: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def insert_many(
        self,
        documents: list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def insert_many_with_session(
        self,
        session: CoreSession,
        documents: list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def delete_one(
        self,
        filter: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def delete_one_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def delete_many(
        self,
        filter: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def delete_many_with_session(
        self,
        session: CoreSession,
        filter: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def count_documents(
        self,
        filter: bytes | None,
        options: bytes | None,
    ) -> int: ...
    async def count_documents_with_session(
        self,
        session: CoreSession,
        filter: bytes | None,
        options: bytes | None,
    ) -> int: ...
    async def estimated_document_count(self, options: bytes | None) -> int: ...
    async def create_index(self, model: bytes, options: bytes | None) -> bytes: ...
    async def create_index_with_session(
        self,
        session: CoreSession,
        model: bytes,
        options: bytes | None,
    ) -> bytes: ...
    async def create_indexes(
        self,
        model: list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def create_indexes_with_session(
        self,
        session: CoreSession,
        model: list[bytes],
        options: bytes | None,
    ) -> bytes: ...
    async def drop_index(self, name: str, options: bytes | None) -> None: ...
    async def drop_index_with_session(
        self,
        session: CoreSession,
        name: str,
        options: bytes | None,
    ) -> None: ...
    async def drop_indexes(self, options: bytes | None) -> None: ...
    async def drop_indexes_with_session(
        self,
        session: CoreSession,
        options: bytes | None,
    ) -> None: ...
    async def list_indexes(self, options: bytes | None) -> list[bytes]: ...
    async def list_indexes_with_session(
        self,
        session: CoreSession,
        options: bytes | None,
    ) -> list[bytes]: ...
    async def drop(self, options: bytes | None) -> None: ...
    async def drop_with_session(
        self,
        session: CoreSession,
        options: bytes | None,
    ) -> None: ...

@final
class CoreBatchCursor:
    async def next_batch(self) -> bytes: ...
    async def collect(self) -> bytes: ...

@final
class CoreSessionBatchCursor:
    async def next_batch(self) -> bytes: ...
    async def collect(self) -> bytes: ...

@final
class CoreSession:
    async def start_transaction(self, options: bytes | None) -> None: ...
    async def commit_transaction(self) -> None: ...
    async def abort_transaction(self) -> None: ...

@final
class CoreGridFsBucket:
    async def put(
        self,
        data: bytes,
        options: bytes | None,
        metadata: bytes | None,
    ) -> bytes: ...
    async def get_by_id(self, options: bytes) -> bytes: ...
    async def get_by_name(self, options: bytes) -> bytes: ...
    async def delete(self, options: bytes) -> None: ...

async def core_create_client(url: str) -> CoreClient: ...

class PyMongoError(Exception): ...
class OperationFailure(PyMongoError): ...
class WriteError(OperationFailure): ...
class WriteConcernError(OperationFailure): ...
class DuplicateKeyError(WriteError): ...
class BsonSerializationError(PyMongoError): ...
class BsonDeserializationError(PyMongoError): ...
class ConnectionFailure(PyMongoError): ...
class ServerSelectionError(ConnectionFailure): ...
class ConfigurationError(PyMongoError): ...
class GridFSError(PyMongoError): ...
class NoFile(GridFSError): ...
class FileExists(GridFSError): ...
