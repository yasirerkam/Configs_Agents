// Windows toast at main-session turn completion, and when the agent parks
// waiting on us (ask dialog, tool approval), only when the terminal is NOT the
// foreground window. Built-in completion.notify degrades to BEL on this
// terminal ("vscode" profile -> Notify: BEL; the native desktop fallback is
// Linux-only), so we raise WinRT toasts via PowerShell instead.
// Focus rule: walk the process ancestry to find the first windowed ancestor
// (the terminal) and toast only if it is not the foreground window.
// Fail-open: if no windowed ancestor is found, always toast.
//
// Non-win32 (this ssh server: notify-send absent, no DISPLAY, no notification
// daemon): only tool approval is signalled here — a terminal BEL, because the
// built-in attention bell already rings once for turn completion AND once when
// the ask dialog opens (measured on this terminal), so belling there too would
// double-ring. notify-send runs first, so a real desktop gets a compositor
// notification instead of a bell.
//
// Why two wait events:
// - tool_call (toolName === "ask"): the ask tool blocks the turn until the
//   dialog is answered, so session_stop never fires while it waits.
// - tool_approval_requested: approval prompts park the same way; this fires
//   only when a call actually needs a decision.
import { platform } from "node:os";
import process from "node:process";
export default function (pi) {
	let startedAt = 0;
	pi.on("agent_start", () => {
		startedAt = Date.now();
	});

	// Linux/ssh: no desktop notification service here, and the built-in bell
	// already covers turn completion and ask dialogs, so the BEL fallback is
	// requested only for the one park event left silent (tool approval).
	const toast = async (title, line2, line3, { bell = false } = {}) => {
		if (platform() !== "win32") {
			if (!bell) return; // covered by the built-in bell
			// Same target as omp's built-in Linux fallback; no focus guard,
			// compositor notifications are non-intrusive there.
			try {
				const res = await pi.exec("notify-send", [
					"-a", "OMP",
					"-u", "normal",
					"-t", "5000",
					`${title} — ${line2}`,
					line3,
				], { signal: AbortSignal.timeout(5000) });
				if (res?.code === 0) return;
			} catch { /* notify-send yok -> BEL */ }
			// A bell only means something on a terminal: writing it into a piped
			// stdout (RPC JSONL, redirected output) injects stray bytes into the
			// stream, and no terminal is there to ring.
			if (!process.stdout.isTTY) return;
			// Son çare: BEL — terminal (ör. VS Code "vscode" profili) zili kendi ayarına göre gösterir.
			try { process.stdout.write("\u0007"); } catch { }
			return;
		}
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
	// the user answers, so announce it immediately. Non-win32 relies on the
	// built-in bell the dialog itself rings; win32 still raises the toast.
	pi.on("tool_call", async (event, ctx) => {
		if (!ctx?.hasUI) return; // headless runs: no toast
		if (event?.toolName !== "ask") return;
		const q = event?.input?.questions?.[0]?.question;
		const detail = String(typeof q === "string" && q.trim() ? q : "(soru metni yok)").split("\n")[0].trim();
		await toast("OMP — ASK?", "Seçim bekleniyor!", detail.slice(0, 120));
	});

	// A tool needs permission: same parking, announce with the tool name.
	// This is the only park event the built-in bell does not cover.
	pi.on("tool_approval_requested", async (event, ctx) => {
		if (!ctx?.hasUI) return; // headless runs: no toast
		const tool = String(event?.toolName ?? "").trim() || "tool";
		await toast("OMP — APPROVAL?", "Onay bekleniyor!", tool.slice(0, 120), { bell: true });
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
		// win32 only: the Linux/ssh path leaves turn-end bell to the built-in,
		// which already rings once, so this branch must not add a second bell.
		await toast(title, line2, line3);
	});
}
