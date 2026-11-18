# Ticket Bell

Watch a specific ticket page and signal the transition to an enabled purchase control.

Use the bar when two performances share a ticketing page and only one is yours. Selecting the event section keeps an on-sale button for a different performance from lighting up your desk.

## Watch the performance you want

1. Open the public event detail page. Put its URL, event name and exact purchase-button text in the companion configuration.
2. If several events are listed, set `scope_id` to the HTML section for yours. Start the companion and read **BOX OFFICE**.
3. A disabled control gives **WAIT**. An enabled one gives **OPEN**. Turn the wheel to see how many openings have occurred this session.

![BOX OFFICE reads OPEN and the wheel reveals one opening.](media/guide/check-opening-count.gif)

## Return to the sale status

1. Look at the rear screen on **OPENINGS** for the last change time.
2. Turn back to **BOX OFFICE**. Press **Start** to pin that page if you are leaving the bar on your desk.
3. Open the ticket seller’s page yourself when you are ready. The app observes the control and the seller handles the purchase.

![The openings counter returns to OPEN on the box-office page.](media/guide/watch-box-office.gif)

## Example from the emulator

An initially disabled button was enabled in the selected section. That added one opening. Starting the companion while a sale is already open shows OPEN immediately, but the initial observation does not count as a new opening. Local HTML ticket page served over HTTP.

## Set up the source

Run the companion with a JSON configuration containing url, name, labels (exact visible button labels), and optionally scope_id (the event section ID). It checks only this public page once a minute and never places an order. Markup must expose an enabled link or button in the HTML response. A browser-rendered sale with no server-side control needs an official feed or a different page. The first observation establishes the initial state.

## Connect the bar

Copy companion/example.json to a private config.json and adjust it for your source. From the project folder run `python3 companion/serve.py --config config.json`. Use Python 3.10+. Set Local companion URL to `http://127.0.0.1:8770/reading` on the emulator and allow local port 8770. On hardware, bind the companion to a trusted LAN interface and set its reachable address. The wheel browses pages. Click refreshes. Start pins or unpins the current page. The last good reading is labeled offline after a source error.

## Run in the emulator

Open BUSY Bar Emulator. From this repository, run:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

Press **Back** to exit.

The GIFs are excerpts from the emulator recording. Each front-display pixel is shown at 9× its original width and height. The end frames pause for reading.

[Full recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md) · [MIT license](LICENSE)
