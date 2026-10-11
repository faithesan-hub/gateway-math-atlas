# Publish guide

*Plain-language note: the steps to put version 1.0 online and get its DOI, written for a first-timer. Do these only after your checking list is complete and you have told Claude you approve. About 30 minutes. Claude can do steps 1 and 2 for you if you create two temporary access keys (see "Faster option" at the end).*

## Copy-ready text

- **Repository name:** `gateway-math-atlas`
- **Title:** US Gateway Mathematics Outcomes Atlas
- **Version:** 1.0.0
- **Author:** Esan, Faith Oluwafunmitan · ORCID 0009-0001-3694-157X · Independent Researcher, Laramie, Wyoming, USA
- **Short description:** Institution-level gateway mathematics completion outcomes for California (CCCCO metric 502C) and Texas (THECB measure C18UC) public two-year colleges, matched to IPEDS UNITIDs with documented crosswalks and joined to federal enrollment and Pell data.
- **Keywords:** gateway mathematics; community colleges; developmental education; corequisite; IPEDS; postsecondary data
- **License:** Creative Commons Attribution 4.0 (data and documents); MIT (code)

## 1. GitHub (10 min)

1. Go to https://github.com/new while signed in as **faithesan-hub**.
2. Repository name: `gateway-math-atlas`. Choose **Public**. Leave every "Add" box unticked. Click **Create repository**.
3. Claude gives you the finished project as one zip file. Unzip it.
4. On the new repository page, click **uploading an existing file**, drag in everything from the unzipped folder, and click **Commit changes**.
5. Click **Releases** (right side), then **Draft a new release**. Tag: `v1.0.0`. Title: `Version 1.0`. Paste the short description. Click **Publish release**.

You should see the release page with a zip file listed under "Assets".

## 2. Zenodo DOI (10 min)

1. Go to https://zenodo.org and log in with **ORCID**.
2. Easiest: click your name, then **GitHub**. Flip the switch next to `gateway-math-atlas` to **On**. Then go back to GitHub and publish the release from step 1.5 (if you already did, make a new release `v1.0.1`).
3. Within a few minutes Zenodo shows a new record with a DOI that looks like `10.5281/zenodo.1234567`.
4. Open the record, click **Edit**, and check the title, your name and ORCID, the description, the license and the keywords against the copy-ready text above. Click **Publish**.

## 3. Same day: record it (5 min)

1. Tell Claude the DOI. Claude puts it in `CITATION.cff`, the README and the atlas page.
2. Add a row to `docs/EVIDENCE_LOG.csv` with the date, the DOI and the GitHub link. Save a PDF of the Zenodo record and the GitHub release page.

## Faster option

Create two temporary keys and give them to Claude in the chat. Claude then creates the repository, uploads, tags the release and publishes the Zenodo record for you. Revoke both keys afterward.

- GitHub key: https://github.com/settings/tokens/new , tick **repo**, set expiry to 7 days.
- Zenodo key: https://zenodo.org/account/settings/applications/tokens/new/ , tick **deposit:write** and **deposit:actions**.
