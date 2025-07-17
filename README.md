## Ingestion Pipeline

### 🔹 How to Ingest
Use `main.py` in the `INGEST` folder.

- **Input**: CSV file with **3 columns**:  
  `[Fish Name, Summary Description, Image Links]`

- **What it Does**:
  - Embeds the `Summary Description`
  - Adds a new column: `embedding`
  - Stores all 4 columns in the Elasticsearch database

- **Output**:  
  None (but **remember the index name** — you'll need it for querying)

---

## Query Pipeline

### 🔹 How to Query
Use `main.py` in the `BE` folder.

- **Input**:
  1. Index name of the Elasticsearch DB used during ingestion
  2. Image path to search

- **What it Does**:
  - Transforms the image into 64x64
  - Generates a caption using WXAI
  - Embeds the caption
  - Queries the ES database using the embedded caption
  - Retrieves the top **N** matching fish

- **Output**:  
  JSON format of the top **N** fish results



## 📓 Example Service Usage

Check out [`service example.ipynb`](NOTEBOOKS/service_example.ipynb) in the `NOTEBOOKS` folder for more detail on ElasticsearchManager, ElasticsearchQuery and EmbeddingService