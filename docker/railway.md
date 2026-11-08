# Deploying to Railway from the published image

Railway no longer builds this repository. `.github/workflows/image-publish.yml`
builds the image on GitHub and pushes it to GHCR; Railway pulls that image.

This is a change of the service's **source**, not of its runtime settings.
`railway.json` is not used (it is deprecated and applies file-level settings to
every service in the project — see commit `3a18c7fa7`), so healthcheck and
restart policy stay configured on each service in the dashboard.

## What CI publishes

| Tag | When | Use |
|---|---|---|
| `sha-<short>` | every push to `sirh-v1` | pin a deployment to an exact commit |
| `sirh-v1` | every push to `sirh-v1` | follow the branch |
| `latest` | default branch only | staging convenience |
| `X.Y.Z` | on a version tag | releases |

Registry path: `ghcr.io/<owner>/<repo>` with the owner/repo lowercased, i.e.
`ghcr.io/yon1427/horilla-hr`.

## Wiring it up, once per service

Both services (`web` and the scheduler) run the same image; only the start
command differs.

1. Railway → the service → **Settings → Source**.
2. Choose **Docker Image** and enter
   `ghcr.io/yon1427/horilla-hr:sha-<short>` (pin it) or `:sirh-v1` (follow).
3. **web**: leave the start command empty so the image's
   `CMD ["gunicorn", ...]` is used. Set the healthcheck path to `/health/`
   with a 300 s window — first boot applies migrations and runs
   `collectstatic` before gunicorn binds.
4. **scheduler**: same image, start command
   `python manage.py run_scheduler`, no healthcheck (it binds no port;
   inheriting the web healthcheck is what made `railway.json` fail).

### Pull credentials

A GHCR package is **private** until its visibility is changed, and Railway
cannot pull a private package anonymously.

- Simplest: package settings → **Change visibility → Public**, then no
  credentials are needed.
- Otherwise: create a classic PAT with `read:packages`, and add it in Railway
  under **Settings → Source → image pull credentials** (username = your GitHub
  username, password = the PAT).

## Redeploying after a push

Railway does not watch the registry, so a new image needs a deploy:

- dashboard: **Deploy** on the service (or *Redeploy*), or
- CLI: `railway redeploy --service web`, or
- change the tag to the new `sha-<short>`.

Until that happens the service keeps running the previously pulled image, which
is the point of pinning by digest-style tag: a deploy is always an explicit
action.

## Verifying a deployment

```bash
curl -fsS https://<service>.up.railway.app/health/
# {"status": "ok", "product": "sanad", "api": 1}
```

`product` confirms the Sanad build, not an upstream Horilla image.

## Local equivalent

```bash
docker build -t ghcr.io/yon1427/horilla-hr:local .
docker run --rm -e DATABASE_URL=... -p 8000:8000 ghcr.io/yon1427/horilla-hr:local
```

The entrypoint compiles the gettext catalogues when they are missing and
applies migrations on start, so the image is self-sufficient for a first boot.
