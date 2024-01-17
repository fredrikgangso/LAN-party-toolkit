# Router Speed Test Tool 🚀

The **Router Speed Test Tool** is a command-line utility written in Python that allows you to conduct speed tests for a router and log the results in a CSV file. This tool utilizes the `speedtest` module to measure download and upload speeds.

[back to readme](/README.md)

## Index 📑

- [Usage ⚙️](#usage)
- [Options 🛠️](#options)
- [Output 📊](#output)
- [Dependencies 🌐](#dependencies)

## Usage ⚙️

Execute the script by running the following command:

```bash
python scripts/routerSpeedTest.py [-r] [-v]
```

## Options 🛠️

- `-r, --router`: Specify the router number (default is "x").
- `-v, --verbose`: Enable verbose output for debugging.

## Output 📊

The tool will generate a CSV log file in the "archive/router-speed-test/YYYY-MM-DD/" directory, containing the router number, date, time, and speed test results. 📊

## Dependencies 🌐

- **speedtest-cli**: [https://pypi.org/project/speedtest-cli/](https://pypi.org/project/speedtest-cli/) 🌐
