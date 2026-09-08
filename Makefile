.PHONY: test verify doctor publish-check npm-pack
verify:
	./scripts/verify

test:
	python3 -m unittest discover -s tests -v
	node --test tests/npm.test.mjs

doctor:
	./bin/potetos doctor

publish-check:
	python3 scripts/publish_check.py

npm-pack:
	npm pack --dry-run --ignore-scripts
