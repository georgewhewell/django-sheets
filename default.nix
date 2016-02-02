with import <nixpkgs> {}; {
  pyEnv = stdenv.mkDerivation {
    name = "py";
    buildInputs = [
    stdenv
    mercurial
    pypy
    python26
    python27Packages.virtualenv
    python32
    python33
    python34
    python35
  ];
 };
}
