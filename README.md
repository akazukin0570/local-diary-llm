# LLMDiary (Local Diary LLM)

A privacy-first AI-powered long-term reflective journal built with PyQt6 and a local LLM.

---

## Vision

I built this project to have a diary system I can trust for the next 10 years.  
Personal reflections — pain, insecurity, growth — should never leave my device.

This project explores:

- Fully local LLM architecture
- Long-term searchable diary memory
- Emotional AI modes (gentle / strict)
- Privacy-preserving AI UX

---

## Architecture

PyQt6 UI → Prompt Builder → Ollama CLI (subprocess) → Local LLM (llama3:8b)

---

## Technical Highlights

- Local LLM inference via CLI
- JSON-based configuration persistence
- Theme-switchable desktop UI
- Automatic diary & chat backups
- HTML & PDF export support

---

## Screenshots

![Main UI](docs/screenshot.png)

---

## Future Improvements

- Vector search for multi-year diary retrieval
- Emotion tagging system
- QThread-based async inference
- RAG-based long-term memory support
