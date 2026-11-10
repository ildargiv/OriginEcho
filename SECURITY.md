# Security policy

## Supported versions

Only the [latest release](https://github.com/ildargiv/OriginEcho/releases/latest) receives fixes.

## Reporting a vulnerability

Please do not open a public issue for a security problem.

Report it privately: the **Security** tab of this repository, then **Report a vulnerability**
(<https://github.com/ildargiv/OriginEcho/security/advisories/new>).

Include the version, the operating system, what you did and what happened. A proof of concept helps, a fix is not required. You can expect a first answer within a week.

## What is in scope

- Photos and metadata that make the program run code, or write or delete files outside the chosen folders.
- The MCP server (`tools/mcp_server.py`): tool calls that reach files the user did not point it to.
- The bundled ExifTool: the build downloads a pinned version and checks every file against `tools/exiftool.sha256`; a way around that check is in scope.

OriginEcho works offline and sends nothing to the network.

## Checking a download

Releases are built by GitHub Actions from this repository ([build workflow](.github/workflows/build.yml)). Starting with the release after v1.1.0, each release carries `SHA256SUMS.txt`. To check a file in PowerShell:

```powershell
(Get-FileHash .\OriginEcho-Setup-<version>.exe -Algorithm SHA256).Hash
```

and compare the result with the line for that file. GitHub also shows a SHA-256 digest next to each release file. The executables are not code-signed, so Windows SmartScreen may warn on first start.
