# Vendored skills

Installed for the `sirh-v1` agent squad. Upstream content is kept unmodified;
license texts live in `LICENSES/`.

| Skill | Upstream | Revision | License |
|---|---|---|---|
| `django-safe-migration` | [vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins) | `b8af268` | MIT |
| `django-reviewer` | [vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins) | `b8af268` | MIT |
| `test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers) | `22f0b46` | MIT |
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers) | `22f0b46` | MIT |
| `differential-review` | [trailofbits/skills](https://github.com/trailofbits/skills) | `e4dd0bb` | CC BY-SA 4.0 |
| `ponytail` | local install (`~/.agents/skills/ponytail`) | - | MIT (per frontmatter) |

`django-ai-plugins` declares MIT in its README/catalog; the upstream repository
does not carry a root `LICENSE` file, so the standard MIT text is included with
the Vinta copyright notice.

`differential-review` is CC BY-SA 4.0. It is kept in its own directory with the
license text; do not relicense it. Its `allowed-tools` frontmatter mentions Bash
and Write, but the OpenCode agent permissions still gate what each agent can do.
