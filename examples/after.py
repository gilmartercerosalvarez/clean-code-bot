"""
Example of a plausible refactor for ``before.py``.

The live CLI output may differ; this file illustrates the intended direction:
clear names, small functions, typed API, and docstrings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, MutableMapping


class Operation(str, Enum):
    """Supported binary operations for the tiny calculator."""

    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"


def apply_operation(left: float, right: float, operation: Operation) -> float:
    """Apply ``operation`` to ``left`` and ``right``."""
    if operation is Operation.ADD:
        return left + right
    if operation is Operation.SUB:
        return left - right
    if operation is Operation.MUL:
        return left * right
    if operation is Operation.DIV:
        return left / right
    raise ValueError(f"Unsupported operation: {operation!r}")


@dataclass
class KeyValueStore:
    """Minimal string-keyed store for non-numeric items."""

    _data: MutableMapping[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any | None:
        """Return the value for ``key`` if present."""
        return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        """Associate ``value`` with ``key``."""
        self._data[key] = value

    def as_mapping(self) -> Mapping[str, Any]:
        """Return an immutable view of the underlying mapping."""
        return dict(self._data)


def process_mixed_items(
    items: list[Any],
    operation: Operation,
    *,
    numeric_operand: float = 2.0,
) -> tuple[list[float], KeyValueStore]:
    """
    For each numeric item, combine it with ``numeric_operand`` using ``operation``.

    Non-numeric items are stored in a ``KeyValueStore`` keyed by their string form.
    """
    results: list[float] = []
    store = KeyValueStore()
    for item in items:
        if isinstance(item, (int, float)):
            results.append(apply_operation(float(item), numeric_operand, operation))
        else:
            store.set(str(item), item)
    return results, store


if __name__ == "__main__":
    processed = process_mixed_items([1, 2, "x"], Operation.ADD)
    print(processed)
