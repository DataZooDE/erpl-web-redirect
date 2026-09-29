# This file is included by DuckDB's build system. It specifies which extension to load.
#
# DONT_LINK is essential here, not an optimisation: a statically linked extension is
# loaded while DuckDB starts up, so a stub whose whole job is to throw from LOAD would
# stop the shell from starting at all. Built as a loadable module it only throws when a
# user actually runs LOAD erpl_web.
duckdb_extension_load(erpl_web
    SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}
    DONT_LINK
)
