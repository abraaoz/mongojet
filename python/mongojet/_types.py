from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import IntEnum
from typing import (
    Any,
    Literal,
    Optional,
    TypedDict,
    Union,
)

try:
    from typing import Required
except ImportError:
    from typing_extensions import Required

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

Document = dict[str, Any]

ReadConcernLevel = Literal[
    "local",
    "majority",
    "linearizable",
    "available",
    "snapshot",
]

ReadPreferenceMode = Literal[
    "primary",
    "secondary",
    "primaryPreferred",
    "secondaryPreferred",
    "nearest",
]


class ReadConcern(TypedDict):
    level: ReadConcernLevel


class WriteConcern(TypedDict, total=False):
    w: int | Literal["majority"] | None
    wtimeout: int | None
    j: bool | None


class HedgedReadOptions(TypedDict):
    enabled: bool


class ReadPreference(TypedDict, total=False):
    mode: Required[ReadPreferenceMode]
    tagSets: Sequence[Mapping[str, Any]] | None
    maxStalenessSeconds: int | None
    hedge: HedgedReadOptions | None


class DatabaseOptions(TypedDict, total=False):
    read_concern: ReadConcern | None
    write_concern: WriteConcern | None
    read_preference: ReadPreference | None


class CollectionOptions(TypedDict, total=False):
    read_concern: ReadConcern | None
    write_concern: WriteConcern | None
    read_preference: ReadPreference | None


CursorType = Literal[
    "tailable",
    "nonTailable",
    "tailableAwait",
]


class CollationStrength(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    TERTIARY = 3
    QUATERNARY = 4
    IDENTICAL = 5


CollationCaseFirst = Literal["upper", "lower", "off"]
CollationAlternate = Literal["non-ignorable", "shifted"]
CollationMaxVariable = Literal["punct", "space"]


class Collation(TypedDict, total=False):
    locale: str
    strength: CollationStrength | None
    caseLevel: bool | None
    caseFirst: CollationCaseFirst | None
    numericOrdering: bool | None
    alternate: CollationAlternate | None
    maxVariable: CollationMaxVariable | None
    normalization: bool | None
    backwards: bool | None


class FindOptions(TypedDict, total=False):
    sort: Document | None
    projection: Document | None
    skip: int | None
    limit: int | None
    cursor_type: CursorType | None
    no_cursor_timeout: bool | None
    allow_partial_results: bool | None
    batch_size: int | None
    max_time_ms: int | None
    allow_disk_use: bool | None
    max: Document | None
    min: Document | None
    hint: str | Document | None
    collation: Collation | None
    comment: str | Document | None
    max_await_time_ms: int | None
    max_scan: int | None
    read_concern: ReadConcern | None
    read_preference: ReadPreference | None
    return_key: bool | None
    show_record_id: bool | None
    let: Document | None


class FindOneOptions(TypedDict, total=False):
    sort: Document | None
    projection: Document | None
    skip: int | None
    allow_partial_results: bool | None
    max_time_ms: int | None
    max: Document | None
    min: Document | None
    hint: str | Document | None
    collation: Collation | None
    comment: str | Document | None
    max_scan: int | None
    read_concern: ReadConcern | None
    read_preference: ReadPreference | None
    return_key: bool | None
    show_record_id: bool | None
    let: Document | None


class FindOneAndUpdateOptions(TypedDict, total=False):
    sort: Document | None
    projection: Document | None
    upsert: bool | None
    return_document: Literal["after", "before"] | None
    array_filters: Sequence[Document] | None
    hint: str | Document | None
    collation: Collation | None
    bypass_document_validation: bool | None
    max_time_ms: int | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class FindOneAndReplaceOptions(TypedDict, total=False):
    sort: Document | None
    projection: Document | None
    upsert: bool | None
    return_document: Literal["after", "before"] | None
    hint: str | Document | None
    collation: Collation | None
    bypass_document_validation: bool | None
    max_time_ms: int | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class FindOneAndDeleteOptions(TypedDict, total=False):
    sort: Document | None
    projection: Document | None
    hint: str | Document | None
    collation: Collation | None
    max_time_ms: int | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class AggregateOptions(TypedDict, total=False):
    bypass_document_validation: bool | None
    batch_size: int | None
    max_time_ms: int | None
    allow_disk_use: bool | None
    hint: str | Document | None
    collation: Collation | None
    comment: str | Document | None
    max_await_time_ms: int | None
    read_concern: ReadConcern | None
    read_preference: ReadPreference | None
    write_concern: WriteConcern | None
    let: Document | None


class UpdateOptions(TypedDict, total=False):
    upsert: bool | None
    bypass_document_validation: bool | None
    collation: Collation | None
    array_filters: Sequence[Document] | None
    hint: str | Document | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class ReplaceOptions(TypedDict, total=False):
    upsert: bool | None
    bypass_document_validation: bool | None
    collation: Collation | None
    hint: str | Document | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class InsertOneOptions(TypedDict, total=False):
    bypass_document_validation: bool | None
    write_concern: WriteConcern | None
    comment: Any | None


class InsertManyOptions(TypedDict, total=False):
    ordered: bool | None
    bypass_document_validation: bool | None
    write_concern: WriteConcern | None
    comment: Any | None


class DeleteOptions(TypedDict, total=False):
    collation: Collation | None
    hint: str | Document | None
    write_concern: WriteConcern | None
    let: Document | None
    comment: Any | None


class CountOptions(TypedDict, total=False):
    skip: int | None
    limit: int | None
    max_time_ms: int | None
    hint: str | Document | None
    collation: Collation | None
    read_preference: ReadPreference | None
    read_concern: ReadConcern | None
    comment: Any | None


class EstimatedCountOptions(TypedDict, total=False):
    max_time_ms: int | None
    read_preference: ReadPreference | None
    read_concern: ReadConcern | None
    comment: Any | None


class DistinctOptions(TypedDict, total=False):
    max_time_ms: int | None
    read_preference: ReadPreference | None
    read_concern: ReadConcern | None
    collation: Collation | None
    comment: Any | None


class TransactionOptions(TypedDict, total=False):
    read_concern: ReadConcern | None
    write_concern: WriteConcern | None
    read_preference: ReadPreference | None
    max_commit_time_ms: int | None


class SessionOptions(TypedDict, total=False):
    causal_consistency: bool | None
    default_transaction_options: TransactionOptions | None
    snapshot: bool | None


class UpdateResult(TypedDict):
    matched_count: int
    modified_count: int
    upserted_id: Any


class InsertOneResult(TypedDict):
    inserted_id: Any


class InsertManyResult(TypedDict):
    inserted_ids: Sequence[Any]


class DeleteResult(TypedDict):
    deleted_count: int


CommitQuorum = Union[
    Literal["votingMembers", "majority"],  # noqa: PYI051
    str,  # replica set tag name
    int,  # nodes
]


class CreateIndexOptions(TypedDict, total=False):
    maxTimeMS: int | None
    comment: Any | None  # Document | str
    writeConcern: WriteConcern | None
    commitQuorum: CommitQuorum | None


class DropIndexOptions(TypedDict, total=False):
    maxTimeMS: int | None
    comment: Any | None  # Document | str
    writeConcern: WriteConcern | None


class ListIndexesOptions(TypedDict, total=False):
    maxTimeMS: int | None
    comment: Any | None  # Document | str
    batchSize: int | None


class IndexKeysDef(TypedDict):
    key: Document


IndexOptionsDef = TypedDict(
    "IndexOptionsDef",
    {
        "name": Optional[str],
        "unique": Optional[bool],
        "background": Optional[bool],
        "expireAfterSeconds": Optional[int],
        "sparse": Optional[bool],
        "storageEngine": Optional[Document],
        "v": Optional[int],
        "default_language": Optional[str],
        "language_override": Optional[str],
        "textIndexVersion": Optional[int],
        "weights": Optional[Document],
        "sphere2dIndexVersion": Optional[int],
        "2dsphereIndexVersion": Optional[int],
        "bits": Optional[int],
        "min": Optional[int],
        "max": Optional[int],
        "bucketSize": Optional[int],
        "partialFilterExpression": Optional[Document],
        "collation": Optional[Collation],
        "wildcardProjection": Optional[Document],
        "hidden": Optional[bool],
        "clustered": Optional[bool],
    },
    total=False,
)


class IndexModelDef(IndexKeysDef, IndexOptionsDef):
    pass


class CreateIndexArgs(IndexOptionsDef, CreateIndexOptions):
    pass


class CreateIndexResult(TypedDict):
    index_name: str


class CreateIndexesResult(TypedDict):
    index_names: Sequence[str]


IndexList = Union[
    Sequence[Union[str, tuple[str, Union[int, str, Mapping[str, Any]]]]],
    Mapping[str, Any],
]
Sort = IndexList

IndexKeys = Union[str, IndexList]


class IndexModel:
    __slots__ = ("__document",)

    def __init__(self, keys: IndexKeys, **kwargs: Unpack[IndexOptionsDef]) -> None:
        from ._helpers import create_index_model  # noqa: PLC0415

        self.__document = create_index_model(keys, **kwargs)

    @property
    def document(self) -> IndexModelDef:
        return self.__document


class DropCollectionOptions(TypedDict, total=False):
    write_concern: WriteConcern | None


class IndexOptionDefaults(TypedDict):
    storageEngine: Document


class TimeseriesOptions(TypedDict, total=False):
    timeField: str
    metaField: str | None
    granularity: Literal["seconds", "minutes", "hours"] | None
    bucketMaxSpanSeconds: int | None
    bucketRoundingSeconds: int | None


class ChangeStreamPreAndPostImages(TypedDict):
    enabled: bool


class ClusteredIndex(TypedDict, total=False):
    key: Document
    unique: bool
    name: str | None
    v: int | None  # currently must be 2 if provided.


class CreateCollectionOptions(TypedDict, total=False):
    capped: bool | None
    size: int | None
    max: int | None
    storageEngine: Document | None
    validator: Document | None
    validationLevel: Literal["off", "strict", "moderate"] | None
    validationAction: Literal["error", "warn"] | None
    viewOn: str | None
    pipeline: Sequence[Document] | None
    collation: Collation | None
    writeConcern: WriteConcern | None
    indexOptionDefaults: IndexOptionDefaults | None
    timeseries: TimeseriesOptions | None
    expireAfterSeconds: int | None
    changeStreamPreAndPostImages: ChangeStreamPreAndPostImages | None
    clusteredIndex: ClusteredIndex | None
    comment: Any | None


class ListCollectionsOptions(TypedDict, total=False):
    batchSize: int | None
    comment: Any | None


class CollectionSpecification(TypedDict, total=False):
    name: str
    type: Literal["collection", "view", "timeseries"]
    options: CreateCollectionOptions
    info: dict
    idIndex: Document | None


class RunCommandOptions(TypedDict, total=False):
    read_preference: ReadPreference | None


class GridFsBucketOptions(TypedDict, total=False):
    bucket_name: str | None
    chunk_size_bytes: int | None
    write_concern: WriteConcern | None
    read_concern: ReadConcern | None
    read_preference: ReadPreference | None


class GridFsPutResult(TypedDict, total=False):
    file_id: Any


class DropDatabaseOptions(TypedDict, total=False):
    write_concern: WriteConcern | None
