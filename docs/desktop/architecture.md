# ZevNT desktop architecture

## Goal

ZevNT keeps the NT kernel and Win32 compatibility layer while developing a distinct native desktop experience. Desktop processes remain in user mode: a shell or compositor failure must not take down the kernel.

## Existing upstream components

The fork already contains an NT-compatible DWM host at `base/system/dwm`, the Explorer shell at `base/shell/explorer`, and DWM settings UI at `base/applications/dwmsettings`. These are substantial existing components and must not be replaced or bypassed without a reviewed migration plan.

## ZevNT components

The intended logical components are:

- **ZevDWM**: window/surface policy, composition coordination, workspaces, animation policy, and theme application.
- **ZevShell**: desktop, taskbar, Start experience, notifications, quick settings, and workspace switcher.
- **ZevExplorer**: file-management experience, kept separate from the compositor and shell.
- **ZevTheme**: validates ZTM packages, resolves design tokens, exposes immutable theme snapshots, and applies user overrides.

The first implementation milestone is the ZTM v1 theme contract and Zev Original package. It is data-only. No new compositor executable or kernel interface is introduced in this milestone.

## Process and API boundaries

- Keep the compositor and shell in user mode.
- Use documented Win32/NT interfaces and existing DWM/WDDM contracts; do not invent kernel ABI or private structure layouts.
- Win32 applications continue to use normal window APIs. They must not receive direct control over compositor internals.
- Theme loading is untrusted input: validate paths, types, ranges, resource references, and package version before activation.
- Theme changes are transactional. A parse or validation failure must preserve the currently active theme.
- Optional visual effects must have usable opaque fallbacks.
- User preferences override theme values; theme values override renderer defaults.

## Theme roadmap

The initial theme is **Zev Original**. Planned optional themes are Zev 11, Zev 10, Zev 7, and Zev Fusion (Windows 10 layout with Windows 7-inspired visual treatment). The optional themes must not change application compatibility behavior.

## Implementation sequence

1. Define and validate ZTM v1.
2. Implement ZevTheme token resolution and package validation with unit tests.
3. Define the stable C ABI between ZevTheme, ZevDWM, and ZevShell.
4. Integrate the theme snapshot into the existing DWM path without breaking Win32 composition.
5. Implement ZevShell as a separate user-mode process.
6. Add VM boot and interaction tests before making ZevNT desktop components the default.
