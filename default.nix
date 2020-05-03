{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  name = "mandla.me";
  buildInputs = [];
  src = if builtins.pathExists(./source.nix) then
          builtins.fetchGit {
            url="git://github.com/lunamystry/mandla.me";
            rev=import ./source.nix;
          }
        else
          ./.;
  buildPhase = "";
  installPhase = "cp -a index $out";
}
