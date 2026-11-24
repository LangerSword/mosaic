window.MOSAIC_INVENT = {
  "briefs": [
    {
      "brief": "A quiet onboarding for a design tool that feels like a workshop",
      "constraints": "keyboard first, no hover-only states",
      "candidates": [
        {
          "name": "Quiet Turn",
          "input": "scroll",
          "physics": "breathe",
          "feedback": "label",
          "metaphor": "weather",
          "forge_kind": "thinking",
          "overall": 8.6,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 8
          },
          "thesis": "A weather field that answers a scroll with breathe, then makes the result visible with label.",
          "state_machine": [
            {
              "state": "rest",
              "event": "enter viewport",
              "result": "one reveal, no hidden content"
            },
            {
              "state": "progress",
              "event": "scroll",
              "result": "rail matches position"
            },
            {
              "state": "settled",
              "event": "leave",
              "result": "content remains readable"
            }
          ]
        },
        {
          "name": "Field Turn",
          "input": "tap",
          "physics": "pour",
          "feedback": "ring",
          "metaphor": "weather",
          "forge_kind": "paper-plane",
          "overall": 8.6,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 8
          },
          "thesis": "A weather rail that answers a tap with pour, then makes the result visible with ring.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or key",
              "result": "contact is visible"
            },
            {
              "state": "active",
              "event": "release",
              "result": "one action, with a result"
            },
            {
              "state": "reset",
              "event": "result acknowledged",
              "result": "surface returns"
            }
          ]
        },
        {
          "name": "Loom Thread",
          "input": "swipe",
          "physics": "settle",
          "feedback": "trail",
          "metaphor": "signal",
          "forge_kind": "swipe-confirm",
          "overall": 8.4,
          "scores": {
            "coherence": 9,
            "legibility": 7,
            "novelty": 9,
            "restraint": 9,
            "fit": 8
          },
          "thesis": "A signal card that answers a swipe with settle, then makes the result visible with trail.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or grab",
              "result": "surface responds"
            },
            {
              "state": "contact",
              "event": "hold or drag",
              "result": "progress is visible and cancellable"
            },
            {
              "state": "armed",
              "event": "threshold",
              "result": "label states the consequence"
            },
            {
              "state": "resolved",
              "event": "release",
              "result": "check or explicit result"
            },
            {
              "state": "reset",
              "event": "acknowledge",
              "result": "surface returns without a ghost action"
            }
          ]
        }
      ]
    },
    {
      "brief": "A music archive where browsing feels like tuning a radio",
      "constraints": "calm, one signal, no infinite scroll",
      "candidates": [
        {
          "name": "Quiet Turn",
          "input": "scroll",
          "physics": "breathe",
          "feedback": "label",
          "metaphor": "weather",
          "forge_kind": "thinking",
          "overall": 8.5,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 7
          },
          "thesis": "A weather field that answers a scroll with breathe, then makes the result visible with label.",
          "state_machine": [
            {
              "state": "rest",
              "event": "enter viewport",
              "result": "one reveal, no hidden content"
            },
            {
              "state": "progress",
              "event": "scroll",
              "result": "rail matches position"
            },
            {
              "state": "settled",
              "event": "leave",
              "result": "content remains readable"
            }
          ]
        },
        {
          "name": "Field Turn",
          "input": "tap",
          "physics": "pour",
          "feedback": "ring",
          "metaphor": "weather",
          "forge_kind": "paper-plane",
          "overall": 8.5,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 7
          },
          "thesis": "A weather rail that answers a tap with pour, then makes the result visible with ring.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or key",
              "result": "contact is visible"
            },
            {
              "state": "active",
              "event": "release",
              "result": "one action, with a result"
            },
            {
              "state": "reset",
              "event": "result acknowledged",
              "result": "surface returns"
            }
          ]
        },
        {
          "name": "Loom Thread",
          "input": "swipe",
          "physics": "settle",
          "feedback": "trail",
          "metaphor": "signal",
          "forge_kind": "swipe-confirm",
          "overall": 8.3,
          "scores": {
            "coherence": 9,
            "legibility": 7,
            "novelty": 9,
            "restraint": 9,
            "fit": 7
          },
          "thesis": "A signal card that answers a swipe with settle, then makes the result visible with trail.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or grab",
              "result": "surface responds"
            },
            {
              "state": "contact",
              "event": "hold or drag",
              "result": "progress is visible and cancellable"
            },
            {
              "state": "armed",
              "event": "threshold",
              "result": "label states the consequence"
            },
            {
              "state": "resolved",
              "event": "release",
              "result": "check or explicit result"
            },
            {
              "state": "reset",
              "event": "acknowledge",
              "result": "surface returns without a ghost action"
            }
          ]
        }
      ]
    },
    {
      "brief": "A banking app where a transfer feels deliberate",
      "constraints": "irreversible action, explicit cancel",
      "candidates": [
        {
          "name": "Quiet Turn",
          "input": "scroll",
          "physics": "breathe",
          "feedback": "label",
          "metaphor": "weather",
          "forge_kind": "thinking",
          "overall": 8.4,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 6
          },
          "thesis": "A weather field that answers a scroll with breathe, then makes the result visible with label.",
          "state_machine": [
            {
              "state": "rest",
              "event": "enter viewport",
              "result": "one reveal, no hidden content"
            },
            {
              "state": "progress",
              "event": "scroll",
              "result": "rail matches position"
            },
            {
              "state": "settled",
              "event": "leave",
              "result": "content remains readable"
            }
          ]
        },
        {
          "name": "Field Turn",
          "input": "tap",
          "physics": "pour",
          "feedback": "ring",
          "metaphor": "weather",
          "forge_kind": "paper-plane",
          "overall": 8.4,
          "scores": {
            "coherence": 9,
            "legibility": 8,
            "novelty": 9,
            "restraint": 9,
            "fit": 6
          },
          "thesis": "A weather rail that answers a tap with pour, then makes the result visible with ring.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or key",
              "result": "contact is visible"
            },
            {
              "state": "active",
              "event": "release",
              "result": "one action, with a result"
            },
            {
              "state": "reset",
              "event": "result acknowledged",
              "result": "surface returns"
            }
          ]
        },
        {
          "name": "Loom Thread",
          "input": "swipe",
          "physics": "settle",
          "feedback": "trail",
          "metaphor": "signal",
          "forge_kind": "swipe-confirm",
          "overall": 8.2,
          "scores": {
            "coherence": 9,
            "legibility": 7,
            "novelty": 9,
            "restraint": 9,
            "fit": 6
          },
          "thesis": "A signal card that answers a swipe with settle, then makes the result visible with trail.",
          "state_machine": [
            {
              "state": "idle",
              "event": "press or grab",
              "result": "surface responds"
            },
            {
              "state": "contact",
              "event": "hold or drag",
              "result": "progress is visible and cancellable"
            },
            {
              "state": "armed",
              "event": "threshold",
              "result": "label states the consequence"
            },
            {
              "state": "resolved",
              "event": "release",
              "result": "check or explicit result"
            },
            {
              "state": "reset",
              "event": "acknowledge",
              "result": "surface returns without a ghost action"
            }
          ]
        }
      ]
    }
  ]
};
