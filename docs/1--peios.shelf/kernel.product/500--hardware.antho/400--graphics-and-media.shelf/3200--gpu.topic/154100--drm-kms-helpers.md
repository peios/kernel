---
title: "Mode Setting Helper Functions"
type: reference
description: "The DRM subsystem aims for a strong separation between core code and helper libraries. Core code takes care of general setup and teardown and decoding userspace requests to kernel internal objects. Everything else is handled by a large set…"
---

<a id="rst-mode-setting-helper-functions"></a>

The DRM subsystem aims for a strong separation between core code and helper libraries. Core code takes care of general setup and teardown and decoding userspace requests to kernel internal objects. Everything else is handled by a large set of helper libraries, which can be combined freely to pick and choose for each driver what fits, and avoid shared code where special behaviour is needed.

This distinction between core code and helpers is especially strong in the modesetting code, where there's a shared userspace ABI for all drivers. This is in contrast to the render side, where pretty much everything (with very few exceptions) can be considered optional helper code.

There are a few areas these helpers can grouped into:

- Helpers to implement modesetting. The important ones here are the atomic helpers. Old drivers still often use the legacy CRTC helpers. They both share the same set of common helper vtables. For really simple drivers (anything that would have been a great fit in the deprecated fbdev subsystem) there's also the simple display pipe helpers.

- There's a big pile of helpers for handling outputs. First the generic bridge helpers for handling encoder and transcoder IP blocks. Second the panel helpers for handling panel-related information and logic. Plus then a big set of helpers for the various sink standards (DisplayPort, HDMI, MIPI DSI). Finally there's also generic helpers for handling output probing, and for dealing with EDIDs.

- The last group of helpers concerns itself with the frontend side of a display pipeline: Planes, handling rectangles for visibility checking and scissoring, flip queues and assorted bits.

<a id="rst-modeset-helper-reference-for-common-vtables"></a>

## Modeset Helper Reference for Common Vtables

```{kernel-doc} include/drm/drm_modeset_helper_vtables.h
:doc: overview
```

```{kernel-doc} include/drm/drm_modeset_helper_vtables.h
:internal:
```

<a id="rst-atomic-modeset-helper-functions-reference"></a>
<a id="rst-drm-atomic-helper"></a>

## Atomic Modeset Helper Functions Reference

<a id="rst-overview"></a>

### Overview

```{kernel-doc} drivers/gpu/drm/drm_atomic_helper.c
:doc: overview
```

<a id="rst-implementing-asynchronous-atomic-commit"></a>

### Implementing Asynchronous Atomic Commit

```{kernel-doc} drivers/gpu/drm/drm_atomic_helper.c
:doc: implementing nonblocking commit
```

<a id="rst-helper-functions-reference"></a>

### Helper Functions Reference

```{kernel-doc} include/drm/drm_atomic_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_atomic_helper.c
:export:
```

<a id="rst-atomic-state-reset-and-initialization"></a>

### Atomic State Reset and Initialization

```{kernel-doc} drivers/gpu/drm/drm_atomic_state_helper.c
:doc: atomic state reset and initialization
```

<a id="rst-atomic-state-helper-reference"></a>

### Atomic State Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_atomic_state_helper.c
:export:
```

<a id="rst-gem-atomic-helper-reference"></a>

### GEM Atomic Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_gem_atomic_helper.c
:doc: overview
```

```{kernel-doc} include/drm/drm_gem_atomic_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_gem_atomic_helper.c
:export:
```

<a id="rst-vblank-helper-reference"></a>

### VBLANK Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_vblank_helper.c
:doc: overview
```

```{kernel-doc} include/drm/drm_vblank_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_vblank_helper.c
:export:
```

<a id="rst-simple-kms-helper-reference"></a>

## Simple KMS Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_simple_kms_helper.c
:doc: overview
```

```{kernel-doc} include/drm/drm_simple_kms_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_simple_kms_helper.c
:export:
```

<a id="rst-fbdev-helper-functions-reference"></a>

## fbdev Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_fb_helper.c
:doc: fbdev helpers
```

```{kernel-doc} include/drm/drm_fb_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_fb_helper.c
:export:
```

<a id="rst-format-helper-functions-reference"></a>

## format Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_format_helper.c
:export:
```

<a id="rst-framebuffer-dma-helper-functions-reference"></a>

## Framebuffer DMA Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_fb_dma_helper.c
:doc: framebuffer dma helper functions
```

```{kernel-doc} drivers/gpu/drm/drm_fb_dma_helper.c
:export:
```

<a id="rst-framebuffer-gem-helper-reference"></a>

## Framebuffer GEM Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_gem_framebuffer_helper.c
:doc: overview
```

```{kernel-doc} drivers/gpu/drm/drm_gem_framebuffer_helper.c
:export:
```

<a id="rst-bridges"></a>
<a id="rst-drm-bridges"></a>

## Bridges

<a id="rst-overview-1"></a>

### Overview

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:doc: overview
```

<a id="rst-display-driver-integration"></a>

### Display Driver Integration

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:doc: display driver integration
```

<a id="rst-special-care-with-mipi-dsi-bridges"></a>

### Special Care with MIPI-DSI bridges

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:doc: special care dsi
```

<a id="rst-bridge-operations"></a>

### Bridge Operations

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:doc: bridge operations
```

<a id="rst-bridge-connector-helper"></a>

### Bridge Connector Helper

```{kernel-doc} drivers/gpu/drm/display/drm_bridge_connector.c
:doc: overview
```

<a id="rst-bridge-helper-reference"></a>

### Bridge Helper Reference

```{kernel-doc} include/drm/drm_bridge.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:export:
```

<a id="rst-mipi-dsi-bridge-operation"></a>

### MIPI-DSI bridge operation

```{kernel-doc} drivers/gpu/drm/drm_bridge.c
:doc: dsi bridge operations
```

<a id="rst-bridge-connector-helper-reference"></a>

### Bridge Connector Helper Reference

```{kernel-doc} drivers/gpu/drm/display/drm_bridge_connector.c
:export:
```

<a id="rst-panel-bridge-helper-reference"></a>

### Panel-Bridge Helper Reference

```{kernel-doc} drivers/gpu/drm/bridge/panel.c
:export:
```

<a id="rst-panel-helper-reference"></a>
<a id="rst-drm-panel-helper"></a>

## Panel Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_panel.c
:doc: drm panel
```

```{kernel-doc} include/drm/drm_panel.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_panel.c
:export:
```

```{kernel-doc} drivers/gpu/drm/drm_panel_orientation_quirks.c
:export:
```

```{kernel-doc} drivers/gpu/drm/drm_panel_backlight_quirks.c
:export:
```

<a id="rst-panel-self-refresh-helper-reference"></a>

## Panel Self Refresh Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_self_refresh_helper.c
:doc: overview
```

```{kernel-doc} drivers/gpu/drm/drm_self_refresh_helper.c
:export:
```

<a id="rst-hdmi-atomic-state-helpers"></a>

## HDMI Atomic State Helpers

<a id="rst-overview-2"></a>

### Overview

```{kernel-doc} drivers/gpu/drm/display/drm_hdmi_state_helper.c
:doc: hdmi helpers
```

<a id="rst-functions-reference"></a>

### Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_hdmi_state_helper.c
:export:
```

<a id="rst-hdcp-helper-functions-reference"></a>

## HDCP Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_hdcp_helper.c
:export:
```

<a id="rst-display-port-helper-functions-reference"></a>

## Display Port Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_dp_helper.c
:doc: dp helpers
```

```{kernel-doc} include/drm/display/drm_dp.h
:internal:
```

```{kernel-doc} include/drm/display/drm_dp_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/display/drm_dp_helper.c
:export:
```

<a id="rst-display-port-cec-helper-functions-reference"></a>

## Display Port CEC Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_dp_cec.c
:doc: dp cec helpers
```

```{kernel-doc} drivers/gpu/drm/display/drm_dp_cec.c
:export:
```

<a id="rst-display-port-dual-mode-adaptor-helper-functions-reference"></a>

## Display Port Dual Mode Adaptor Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_dp_dual_mode_helper.c
:doc: dp dual mode helpers
```

```{kernel-doc} include/drm/display/drm_dp_dual_mode_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/display/drm_dp_dual_mode_helper.c
:export:
```

<a id="rst-display-port-mst-helpers"></a>

## Display Port MST Helpers

<a id="rst-overview-3"></a>

### Overview

```{kernel-doc} drivers/gpu/drm/display/drm_dp_mst_topology.c
:doc: dp mst helper
```

```{kernel-doc} drivers/gpu/drm/display/drm_dp_mst_topology.c
:doc: Branch device and port refcounting
```

<a id="rst-functions-reference-1"></a>

### Functions Reference

```{kernel-doc} include/drm/display/drm_dp_mst_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/display/drm_dp_mst_topology.c
:export:
```

<a id="rst-topology-lifetime-internals"></a>

### Topology Lifetime Internals

These functions aren't exported to drivers, but are documented here to help make the MST topology helpers easier to understand

```{kernel-doc} drivers/gpu/drm/display/drm_dp_mst_topology.c
:functions: drm_dp_mst_topology_try_get_mstb drm_dp_mst_topology_get_mstb drm_dp_mst_topology_put_mstb drm_dp_mst_topology_try_get_port drm_dp_mst_topology_get_port drm_dp_mst_topology_put_port drm_dp_mst_get_mstb_malloc drm_dp_mst_put_mstb_malloc
```

<a id="rst-mipi-dbi-helper-functions-reference"></a>

## MIPI DBI Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_mipi_dbi.c
:doc: overview
```

```{kernel-doc} include/drm/drm_mipi_dbi.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_mipi_dbi.c
:export:
```

<a id="rst-mipi-dsi-helper-functions-reference"></a>

## MIPI DSI Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_mipi_dsi.c
:doc: dsi helpers
```

```{kernel-doc} include/drm/drm_mipi_dsi.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_mipi_dsi.c
:export:
```

<a id="rst-display-stream-compression-helper-functions-reference"></a>

## Display Stream Compression Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_dsc_helper.c
:doc: dsc helpers
```

```{kernel-doc} include/drm/display/drm_dsc.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/display/drm_dsc_helper.c
:export:
```

<a id="rst-output-probing-helper-functions-reference"></a>

## Output Probing Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_probe_helper.c
:doc: output probing helper overview
```

```{kernel-doc} drivers/gpu/drm/drm_probe_helper.c
:export:
```

<a id="rst-edid-helper-functions-reference"></a>

## EDID Helper Functions Reference

```{kernel-doc} include/drm/drm_edid.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_edid.c
:export:
```

```{kernel-doc} include/drm/drm_eld.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_eld.c
:export:
```

<a id="rst-scdc-helper-functions-reference"></a>

## SCDC Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/display/drm_scdc_helper.c
:doc: scdc helpers
```

```{kernel-doc} include/drm/display/drm_scdc_helper.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/display/drm_scdc_helper.c
:export:
```

<a id="rst-hdmi-infoframes-helper-reference"></a>

## HDMI Infoframes Helper Reference

Strictly speaking this is not a DRM helper library but generally usable by any driver interfacing with HDMI outputs like v4l or alsa drivers. But it nicely fits into the overall topic of mode setting helper libraries and hence is also included here.

```{kernel-doc} include/linux/hdmi.h
:internal:
```

```{kernel-doc} drivers/video/hdmi.c
:export:
```

<a id="rst-rectangle-utilities-reference"></a>

## Rectangle Utilities Reference

```{kernel-doc} include/drm/drm_rect.h
:doc: rect utils
```

```{kernel-doc} include/drm/drm_rect.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_rect.c
:export:
```

<a id="rst-flip-work-helper-reference"></a>

## Flip-work Helper Reference

```{kernel-doc} include/drm/drm_flip_work.h
:doc: flip utils
```

```{kernel-doc} include/drm/drm_flip_work.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_flip_work.c
:export:
```

<a id="rst-auxiliary-modeset-helpers"></a>

## Auxiliary Modeset Helpers

```{kernel-doc} drivers/gpu/drm/drm_modeset_helper.c
:doc: aux kms helpers
```

```{kernel-doc} drivers/gpu/drm/drm_modeset_helper.c
:export:
```

<a id="rst-of-dt-helpers"></a>

## OF/DT Helpers

```{kernel-doc} drivers/gpu/drm/drm_of.c
:doc: overview
```

```{kernel-doc} drivers/gpu/drm/drm_of.c
:export:
```

<a id="rst-legacy-plane-helper-reference"></a>

## Legacy Plane Helper Reference

```{kernel-doc} drivers/gpu/drm/drm_plane_helper.c
:doc: overview
```

```{kernel-doc} drivers/gpu/drm/drm_plane_helper.c
:export:
```

<a id="rst-legacy-crtc-modeset-helper-functions-reference"></a>

## Legacy CRTC/Modeset Helper Functions Reference

```{kernel-doc} drivers/gpu/drm/drm_crtc_helper.c
:doc: overview
```

```{kernel-doc} drivers/gpu/drm/drm_crtc_helper.c
:export:
```

<a id="rst-privacy-screen-class"></a>

## Privacy-screen class

```{kernel-doc} drivers/gpu/drm/drm_privacy_screen.c
:doc: overview
```

```{kernel-doc} include/drm/drm_privacy_screen_driver.h
:internal:
```

```{kernel-doc} include/drm/drm_privacy_screen_machine.h
:internal:
```

```{kernel-doc} drivers/gpu/drm/drm_privacy_screen.c
:export:
```
