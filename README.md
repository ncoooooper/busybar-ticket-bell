# Ticket Bell

Watch product prices and limited-stock rewards, or wait for a ticket purchase link to open.

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

An initially disabled button was enabled in the selected section. That added one opening. Starting the companion while a sale is already open shows OPEN immediately, but the initial observation does not count as a new opening. The recording used a local test page served over HTTP.

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

## Additional source setup

The original box-office mode still watches its selected purchase control. For prices and limited drops use the watchlist config. Start the included example feed with `python3 -m http.server 8780 --bind 127.0.0.1 --directory companion/examples` in a second terminal. Replace its URLs with a permitted product or reward feed before tracking a real sale. For JSON, `price_path` and `stock_path` select dot-separated fields. For HTML, omit both paths and supply `currency` for a single Product offer in JSON-LD. Each product, edition, store region and currency needs its own entry. A price-history file is written alongside the config path you specify.

From the repository root, copy the example and start the companion with Python 3.10 or newer.

```sh
cp companion/live-example.json config.json
# Edit config.json for your source before starting the server.
python3 companion/serve.py --config config.json
```

In the emulator, run `~/.busy-emulator/bin/busy-emulator allow-local 8770` and approve that port. Open **Apps → Ticket Bell → Setup**, set **Local companion URL** to `http://127.0.0.1:8770/reading`, save, then reopen the app. For a physical bar, start the companion with `--host YOUR_LAN_IP` and replace `127.0.0.1` with that address. Bind only to your trusted network. Open `/reading` on the host to inspect the current reading. Keep credentials in the host environment.


### PS Deals price alerts

Enable a price alert for one edition and region in your PS Deals account. After the first email arrives, copy its sender address, a subject fragment specific to that game, and the text immediately before the new price. In a watchlist item set `type` to `price_email`. Set `mail_host`, `username`, `sender`, `subject`, `price_label`, `currency_mark`, `currency`, `name` and `limit`. For an email that says “New price: $14.99”, use `"price_label":"New price"` and `"currency_mark":"$"`. Set `IMAP_PASSWORD` on the host. This reads the latest matching message from a mailbox that supports IMAP password authentication. The price updates when an email arrives. If the provider changes its wording, the page reads Unknown until the label matches again.

### Kickstarter reward quantities

Select the exact reward tier. For a permitted project JSON response containing `project.rewards` or `rewards`, use `{"type":"kickstarter_reward","name":"First print","url":"YOUR_FEED_URL","reward_id":12345}`. Replace the ID with the tier's numeric ID. The companion reads the tier's explicit `remaining` field, including zero. Use a creator-provided JSON feed and `stock_path` when the project page withholds this data. The in-repository example lets you test the display without a campaign account.

## Catch a price cut

Run one check with the sample game at 24.99. Change `companion/examples/game.json` to 14.99 and wait at least 60 seconds. A price strictly below the configured limit shows BELOW LIMIT. A fresh low can also trigger the desk signal. The history starts with the first successful observation and survives restarts.

![An example game under its limit gives way to the remaining reward count.](media/guide/use-1.gif)

## Read the remaining quantity

Select a reward tier or product whose source exposes a numeric remaining quantity. Turn the wheel to REMAINING. Four means four units of that tier. An unavailable feed reads Unknown. Neither campaign pledge totals nor a binary InStock label give a unit count.

![A four-unit reward page gives way to the game price.](media/guide/use-2.gif)

The recordings use example responses on emulator firmware. Each display pixel is enlarged to a 9 × 9 square.
