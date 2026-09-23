# Portable brand skills

One full-system skill and five independent product plugins. Each product package contains its own references, tokens, vector assets and fonts; it does not depend on installing the parent package.

| Brand | Invoke | Skill entrypoint | Chatbot document |
| --- | --- | --- | --- |
| Persistent Labs | `$persistent-labs-brand` | [SKILL.md](plugins/persistent-labs-brand/skills/persistent-labs-brand/SKILL.md) | [chatbot.md](plugins/persistent-labs-brand/chatbot.md) |
| FireFlow | `$fireflow-brand` | [SKILL.md](plugins/fireflow-brand/skills/fireflow-brand/SKILL.md) | [chatbot.md](plugins/fireflow-brand/chatbot.md) |
| Unfazed.dev | `$unfazed-brand` | [SKILL.md](plugins/unfazed-brand/skills/unfazed-brand/SKILL.md) | [chatbot.md](plugins/unfazed-brand/chatbot.md) |
| Lanni | `$lanni-brand` | [SKILL.md](plugins/lanni-brand/skills/lanni-brand/SKILL.md) | [chatbot.md](plugins/lanni-brand/chatbot.md) |
| PrivateInference | `$privateinference-brand` | [SKILL.md](plugins/privateinference-brand/skills/privateinference-brand/SKILL.md) | [chatbot.md](plugins/privateinference-brand/chatbot.md) |
| Galactica | `$galactica-brand` | [SKILL.md](plugins/galactica-brand/skills/galactica-brand/SKILL.md) | [chatbot.md](plugins/galactica-brand/chatbot.md) |

## Use with an agent

Copy the desired `plugins/<name>/skills/<name>/` directory into the agent’s supported skill directory, or point it directly to that SKILL.md. Hosts with skill discovery can select by the frontmatter description; explicit invocation uses the names above. Host setup varies, so no universal automatic installation is implied. In Claude Code, installed plugin skills use the host’s slash-command namespace (for example `/fireflow-brand:fireflow-brand`); the `$` notation above is for agents that support it.

Each plugin also includes `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`. Use the host’s supported local/private-repository plugin installation flow. The repository-level Claude marketplace catalog lists all six plugins. None has been silently installed into an account or local app. Packaging follows [Claude Code’s plugin reference](https://code.claude.com/docs/en/plugins-reference) and the bundled Codex plugin manifest schema.

## Use with a chatbot

Attach or paste the desired `chatbot.md` and give the actual task. It combines instructions, detailed brand rules and tokens in plain Markdown/JSON. If the chatbot can use files, also attach the plugin ZIP or the SVG/font files required by the deliverable. A text-only chatbot can follow the writing and specification guidance but cannot render or validate files without suitable tools.

## Rebuild and validate

Run `python3 scripts/package_skills.py` after changing the bible sources, then `python3 scripts/check_skills.py`. The packaging process derives references and tokens from the same sources as the web bible. Preserve owner decisions and product exceptions when extending the system.

The GitHub repository is intended to remain private. Publishing the reading website does not publish this repository or its plugin catalog.
