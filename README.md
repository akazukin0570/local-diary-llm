# Local Diary LLM

自身の内面も含めたなんでも書ける日記という非常にパーソナルな情報を扱うため、
広くインターネット上に保存することに心理的な抵抗があり、ローカル実行を前提として設計しました。

結果として、外部APIやクラウドに依存しない構成となり、
セキュリティ面でも安心できるアーキテクチャになっています。

> A privacy-focused desktop diary application powered by a locally running LLM.
> 
> This project explores practical, secure, local-first AI usage without relying on external APIs.

---

## Overview

Local Diary LLM is a lightweight desktop application built with Python and PyQt6.
It integrates a locally executed large language model (via Ollama) to support:

- Daily reflection
- Structured summarization
- Interactive AI consultation
- Prompt-controlled behavior tuning

All processing is done locally.

---

## Features

- Diary writing with date-based storage
- LLM-powered summary generation
- AI consultation mode
- Editable system prompt
- Theme switching
- HTML / PDF export
- Automatic backup
- Fully local execution (no external API calls)

---

## Design Intent

This project was built to explore practical local-first AI usage.

Instead of relying on cloud APIs, the application executes LLMs locally via Ollama, focusing on:

- Privacy-first architecture
- Prompt control and behavior tuning
- Usable desktop AI workflows
- Minimal but structured state persistence

The goal was to experiment with how AI can support real personal knowledge workflows without external dependencies.

---

## Architecture

- Python
- PyQt6 (Desktop UI)
- Ollama (Local LLM execution)
- File-based persistence (no database)
- Configurable model selection

---

## Requirements

- Python 3.9+
- Ollama installed locally
- A downloaded model (e.g. llama3)

---

## Installation

### macOS / Linux

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python diary_app.py

### Windows (PowerShell)

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python diary_app.py

---

## Notes

- The application assumes Ollama is available in PATH.
- Default model can be changed in settings.
- Prompt behavior can be edited inside the app.

---

## Motivation

This repository represents an exploration of applied AI in practical workflows.

Rather than building a cloud-based SaaS product, the focus was:

- Understanding local LLM behavior
- Designing controllable prompt systems
- Integrating AI into real desktop tools

It is intentionally minimal but structured.

---

## License

MIT License

## Status

Version: 0.0.1

This is a personal experimental project focused on exploring local LLM integration and prompt-controlled AI workflows.

The application is functional but intentionally minimal.
