# This file is included by DuckDB's build system. It specifies which extension to load.
#
# DONT_LINK is essential here, not an optimisation: a statically linked extension is
# loaded while DuckDB starts up, so a stub whose whole job is to throw from LOAD would
# stop the shell from starting at all. Built as a loadable module it only throws when a
# user actually runs LOAD erpl_web.
#
# DuckDB 2.0 removed DONT_LINK (configure fails with "DONT_LINK was removed") and links
# an extension statically only when it is listed with duckdb_extension_statically_link()
# -- so on 2.0 the plain form already keeps the stub loadable-only. Verified on 2.0: the
# shell starts, erpl_web is not loaded, and LOAD erpl_web throws the redirect message.
if(DUCKDB_MAJOR_VERSION LESS 2)
    duckdb_extension_load(erpl_web
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}
        DONT_LINK
    )
else()
    duckdb_extension_load(erpl_web
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}
    )
endif()
