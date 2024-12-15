{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-linux"
      ];
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.graphviz
              pkgs.fish
              pkgs.just
              pkgs.git
            ];
            buildInputs = with pkgs.python3Packages; [
              networkx
              pygraphviz
              matplotlib
            ];
            shellHook = ''
              fish
            '';
          };
        }
      );
    };
}
