import {instrument} from "@shared/instrument";

instrument({
  "title": "TICKET BELL",
  "primary": "Ticket Bell",
  "accent": "#FFAA65",
  "cadence": 60000,
  "motion": {
    "motif": "ticket",
    "color": "#FFAA65",
    "shine": "#FFF2D6"
  },
  "setup": "Start companion/serve.py"
});
