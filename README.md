# ID Translator

* Translate almost any Chem ID into any other Chem ID!
* Works best with InCHI/SMARTS-based IDs.
* A repo with bits and pieces of ID translators, looking to merge into a universal tool. 

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
