# nix-vendor

Nix-vendor is a small tool which uses flakes for vendoring external dependencies and maintaining their integrity.

It can vendor any supported flake input.

Right now it is just a proof of concept, expect it to be broken.

## Configuration

Nix-vendor will attempt to find a `vendor.nix` file at the root of your current git repository, alternatively you can specify it with `--vendor-file`.

The `vendor.nix` should contain a set, but it is evaluated, meaning imports and function calls are possible.
```nix
{
    vim-nix.url = "github:TypicalFence/vim.nix";   
    vim-nix.path = "./vendor/vim";
    gettext = {
        url = "https://ftp.gnu.org/pub/gnu/gettext/gettext-1.0.tar.gz";
        path = "./vendor/gettext";
    };
}
```

## Usage
To vendor the dependecies use the `vendor` subcommand:
```bash
nix-vendor vendor
```
```
gettext is missing, vendoring...
Vendored gettext to ./vendor/gettext
Vendoring vim-nix from github:TypicalFence/vim.nix to ./vendor/vim
vim-nix is missing, vendoring...
Vendored vim-nix to ./vendor/vim
Writing updated lock file...
```

This will:
- fetch the dependencies to the store
- copy the dependencies from the store to the specified paths
- create a vendor.lock file.

To check the integrity of the vendored dependencies use the `check` subcommand:
```bash
nix-vendor check
```
```
gettext: Locked - valid
vim-nix: Locked - valid
All dependencies are valid.
```

To get an overview use the `show` subcommand:
```bash
nix-vendor show
```
```
/home/fence/nix-vendor/vendor.nix
├── gettext
│   ├── url: https://ftp.gnu.org/pub/gnu/gettext/gettext-1.0.tar.gz
│   ├── path: ./vendor/gettext
│   └── hash: 
│       ├── path: sha256-Uy+G3bG0SD7NZR4uRLf5NWhEhtOSY0ndQMr1WVXGnJk=
│       └── lock: sha256-Uy+G3bG0SD7NZR4uRLf5NWhEhtOSY0ndQMr1WVXGnJk=
└── vim-nix
    ├── url: github:TypicalFence/vim.nix
    ├── path: ./vendor/vim
    └── hash: 
        ├── path: sha256-/VqmiNdtTY2K9PbZlmLoVJml77/wnJJ9szg3NbHjSLw=
        └── lock: sha256-/VqmiNdtTY2K9PbZlmLoVJml77/wnJJ9szg3NbHjSLw=
```

## License

Licensed under the EUPL-1.2. See the LICENSE file. 