from types import SimpleNamespace

import app.ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="answer",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = SimpleNamespace(
                generate_content=lambda **kwargs: response,
            )

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    assert ask_module.ask("question") == "answer"
    assert "入力: 12 / 出力: 34" in capsys.readouterr().out