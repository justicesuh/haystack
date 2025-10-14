from typing import Any
from urllib.parse import urljoin, urlparse

from bs4.element import Tag


def remove_query(url: str | None) -> str | None:
    """Remove query string from url."""
    if url is None:
        return None
    return urljoin(url, urlparse(url).path)


class NullableTag:
    """Chainable wrapper around Tag."""

    def __init__(self, tag: Tag | None, raise_exc: bool = True) -> None:
        self._tag = tag
        self._raise_exc = raise_exc
        self._error_msg = 'NullableTag is None'

    def unwrap(self) -> Tag | None:
        """Return internal Tag object."""
        return self._tag

    def find(
        self,
        name: Any = None,
        attrs: dict[str, Any] | None = None,
        recursive: bool = True,
        string: Any = None,
        **kwargs: Any,
    ) -> 'NullableTag':
        """Chainable `find()`."""
        if self._tag is None:
            if self._raise_exc:
                raise ValueError(self._error_msg)
            return NullableTag(None)
        return NullableTag(self._tag.find(name=name, attrs=attrs, recursive=recursive, string=string, **kwargs))

    def get(self, key: str, default: Any = None) -> str | None:
        """Chainable `get()`."""
        if self._tag is None:
            if self._raise_exc:
                raise ValueError(self._error_msg)
            return None
        attr = self._tag.get(key, default)
        if isinstance(attr, list):
            return ','.join(attr)
        return attr

    def text(self, strip: bool = True) -> str | None:
        """Chainable `get_text()`."""
        if self._tag is None:
            if self._raise_exc:
                raise ValueError(self._error_msg)
            return None
        return self._tag.get_text(strip=strip)

    def decode_contents(self, *args: Any, **kwargs: Any) -> str:
        """Return inner html of Tag."""
        if self._tag is None:
            if self._raise_exc:
                raise ValueError(self._error_msg)
            return ''
        return self._tag.decode_contents(*args, **kwargs)

    def __bool__(self) -> bool:
        """Return if internal Tag is not None."""
        return self._tag is not None

    def __str__(self) -> str:
        """Return string representation."""
        if self._tag is None:
            return ''
        return str(self._tag)
