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