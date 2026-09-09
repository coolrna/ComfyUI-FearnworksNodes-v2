# ComfyUI Fearnworks Nodes V2

Modern utility nodes for ComfyUI, inspired by the archived Fearnworks Nodes project.

## Initial scope

- Token analysis with no hard-coded tokenizer layout assumptions
- Token-budget trimming with accepted/overflow text and counts
- Prompt segment ranking and inspection
- General text statistics
- Safer filesystem counting and listing utilities
- Modern package metadata and test coverage
- Backward-compatible legacy node concepts where practical

## Repository status

This is the V2 rewrite. The implementation is intentionally split into reusable core modules and ComfyUI node adapters so ComfyUI API changes do not require rewriting the underlying algorithms.

## Development

Install the package in editable mode from the repository root when developing locally.

Run tests with:

```bash
python -m pytest
```

## License

Apache-2.0
