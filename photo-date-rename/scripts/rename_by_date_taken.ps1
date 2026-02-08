param(
  [Parameter(Mandatory=$true)][string]$Path,
  [string]$PreviewCsv = (Join-Path $Path 'rename_preview_date_taken_only.csv'),
  [string]$Format = 'yyyy.MM.dd_HHmmss'
)

$shell = New-Object -ComObject Shell.Application
$folder = $shell.NameSpace($Path)
$idx = 12 # 拍摄日期
$imgExt = '.jpg','.jpeg','.png','.heic','.gif','.bmp','.tif','.tiff','.webp'
$files = Get-ChildItem -LiteralPath $Path -File | Where-Object { $imgExt -contains $_.Extension.ToLower() }
$used = @{}
$rows = foreach ($f in $files) {
  $dtRaw = $folder.GetDetailsOf($folder.ParseName($f.Name), $idx)
  if (-not $dtRaw) { continue }
  $m = [regex]::Match($dtRaw, '(\d{4})\D+(\d{1,2})\D+(\d{1,2})\D+(\d{1,2})\D+(\d{2})')
  if (-not $m.Success) { continue }
  $year  = [int]$m.Groups[1].Value
  $month = [int]$m.Groups[2].Value
  $day   = [int]$m.Groups[3].Value
  $hour  = [int]$m.Groups[4].Value
  $min   = [int]$m.Groups[5].Value
  $dt = Get-Date -Year $year -Month $month -Day $day -Hour $hour -Minute $min -Second 0
  $base = $dt.ToString($Format)
  $newName = $base + $f.Extension.ToLower()
  $n = 1
  while ($used.ContainsKey($newName) -or (Test-Path -LiteralPath (Join-Path $Path $newName))) {
    $newName = '{0}_{1:00}{2}' -f $base, $n, $f.Extension.ToLower()
    $n++
  }
  $used[$newName] = $true
  [pscustomobject]@{ OldName = $f.Name; NewName = $newName; DateTakenRaw = $dtRaw; DateTaken = $dt }
}
$rows | Sort-Object OldName | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $PreviewCsv
foreach ($r in $rows) {
  $oldPath = Join-Path $Path $r.OldName
  $newPath = Join-Path $Path $r.NewName
  if (Test-Path -LiteralPath $oldPath) {
    Move-Item -LiteralPath $oldPath -Destination $newPath
  }
}
