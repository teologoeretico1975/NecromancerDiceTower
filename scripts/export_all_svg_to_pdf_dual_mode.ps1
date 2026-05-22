# Export all SVG files (Standard and Beginner modes) to PDF
$svgDir = "D:\repos\NecromancerDiceTower\01_Technical_Template\svg"
$pdfDir = "D:\repos\NecromancerDiceTower\01_Technical_Template\pdf"

$svgFiles = @(
    "sheet_01_body_a.svg",
    "sheet_02_body_b.svg", 
    "sheet_03_ramps_ab.svg",
    "sheet_04_ramp_c.svg",
    "sheet_05_base_tray.svg",
    "sheet_01_body_a_beginner.svg",
    "sheet_02_body_b_beginner.svg",
    "sheet_03_ramps_ab_beginner.svg",
    "sheet_04_ramp_c_beginner.svg",
    "sheet_05_base_tray_beginner.svg"
)

Write-Host "Exporting all SVG files (Standard and Beginner modes) to PDF..."
Write-Host ""

foreach ($svgFile in $svgFiles) {
    $svgPath = Join-Path $svgDir $svgFile
    $pdfFile = $svgFile -replace "\.svg$", ".pdf"
    $pdfPath = Join-Path $pdfDir $pdfFile
    
    if (Test-Path $svgPath) {
        Write-Host "Exporting: $svgFile -> $pdfFile"
        & inkscape $svgPath --export-type=pdf "--export-filename=$pdfPath"
    } else {
        Write-Host "WARNING: File not found: $svgFile"
    }
}

Write-Host ""
Write-Host "All exports completed!"
