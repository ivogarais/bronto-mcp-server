import runpy

import bronto.server as server


def test_main_module_invokes_server_main(monkeypatch):
    call_count = {"value": 0}

    def fake_main():
        call_count["value"] += 1

    monkeypatch.setattr(server, "main", fake_main)

    runpy.run_module("bronto.__main__", run_name="__main__")

    assert call_count["value"] == 1
