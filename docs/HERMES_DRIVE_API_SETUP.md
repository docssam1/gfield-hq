# HERMES_DRIVE_API_SETUP

Last updated: 2026-05-30 KST

## Goal

Connect G-FIELD Hermes VM to Google Drive so Telegram commands can scan and classify all G-FIELD Drive materials.

## Account Structure

- GCP project: project-56629b95-34aa-49fc-8cf
- Drive data owner: docssam1 account
- Automation runner: gfield-hq-vm
- Service account: should be created in the GCP project and shared into docssam1 Drive folders

## Required Setup

1. Enable Google Drive API in the GCP project.
2. Create a service account, recommended name: gfield-drive-sa.
3. Create a JSON key for that service account.
4. Upload the JSON key to VM outside GitHub.
5. Share the target docssam1 Drive root folders with the service account email.
6. Add the JSON path to VM .env.
7. Add Drive scan script and Telegram command.

## Recommended VM Secret Location

Do not commit JSON key to GitHub.

Recommended path:

```bash
/home/gfield7265/secrets/gfield-drive-sa.json
```

Recommended .env entries:

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/gfield7265/secrets/gfield-drive-sa.json
GFIELD_DRIVE_ROOT_FOLDER_ID=PUT_ROOT_FOLDER_ID_HERE
```

## Permissions

For analysis only:

- Viewer permission on Drive folder is enough.

For saving reports / generated files:

- Editor permission is recommended.

## Planned Telegram Command

```text
/run drive_scan
```

Expected behavior:

1. VM reads Drive folder tree.
2. Saves inventory as CSV/JSON.
3. Classifies files by type:
   - reports
   - homepage assets
   - textbooks
   - videos
   - Kakao exports
   - student photos
   - unknown
4. Sends summary back to Telegram.

## Output Location

Recommended:

```bash
/home/gfield7265/gfield_output/drive_inventory/
```

Possible output files:

```text
drive_inventory.csv
drive_inventory.json
drive_summary.txt
```

## Security Rules

- Never store service account JSON in GitHub.
- Never store child photos or student DB in GitHub.
- GitHub only stores code and documentation.
- Drive and Sheets store private operational data.

## Next Step

After this setup document:

1. Install Google API dependencies.
2. Add `scripts/drive_scan.py`.
3. Add `/run drive_scan` to bot_runner.py.
4. Test with a small folder.
5. Then run full Drive scan.
