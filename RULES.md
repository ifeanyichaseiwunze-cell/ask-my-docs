# Project Rules

**Goal:** A website where you ask a question, a local AI model answers it, and every question and answer is saved in MongoDB.

**Stack:** Next.js + TypeScript (frontend), FastAPI (Python backend), Ollama qwen2.5:3b (AI model), MongoDB Atlas (database), pytest + GitHub Actions (testing).

## Rules for AI-written code
1. Build one step at a time. Each step has a goal, a reason, and a plan.
2. I read and can explain every file before moving on.
3. No secrets in code. They go in .env, which is never committed.
4. Every feature gets at least one test.
5. Keep it simple. No extra libraries unless a step needs them.

## How I check the AI's work
I run it, test it, and explain it back in my own words.
