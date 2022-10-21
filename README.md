
# 1. HMDB Compound Classification

* Overview of steps: first generate a dict of `"primary_key"`:[list_of_secondary_keys]. This will not be done frequently.
* Given the `hmdb_metabolites.xml` file, scrape a dictionary of primary HMDB accession numbers, with their respective secondary accession numbers, and save it all in a `json`.
* **Input:** `abs/path/to/hmdb_metabolites.xml`. Download this from here (link "All Metabolites" XML file): https://hmdb.ca/downloads
* Necessary because MetaboAnalyst sometimes returns secondary accession numbers instead of primary ones, and a GET request to `https://hmdb.ca/metabolites/{hmdb_id}.xml` won't work for secondary HMDB accession numbers (browser behaviour: auto-redirect to primary accession number, which confuses the GET request, causing it to return javascript gibberish with status code 200).
* runtime: approx 200s.

# 2. ID Translator Scratch Work

* A repo with bits and pieces of ID translators, looking to merge into a universal tool.

### Best Strat So Far

* Export InCHI/InCHIkey from wherever (mzvault/cloud/NIST)
* Use fiehnlab API to get HMDB, if possible
* The Pubchem search engine is actually pretty good: it searches for all known synonyms, and has good fuzzy logic
(mis-spellings, different bracket conventions, etc.)

### Strategies

* Translate InCHI/InCHIkey-PubchemID (can be either to or from)
* MetaboAnalyst accepts Pubchem ID as input to get HMDB, KEGG, etc.
* Most end-point-services (e.g. HMDB classifier, KEGG pathway classifier) use HMDB_ID or KeggID.

### InCHIKey-to-something-else Translator/Pubchem Scraper

* **Issue** - Pubchem seems to be the best manual search engine to search by InCHI/InCHIkey; it returns a single, exact result quite reliably. Can this be done programmatically for a batch? Pubchem API doesn't support search-by-InCHI/InCHIkey.
*
* **Solution** - Full download of Pubchem XML.

### HMDB Primary/Secondary Accessions

* **Issue**: A compound can have multiple HMDB IDs. It's assumed that one HMDB ID takes precedence (the "primary" HMDB ID), and the rest are secondary. Indeed, visiting a HMDB url with the secondary ID will redirect to a url with the primary HMDB ID; this redirect will confuse a GET request (the GET request will return the redirect request with status code 200)
* **Solution** - Full bulk download of all metabolites in HMDB.
