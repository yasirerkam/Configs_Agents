// Windows toast at main-session turn completion, and when the agent parks
// waiting on us (ask dialog, tool approval), only when the terminal is NOT the
// foreground window. Built-in completion.notify degrades to BEL on this
// terminal ("vscode" profile -> Notify: BEL; the native desktop fallback is
// Linux-only), so we raise WinRT toasts via PowerShell instead.
// Focus rule: walk the process ancestry to find the first windowed ancestor
// (the terminal) and toast only if it is not the foreground window.
// Fail-open: if no windowed ancestor is found, always toast.
//
// Why two wait events:
// - tool_call (toolName === "ask"): the ask tool blocks the turn until the
//   dialog is answered, so session_stop never fires while it waits.
// - tool_approval_requested: approval prompts park the same way; this fires
//   only when a call actually needs a decision.
export default function (pi) {
	let startedAt = 0;
	pi.on("agent_start", () => {
		startedAt = Date.now();
	});

	const toast = async (title, line2, line3) => {
		const t64 = Buffer.from(title, "utf8").toString("base64");
		const a64 = Buffer.from(line2, "utf8").toString("base64");
		const b64 = Buffer.from(line3, "utf8").toString("base64");
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
    $t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText04)
    $items = $t.GetElementsByTagName('text')
    $items.Item(0).InnerText = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${t64}'))
    $items.Item(1).InnerText = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${a64}'))
    $items.Item(2).InnerText = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${b64}'))
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($t))
  } catch { }
}`;
		await pi.exec("powershell", ["-NoProfile", "-NonInteractive", "-EncodedCommand", Buffer.from(ps, "utf16le").toString("base64")], {
			signal: AbortSignal.timeout(5000),
		});
	};

	// Model opened a choice dialog (ask tool): the turn cannot finish until
	// the user answers, so announce it immediately.
	pi.on("tool_call", async (event, ctx) => {
		if (!ctx?.hasUI) return; // headless runs: no toast
		if (event?.toolName !== "ask") return;
		const q = event?.input?.questions?.[0]?.question;
		const detail = String(typeof q === "string" && q.trim() ? q : "(soru metni yok)").split("\n")[0].trim();
		await toast("OMP — ASK?", "seçim bekleniyor", detail.slice(0, 120));
	});

	// A tool needs permission: same parking, announce with the tool name.
	pi.on("tool_approval_requested", async (event, ctx) => {
		if (!ctx?.hasUI) return; // headless runs: no toast
		const tool = String(event?.toolName ?? "").trim() || "tool";
		await toast("OMP — APPROVAL?", "onay bekleniyor", tool.slice(0, 120));
	});

	pi.on("session_stop", async (event, ctx) => {
		if (event.stop_hook_active) return; // continuation-loop guard
		if (!ctx.hasUI) return; // headless runs: no toast
		const sessionName = ctx.sessionManager?.getSessionName?.() || "omp";
		const secs = startedAt ? Math.max(1, Math.round((Date.now() - startedAt) / 1000)) : 0;
		const lastMsg =
			event.last_assistant_message?.role === "assistant"
				? event.last_assistant_message
				: undefined;
		const isError = lastMsg?.stopReason === "error";
		const title = isError ? "OMP — ERROR!" : "OMP — DONE!";
		// First text line of the final assistant message, capped for toast width.
		const text = (lastMsg?.content ?? [])
			.filter((b) => b?.type === "text" && typeof b.text === "string")
			.map((b) => b.text.split("\n")[0].trim())
			.find(Boolean);
		const fallback = isError ? String(lastMsg?.errorMessage ?? "").trim() : "";
		const detail = (text || fallback) || "(detay yok)";
		const line2 = `${sessionName}${secs ? ` — ${secs}sn` : ""}`;
		const line3 = detail.slice(0, 120);
		await toast(title, line2, line3);
	});
}
