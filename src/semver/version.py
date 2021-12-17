from dataclasses import dataclass
from typing import Optional

__all__ = [
    'Version'
]


@dataclass(repr=False, order=False, frozen=True)
class Version:
    """
    A version object which includes ordering and string representations of itself.
    """
    major: int
    minor: int
    patch: int

    tag: Optional[str] = None

    def __post_init__(self) -> None:
        if self.major == 0 and self.minor == 0 and self.patch == 0:
            raise ValueError('v0.0.0 is invalid')

        if self.major < 0:
            raise ValueError(f'Major value `{self.major}` is invalid')
        if self.minor < 0:
            raise ValueError(f'Minor value `{self.minor}` is invalid')
        if self.patch < 0:
            raise ValueError(f'Patch value `{self.patch}` is invalid')
        if self.tag == '':
            raise ValueError('Empty tag value is invalid')

    @classmethod
    def parse(cls, version: str) -> 'Version':
        """Parse version string into Version object."""
        if version[0] == 'v':
            version = version[1:]

        parts = version.split('.')

        if len(parts) < 3:
            raise ValueError(f'"{version}" is not a valid version')

        major, minor, patchAndTag = parts[0], parts[1], parts[2:]

        patchAndTag = '.'.join(patchAndTag)

        patchParts = patchAndTag.split('-')

        if len(patchParts) == 1:
            patch = patchParts[0]
            tag = None
        else:
            patch, tagParts = patchParts[0], patchParts[1:]
            tag = '-'.join(tagParts)

        try:
            major, minor, patch = int(major), int(minor), int(patch)
        except ValueError:
            raise ValueError(f'"{version}" is not a valid version')

        return cls(major, minor, patch, tag=tag)

    @property
    def string(self) -> str:
        if self.tag is not None:
            return f'{self.major}.{self.minor}.{self.patch}-{self.tag}'
        return f'{self.major}.{self.minor}.{self.patch}'

    @property
    def tuple(self):
        return self.major, self.minor, self.patch

    def __repr__(self) -> str:
        return self.string

    def __str__(self) -> str:
        return f'v{self.string}'

    def __lt__(self, other: 'Version') -> bool:
        if not isinstance(other, Version):
            raise TypeError('Other argument is not a version')
        return self.tuple < other.tuple

    def __le__(self, other: 'Version') -> bool:
        if not isinstance(other, Version):
            raise TypeError('Other argument is not a version')
        return self.tuple <= other.tuple

    def __gt__(self, other: 'Version') -> bool:
        if not isinstance(other, Version):
            raise TypeError('Other argument is not a version')
        return self.tuple > other.tuple

    def __ge__(self, other: 'Version') -> bool:
        if not isinstance(other, Version):
            raise TypeError('Other argument is not a version')
        return self.tuple >= other.tuple
