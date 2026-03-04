# PowerShell script to download EEA Industrial Emissions data files

$baseUrl = "https://sdi.eea.europa.eu/datashare/s/6wrowetdF5ByE8X/download?path=%2FCSV&files="
$outputDir = "C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\downloaded_data"

# Create output directory if it doesn't exist
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force
}

# List of all CSV files to download
$files = @(
    "F1_1_Total Releases at National Level into Air.csv",
    "F1_2_Total Release at E-PRTR Sector Level into Air.csv",
    "F1_3_Total Release at E-PRTR Annex I Activity into Air.csv",
    "F1_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Air.csv",
    "F2_1_Total Releases at National Level into Water.csv",
    "F2_2_Total Release at E-PRTR Sector Level into Water.csv",
    "F2_3_Total Release at E-PRTR Annex I Activity into Water.csv",
    "F2_4_Detailed releases at facility level with E-PRTR Sector and Annex I Activity detail into Water.csv",
    "F3_1_Total pollutant transfer.csv",
    "F3_2_Detailed pollutant transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F4_1_Total waste transfer.csv",
    "F4_2_Detailed waste transfer at facility level with E-PRTR Sector and Annex I Activity.csv",
    "F5_1_Total emissions and energy input from LCP at national level.csv",
    "F5_2_Detailed emissions and energy input from LCP.csv",
    "F6_1_Total Information on Installations.csv",
    "F7_1_Detailed information on WI and co-WI.csv"
)

Write-Host "Starting download of $($files.Count) CSV files..." -ForegroundColor Green
Write-Host "Output directory: $outputDir" -ForegroundColor Cyan
Write-Host ("-" * 80)

$successCount = 0
$failCount = 0

foreach ($file in $files) {
    try {
        $encodedFile = [System.Uri]::EscapeDataString($file)
        $downloadUrl = $baseUrl + $encodedFile
        $outputPath = Join-Path $outputDir $file
        
        Write-Host "`nDownloading: $file" -ForegroundColor Yellow
        
        # Download the file
        Invoke-WebRequest -Uri $downloadUrl -OutFile $outputPath -UseBasicParsing
        
        # Check if file was created and get size
        if (Test-Path $outputPath) {
            $fileSize = (Get-Item $outputPath).Length
            Write-Host "  SUCCESS - Downloaded $([math]::Round($fileSize/1MB, 2)) MB" -ForegroundColor Green
            $successCount++
        }
    }
    catch {
        Write-Host "  FAILED - $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
    }
}

Write-Host "`n$("=" * 80)" -ForegroundColor Cyan
Write-Host "Download Complete!" -ForegroundColor Green
Write-Host "  Successful: $successCount files" -ForegroundColor Green
Write-Host "  Failed: $failCount files" -ForegroundColor Red
Write-Host "`nFiles saved to: $outputDir" -ForegroundColor Cyan
