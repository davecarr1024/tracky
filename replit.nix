{pkgs}: {
  deps = [
    pkgs.portmidi
    pkgs.pkg-config
    pkgs.libpng
    pkgs.libjpeg
    pkgs.freetype
    pkgs.fontconfig
    pkgs.SDL2_ttf
    pkgs.SDL2_mixer
    pkgs.SDL2_image
    pkgs.SDL2
    pkgs.python312Packages.docformatter
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