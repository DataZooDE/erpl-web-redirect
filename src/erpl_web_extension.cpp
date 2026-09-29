#define DUCKDB_EXTENSION_MAIN

#include "erpl_web_extension.hpp"
#include "duckdb.hpp"
#include "duckdb/common/exception.hpp"

namespace duckdb {

// Kept as one string so the wording is asserted verbatim by scripts/smoke_test.py.
static constexpr const char *REDIRECT_MESSAGE =
    "The erpl_web extension has been renamed to erpl_odata. "
    "Run: INSTALL erpl_odata FROM community; LOAD erpl_odata; "
    "(or INSTALL erpl_odata FROM 'http://get.erpl.io';). "
    "All functions, secrets and settings are unchanged. "
    "See https://erpl.io/docs/erpl-odata";

void ErplWebExtension::Load(ExtensionLoader &loader) {
	throw InvalidInputException(REDIRECT_MESSAGE);
}

std::string ErplWebExtension::Name() {
	return "erpl_web";
}

std::string ErplWebExtension::Version() {
#ifdef EXT_VERSION_ERPL_WEB
	return EXT_VERSION_ERPL_WEB;
#else
	return "";
#endif
}

} // namespace duckdb

extern "C" {

DUCKDB_CPP_EXTENSION_ENTRY(erpl_web, loader) {
	duckdb::ErplWebExtension::Load(loader);
}

}
