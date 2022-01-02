from mlib import human_readable_payload, scale_input#, height_human
import numpy as np
import pytest
from click.testing import CliRunner
#from cli import predictcli
#import utilscli


def test_human_readable_payload():
    result = human_readable_payload(1.5)
    assert 1.5 == result['value_log']
    assert "4.48 euros" == result['value_money']

