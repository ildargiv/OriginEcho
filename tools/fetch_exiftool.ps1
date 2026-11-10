# Downloads the pinned ExifTool build into tools\exiftool and checks every file against
# tools\exiftool.sha256. Used by the GitHub build and by anyone running OriginEcho from source:
#
#   powershell -ExecutionPolicy Bypass -File tools\fetch_exiftool.ps1
#
# ExifTool is needed only for the full XMP/IPTC copy; without it OriginEcho copies EXIF + ICC.
$ErrorActionPreference = "Stop"
$Version = "13.59"
$Name = "exiftool-${Version}_64"
# SHA-256 of the zip itself, if known. Empty: only the per-file manifest is checked.
$ZipSha256 = ""
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dest = Join-Path $Here "exiftool"
$Manifest = Join-Path $Here "exiftool.sha256"
$Zip = Join-Path ([IO.Path]::GetTempPath()) "$Name.zip"
$Urls = @(
    "https://sourceforge.net/projects/exiftool/files/$Name.zip/download",
    "https://exiftool.org/$Name.zip"
)

function Test-Zip($path) {
    if (-not (Test-Path $path)) { return $false }
    $fs = [IO.File]::OpenRead($path)
    try { $b = New-Object byte[] 2; [void]$fs.Read($b, 0, 2) } finally { $fs.Close() }
    return ($b[0] -eq 0x50 -and $b[1] -eq 0x4B)      # "PK"
}

function Get-Sha256Bytes([byte[]]$bytes) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return -join ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) } finally { $sha.Dispose() }
}

$ok = $false
foreach ($u in $Urls) {
    Write-Host "Downloading $u"
    & curl.exe -L --fail --silent --show-error --retry 3 -A "OriginEcho-build" -o $Zip $u
    if ($LASTEXITCODE -eq 0 -and (Test-Zip $Zip)) { $ok = $true; break }
    Write-Host "  not available here, trying the next source"
}
if (-not $ok) { throw "Could not download $Name.zip" }

$zipHash = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLower()
Write-Host "zip sha256: $zipHash"
if ($ZipSha256 -and $zipHash -ne $ZipSha256.ToLower()) { throw "The zip does not match the pinned SHA-256" }

if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
New-Item -ItemType Directory -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest
$Root = Join-Path $Dest $Name
if (-not (Test-Path -LiteralPath (Join-Path $Root "exiftool(-k).exe"))) { throw "Unexpected layout inside $Name.zip" }
# The download ships "exiftool(-k).exe" (waits for a key press); the plain name runs without the pause.
Copy-Item -LiteralPath (Join-Path $Root "exiftool(-k).exe") -Destination (Join-Path $Root "exiftool.exe")

$bad = @(); $n = 0
foreach ($line in Get-Content $Manifest -Encoding UTF8) {
    if (-not $line.Trim()) { continue }
    $want = $line.Substring(0, 64); $rel = $line.Substring(66)
    $file = Join-Path $Dest ($rel -replace "/", "\")
    if (-not (Test-Path -LiteralPath $file)) { $bad += "missing: $rel"; continue }
    $bytes = [IO.File]::ReadAllBytes($file)
    $got = Get-Sha256Bytes $bytes
    if ($got -ne $want) {
        # The manifest was taken from a git checkout with LF line endings: compare text files without CR.
        $lf = New-Object System.Collections.Generic.List[byte] ($bytes.Length)
        for ($i = 0; $i -lt $bytes.Length; $i++) {
            if ($bytes[$i] -eq 13 -and $i + 1 -lt $bytes.Length -and $bytes[$i + 1] -eq 10) { continue }
            $lf.Add($bytes[$i])
        }
        if ((Get-Sha256Bytes $lf.ToArray()) -ne $want) { $bad += "changed: $rel" }
    }
    $n++
}
if ($bad.Count) { $bad | Select-Object -First 20 | ForEach-Object { Write-Host $_ }; throw "ExifTool check failed: $($bad.Count) file(s)" }
Write-Host "ExifTool $Version ready in $Root ($n files checked)"
