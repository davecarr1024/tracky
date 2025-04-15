{pkgs}: {
  deps = [
    pkgs.watchexec
    pkgs.pyright
    pkgs.ruff
    pkgs.python312Packages.black
    pkgs.poethepoet
    pkgs.python312Packages.pytest
    pkgs.python312Packages.pytest-cov
    pkgs.python312Packages.pytest-subtests
  ];
}