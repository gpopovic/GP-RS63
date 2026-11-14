# Local Transcription Operations

## Approved Local Baseline

Triton uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) `1.2.1` with the multilingual `small` model on CPU using INT8 quantisation. It is open source and runs locally after the one-time model download. The baseline avoids a cloud transcription provider and does not rely on the laptop's 4 GB GPU.

## Data Boundary

The audio source and transcript remain local. Do not place production customer recordings in the Company OS unless the project data-flow record explicitly permits that route. The script writes only to the chosen output directory and never sends source audio to an API.

## Operator Commands

From the project root:

```powershell
04_Execution_Engine\Local_Transcription\.venv\Scripts\python.exe 04_Execution_Engine\Local_Transcription\transcribe_local.py --warmup --model small
04_Execution_Engine\Local_Transcription\.venv\Scripts\python.exe 04_Execution_Engine\Local_Transcription\transcribe_local.py "C:\path\to\recording.m4a" --language de --offline
```

The second command creates a `.txt` transcript and an `.srt` file beside the recording by default. Use `--output-dir` to keep outputs in a different approved location. Use `--language auto` only where the spoken language is uncertain.

## Maintenance

Treat package/model updates as configuration changes. Re-run the existing recordings as a small regression set, compare language accuracy and processing time, then record a promote, keep, or rollback decision. Do not replace the local baseline solely because a newer model exists.
