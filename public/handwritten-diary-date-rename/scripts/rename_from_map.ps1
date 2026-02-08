param(
    [Parameter(Mandatory = $true)]
    [string]$Csv,
    [string]$Path = "."
)

if (-not (Test-Path -LiteralPath $Csv)) {
    throw "CSV not found: $Csv"
}

$knownExts = @(
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".webp"
)

$rows = Import-Csv -LiteralPath $Csv
foreach ($row in $rows) {
    $old = $row.old
    $new = $row.new

    if (-not $old -or -not $new) {
        Write-Warning "Skip row with empty old/new: $($row | ConvertTo-Json -Compress)"
        continue
    }

    $oldPath = Join-Path $Path $old
    if (-not (Test-Path -LiteralPath $oldPath)) {
        Write-Warning "Missing file: $oldPath"
        continue
    }

    $ext = [IO.Path]::GetExtension($oldPath)
    $newName = $new
    $newExt = [IO.Path]::GetExtension($newName)
    $hasKnownExt = $false
    if ($newExt) {
        $hasKnownExt = $knownExts -contains $newExt.ToLower()
    }

    if (-not $hasKnownExt) {
        $newName = $newName + $ext
    }

    $destPath = Join-Path $Path $newName
    if ($oldPath -ieq $destPath) {
        Write-Host "No change: $old"
        continue
    }

    if (Test-Path -LiteralPath $destPath) {
        $base = [IO.Path]::GetFileNameWithoutExtension($destPath)
        $destExt = [IO.Path]::GetExtension($destPath)
        $i = 1
        do {
            $candidate = Join-Path $Path ("{0}_{1:00}{2}" -f $base, $i, $destExt)
            $i++
        } while (Test-Path -LiteralPath $candidate)
        $destPath = $candidate
    }

    $destName = [IO.Path]::GetFileName($destPath)
    Rename-Item -LiteralPath $oldPath -NewName $destName
    Write-Host "Renamed: $old -> $destName"
}
