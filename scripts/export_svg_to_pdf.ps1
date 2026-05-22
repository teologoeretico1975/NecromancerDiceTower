param(
    [Parameter(Mandatory = $true)]
    [string]$SvgPath,

    [Parameter(Mandatory = $true)]
    [string]$PdfPath
)

function Resolve-WorkspacePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathValue,
        [switch]$MustExist
    )

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        $full = $PathValue
    }
    else {
        $repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
        $full = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $PathValue))
    }

    if ($MustExist -and -not (Test-Path $full)) {
        throw "Path not found: $full"
    }

    return $full
}

$svgFullPath = Resolve-WorkspacePath -PathValue $SvgPath -MustExist
$pdfFullPath = Resolve-WorkspacePath -PathValue $PdfPath

$pdfDir = Split-Path -Parent $pdfFullPath
if (-not (Test-Path $pdfDir)) {
    New-Item -ItemType Directory -Path $pdfDir -Force | Out-Null
}

$tempPdfPath = Join-Path $pdfDir ("__export_tmp_{0}.pdf" -f [System.Guid]::NewGuid().ToString('N'))

$inkscape = (Get-Command inkscape -ErrorAction SilentlyContinue).Source
if (-not $inkscape) {
    $fallback = 'C:\Program Files\Inkscape\inkscape.com'
    if (Test-Path $fallback) {
        $inkscape = $fallback
    }
}

if (-not $inkscape) {
    $fallback = 'C:\Program Files\Inkscape\inkscape.exe'
    if (Test-Path $fallback) {
        $inkscape = $fallback
    }
}

if (-not $inkscape) {
    Write-Error 'Inkscape non trovato. Installa Inkscape o aggiungilo al PATH.'
    exit 1
}

$helpText = (& $inkscape --help 2>$null | Out-String)
$supportsModernCli = $helpText -match '--export-type'

if ($supportsModernCli) {
    & $inkscape $svgFullPath '--export-type=pdf' "--export-filename=$tempPdfPath"
}
else {
    & $inkscape $svgFullPath -A $tempPdfPath
}

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not (Test-Path $tempPdfPath)) {
    Write-Error "Export fallito: PDF temporaneo non creato ($tempPdfPath)."
    exit 1
}

try {
    Move-Item -Path $tempPdfPath -Destination $pdfFullPath -Force
}
catch {
    if (Test-Path $tempPdfPath) {
        Remove-Item $tempPdfPath -Force -ErrorAction SilentlyContinue
    }
    Write-Error "Export fallito durante la scrittura finale ($pdfFullPath): $($_.Exception.Message)"
    exit 1
}
