set(ZEV_ORIGINAL_THEME_OUTPUT "${CMAKE_BINARY_DIR}/ZevOriginal.ztm")

add_custom_target(zev_original_theme ALL
    COMMAND ${CMAKE_COMMAND} -E rm -rf "${ZEV_ORIGINAL_THEME_OUTPUT}"
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${CMAKE_CURRENT_SOURCE_DIR}"
        "${ZEV_ORIGINAL_THEME_OUTPUT}"
    COMMENT "Packaging Zev Original ZTM theme"
    VERBATIM)
