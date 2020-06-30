options = [
        {"name": "IDLE", "initial": True, "value": "idle"},  # 0
        {"name": "SCAN", "initial": False, "value": "scan"},  # 1
        {"name": "CLASSIFY", "initial": False, "value": "classify"},  # 2
        {"name": "GRIP", "initial": False, "value": "grip"},  # 3
        {"name": "EVALUATE", "initial": False, "value": "evaluate"},  # 4
        {"name": "TRASH", "initial": False, "value": "trash"},  # 5
        {"name": "TRANSPORT_A", "initial": False, "value": "transport_a"},  # 6
        {"name": "TRANSPORT_B", "initial": False, "value": "transport_b"},  # 7
        {"name": "DETACH", "initial": False, "value": "detach"},  # 8
        {"name": "FAILED", "initial": False, "value": "failed"},  # 9
        {"name": "MALFUNCTION_SERVICE", "initial": False, "value": "malfunction_service"},  # 10
    ]

options_idx = {
        "idle" : 0,
        "scan" : 1,
        "classify" : 2,
        "grip" : 3,
        "evaluate" : 4,
        "trash" : 5,
        "transport_a" : 6,
        "transport_b" : 7,
        "detach" : 8,
        "failed" : 9,
        "malfunction" : 10
}