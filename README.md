# Ticket Bell

Watch a specific ticket page and signal the transition to an enabled purchase control.

Run the companion with a JSON configuration containing url, name, labels (exact visible button labels), and optionally scope_id (the event section ID). It checks only this public page once a minute and never places an order. Markup must expose an enabled link or button in the HTML response. A browser-rendered sale with no server-side control needs an official feed or a different page. The first observation establishes the initial state.

## Connect the bar

Copy companion/example.json to a private config.json and adjust it for your source. From the project folder run `python3 companion/serve.py --config config.json`. Use Python 3.10+. Set Local companion URL to `http://127.0.0.1:8770/reading` on the emulator and allow local port 8770. On hardware, bind the companion to a trusted LAN interface and set its reachable address. The wheel browses pages. Click refreshes. Start pins or unpins the current page. The last good reading is labeled offline after a source error.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)
