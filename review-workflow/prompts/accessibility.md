# Accessibility and implementation consistency

Inspect semantic structure, anchor validity, focus visibility, keyboard access,
reduced-motion handling, color roles, text contrast, responsive overflow and
legibility at zoom. Contrast claims require actual foreground/background values
and a reproducible calculation. Never label decorative or inactive content as an
interactive contrast failure without explaining its role.

Review implementation-level discrepancies: duplicated IDs, missing destinations,
unreliable font dependencies, inconsistent design tokens, unreadable code samples,
contradictory minimum sizes and color rules. If supplied runtime evidence cannot
establish keyboard or responsive behavior, record the specific limitation.

If every check that requires browser interaction lacks evidence, set
complete=false. Source review and supplied automated/browser results may support
individual checks, but never claim an accessibility certification or full WCAG
conformance. Surface meaningful gaps in this design guide's own usability.
