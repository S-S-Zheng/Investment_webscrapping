import pytest
import pandas as pd
from stock_screener.fetcher import fetch_meta, fetch_ratios

def test_fetch_meta(monkeypatch):
    class DummyResp:
        status_code = 200
        text = """
        <h2 class="m-0 badge txt-b5 txt-s1">TAGVAL</h2>
        <h2 class="m-0 badge txt-b5 txt-s1">FR0000079698</h2>
        <td class="txt-s7 txt-align-left is__realtime-last">123.45 €</td>
        """
        def raise_for_status(self): pass
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: DummyResp())
    meta = fetch_meta("DUMMY")
    assert meta == {"TAG": "TAGVAL", "ISIN": "FR0000079698", "Prix_devise": "123.45 €", "Prix":123.45}

def test_fetch_ratios(monkeypatch):
    # HTML minimal pour un tableau de ratios à deux années
    html = """
    <thead><span>2022</span><span>2023</span></thead>
    <tbody>
      <tr><td class="table-child--w200">PER</td><td>10</td><td>12</td></tr>
      <tr><td class="table-child--w200">PEG</td><td>0.8</td><td>0.9</td></tr>
    </tbody>
    """
    class DummyResp:
        status_code = 200
        text = html
        def raise_for_status(self): pass
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: DummyResp())
    df = fetch_ratios("DUMMY", "valorisation")
    pd.testing.assert_frame_equal(
        df[0], pd.DataFrame({"PER":[10,12], "PEG":[0.8,0.9]}).T
    )
