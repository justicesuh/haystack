from typing import Any

from bs4.element import Tag


class NullableTag:
    """Chainable wrapper around Tag."""

    def __init__(self, tag: Tag | None) -> None:
        self._tag = tag

    def unwrap(self) -> Tag | None:
        """Return internal Tag object."""
        return self._tag

    def find(
        self,
        name: Any = None,
        attrs: dict[str, Any] | None = None,
        recursive: bool = True,
        string: Any = str,
        **kwargs: Any
    ) -> 'NullableTag':
        """Chainable `find()`."""
        if self._tag is None:
            return NullableTag(None)
        return NullableTag(self._tag.find(name=name, attrs=attrs, recursive=recursive, string=string, **kwargs))

    def text(self, strip: bool = False) -> str | None:
        """Chainable `get_text()`."""
        if self._tag is None:
            return None
        return self._tag.get_text(strip=strip)

    def __bool__(self) -> bool:
        """Return if internal Tag is not None."""
        return self._tag is not None
