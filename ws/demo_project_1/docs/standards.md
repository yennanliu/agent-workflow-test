# Coding standards

- Standard library only. No third-party packages.
- Type hints on every public function and method.
- HTTP errors are JSON: `{"error": "<message>"}` with the matching status code.
- SQL uses parameters, never string formatting.
- Tests use `unittest` and test behaviour through public interfaces.
