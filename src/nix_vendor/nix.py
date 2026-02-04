from ._process import run_command, Args
from .schema import parse_json, FlakePrefetch

NIX_BIN = "nix"

def run_nix(args: Args):
    return run_command(NIX_BIN, args)


def prefetch_flake(flake: str) -> str:
    result = run_nix(["flake", "prefetch", "--json", flake])
    if result['exitCode'] != 0:
        print(result['stderr'])
        raise RuntimeError(f"nix flake prefetch failed: {result['stderr']}")

    return parse_json(FlakePrefetch, result['stdout'])


def evaluate_file(file: str) -> dict:
    result = run_nix(["eval", "--json", '--file', file])
    if result['exitCode'] != 0:
        print(result['stderr'])
        raise RuntimeError(f"nix eval failed: {result['stderr']}")

    return parse_json(dict, result['stdout'])


def hash_path(path: str) -> str:
    result = run_nix(["hash", "path", path])
    if result['exitCode'] != 0:
        print(result['stderr'])
        raise RuntimeError(f"nix hash path failed: {result['stderr']}")

    return result['stdout'].strip()