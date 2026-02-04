from typing import Union, TypedDict, Literal, TypeVar, Mapping, List
from pydantic import TypeAdapter

# nix flake prefetch schema
FlakeGithubRef = TypedDict('FlakeGithubRef', {
    "owner": str,
    "repo": str,
    "type": Literal['github'],
})
FlakeGithubRefLocked = TypedDict('FlakeGithubRefLocked ', {
    "lastModified": int,
    "owner": str,
    'repo': str,
    'rev': str,
    'type': Literal['github'],
})
FlakeTarBallRef = TypedDict('FlakeTarBallRef', {
    "url": str,
    "type": Literal['tarball'],
})
FlakeTarballRefLocked = TypedDict('FlakeTarballRefLocked', {
    "lastModified": int,
    "url": str,
    "narHash": str,
    "type": Literal['tarball'],
})
LockedFlakeRef = Union[FlakeGithubRefLocked, FlakeTarballRefLocked]
FlakeRef = Union[FlakeGithubRef, FlakeTarBallRef]

FlakePrefetch = TypedDict('FlakePrefetch', {
    "hash": str,
    "storePath": str,
    "locked": LockedFlakeRef,
    "original": FlakeRef,
})

# venodor.nix
VendorInput = TypedDict('VendorInput', {
    "url": str,
    "path": str,
})

VendorConfig = Mapping[str, VendorInput]

# vendor.lock
LockItem = TypedDict('LockItem', {
    'hash': str,
    'path': str,
    'name': str,
})
LockFile = List[LockItem]

# parsing

T = TypeVar('T')

def parse_json(type: T, json_str: str) -> T:
    ta = TypeAdapter(type)
    return ta.validate_json(json_str)

