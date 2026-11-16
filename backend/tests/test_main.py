from fastapi.testclient import TestClient

import main
from rag import cosine_similarity

client = TestClient(main.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_cached_answer(monkeypatch):
    monkeypatch.setattr(main, "find_answer", lambda q: "saved answer")

    def fail_if_called(*args):
        raise AssertionError("AI should not run when the answer is cached")

    monkeypatch.setattr(main, "ask_ai", fail_if_called)

    response = client.post("/ask", json={"question": "Who is Chase?"})

    assert response.status_code == 200
    assert response.json()["answer"] == "saved answer"
    assert response.json()["cached"] is True


def test_ask_uses_rag_when_not_cached(monkeypatch):
    saved = {}

    monkeypatch.setattr(main, "find_answer", lambda q: None)
    monkeypatch.setattr(
        main,
        "find_relevant_chunks",
        lambda q: [{"text": "Chase played right tackle.", "source": "about_chase.md"}],
    )
    monkeypatch.setattr(main, "ask_ai", lambda q, context: "fake answer using: " + context)
    monkeypatch.setattr(main, "save_answer", lambda q, a: saved.update({q: a}))

    response = client.post("/ask", json={"question": "What position did Chase play?"})
    data = response.json()

    assert data["cached"] is False
    assert "Chase played right tackle." in data["answer"]
    assert data["sources"] == ["about_chase.md"]
    assert saved["What position did Chase play?"] == data["answer"]


def test_ask_rejects_missing_question():
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_same_direction_is_1():
    assert round(cosine_similarity([1, 2], [2, 4]), 5) == 1.0


def test_perpendicular_is_0():
    assert cosine_similarity([1, 0], [0, 1]) == 0.0