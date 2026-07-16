#!/usr/bin/env python3
"""Publish converted Markdown to Confluence Cloud via the REST API.

Reads credentials from the environment so nothing sensitive is ever passed on
the command line or written to disk:
    CONF_SITE   e.g. yourcompany.atlassian.net   (no https://, no /wiki)
    CONF_EMAIL  your Atlassian account email
    CONF_TOKEN  an API token from
                https://id.atlassian.com/manage-profile/security/api-tokens
Atlassian Cloud authenticates as Basic  base64("<email>:<token>").

Usage:
  # update an existing page (keeps title, bumps version):
  publish.py --html OUT.html --mmd-dir MMD_DIR --update PAGE_ID

  # create a new page:
  publish.py --html OUT.html --mmd-dir MMD_DIR \
             --create "Page Title" --space SPACEKEY [--parent PARENT_PAGE_ID]

Body is set first, then every diagram-*.mmd is rendered to PNG (retina, 3x) and
uploaded as attachment mermaid-<i>.png so the <ac:image> macros resolve.
Requires npx + @mermaid-js/mermaid-cli on PATH only when diagrams are present.
"""
import os, sys, json, base64, subprocess, pathlib, argparse
import urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("--html", required=True)
ap.add_argument("--mmd-dir", required=True)
ap.add_argument("--update", help="existing page id to overwrite")
ap.add_argument("--create", help="title for a new page")
ap.add_argument("--space", help="space key (with --create)")
ap.add_argument("--parent", help="parent page id (optional, with --create)")
args = ap.parse_args()

try:
    SITE = os.environ["CONF_SITE"]
    EMAIL = os.environ["CONF_EMAIL"]
    TOKEN = os.environ["CONF_TOKEN"]
except KeyError as e:
    sys.exit(f"missing env var {e}. Set CONF_SITE, CONF_EMAIL, CONF_TOKEN.")

BASE = f"https://{SITE}/wiki/rest/api"
AUTH = "Basic " + base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()

def api(method, path, data=None, headers=None, raw=False):
    url = path if path.startswith("http") else BASE + path
    h = {"Authorization": AUTH, "Accept": "application/json"}
    body = None
    if data is not None and not raw:
        h["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    elif raw:
        body = data
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:800], file=sys.stderr)
        raise

storage = pathlib.Path(args.html).read_text()

# 1. Create or update the page (body first, so the image macros exist before we
#    attach the PNGs they point at).
if args.update:
    cur = api("GET", f"/content/{args.update}?expand=version")
    pid = args.update
    ver = cur["version"]["number"] + 1
    payload = {"id": pid, "type": "page", "title": cur["title"],
               "version": {"number": ver},
               "body": {"storage": {"value": storage, "representation": "storage"}}}
    page = api("PUT", f"/content/{pid}", payload)
    print(f"UPDATED page {pid} -> version {ver}")
elif args.create:
    if not args.space:
        sys.exit("--create requires --space SPACEKEY")
    payload = {"type": "page", "title": args.create,
               "space": {"key": args.space},
               "body": {"storage": {"value": storage, "representation": "storage"}}}
    if args.parent:
        payload["ancestors"] = [{"id": args.parent}]
    page = api("POST", "/content", payload)
    pid = page["id"]
    print(f"CREATED page {pid}")
else:
    sys.exit("pass either --update PAGE_ID or --create TITLE --space KEY")

# 2. Render + upload each mermaid diagram.
mmd_dir = pathlib.Path(args.mmd_dir)
diagrams = sorted(mmd_dir.glob("diagram-*.mmd"))
if diagrams:
    pup = mmd_dir / "puppeteer.json"
    pup.write_text('{"args":["--no-sandbox"]}')
    for d in diagrams:
        i = d.stem.split("-")[1]
        png = mmd_dir / f"mermaid-{i}.png"
        subprocess.run(
            ["npx", "-y", "-p", "@mermaid-js/mermaid-cli", "mmdc",
             "-i", str(d), "-o", str(png), "-b", "white", "-w", "1400",
             "-s", "3", "-p", str(pup)],
            check=True)
        boundary = "----confluenceboundary"
        fname = f"mermaid-{i}.png"
        multipart = b"".join([
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
            f'filename="{fname}"\r\nContent-Type: image/png\r\n\r\n'.encode(),
            png.read_bytes(),
            f"\r\n--{boundary}--\r\n".encode()])
        # PUT (not POST) to child/attachment upserts by filename, so re-runs
        # replace the image instead of stacking duplicates.
        api("PUT", f"/content/{pid}/child/attachment", data=multipart, raw=True,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                     "X-Atlassian-Token": "no-check"})
        print(f"uploaded {fname}")

link = page.get("_links", {})
print(f"DONE: {link.get('base','https://'+SITE+'/wiki')}{link.get('webui','')}")
