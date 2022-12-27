"""Add plugins here.

- bandit
- safety
- dodgy
- dlint
- semgrep
- trivy

Functions return finding dictionary

```json
{
    title: str
    description: str
    file: str
    evidence: list[Line]
    severity: Level
    confidence: Level
    line: int
    _other: dict[str, str]
}
```
"""
from __future__ import annotations

import platform
import subprocess
from json import loads
import os
from pathlib import Path
from typing import Any
import re

from simplesecurity.level import Level
from simplesecurity.types import Finding, Line

THISDIR = str(Path(__file__).resolve().parent)

EXCLUDED = [
    "./.env",
    "./tests",
    "./.venv",
    "./env/",
    "./venv/",
    "./ENV/",
    "./env.bak/",
    "./venv.bak/",
]


def _doSysExec(command: str, errorAsOut: bool = True) -> tuple[int, str]:
    """Execute a command and check for errors.

    Args:
                    command (str): commands as a string
                    errorAsOut (bool, optional): redirect errors to stdout

    Raises:
                    RuntimeWarning: throw a warning should there be a non exit code

    Returns:
                    tuple[int, str]: tuple of return code (int) and stdout (str)
    """
    with subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT if errorAsOut else subprocess.PIPE,
        encoding="utf-8",
        errors="ignore",
    ) as process:
        out = process.communicate()[0]
        exitCode = process.returncode
    return exitCode, out

def string_matches_in_file(file: str, pattern: str):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    with open(file, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if pattern in line:
                list_of_results.append(line_number)
    return list_of_results
def extractEvidence(LineNrOrWord: [int, str], file: str) -> list[Line]:
    """Grab evidence from the source file.

    Args:
            desiredLine (int): line to highlight
            file (str): file to extract evidence from

    Returns:
            list[Line]: list of lines
    """

    if type(LineNrOrWord) == str:
        line_nrs = string_matches_in_file(file=file, pattern=LineNrOrWord)

    elif type(LineNrOrWord) == int:
        line_nrs = [LineNrOrWord]

    for line_nr in line_nrs:
        with open(file, encoding="utf-8", errors="ignore") as fileContents:
            start = max(line_nr - 3, 0)
            for line in range(start):
                next(fileContents)
            content = []
            for line in range(start + 1, line_nr + 3):
                try:
                    lineContent = next(fileContents).rstrip().replace("\t", "    ")
                except StopIteration:
                    break
                content.append({"selected": line == line_nr, "line": line, "content": lineContent})
    return content


def bandit(scan_dir: str) -> list[Finding]:
    """Generate list of findings using bandit. requires bandit on the system path.

    Raises:
            RuntimeError: if bandit is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    if _doSysExec("bandit -h")[0] != 0:
        raise RuntimeError("bandit is not on the system path")
    findings = []
    levelMap = {
        "LOW": Level.LOW,
        "MEDIUM": Level.MED,
        "HIGH": Level.HIGH,
        "UNDEFINED": Level.UNKNOWN,
    }
    results = loads(
        _doSysExec(f"bandit -lirq -x {','.join(EXCLUDED)} -f json {scan_dir}", False)[1]
    )["results"]
    for result in results:
        file = result["filename"].replace("\\", "/")
        findings.append(
            {
                "id": result["test_id"],
                "title": f"{result['test_id']}: {result['test_name']}",
                "description": result["issue_text"],
                "file": file,
                "evidence": extractEvidence(result["line_number"], file),
                "severity": levelMap[result["issue_severity"]],
                "confidence": levelMap[result["issue_confidence"]],
                "line": result["line_number"],
                "_other": {
                    "more_info": result["more_info"],
                    "line_range": result["line_range"],
                },
            }
        )
    return findings


def _doSafetyProcessing(results: dict[str, Any]) -> list[Finding]:
    findings = []
    for result in results:
        findings.append(
            {
                "id": result[4],
                "title": f"{result[4]}: {result[0]}",
                "description": result[3],
                "file": "Project Requirements",
                "evidence": [
                    {
                        "selected": True,
                        "line": 0,
                        "content": f"{result[0]} version={result[2]} affects{result[1]}",
                    }
                ],
                "severity": Level.MED,
                "confidence": Level.HIGH,
                "line": "Unknown",
                "_other": {"id": result[4], "affected": result[1]},
            }
        )
    return findings


def _doPureSafety():
    if os.path.exists("requirements.txt"):
        safe = _doSysExec("safety check -r requirements.txt --json")[1]
    else:
        safe = _doSysExec("safety check --json")[1]
        if safe.startswith("Warning:"):
            raise RuntimeError("some error occurred: " + safe)
    return loads(safe)


def safety(scan_dir: str) -> list[Finding]:
    """Generate list of findings using safety.

    Raises:
            RuntimeError: if safety is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    if _doSysExec("safety --help")[0] != 0:
        raise RuntimeError("safety is not on the system path")
    # TODO Do we need to run poetry lock before commiting to poetry show? when using just venv it doesnt produce the poetry.lock file, which is required for scanning with poetry show.
    pShow = _doSysExec("poetry show")
    if not pShow[0]:
        lines = pShow[1].splitlines(False)
        data = []
        for line in lines:
            parts = line.replace("(!)", "").split()
            if len(parts) > 1:
                data.append(f"{parts[0]}=={parts[1]}")
            else:
                data.append(f"{parts[0]}")
        with open("reqs.txt", "w", encoding="utf-8", errors="ignore") as reqs:
            reqs.write("\n".join(data))
        results = loads(_doSysExec("safety check -r reqs.txt --json")[1])
        os.remove("reqs.txt")
    elif not _doSysExec("pipreqs --savepath reqs.txt --encoding utf-8")[0]:
        results = loads(_doSysExec("safety check -r reqs.txt --json")[1])
        os.remove("reqs.txt")
    else:
        # Use plain old safety (this will miss optional dependencies)
        results = _doPureSafety()
    return _doSafetyProcessing(results)


def dodgy(scan_dir: str) -> list[Finding]:
    """Generate list of findings using dodgy. Requires dodgy on the system path.

    Raises:
            RuntimeError: if dodgy is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    if _doSysExec("dodgy -h")[0] != 0:
        raise RuntimeError("dodgy is not on the system path")
    findings = []
    results = loads(_doSysExec(f"dodgy {scan_dir} -i {' '.join(EXCLUDED)}")[1])["warnings"]
    for result in results:
        file = "./" + result["path"].replace("\\", "/")
        findings.append(
            {
                "id": result["code"],
                "title": result["message"],
                "description": result["message"],
                "file": file,
                "evidence": extractEvidence(result["line"], file),
                "severity": Level.MED,
                "confidence": Level.MED,
                "line": result["line"],
                "_other": {},
            }
        )
    return findings


def dlint(scan_dir: str) -> list[Finding]:
    """Generate list of findings using dlint. Requires flake8 and dlint on the system path.

    Raises:
            RuntimeError: if flake8 is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    if _doSysExec("flake8 -h")[0] != 0:
        raise RuntimeError("flake8 is not on the system path")
    findings = []

    # Using codeclimate format instead of json as it supports serverity indicators
    results = _doSysExec(
        f"flake8 --select=DUO --exclude {','.join(EXCLUDED)} --format=codeclimate {scan_dir}"
    )[1].splitlines(False)
    json_results = loads(results[0])
    levelMap = {"info": Level.LOW, "minor": Level.MED, "major": Level.HIGH, "critical": Level.HIGH, "blocker": Level.HIGH}
    for path_of_file, scan_results in json_results.items():
        for scan_result in scan_results:
            findings.append(
                {
                    "id": scan_result["check_name"],
                    "title": f"{scan_result['check_name']}: {scan_result['description']}",
                    "description": f"{scan_result['check_name']}: {scan_result['description']}",
                    "file": path_of_file,
                    "evidence": extractEvidence(
                        scan_result["location"]["positions"]["begin"]["line"], path_of_file
                    ),
                    "severity": levelMap[scan_result["severity"]],
                    "confidence": Level.MED,
                    "line": scan_result["location"]["positions"]["begin"]["line"],
                    "_other": {
                        "col": scan_result["location"]["positions"]["begin"]["column"],
                        "start": scan_result["location"]["positions"]["begin"]["line"],
                        "end": scan_result["location"]["positions"]["end"]["line"],
                        "fingerprint": scan_result["fingerprint"],
                    },
                }
            )
    return findings


def semgrep(scan_dir: str) -> list[Finding]:
    """Generate list of findings using for semgrep. Requires semgrep on the
    system path (wsl in windows).

    Raises:
            RuntimeError: if semgrep is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    findings = []
    if platform.system() == "Windows":
        raise RuntimeError("semgrep is not supported on windows")
    if _doSysExec("semgrep --help")[0] != 0:
        raise RuntimeError("semgrep is not on the system path")
    sgExclude = ["--exclude {x}" for x in EXCLUDED]
    results = loads(
        _doSysExec(
            f"semgrep -f {THISDIR}/semgrep_sec.yaml {scan_dir} {' '.join(sgExclude)} "
            "-q --json --no-rewrite-rule-ids"
        )[1].strip()
    )["results"]
    levelMap = {"INFO": Level.LOW, "WARNING": Level.MED, "ERROR": Level.HIGH}
    for result in results:
        file = "./" + result["path"].replace("\\", "/")
        findings.append(
            {
                "id": result["check_id"],
                "title": result["check_id"].split(".")[-1],
                "description": result["extra"]["message"].strip(),
                "file": file,
                "evidence": extractEvidence(result["start"]["line"], file),
                "severity": levelMap[result["extra"]["severity"]],
                "confidence": Level.HIGH,
                "line": result["start"]["line"],
                "_other": {
                    "col": result["start"]["col"],
                    "start": result["start"],
                    "end": result["end"],
                    "extra": result["extra"],
                },
            }
        )
    return findings


def trivy(scan_dir: str) -> list[Finding]:
    """Generate list of findings using for semgrep. Requires semgrep on the
    system path (wsl in windows).

    Raises:
            RuntimeError: if semgrep is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    findings = []
    if platform.system() == "Windows":
        raise RuntimeError("trivy is not supported on windows")
    if _doSysExec("trivy --help")[0] != 0:
        raise RuntimeError("trivy is not on the system path")
    # sgExclude = ["--exclude {x}" for x in EXCLUDED]
    payload = loads(_doSysExec(f"trivy fs {scan_dir} " " --format json -q")[1].strip())

    levelMap = {
        "UNKNOWN": Level.UNKNOWN,
        "LOW": Level.LOW,
        "MEDIUM": Level.MED,
        "HIGH": Level.HIGH,
        "CRITICAL": Level.HIGH,
    }

    if "Results" in payload.keys():
        results = payload["Results"]
        for result in results:
            file = scan_dir + "/" + result["Target"].replace("\\", "/")
            # Title key is not always present in JSON, e.g. with secret scanning.
            if "Vulnerabilities" in result.keys():
                for vulnerability in result["Vulnerabilities"]:
                    # Title key is not always present in JSON
                    if "Title" in vulnerability.keys():
                        title = vulnerability["Title"]
                    else:
                        title = ""

                    if "PkgName" in vulnerability.keys():
                        evidence = extractEvidence(vulnerability["PkgName"], file)
                    else:
                        evidence = extractEvidence(0, file)
                    # Description contains a lot of additional new lines that are replaced with single new line.
                    simplified_description = vulnerability['Description'].replace('\n\n', '\n')
                    findings.append(
                        {
                            "id": vulnerability["VulnerabilityID"],
                            "title": f"{vulnerability['VulnerabilityID']} : {title}",
                            "description": f"{simplified_description} {vulnerability['PrimaryURL']}",
                            "file": file,
                            "evidence": evidence,
                            "severity": levelMap[vulnerability["Severity"]],
                            "confidence": Level.HIGH,
                            "line": 0,  # TODO, evaluate what to do when we do not have a line to address
                        }
                    )
            elif result['Class'] == "secret": # When dealing with secrets
                for secret in result["Secrets"]:
                    findings.append(
                        {
                            "id": secret["RuleID"],
                            "title": f"{secret['RuleID']} : {secret['Title']}",
                            "description": f"secrets issue",
                            "file": file,
                            "evidence": extractEvidence(secret["StartLine"], file),
                            "severity": levelMap[secret["Severity"]],
                            "confidence": Level.HIGH,
                            "line": secret["StartLine"],
                        }
                    )
            else:
                print("Unhandled type of class: ")
                print(result)
    else: # Handling no results.
        findings = []
    return findings
