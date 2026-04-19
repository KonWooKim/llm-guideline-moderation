# Data Layout

Expected local layout for moderation reproduction:

```text
data/
  guidelines/
    ncbi_disease_guidelines.txt
    bc5cdr_guidelines.txt
    biored_guidelines.txt
  schemas/
    disease_only.schema.json
    ncbi_entities.schema.json
    biored_entities.schema.json
  ncbi_disease/
    train/
      *.json
    valid/
      ncbi-disease-valid-gpt-r-g.pubann.json
  bc5cdr/
    train/
      *.json
    valid/
      bc5cdr-valid-gpt-r-g.pubann.json
  biored/
    train/
      *.json
    valid/
      biored-valid-gpt-r-g.pubann.json
```

Schema files are simple JSON arrays of entity names.
