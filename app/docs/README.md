# Documentation Guide

## Adding Additional Sources

To add additional sources to the documentation in the same way as Controllers and Routes, run the following command in this folder:

```sh
sphinx-apidoc -o source/controllers ../controllers
```

## Clearing Previously Generated Documentation

To clear previously generated documentation, run:

```sh
make clean
```

## Building the HTML Documentation

To build the new HTML documentation, run:

```sh
make html
```

