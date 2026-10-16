# Duplicate Record Resolver

Finds likely duplicate entities using fuzzy similarity across selected fields.

## Usage
```bash
pip install -r requirements.txt
python src/resolve_duplicates.py sample/customers.csv   --fields name,email,address --threshold 82
```

The output lists candidate pairs and a weighted similarity score. It does not merge records automatically; that decision remains reviewable.
