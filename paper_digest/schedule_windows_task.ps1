param(
    [string]$TaskName = "PaperDigestDaily",
    [string]$Time = "08:00"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = (Get-Command python).Source
$Action = New-ScheduledTaskAction -Execute $Python -Argument "-m paper_digest --config `"$ScriptDir\config.example.json`"" -WorkingDirectory $ScriptDir
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Force
