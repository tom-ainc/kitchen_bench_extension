# Task: Kitchen bench extension design

## Design an integrated extension unit to `bench.step`.

A placeholder benchtop & kickboard are included in the file, named `BenchtopExt` & `KickboardExt` respecitvely (for size & position reference).

The cabinet should include:

- 3x full width drawers
  - 2x standard height utensil drawers
  - 1x large bottom drawer
  - All drawers with undermount, soft close slides (please source and include in 3D model)
- Sturdy drawer construction:
  - Pocket hole screw joints
  - Routed baseboard slots in sides & front panels
- Semi-freestanding unit
  - To be integrated in a way that appears permenent but can be easily removed in future if needed

Design considerations:

- Does not require CNC routing, hand routing only
- The unit should be sturdy and aesthetically pleasing
- Keep cost to a minimum where it doesn't detract from the form/function

# Workflow

## Golf MCP

Use the published
[Golf MCP 0.1.0rc9 release](https://github.com/designonce/golf-mcp/releases/tag/v0.1.0-rc.9), which
includes Cinema Live.

Installation:

- Create a fresh virtual environment and project directory in this directory.

- Install the released launcher from its exact URL. It installs the matching platform package
  automatically. Replace `<venv>` with the virtual environment's absolute path:

  ```sh
  uv --no-cache pip install --python <venv>/bin/python --no-index --reinstall https://github.com/designonce/golf-mcp/releases/download/v0.1.0-rc.9/golf_mcp-0.1.0rc9-py3-none-any.whl
  ```

- Keep `--no-cache` and `--reinstall`: earlier local test wheels used the same version number.
  Verify that both the launcher and platform package came from this GitHub release.

- Register the virtual environment’s absolute bin/golf path as the MCP command, with arguments:
  `serve --project <new empty directory outside the repository>`

- Reconnect the client’s MCP connection and verify that Golf tools—including live_new_project—are
  actually available. Configuration alone is not proof of connection.

Do not use tools/golf-mcp, oss//golf_mcp:dist, locally built wheels, localhost wheel servers, or an
earlier test environment. Never copy or symlink viewer assets or skills from another project.

Before sharing a live viewer URL:

- Confirm the project has no prior versions or conversation history.
- Verify its served live.html, live.css, live.js, and live-scan.js match the freshly installed
  distribution.
- Share the URL and wait until MCP reports that the viewer is connected before starting CAD work.

If installation or connection fails, report the exact blocker. Do not silently substitute another
build or launch an unrelated server.

Do not publish or release anything.

## Golf Live

Use Golf Live throughout this CAD project as the primary place to communicate progress, explain
geometry, and ask design questions.

Before starting CAD work:

- Check the project and conversation state. Use live_new_project for a fresh task.
- Call live_view and share its URL.
- Call live_wait until MCP reports viewer_connected=true. A timeout is not permission to proceed.
- Continue without the viewer only if I explicitly ask you to.

While working:

- Start each meaningful phase with live_message: briefly explain what you’re about to do.
- Perform related CAD tool calls within that thread so their automatic visualizations stay grouped
  with the update.
- Use readable formatting and inline geometry links for relevant features, measurements, and views.
- Make geometric choices visual: give each relevant option its own `{label, presentation}` so the
  option button previews the affected faces, dimensions, section, view or recorded revision. Use
  inspected geometry IDs and rich links in the question text; avoid plain-English-only references
  such as “this edge” or “the other side”. Use visualization wherever it clarifies a finding,
  trade-off or decision. Plain text options are appropriate for non-geometric choices.
- Close each phase with live_close, summarizing findings and including any CAD-related visual
  questions.
- Wait for all answers through MCP. Once you have something useful to say about them, start the next
  live_message thread promptly.
- If the viewer disconnects, restore the connection before continuing CAD work unless I explicitly
  waive it.

Treat this as a normal design collaboration. Ask questions about the design, not whether app
features or animations work. Keep chat outside the viewer brief: setup, connection problems, and
final file links.
