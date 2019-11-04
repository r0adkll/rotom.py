# rotom.py

This script is meant to help bridge the gap between pokemontcg.io's API data and data dumped from other sources.

This is very much a **WIP** and will continue to be iterated and automated upon to better streamline the data pipeline.

## Usage

```shell script
Usage:
    rotom.py transform <source> <destination> [-c FILE] [-o OUTPUT] [--diffOnly]
    rotom.py images <set_code>
    rotom.py (-h | --help)
    rotom.py --version
    
Options:
    --diffOnly    Output only the difference between files
    -o --output   The output file to dump the transformed json into
    -c --config   Specify a custom config
    -h --help     Show this screen.
    --version     Show version.
```

## Contributing

Please follow the guidelines set forth in the [CONTRIBUTING](CONTRIBUTING.md) document.

## License

GNU General Public License v3.0

See [LICENSE](LICENSE) to see the full text.
