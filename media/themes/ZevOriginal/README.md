# Zev Original

Zev Original is the default ZevNT desktop theme. It is a declarative ZTM package: it describes visual tokens and component metrics without embedding executable code.

## Package layout

- `manifest.json` identifies the package and maps each resource document.
- `resources/` contains colors, typography, dimensions, effects, animation, and component styles.
- `assets/` is reserved for redistributable theme assets. The initial package intentionally ships no third-party fonts, cursors, sounds, or icons.

## Design

The visual identity uses graphite surfaces, electric blue as the primary accent, violet as a secondary accent, and cyan for tertiary emphasis. Text contrast and reduced-motion preferences take precedence over decorative effects.

## Runtime contract

A theme is data, not trusted code. A future ZevTheme loader must:

1. Validate the manifest and every referenced resource before activation.
2. Reject absolute paths, parent-directory traversal, duplicate resource keys, and unsupported format versions.
3. Resolve token references only from the package's declared token namespace.
4. Clamp numeric dimensions and animation durations to renderer-defined limits.
5. Treat blur, transparency, and shadows as optional capabilities with opaque fallbacks.
6. Keep user overrides above the active theme, and renderer defaults below it.
7. Apply a theme atomically; a failed load must leave the previous theme active.

ZTM v1 is a proposed ZevNT package contract, not yet a runtime-supported format. The package is not wired into the boot image until a loader and packaging test exist.
