from mlib import human_readable_payload, get_position_zone, scale_target

import numpy as np
import pandas as pd


def test_human_readable_payload():
    result = human_readable_payload(1.5)
    assert 1.5 == result["value_log"]
    assert "4.48 euros" == result["value_money"]


def test_get_position_zone():
    # intialise data of lists.
    data = {
        "preferred_positions": [["LF", "RF", "CAM"], ["CAM"], ["LWB", "RWB", "RB"]],
        "name": ["test1", "test2", "test3"],
    }
    # Create DataFrame
    df = pd.DataFrame(data)
    result = get_position_zone(df)
    assert ["ATTACKING", "MIDFIELD", "DEFENDING"] == result["position_zone"].tolist()


def test_scale_target():
    # intialise data of lists.
    data = {"Value": [1, 3, 4, 3, 4, 5]}

    # Create DataFrame
    df = pd.DataFrame(data)
    result = scale_target([[1]], df)
    assert 1.62 == float(np.round(result, 2))
