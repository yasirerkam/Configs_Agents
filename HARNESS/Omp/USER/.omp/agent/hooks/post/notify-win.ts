// Windows toast at main-session turn completion, only when the terminal is
// NOT the foreground window. Built-in completion.notify degrades to BEL on
// this terminal ("vscode" profile -> Notify: BEL; the native desktop fallback
// is Linux-only), so we raise a WinRT toast via PowerShell instead.
// Focus rule: walk the process ancestry to find the first windowed ancestor
// (the terminal) and toast only if it is not the foreground window.
// Fail-open: if no windowed ancestor is found, always toast.
export default function (pi) {
	pi.on("session_stop", async (event, ctx) => {
		if (event.stop_hook_active) return; // continuation-loop guard
		if (!ctx.hasUI) return; // headless runs: no toast
		const ps = `
$show = $true
try {
  $term = [IntPtr]::Zero
  $cur = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
  for ($i = 0; $i -lt 12 -and $cur; $i++) {
    $pr = Get-Process -Id $cur.ProcessId
    if ($pr -and $pr.MainWindowHandle -ne 0) { $term = $pr.MainWindowHandle; break }
    if (-not $cur.ParentProcessId) { break }
    $cur = Get-CimInstance Win32_Process -Filter "ProcessId=$($cur.ParentProcessId)"
  }
  Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class W { [DllImport("user32.dll", EntryPoint = "GetForegroundWindow")] public static extern IntPtr GetFG(); }'
  if (-not ('W' -as [type])) { throw 'W type missing' }
  if ($term -ne [IntPtr]::Zero) { $show = ([W]::GetFG() -ne $term) }
} catch { $show = $true } # fail-open: focus unknown -> toast
if ($show) {
  [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
  try {
    $app = (Get-StartApps | Where-Object { $_.AppID -match '[Pp]owerShell' } | Select-Object -First 1).AppID
    if (-not $app) { $app = 'Microsoft.Windows.PowerShell' }
    $t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $items = $t.GetElementsByTagName('text')
    $items.Item(0).InnerText = 'OMP'
    $items.Item(1).InnerText = 'İş tamamlandı'
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($t))
  } catch { }
}`;
		await pi.exec("powershell", ["-NoProfile", "-NonInteractive", "-EncodedCommand", Buffer.from(ps, "utf16le").toString("base64")], {
			signal: AbortSignal.timeout(5000),
		});
	});
}
