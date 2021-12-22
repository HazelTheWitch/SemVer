from dataclasses import dataclass
from typing import Optional
from re import compile

__all__ = [
    'Version'
]


VERSION_REGEX = compile(r'^v?(\d+)\.(\d+)\.(\d+)(?:-(.+))?$')


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
        match = VERSION_REGEX.match(version)

        if match is None:
            raise ValueError(f'Invalid version "{version}"')

        groups = match.groups()

        major = int(groups[0])
        minor = int(groups[1])
        patch = int(groups[2])
        tag = groups[3]

        if major == minor == patch == 0:
            raise ValueError(f'"{version}" is invalid')

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
