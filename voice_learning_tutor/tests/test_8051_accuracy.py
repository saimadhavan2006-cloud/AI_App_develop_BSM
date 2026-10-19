from app.services.accuracy_validator import validate_8051_answer

import re

def test_good_answer_has_no_detected_issues():
    answer = """
    The classic 8051 has 128 bytes of internal RAM and 4 KB of
    on-chip program ROM. It has Timer 0 (T0) and Timer 1 (T1).
    SFRs occupy a separate address region.
    """
    assert validate_8051_answer(answer) == []


def test_detects_timer_typo():
    answer = """
    The classic 8051 has 128 bytes of internal RAM and 4 KB
    of program ROM. Its timers are TO and T1.
    """
    assert any("T0" in issue for issue in validate_8051_answer(answer))


def test_detects_sfr_memory_confusion():
    answer = """
    The classic 8051 has 128 bytes of internal RAM and 4 KB
    of program ROM, plus 128 bytes of special function register memory.
    """
    assert any("SFR" in issue for issue in validate_8051_answer(answer))


def test_detects_misleading_rom_range():
    answer = """
    The classic 8051 has internal ROM or EPROM of 0 to 4 KB.
    """
    issues = validate_8051_answer(answer)
    assert any("program ROM" in issue for issue in issues)


def test_detects_general_purpose_memory_mislabel():
    answer = "The 8051 has sixteen bytes of general-purpose data memory."
    issues = validate_8051_answer(answer)
    assert any("bit-addressable" in issue for issue in issues)


def test_detects_8_bit_program_counter():
    issues = validate_8051_answer(
        "The classic 8051 has an 8-bit Program Counter."
    )
    assert any("PC) is 16-bit" in issue for issue in issues)


def test_detects_16_bit_psw():
    issues = validate_8051_answer(
        "The classic 8051 has a 16-bit PSW."
    )
    assert any("PSW" in issue and "8-bit" in issue for issue in issues)


def test_detects_80_byte_general_purpose_ram_claim():
    issues = validate_8051_answer(
        "The classic 8051 has 80 bytes of general-purpose RAM."
    )
    assert any("128 bytes" in issue for issue in issues)


def test_accepts_classic_8051_internal_ram_statement():
    answer = (
        "Internal RAM: 128 bytes, organized into three areas. "
        "Internal ROM: 4 KB (variants differ)."
    )

    issues = validate_8051_answer(answer)

    assert not any(
        "128-byte internal RAM" in issue
        for issue in issues
    )



def test_accepts_correct_8051_ram_regions():
    answer = """
    The classic 8051 has 128 bytes of internal RAM.
    Register banks occupy 00H-1FH (32 bytes).
    Bit-addressable RAM occupies 20H-2FH (16 bytes).
    General-purpose RAM occupies 30H-7FH (80 bytes).
    These are three regions within the same 128-byte RAM.
    """

    issues = validate_8051_answer(
        answer,
        "Explain the internal RAM layout and address map.",
    )

    assert issues == []



def test_detects_incorrect_256_byte_internal_ram_total():
    answer = """
    The classic 8051 has 256 bytes of internal RAM.
    """
    issues = validate_8051_answer(answer)
    assert issues


def test_detects_additional_ram_claim():
    answer = """
    The classic 8051 has 128 bytes of internal RAM,
    plus an additional 80 bytes of general-purpose RAM.
    """
    issues = validate_8051_answer(answer)
    assert any(
        "additional memory" in issue or "128 bytes" in issue
        for issue in issues
    )


def test_requires_regions_when_question_asks_for_ram_layout():
    answer = """
    The classic 8051 has 128 bytes of internal RAM.
    """
    issues = validate_8051_answer(
        answer,
        "Explain the internal RAM layout and address map.",
    )
    assert any("RAM layout" in issue for issue in issues)
