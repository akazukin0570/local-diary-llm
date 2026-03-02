# LLMDiary (Local Diary LLM)

**Privacy-first AI-powered long-term reflective diary**  
Built with PyQt6 and a local LLM (llama3:8b), designed to help users reflect, analyze, and track emotions over years — completely offline.

## 🎯 Vision

I created LLMDiary to have a **trusted digital diary** that I can keep for 10+ years.  
- Personal reflections, emotional ups and downs, and growth are stored locally.  
- The system never sends data online — privacy is guaranteed.  
- AI assists with emotional support (gentle encouragement or strict feedback) and insight generation.

**Key goals:**

- **Long-term memory:** Searchable diary content spanning years  
- **Emotional intelligence:** Gentle / strict AI modes  
- **Offline-first:** Full local LLM inference  
- **User empowerment:** Customizable prompts, themes, and export options

## 🛠 Technical Highlights

- Desktop UI with **PyQt6**  
- **Local LLM integration** via CLI (Ollama)  
- JSON-based **config persistence** for settings  
- Automatic diary & chat **backups**  
- HTML & PDF **export support**  
- Theme-switchable UI (standard / Windows98 style)  
- Modular code structure for maintainability

---

## 💡 Architecture
User UI (PyQt6)
- Prompt Builder
- LLM CLI (Ollama)
- Local LLM (llama3:8b)
- All AI inference runs locally  
- No data is sent online  
- Supports asynchronous chat and diary summarization

## 🔍 Design Philosophy

- **Privacy-first:** All content remains on the user’s machine  
- **Reflective:** Helps users process emotions and daily events  
- **Flexible:** Gentle encouragement or strict feedback modes  
- **Future-ready:** Designed to support multi-year diary search and AI-assisted insights

---

## 🚀 Next Steps / Improvements

- Multi-year vector search for diary content  
- Advanced emotion tagging  
- Async LLM inference with QThread  
- RAG-based long-term memory support for even deeper insights

## ⚡ Skills Demonstrated

- Desktop app development with Python & PyQt6  
- Local AI integration and prompt engineering  
- Data privacy and offline-first system design  
- Clean code organization and modularity  
- Thoughtful UX design balancing automation and human control

---

> **Note:** This project is designed for personal use but demonstrates **AI-powered application design**, **local LLM integration**, and **privacy-conscious development** — all valuable skills for AI-focused engineering roles.
