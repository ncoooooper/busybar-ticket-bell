# Emulator verification

Local HTML ticket page served over HTTP.

An initially disabled purchase button became enabled. The companion parsed the exact configured event section and the firmware displayed OPEN.

14 distinct frames were recorded on firmware 1.3.1. App io.ncoooooper.ticketbell exited: finished; heap peak 82.0 of 128 KiB. Screenshots are in screenshots/ and the recording is in media/.

## Display capture

Firmware 1.3.1 rendered both README examples. The display run replayed sample inputs in a separate emulator project. The source test above describes how those readings were obtained. Each square in a guide GIF is one front LED in a 16 × 16 cell. The production archive was built from the source in this repository.

## New mode

Two interactions were captured on firmware 1.3.1. Recorded source response. Back exited the app cleanly. See [recording details](media/source-mode-check.json).

## Screen transition capture

Firmware 1.3.1 rendered the display sequences in the README. The guide uses a 14 × 14 lit area inside each 16 × 16 cell. Input sequences, frame counts and the release archive checksum are in [the capture record](media/screen-transitions.json).
