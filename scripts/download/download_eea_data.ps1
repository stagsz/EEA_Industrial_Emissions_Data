# PowerShell script to download EEA Industrial Emissions Data
# Target directory
$outputDir = "C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\downloaded_data"

# Base URL for downloads
$baseUrl = "https://sdi.eea.europa.eu/datashare/s/6wrowetdF5ByE8X/download?path=%2FCSV&files="

# List of files to download
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

Write-Host "Starting download of EEA Industrial Emissions Data..." -ForegroundColor Cyan
Write-Host "Output directory: $outputDir" -ForegroundColor Green
Write-Host ("=" * 80)

$successCount = 0
$failCount = 0

foreach ($file in $files) {
    $encodedFile = [System.Web.HttpUtility]::UrlEncode($file)
    $url = $baseUrl + $encodedFile
    $outputPath = Join-Path $outputDir $file
    
    Write-Host ""
    Write-Host "Downloading: $file" -ForegroundColor Yellow
    Write-Host "URL: $url" -ForegroundColor Gray
    
    try {
        # Use Invoke-WebRequest with session handling
        Invoke-WebRequest -Uri $url -OutFile $outputPath -UseBasicParsing
        
        if (Test-Path $outputPath) {
            $fileSize = (Get-Item $outputPath).Length
            $fileSizeMB = [math]::Round($fileSize/1MB, 2)
            Write-Host "Success - Downloaded $fileSizeMB MB" -ForegroundColor Green
            $successCount++
        }
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host ("=" * 80)
Write-Host "Download Summary:" -ForegroundColor Cyan
Write-Host "  Successful: $successCount files" -ForegroundColor Green
Write-Host "  Failed: $failCount files" -ForegroundColor Red
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray
