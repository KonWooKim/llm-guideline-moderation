# Data Layout

Expected local layout for moderation reproduction:

```text
data/
  archives/
    bc5cdr-train.zip
    biored-train.zip
    ncbi-train.zip
  guidelines/
    ncbi_disease_guidelines.txt
    bc5cdr_guidelines.txt
    biored_guidelines.txt
  schemas/
    disease_only.schema.json
    ncbi_entities.schema.json
    biored_entities.schema.json
  ncbi_disease/
    valid/
      ncbi-disease-valid-gpt-r-g.pubann.json
  bc5cdr/
    valid/
      bc5cdr-valid-gpt-r-g.pubann.json
  biored/
    valid/
      biored-valid-gpt-r-g.pubann.json
```

Schema files are simple JSON arrays of entity names.
