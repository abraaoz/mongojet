from __future__ import annotations

from collections.abc import Mapping
from typing import Any, overload

import bson
from bson import CodecOptions


class Codec:
    def __init__(self, options: CodecOptions) -> None:
        self._options = options

    @overload
    def encode(
        self,
        doc: Mapping[str, Any],
        optional: bool = True,  # noqa: FBT001, FBT002
    ) -> bytes: ...

    @overload
    def encode(
        self,
        doc: None,
        optional: bool = True,  # noqa: FBT001, FBT002
    ) -> None: ...

    def encode(
        self,
        doc: Mapping[str, Any] | None,
        optional: bool = True,  # noqa: FBT001, FBT002
    ) -> bytes | None:
        if doc is None:
            return None

        # if optional and doc=={}
        if optional and not doc:
            return None

        # return bson.BSON.encode(doc, codec_options=self._options)
        return bson.encode(doc, codec_options=self._options)

    @overload
    def decode(self, data: bytes) -> dict[str, Any]: ...

    @overload
    def decode(self, data: None) -> None: ...

    def decode(self, data: bytes | None) -> dict[str, Any] | None:
        if data is None:
            return None

        # doc = bson.BSON(data).decode(codec_options=self._options)
        doc = bson.decode(data, codec_options=self._options)

        return doc
