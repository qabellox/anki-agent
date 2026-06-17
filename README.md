# Anki-Agent: Autonomous Knowledge Pipeline

An intelligent agent that bridges the gap between web research and long-term memory. 

## The Problem
Manual flashcard creation is the #1 bottleneck for language learners and students. It is repetitive, slow, and leads to content abandonment.

## The Solution
An autonomous **Agentic ETL (Extract, Transform, Load) Pipeline** that:
- **Extracts:** Autonomous web scraping of educational topics.
- **Transforms:** Semantic cleaning and structuring via Llama 3.3 (Groq).
- **Loads:** API-driven injection into Anki, ensuring structured, high-quality study material.

## Architecture
- **Tech Stack:** Python, Anki-Connect, Groq API, DuckDuckGo Search, Trafilatura.
- **Design Pattern:** Decoupled modules (Client, Config, Utils) for scalability.
- **Metamorphosis:** Designed to evolve into a full-scale automated learning assistant.

## Contribution & Roadmap
- [ ] Add Pydantic validation for robust JSON handling.
- [ ] Implement SQLite memory layer to track mastery.
- [ ] Develop FastAPI staging area for "Human-in-the-Loop" approval.
