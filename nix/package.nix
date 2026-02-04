{
    stdenv,
    python3Packages,
    python313Packages,
    python313,
    uv,
    which,
    git,
}:
let version = "0.1.0";
in
 
python313Packages.buildPythonPackage {
  pname = "nix-vendor";
  inherit version;

  src = ../.;

  pyproject = true;

  nativeBuildInputs = with python313Packages; [
    setuptools
    wheel
  ];

  #buildInputs = [ git ];

  propagatedBuildInputs = with python313Packages; [
    click
    pydantic
    rich
  ] ++ [ git];

  pythonImportsCheck = [ "nix_vendor" ];

  meta = {
    description = "Vendoring tool abusing flakes";
    homepage = "https://github.com/TypicalFence/nix-vendor";
    license = "EUPL-1.2";
    maintainers = [ "fence"];
  };
}
