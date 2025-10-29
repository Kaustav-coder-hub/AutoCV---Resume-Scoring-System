from core.parser import parse_resume

def test_parse_resume_returns_dict():
    res = parse_resume('tests/sample_resume.pdf')
    assert 'text' in res
    assert 'sections' in res
