const inFlight = new Set<string>()
const norm = (p: string) => p.replace(/[\\/]+$/, "").replace(/\\/g, "/").toLowerCase()

export const AutoIndexPlugin = async ({ directory, worktree, client, $ }) => {
  const isIndexed = async (dir: string): Promise<boolean> => {
    const out = await Promise.race([
      $`codebase-memory-mcp.exe cli list_projects`.text(),
      new Promise((_, rej) =>
        setTimeout(() => rej(new Error("list_projects timeout")), 10000)
      ),
    ])
    const data = JSON.parse(out)
    return (data?.projects ?? []).some(
      (p: any) => norm(p?.root_path ?? "") === norm(dir)
    )
  }

  const maybeIndex = async (dir: string) => {
    if (!dir) return
    const key = norm(dir)
    if (inFlight.has(key)) return
    inFlight.add(key)
    try {
      if (await isIndexed(dir)) {
        console.log("[auto-index] already indexed:", dir)
        return
      }
      await $`codebase-memory-mcp.exe cli index_repository --repo-path ${dir} --mode full`.quiet()
      console.log("[auto-index] indexed:", dir)
    } catch (e) {
      console.log("[auto-index] error:", e)
    } finally {
      inFlight.delete(key)
    }
  }

  void maybeIndex(worktree || directory)

  return {
    event: async ({ event }: any) => {
      if (event?.type === "session.created") {
        const cur = await client.project.current().catch(() => null)
        if (cur?.worktree) void maybeIndex(cur.worktree)
      }
    },
  }
}
