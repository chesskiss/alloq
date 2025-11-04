from app import analyzer

def test_detect_algorithms_empty():
    assert analyzer.detect_algorithms("") == []

def test_detect_algorithms_fft():
    code = "def my_fft(): # uses FFT here"
    algos = analyzer.detect_algorithms(code)
    assert "Fast Fourier Transform" in algos
