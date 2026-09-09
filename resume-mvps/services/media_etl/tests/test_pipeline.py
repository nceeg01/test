from services.media_etl.pipeline import Record,normalize
def test_reconciliation_and_quarantine():
    result=normalize([Record(2,"1"," TITLE ","2026-01-01","YouTube"),Record(3,"","Bad","2026/13/01","SPOTIFY")])
    assert result["counts"]=={"input":2,"accepted":1,"quarantined":1,"duplicates":0}
    assert result["accepted"][0]["platform"]=="youtube"
def test_repeat_input_is_deterministic():
    rows=[Record(2,"1","Title","2026-01-01","YouTube")]
    assert normalize(rows)==normalize(rows)