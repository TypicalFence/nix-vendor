import os
import stat
import shutil
import json
from pathlib import Path
from enum import Enum
from pydantic import TypeAdapter
from . import nix
from ._process import run_command 
from .schema import VendorConfig, LockFile, LockItem, VendorInput


def find_vedor_nix():
    root = run_command("git", ["rev-parse", "--show-toplevel"])
    if root['exitCode'] != 0:
        raise RuntimeError("Not a git repository")
    else:
        return f"{root['stdout'].strip()}/vendor.nix"
    

def evaluate_vendor_file(vendor_file: str) -> VendorConfig:
    conf = nix.evaluate_file(vendor_file)
    ta = TypeAdapter(VendorConfig)
    return ta.validate_python(conf)


def load_lock_file(vendor_file: str) -> LockFile:
    lock_file_dir = Path(vendor_file).parent
    lock_file_path = f"{lock_file_dir}/vendor.lock"

    if not Path(lock_file_path).exists():
        return [] 

    lock_file_content = ""
    with open(lock_file_path, "r") as f:
        lock_file_content = f.read()

    ta = TypeAdapter(LockFile)
    return ta.validate_json(lock_file_content)

class PathValidation(Enum):
    VALID = "valid"
    INVALID = "invalid"
    MISSING = "missing"

def validate_lock_item(lock: LockItem) -> PathValidation:
    vendored_path = Path(lock['path'])
    if not vendored_path.exists():
        return PathValidation.MISSING
    
    path_hash = nix.hash_path(vendored_path)

    if path_hash == lock['hash']:
        return PathValidation.VALID
    else:
        return PathValidation.INVALID


def _make_writable(p: Path):
    st = os.stat(p, follow_symlinks=False)
    mode = st.st_mode
    if p.is_dir():
        mod = stat.S_IWUSR | stat.S_IXUSR | stat.S_IWGRP | stat.S_IXGRP
        os.chmod(p, mode | mod , follow_symlinks=False)
    else:
        mod = stat.S_IWUSR | stat.S_IWGRP
        os.chmod(p, mode | mod, follow_symlinks=False)


def _make_tree_writable(path: Path):
    for root, dirs, files in os.walk(path, followlinks=True):
        _make_writable(Path(root))

        for d in dirs:
            _make_writable(Path(root) / d)
        for f in files:
            _make_writable(Path(root) / f)


def vendor_dependency(name: str, input: VendorInput, lock: LockItem|None = None) -> LockItem:
    is_missing = True

    if lock is not None:
        validation = validate_lock_item(lock)
        if validation == PathValidation.VALID:
            print(f"{name} is up to date.")
            return lock
        elif validation == PathValidation.INVALID:
            print(f"{name} does not match it's lock, re-vendoring...")
            is_missing = False
        elif validation == PathValidation.MISSING:
            print(f"{name} is missing, vendoring...")

    prefetch = nix.prefetch_flake(input['url'])

    valid_hash = lock is None or lock['hash'] == prefetch['hash']
    if not valid_hash:
        print(f"Hash mismatch for {name}: expected {lock['hash']}, fetched {prefetch['hash']}")
        return None
    
    path = Path(input['path'])
    if not is_missing:
        os.rmdir(path)


    path.mkdir(parents=True, exist_ok=True)
    store_path = prefetch['storePath']

    # copy contents of store to path
    shutil.copytree(store_path, input['path'], dirs_exist_ok=True)
    _make_tree_writable(path)
    print(f"Vendored {name} to {input['path']}")
    return LockItem(
        name=name,
        path=input['path'],
        hash=prefetch['hash'],
    )


def vendor_dependencies(dir: Path, conf: VendorConfig, lock_file: LockFile) -> LockFile:
    fresh_locks = []

    for name, input in conf.items():
        print(f"Vendoring {name} from {input['url']} to {input['path']}")
        lock = next((item for item in lock_file if item['name'] == name), None)
        new_lock = vendor_dependency(name, input,  lock)
        fresh_locks.append(new_lock)
    
    print("Writing updated lock file...")
    lock_path = dir / "vendor.lock"
    with open(lock_path, "w") as f:
        f.write(json.dumps(fresh_locks, indent=4))

    return fresh_locks
    

def check_dependencies(dir: Path, conf: VendorConfig, lock_file: LockFile) -> bool:
    valid = True

    for name, input in conf.items():
        lock = next((item for item in lock_file if item['name'] == name), None)

        if lock is not None:
            validation = validate_lock_item(lock)
            print(f"{name}: Locked - {validation.value}")
            if validation != PathValidation.VALID:
                valid = False 
        else:
            if Path(input['path']).exists():
                hash = nix.hash_path(input['path'])
                print(f"{name}: Unlocked - {hash}")
            else:
                print(f"{name}: Unlocked - missing")

            valid = False

    return valid
    
        