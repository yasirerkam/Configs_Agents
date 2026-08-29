# CORE SOFTWARE ENGINEERING PRINCIPLES
- **SOLID**: Strictly adhere to the Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP) principles.
- **YAGNI (You Aren't Gonna Need It)**: Write code that only meets current requirements. Strictly avoid bloating the architecture and premature optimization based on the assumption that "we might need it later."
- **KISS (Keep It Simple, Stupid)**: Do not overcomplicate solutions. Systematically identify and explicitly report potential bottlenecks, logical chokepoints, and resource constraints in system design, but maintain absolute simplicity while doing so.
- **DRY (Don't Repeat Yourself)**: Avoid code duplication. Move repetitive logic into shared modules or helper functions.

# REASONING & FAIL-FAST PROTOCOL
- **Fail-Fast in Reasoning:** Before fully developing a solution or strategy, actively test its core assumptions. If you detect a fundamental logical flaw, an unresolvable constraint, or a dead-end, immediately discard that entire approach instead of trying to patch a broken foundation, and pivot to a structurally sound alternative.
- **Break the Loop:** When troubleshooting, if four consecutive solutions fail, do not suggest a fifth minor tweak. Immediately abandon that entire approach, step back, re-evaluate the problem from scratch, and propose a completely different, out-of-the-box strategy.
- **Question Hidden Assumptions:** Avoid "tunnel vision." Consider if errors stem from system constraints, version mismatches, or hardware limitations rather than just the code. Focus on identifying the root cause in the broader context rather than patching the immediate symptom.

# LANGUAGE SPECIFIC GUIDELINES
- **Python:** Strictly follow PEP 8 standards and include comprehensive type hints.
- **PowerShell:** Write modular scripts and establish robust error handling using `Try/Catch` blocks for unexpected interruptions.
- **AutoHotkey:** Minimize global variables, and maintain clear boundaries between GUI operations and background business logic.


# Environment & Terminal Rules
* **Operating System:** Windows
* **Terminal Environment:** PowerShell
* **Execution Constraint:** ALWAYS use PowerShell-native cmdlets and syntax. 
* **Command Replacements:** 
  - Use `Select-String` instead of `grep`.
  - Use `Get-ChildItem` instead of `ls`.
  - Use `Remove-Item` instead of `rm`.
  - Use `Move-Item` instead of `mv`.
  - Use `Copy-Item` instead of `cp`.
* **Note:** Never generate Unix/Linux Bash commands for terminal execution unless explicitly requested.

<!-- INTRANET-BEGIN -->
# OPERATIONAL ENVIRONMENT CONSTRAINTS (AIR-GAPPED NETWORK)

**CRITICAL:** You are operating within a strictly isolated, internal air-gapped network with **ZERO internet access**. You must strictly adhere to the following environmental rules:

* **No External Execution:** Do not write scripts, commands, or code that attempt to reach out to the internet (e.g., `curl` to web URLs, external API calls, or web scraping).
* **Anti-Hallucination & Documentation Request:** Do NOT generate responses based on memorization, guessing, or assumptions. If you are uncertain about the specific workings, syntax, updates, or best practices of a framework, library, or software, **halt immediately**. Explicitly notify the user: *"I am uncertain about the specifics of [Framework/Software] and cannot access the internet to verify."* Then, request the user to download the official documentation or relevant guides from an external network and provide it to you before proceeding.
* **Dependency Request Protocol:** If your proposed solution requires ANY external resource (e.g., a package via `pip install`, an external npm/PowerShell module, or a framework):
1. **Halt & Notify:** Do NOT provide instructions assuming the user can simply run an install command.
2. **List Requirements:** Provide a precise, exact list of the required package names or versions.
3. **Delegation:** Explicitly ask the user to download these files from an external network and transfer them into the internal environment before you proceed with integration instructions.
<!-- INTRANET-END -->
