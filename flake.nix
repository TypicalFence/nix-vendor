{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: 
   let
    systems = [
      "x86_64-linux"
      "aarch64-linux"
      "i686-linux"
    ];
    eachSystem = nixpkgs.lib.genAttrs systems;   
    in
  {
    repl = import ./nix/repl.nix { 
      flake = self; 
      pkgs = nixpkgs.legacyPackages.${builtins.currentSystem}; 
      packages = self.packages.${builtins.currentSystem};
    }; 

    packages = eachSystem (system: 
      let 
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        nix-vendored = pkgs.callPackage ./nix/package.nix {
        };
        default = self.packages.${system}.nix-vendored;
      }
    );
  };
}
