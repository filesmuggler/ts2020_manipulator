# built-in libraries
import argparse
import robopy.base.model as robot
import sys
import numpy as np
from robopy.base import pose
from robopy import rpy2r
from commands.moves import move_lin, move_j

from statemachine import StateMachine, State, Transition

model = robot.Puma560()


class Generator(StateMachine):
    states = []
    transitions = []
    states_map = {}
    current_state = None

    def __init__(self, states, transitions):

        self.states = []
        self.transitions = []
        self.states_map = {}
        self.current_state = states[0]

        for s in states:
            setattr(self, str(s.name).lower(), s)
            self.states.append(s)
            self.states_map[s.value] = str(s.name)

        for key in transitions:
            setattr(self, str(transitions[key].identifier).lower(), transitions[key])
            self.transitions.append(transitions[key])

        super(Generator, self).__init__()

    def __repr__(self):
        return "{}(model={!r}, state_field={!r}, current_state={!r})".format(
            type(self).__name__, self.model, self.state_field,
            self.current_state.identifier,
        )

    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)


def run():
    options = [
        {"name": "IDLE", "initial": True, "value": "idle"},  # 0
        {"name": "SCAN", "initial": False, "value": "scan"},  # 1
        {"name": "CLASSIFY", "initial": False, "value": "classify"},  # 2
        {"name": "GRIP", "initial": False, "value": "grip"},  # 3
        {"name": "EVALUATE", "initial": False, "value": "evaluate"},  # 4
        {"name": "TRASH", "initial": False, "value": "trash"},  # 5
        {"name": "TRANSPORT_A", "initial": False, "value": "transport_a"},  # 6
        {"name": "TRANSPORT_B", "initial": False, "value": "transport_b"},  # 7
        {"name": "DETACH", "initial": False, "value": "detach"}  # 8
    ]

    master_states = [State(**opt) for opt in options]

    form_to = [
        [0, [1]],
        [1, [0, 2]],
        [2, [3]],
        [3, [4]],
        [4, [1, 5, 6, 7, ]],
        [5, [1]],
        [6, [8]],
        [7, [8]],
        [8, [1]],
    ]

    master_transitions = {}
    for indices in form_to:
        from_idx, to_idx_tuple = indices
        for to_idx in to_idx_tuple:
            op_identifier = "m_{}_{}".format(from_idx, to_idx)

            transition = Transition(master_states[from_idx],
                                    master_states[to_idx],
                                    identifier=op_identifier)
            master_transitions[op_identifier] = transition

            master_states[from_idx].transitions.append(transition)

    path_red = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_6", "m_6_8", "m_8_1", "m_1_0"]
    path_blue = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_7", "m_7_8", "m_8_1", "m_1_0"]
    path_trash = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_5", "m_5_1", "m_1_0"]
    path_nothing = ["m_0_1", "m_1_0"]

    path_bases = {'R': path_red, 'B': path_blue, 'T': path_trash, 'N': path_nothing}

    input = ['R', 'B', 'B', 'T', 'N', 'R', 'R', 'T']

    paths = [path_bases[key] for key in input]

    init_state = "idle"
    path_array = []
    start = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    previous_position = start

    for path in paths:

        supervisor = Generator.create_master(master_states, master_transitions)
        print('\n' + str(supervisor))

        print("Executing path: {}".format(path))
        trash = [-90.0, 120.0, 30.0, 0.0, 0.0, 0.0]
        transport_a = [180.0, 120.0, 30.0, 0.0, 0.0, 0.0]
        transport_b = [0.0, 120.0, 30.0, 0.0, 0.0, 0.0]

        for event in path:

            master_transitions[event]._run(supervisor)
            print(supervisor.current_state)

            if supervisor.current_state.value == "idle":
                start = [90.0, 30.0, 30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, start)
                previous_position = start
                path_array.append(path1)
                print("Supervisor done!")

            if supervisor.current_state.value == "scan":
                scan = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, scan)
                previous_position = scan
                path_array.append(path1)

            if supervisor.current_state.value == "classify":
                pass

            if supervisor.current_state.value == "grip":
                grip = [90.0, 120.0, 30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, grip)
                previous_position = grip
                path_array.append(path1)

            if supervisor.current_state.value == "evaluate":
                evaluate = [90.0, 120.0, -30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, evaluate)
                previous_position = evaluate
                path_array.append(path1)

            if supervisor.current_state.value == "trash":
                trash = [-90.0, 120.0, 30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, trash)
                previous_position = trash
                path_array.append(path1)

            if supervisor.current_state.value == "transport_a":
                transport_a = [180.0, 120.0, 30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, transport_a)
                previous_position = transport_a
                path_array.append(path1)

            if supervisor.current_state.value == "transport_b":
                transport_b = [0.0, 120.0, 30.0, 0.0, 0.0, 0.0]
                path1 = move_j(robot, previous_position, transport_b)
                previous_position = transport_b
                path_array.append(path1)

            if supervisor.current_state.value == "detach":
                if previous_position == trash:
                    detach = previous_position
                    path1 = move_j(robot, previous_position, detach)
                    previous_position = detach

                elif previous_position == transport_a:
                    detach = previous_position
                    path1 = move_j(robot, previous_position, detach)
                    previous_position = detach

                elif previous_position == transport_b:
                    detach = previous_position
                    path1 = move_j(robot, previous_position, detach)
                    previous_position = detach
                path_array.append(path1)

    path = np.concatenate(path_array, axis=0)

        #print(path)
        #model.animate(stances=path, frame_rate=30, unit='deg')
    print(path)
    model.animate(stances=path, frame_rate=30, unit='deg')


if __name__ == '__main__':
    run()
