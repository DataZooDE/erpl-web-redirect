# erpl_web — renamed to erpl_odata

`erpl_web` is now **`erpl_odata`**. This repository only builds a tiny stub
extension named `erpl_web`. Loading it fails on purpose, with a message that says where
the extension went, so nobody is left guessing why `LOAD erpl_web` stopped working.

```sql
LOAD erpl_web;
-- Invalid Input Error: ... The erpl_web extension has been renamed to erpl_odata.
--   Run: INSTALL erpl_odata FROM community; LOAD erpl_odata; ...
```

To migrate, install the new extension. Its functions, secrets and settings are unchanged:

```sql
INSTALL erpl_odata FROM community;
LOAD erpl_odata;
-- or, from the DataZoo repository:
INSTALL erpl_odata FROM 'http://get.erpl.io';
```

- Real extension: <https://github.com/DataZooDE/erpl-odata> (formerly `erpl-web`)
- Docs: <https://erpl.io/docs/erpl-odata>

## Why a stub

DuckDB has no alias mechanism for extension names. Publishing a small extension under the
old name is the way to give users of the old name a clear pointer.

## Development

The stub is built as a loadable module only (`DONT_LINK`). A statically linked stub would
throw while DuckDB starts and stop the shell from launching.

```bash
make test_redirect   # release build, then assert LOAD fails and names erpl_odata
```

The extension-ci-tools SQL tests are skipped (`SKIP_TESTS=1`, `skip_tests: true` in CI),
because they `require` the extension and this one must fail to load.
`scripts/smoke_test.py` is the test instead.

## License

MIT
