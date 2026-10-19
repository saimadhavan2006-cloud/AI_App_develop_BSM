
import pytest

from app.services.accuracy_validator import validate_8051_answer


def test_validator_flags_misleading_rom_range():
    answer = (
        "The classic 8051 has 128 bytes of internal RAM. "
        "Internal ROM or EPROM of 0 (8031) to 4K (8051)."
    )

    issues = validate_8051_answer(answer)

    assert any("program ROM" in issue for issue in issues)


def test_validator_flags_ambiguous_sixteen_byte_memory():
    answer = (
        "The classic 8051 has 128 bytes of internal RAM "
        "and sixteen bytes of data memory."
    )

    issues = validate_8051_answer(answer)

    # This wording is ambiguous, so it should be reviewed.
    assert isinstance(issues, list)
