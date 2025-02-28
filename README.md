[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/simplesecurity.svg?style=for-the-badge)](https://pypistats.org/packages/simplesecurity)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fsimplesecurity)](https://pepy.tech/project/simplesecurity)
[![PyPI Version](https://img.shields.io/pypi/v/simplesecurity.svg?style=for-the-badge)](https://pypi.org/project/simplesecurity)

<!-- omit in toc -->
# SimpleSecurity

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Combine multiple popular python security tools and generate reports or output
into different formats

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)

- bandit
- safety
- dodgy
- dlint
- semgrep

Formats

- ansi (for terminal)
- json
- markdown
- csv
- sarif

## Example Use

See below for the output if you run `simplesecurity` in this directory

<img src="readme-assets/screenshots/sec.svg" width="500px">

### Help

```txt
usage: __main__.py [-h] [--format FORMAT] [--plugin PLUGIN] [--file FILE] [--level LEVEL] [--confidence CONFIDENCE]
                   [--no-colour] [--high-contrast] [--fast] [--zero]

Combine multiple popular python security tools...

and generate reports or output into different formats.

optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT, -f FORMAT
                        Output format. One of ansi, json, markdown, csv. default=ansi
  --plugin PLUGIN, -p PLUGIN
                        Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, all, default=all
  --file FILE, -o FILE  Filename to write to (omit for stdout)
  --level LEVEL, -l LEVEL
                        Minimum level/ severity to show
  --confidence CONFIDENCE, -c CONFIDENCE
                        Minimum confidence to show
  --no-colour, -z       No ANSI colours
  --high-contrast, -Z   High contrast colours
  --fast, --skip        Skip long running jobs. Will omit plugins with long run time (applies to -p all only)
  --zero, -0            Return non zero exit code if any security vulnerabilities are found
```

You can also import this into your own project and use any of the functions
in the DOCS

<!-- omit in toc -->
## Table of Contents

- [Example Use](#example-use)
	- [Help](#help)
- [Developer Notes](#developer-notes)
	- [Generate semgrep_sec.yaml](#generate-semgrep_secyaml)
- [Documentation](#documentation)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Windows - Python.org](#windows---pythonorg)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
	- [Dnf](#dnf)
- [Install Python on MacOS](#install-python-on-macos)
	- [Homebrew](#homebrew)
	- [MacOS - Python.org](#macos---pythonorg)
- [How to run](#how-to-run)
	- [Windows](#windows)
	- [Linux/ MacOS](#linux-macos)
- [Download Project](#download-project)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)
	- [Support](#support)
	- [Rationale](#rationale)

## Developer Notes

### Generate semgrep_sec.yaml

1. Clone https://github.com/returntocorp/semgrep-rules
2. cd to `semgrep-rules/python`
3. do

   ```bash
   cat **/security/**/*.yaml >> semgrep_sec.yaml
   cat **/security/*.yaml >> semgrep_sec.yaml
   ```

4. Find and replace `rules:` with `` apart from the first instance
5. Reformat with `ctrl+shift+i`
6. replace simplesecurity/semgrep_sec.yaml with the new one

## Documentation

A high-level overview of how the documentation is organized organized will help you know
where to look for certain things:

<!--
- [Tutorials](/documentation/tutorials) take you by the hand through a series of steps to get
  started using the software. Start here if you’re new.
-->
- The [Technical Reference](/documentation/reference) documents APIs and other aspects of the
  machinery. This documentation describes how to use the classes and functions at a lower level
  and assume that you have a good high-level understanding of the software.
<!--
- The [Help](/documentation/help) guide provides a starting point and outlines common issues that you
  may have.
-->

## Install With PIP

**"Slim" Build:** Install bandit, dlint, dodgy, poetry, and safety with pipx

```python
pip install simplesecurity
```

**Otherwise:**

```python
pip install simplesecurity[full]
```

Head to https://pypi.org/project/SimpleSecurity/ for more info

## Language information

### Built for

This program has been written for Python versions 3.7 - 3.10 and has been tested with both 3.7 and
3.10

## Install Python on Windows

### Chocolatey

```powershell
choco install python
```

### Windows - Python.org

To install Python, go to https://www.python.org/downloads/windows/ and download the latest
version.

## Install Python on Linux

### Apt

```bash
sudo apt install python3.x
```

### Dnf

```bash
sudo dnf install python3.x
```

## Install Python on MacOS

### Homebrew

```bash
brew install python@3.x
```

### MacOS - Python.org

To install Python, go to https://www.python.org/downloads/macos/ and download the latest
version.

## How to run

### Windows

- Module
	`py -3.x -m [module]` or `[module]` (if module installs a script)

- File
	`py -3.x [file]` or `./[file]`

### Linux/ MacOS

- Module
	`python3.x -m [module]` or `[module]` (if module installs a script)

- File
	`python3.x [file]` or `./[file]`

## Download Project

### Clone

#### Using The Command Line

1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2

	```bash
	git clone https://github.com/FHPythonUtils/SimpleSecurity
	```

More information can be found at
https://help.github.com/en/articles/cloning-a-repository

#### Using GitHub Desktop

1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files

### Licence

MIT License
Copyright (c) FredHappyface
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog

See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct

Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md)
 for more information.

### Contributing

Contributions are welcome, please see the
[Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md)
for more information.

### Security

Thank you for improving the security of the project, please see the
[Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md)
for more information.

### Support

Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
[Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md)
for more information.

### Rationale

The rationale acts as a guide to various processes regarding projects such as
the versioning scheme and the programming styles used. Please see the
[Rationale](https://github.com/FHPythonUtils/.github/blob/master/RATIONALE.md)
for more information.
