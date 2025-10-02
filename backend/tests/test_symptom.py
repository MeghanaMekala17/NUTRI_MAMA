import pytest
from app.services.huggingface_service import analyze_symptoms

def test_analyze_symptoms():
    text = "I have a headache and mild fever"
    result = analyze_symptoms(text)
    assert "label" in result
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0
