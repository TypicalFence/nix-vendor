import os
import subprocess
from typing import TypedDict 
from collections.abc import Sequence

type Args = Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes]]

ProcessResult = TypedDict('ProcessResult', {'exitCode': int, 'stdout': str, 'stderr': str}) 

def run_command(bin: str, args: Args) -> ProcessResult:
    r = subprocess.run([
        bin,
        *args
    ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ProcessResult(exitCode=r.returncode, stdout=r.stdout, stderr=r.stderr)

