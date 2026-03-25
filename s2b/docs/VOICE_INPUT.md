# Voice Input for Q1 Free Recall

## Why voice input

Text-based free recall in S2b introduces a cognitive laziness bias: participants under-report what they perceived because typing is effortful. The gap between what was encoded and what gets typed is a measurement artifact, not a cognitive signal.

Voice input reduces production friction, yielding:
- Richer recall data (more words, more detail)
- Lower latency to first output (speaking starts faster than typing)
- More natural retrieval mode (episodic memory is verbal, not typographic)

The voice/text distinction is itself an experimental variable worth measuring.

## Architecture

### Participant-level choice

The input mode (`text` or `voice`) is chosen **once during onboarding** and persists across all tests for that participant. This avoids per-question friction and keeps the experimental condition consistent within a participant.

Stored in: `participants.input_mode TEXT DEFAULT 'text'`

### Per-test recording

Each test records which mode was actually used for Q1:

| Column | Type | Description |
|--------|------|-------------|
| `q1_input_mode` | TEXT | `'text'` or `'voice'` — actual mode used for this test |
| `q1_raw_transcript` | TEXT | Raw STT output before participant edits (voice only) |

The `q1_text` field always contains the final answer (edited transcript or typed text). The `q1_raw_transcript` preserves the unedited STT output for analysis of edit distance.

### Keystroke/speech timing

- In text mode: `q1_first_keystroke_ms` and `q1_last_keystroke_ms` measure keyboard latency.
- In voice mode: these same fields measure time-to-first-speech-result and time-of-last-speech-result, providing equivalent latency metrics for the voice modality.

## Web Speech API

Voice recognition uses the browser-native [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) (`SpeechRecognition` / `webkitSpeechRecognition`).

### Configuration

- Language: `fr-FR`
- Continuous mode: `true` (captures multi-sentence responses)
- Interim results: `true` (real-time visual feedback during speech)

### Browser compatibility

| Browser | Support |
|---------|---------|
| Chrome (desktop + Android) | Full support |
| Edge (Chromium) | Full support |
| Safari | Partial (no `continuous` mode) |
| Firefox | Not supported |

When the browser does not support the Web Speech API, the voice UI automatically falls back to a standard text textarea with a warning message. The participant can still complete the test.

### No API key required

The Web Speech API is free, browser-native, and requires no external service or API key. Audio is processed by the browser's built-in speech engine (Google's for Chrome, Microsoft's for Edge).

## User flow

1. **Onboarding**: Participant selects "Voix" or "Texte" in the input mode fieldset.
2. **Q1 panel** (voice mode):
   - "Parler" button starts recognition.
   - Pulsing red dot indicates active listening.
   - Real-time transcript appears as participant speaks.
   - Recognition auto-stops after silence.
   - Transcript shown in editable textarea for corrections.
   - "Recommencer" button allows re-recording.
   - "Valider" button submits the answer (edited or raw).
3. **Q1 panel** (text mode): Unchanged standard textarea.

## Hypothesis

**H5: S9a(voice) > S9a(text)**

Participants using voice input will produce higher S9a semantic similarity scores than text participants, because reduced production friction allows richer recall that better matches the GA's semantic references.

Secondary hypotheses:
- Voice participants will have shorter `q1_first_keystroke_ms` (faster initiation)
- Voice participants will produce longer `q1_text` (more words)
- Edit distance between `q1_raw_transcript` and `q1_text` quantifies participant trust in STT

## V2 roadmap

- **Whisper with keyword hints**: Use OpenAI Whisper API for higher accuracy, with domain-specific keyword prompting (e.g., medical terminology from GA metadata). Requires API key and server-side processing.
- **Audio storage**: Record and upload raw audio blobs (WebM/Opus) for reanalysis. Requires multipart form handling and file storage infrastructure.
- **Per-language adaptation**: Auto-detect participant language and set `recognition.lang` accordingly.
- **Voice for Q4**: Extend voice input to the optional free comment field.

## Files modified

| File | Change |
|------|--------|
| `db.py` | Added `input_mode` to participants, `q1_input_mode` and `q1_raw_transcript` to tests |
| `app.py` | Onboard accepts `input_mode`, test routes pass it to templates, submit accepts new fields |
| `templates/onboard.html` | Input mode fieldset (voice/text radio buttons) |
| `templates/test.html` | Conditional voice/text Q1 panel, hidden form fields, voice JS |
| `templates/test_flux.html` | Same voice UI changes as test.html |
| `templates/reveal.html` | Shows "voix" tag on Q1 recall when voice was used |
| `static/style.css` | Voice pulse animation, transcript display, input mode tag styles |
