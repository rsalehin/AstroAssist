Scaffold a new source connector with id `$ARGUMENTS` following docs/PLUGIN_SPEC.md and docs/SOURCES.md:
- create src/astroassist/sources/$ARGUMENTS/{__init__.py,manifest.yaml,plugin.py,tools.py,normalize.py,README.md}
- create tests/sources/test_$ARGUMENTS.py with fixture-based tests and one @pytest.mark.live contract test
- add evals/benchmark/$ARGUMENTS.yaml with 3 seed questions
- register in sources/registry.py; update docs/SOURCES.md
Every tool must return a typed artifact with provenance and create a QueryArtifact for each external call. Do not add an agent.
