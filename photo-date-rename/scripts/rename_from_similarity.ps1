param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][string]$Csv,
  [string]$Format = 'yyyy.MM.dd_HHmmss',
  [string]$LogCsv = (Join-Path $Path 'rename_from_similarity_log.csv')
)

$rows = Import-Csv -LiteralPath $Csv
$used = @{}
$renamed = @()
foreach ($r in $rows) {
  $oldPath = Join-Path $Path $r.Target
  if (-not (Test-Path -LiteralPath $oldPath)) { continue }
  $ext = [IO.Path]::GetExtension($r.Target).ToLower()
  $dt = Get-Date -Year $r.Year -Month $r.Month -Day $r.Day -Hour $r.Hour -Minute $r.Minute -Second 0
  $base = $dt.ToString($Format)
  $newName = $base + $ext
  $n = 1
  while ($used.ContainsKey($newName) -or (Test-Path -LiteralPath (Join-Path $Path $newName))) {
    $newName = '{0}_{1:00}{2}' -f $base, $n, $ext
    $n++
  }
  $used[$newName] = $true
  $newPath = Join-Path $Path $newName
  Move-Item -LiteralPath $oldPath -Destination $newPath
  $renamed += [pscustomobject]@{ OldName = $r.Target; NewName = $newName; Match = $r.Match; Score = $r.Score }
}
$renamed | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $LogCsv
