# KiKit - Automation for KiCAD

KiKit is a Python library and CLI tool to automate several tasks in a standard
KiCAD workflow like:

- panelization of the boards (see [examples](doc/examples.md))
- exporting manufacturing data
- building board presentation pages (see [an example presentation page generated
  by KiKit](https://roboticsbrno.github.io/RB0002-BatteryPack))

![KiKit Promo](https://github.com/yaqwsx/KiKit/blob/master/doc/resources/promo.jpg?raw=true)

## Do You Enjoy KiKit?

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E2181LU)

## Installation

KiKit is available as a [PyPi package](https://pypi.org/project/KiKit/), therefore, you can install it via pip:

```
pip3 install kikit
```

If you would like to test the upstream version (which can have more features
implemented but is not guaranteed to be fully tested), you can install it via:

```
pip3 install git+https://github.com/yaqwsx/KiKit@master
```

Note that if you have a stable version installed, you need to add `--force` to
upgrade it to upstream.

## Why Should I Use It?

Everything KiKit does, can also be done via Pcbnew in KiCAD. However, you have
to do it manually. One of the common scenarios is the creation of panels. Most
of the tutorials on the internet guide you to use the "append board"
functionality of Pcbnew. However, this approach is labour-intensive, error-prone
and whenever, you change the board, you have to do it again.

With KiKit you just call a CLI command if you have a simple layout (e.g., a
grid) or write few Python instructions like "place board here", "add bridge
here", "separate boards via mouse bites/v-cuts" and you are done. The process is
repeatable and actually much simpler than hand-drawing the panels. KiKit also
allows you to easily export all the Gerbers in a single step.

You can then write a Makefile and simply call `make` to get all your
manufacturing data and board presentation pages.


See [BatteryPack](https://github.com/RoboticsBrno/RB0002-BatteryPack) as an
example usage of KiKit. Also see [an example presentation page generated by
KiKit](https://roboticsbrno.github.io/RB0002-BatteryPack).

## Feature List

- create panels by appending boards and pieces of substrate (bridges)
- supports board with arbitrary shapes
- easily create mouse-bites/V-CUTS
- compared to hand-creation of panels, your panels will pass DRC (as tracks from
  different instances of the same board have distinct nets when using KiKit)
- if you have multiple boards in a single file, you can split them
- automated export of gerber files
- [3D printed self-registering solder paste stencils](doc/stencil.md)
- [steel stencils with alignment jig](doc/stencil.md)

## How To Use It?

Read the [CLI documentation](doc/cli.md) and the [panelize
documentation](doc/panelization.md). Also don't miss the
[examples](doc/examples.md). If you are interested in generating solder paste
stencils, see [Stencil documentation](doc/stencil.md)

## KiKit Is Broken or Does Not Work as Expected

Please, first check [FAQ](doc/faq.md). If you have not found answer for your
problem there, feel free to open an issue on GitHub.

## How To Use It CI?

To use KiKit in CI (e.g., Travis) you can use prepared Docker image
`yaqwsx/kikit`. Also see [example `.travis.yml`](https://github.com/RoboticsBrno/RB0002-BatteryPack/blob/master/.travis.yml).