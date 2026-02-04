import sys
import click
from rich.tree import Tree
from rich import print
from pathlib import Path
from . import nix
from . import vendoring

@click.group()
@click.option('--vendor-file', type=click.Path(exists=True, dir_okay=False), default=None,
              help='Path to the vendor.nix file.')
@click.pass_context
def cli(ctx, vendor_file) -> None:
    """Flake based code vendoring."""
    ctx.ensure_object(dict)
    ctx.obj['vendor_file'] = vendor_file


@cli.command()
@click.pass_context
def vendor(ctx):
    """Vendors the configured dependencies."""
    vendor_file = ctx.obj['vendor_file'] or vendoring.find_vedor_nix()
    dir = Path(vendor_file).parent
    config = vendoring.evaluate_vendor_file(vendor_file)
    lock = vendoring.load_lock_file(vendor_file)

    vendoring.vendor_dependencies(dir, config, lock)

@cli.command()
@click.pass_context
def check(ctx):
    """Checks the vendored dependencies."""
    vendor_file = ctx.obj['vendor_file'] or vendoring.find_vedor_nix()
    dir = Path(vendor_file).parent
    config = vendoring.evaluate_vendor_file(vendor_file)
    lock = vendoring.load_lock_file(vendor_file)

    valid = vendoring.check_dependencies(dir, config, lock)
    if valid:
        print("All dependencies are valid.")
        sys.exit(0) 
    

    print("Some dependencies are missing or invalid.")
    sys.exit(1)



@cli.command()
@click.pass_context
def show(ctx) -> None:
    vendor_file = ctx.obj['vendor_file'] or vendoring.find_vedor_nix()
    dir = Path(vendor_file).parent
    config = vendoring.evaluate_vendor_file(vendor_file)
    lock_file = vendoring.load_lock_file(vendor_file)

    tree = Tree(f"[bold]{vendor_file}[/bold]")

    for name, input in config.items():
        lock = next((item for item in lock_file if item['name'] == name), None)

        item = tree.add(f"[bold]{name}[/bold]")

        item.add(f"[bold]url:[/bold] {input['url']}")
        item.add(f"[bold]path:[/bold] {input['path']}")

        hash = item.add(f"[bold]hash:[/bold] ")

        if Path(dir / input['path']).exists():
            hash.add(f"[bold]path:[/bold] {nix.hash_path(lock['path'])}")
        else:
            hash.add(f"[bold]path:[/bold] Missing")

        if lock is not None:
            hash.add(f"[bold]lock:[/bold] {lock['hash']}")
        else:
            hash.add(f"[bold]lock:[/bold] None")

    
    print(tree)



if __name__ == '__main__':
    cli()
