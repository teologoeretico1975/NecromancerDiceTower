$ErrorActionPreference = 'Stop'

$exports = @(
    @{ Svg = '01_Technical_Template/svg/sheet_01_body_a.svg'; Pdf = '01_Technical_Template/pdf/sheet_01_body_a.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_02_body_b.svg'; Pdf = '01_Technical_Template/pdf/sheet_02_body_b.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_03_ramps_ab.svg'; Pdf = '01_Technical_Template/pdf/sheet_03_ramps_ab.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_04_ramp_c.svg'; Pdf = '01_Technical_Template/pdf/sheet_04_ramp_c.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_05_base_tray.svg'; Pdf = '01_Technical_Template/pdf/sheet_05_base_tray.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_06_instructions.svg'; Pdf = '01_Technical_Template/pdf/sheet_06_instructions.pdf' },
    @{ Svg = '01_Technical_Template/svg/sheet_07_baffle_isometric.svg'; Pdf = '01_Technical_Template/pdf/sheet_07_baffle_isometric.pdf' }
)

$helper = Join-Path $PSScriptRoot 'export_svg_to_pdf.ps1'
if (-not (Test-Path $helper)) {
    throw "Missing helper script: $helper"
}

Write-Host 'Export All Technical SVGs to PDF'
foreach ($item in $exports) {
    Write-Host ("- Exporting {0}" -f $item.Svg)
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File $helper $item.Svg $item.Pdf
    if ($LASTEXITCODE -ne 0) {
        throw ("Export failed for: {0}" -f $item.Svg)
    }
}
Write-Host 'All technical sheets exported successfully.'
