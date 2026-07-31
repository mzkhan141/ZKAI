"""Native .zk Binary Container Serialization & Integrity Verification Engine."""

import hashlib
import json
import struct
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from zkai.core.exceptions import SerializationError
from zkai.core.logger import get_logger

logger = get_logger("serialization")

# Header Magic Bytes & Binary Spec
MAGIC_BYTES = b"ZKAIMODEL"  # 9 bytes
VERSION = 1


@dataclass
class ZKHeader:
    """Header structure inside a native .zk file."""
    format_version: int = VERSION
    model_name: str = ""
    architecture: str = ""
    parameter_count: int = 0
    dtype: str = "float32"
    created_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class ZKSerializer:
    """Serialization engine for reading and writing native ZKAI binary container (.zk) files."""

    @staticmethod
    def write_zk_file(
        file_path: str,
        header: ZKHeader,
        tensor_payload: bytes,
        extra_data: Optional[bytes] = None,
    ) -> None:
        """Writes data into the indigenous .zk container format with compressed header and SHA256 checksum."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        header_dict = {
            "format_version": header.format_version,
            "model_name": header.model_name,
            "architecture": header.architecture,
            "parameter_count": header.parameter_count,
            "dtype": header.dtype,
            "created_at": header.created_at,
            "metadata": header.metadata,
        }
        header_json = json.dumps(header_dict).encode("utf-8")
        compressed_header = zlib.compress(header_json)

        header_length = len(compressed_header)
        tensor_length = len(tensor_payload)
        extra_length = len(extra_data) if extra_data else 0

        # Construct payload buffer
        payload = bytearray()
        payload.extend(MAGIC_BYTES)
        payload.extend(struct.pack("<I", header.format_version))  # uint32
        payload.extend(struct.pack("<Q", header_length))          # uint64
        payload.extend(struct.pack("<Q", tensor_length))          # uint64
        payload.extend(struct.pack("<Q", extra_length))           # uint64
        payload.extend(compressed_header)
        payload.extend(tensor_payload)
        if extra_data:
            payload.extend(extra_data)

        # Calculate SHA256 Checksum over payload
        checksum = hashlib.sha256(payload).digest()  # 32 bytes
        payload.extend(checksum)

        with open(path, "wb") as f:
            f.write(payload)

        logger.info(f"Successfully wrote native .zk artifact to {file_path} ({len(payload)} bytes)")

    @staticmethod
    def read_zk_file(file_path: str) -> Tuple[ZKHeader, bytes, bytes]:
        """Reads, verifies SHA256 checksum, and unpacks a .zk container file."""
        path = Path(file_path)
        if not path.exists():
            raise SerializationError(f"File not found: {file_path}")

        with open(path, "rb") as f:
            content = f.read()

        if len(content) < len(MAGIC_BYTES) + 28 + 32:
            raise SerializationError("Invalid .zk file: Buffer smaller than minimum header & checksum size")

        payload_part = content[:-32]
        stored_checksum = content[-32:]

        computed_checksum = hashlib.sha256(payload_part).digest()
        if computed_checksum != stored_checksum:
            raise SerializationError("Integrity Check Failed: SHA256 checksum mismatch in .zk file")

        # Unpack binary layout
        offset = 0
        magic = payload_part[: len(MAGIC_BYTES)]
        if magic != MAGIC_BYTES:
            raise SerializationError(f"Invalid magic bytes in container: {magic!r}")
        offset += len(MAGIC_BYTES)

        version, header_len, tensor_len, extra_len = struct.unpack("<IQQQ", payload_part[offset : offset + 28])
        offset += 28

        compressed_header = payload_part[offset : offset + header_len]
        offset += header_len
        tensor_payload = payload_part[offset : offset + tensor_len]
        offset += tensor_len
        extra_payload = payload_part[offset : offset + extra_len]

        header_json = zlib.decompress(compressed_header).decode("utf-8")
        header_dict = json.loads(header_json)

        header = ZKHeader(
            format_version=header_dict.get("format_version", version),
            model_name=header_dict.get("model_name", ""),
            architecture=header_dict.get("architecture", ""),
            parameter_count=header_dict.get("parameter_count", 0),
            dtype=header_dict.get("dtype", "float32"),
            created_at=header_dict.get("created_at", ""),
            metadata=header_dict.get("metadata", {}),
        )

        return header, tensor_payload, extra_payload
