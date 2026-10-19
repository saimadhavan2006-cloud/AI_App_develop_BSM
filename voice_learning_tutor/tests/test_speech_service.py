
from app.services.speech_service import prepare_text_for_speech


def test_8051_pronunciation():
    result = prepare_text_for_speech("The 8051 is a microcontroller.")
    assert "eighty fifty one" in result


def test_uart_adc_dac_pronunciation():
    result = prepare_text_for_speech("UART, ADC, and DAC")
    assert "U A R T" in result
    assert "A D C" in result
    assert "D A C" in result


def test_case_insensitive_replacements():
    result = prepare_text_for_speech("uart and adc")
    assert "U A R T" in result
    assert "A D C" in result


def test_unrelated_text_remains_unchanged():
    text = "Explain the working of a transistor."
    assert prepare_text_for_speech(text) == text


def test_empty_text():
    assert prepare_text_for_speech("") == ""
