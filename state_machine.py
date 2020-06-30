# built-in libraries
import argparse
import random
import robopy.base.model as robot
import sys
import numpy as np
import time
from robopy.base import pose
from robopy import rpy2r
from commands.moves import move_lin, move_j
from statemachine import StateMachine, State, Transition

from Generator import Generator

from positions import *
from options import *
from paths import *
from input_seq import *

model = robot.Puma560()

def run():
    master_states = [State(**opt) for opt in options]

    form_to = [
        [0, [1, 9]],
        [1, [0, 2, 9]],
        [2, [3, 9]],
        [3, [4, 9]],
        [4, [1, 5, 6, 7, 9]],
        [5, [1, 9]],
        [6, [8, 9]],
        [7, [8, 9]],
        [8, [1, 9]],
        [9, [10]],
        [10, [0, 1, 2, 3, 4, 5, 6, 7, 8]]
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

    input = input_sequence

    paths = [path_bases[key] for key in input]

    init_state = "idle"
    path_array = []
    start = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    previous_position = start

    for path in paths:

        supervisor = Generator.create_master(master_states, master_transitions)
        print('\n' + str(supervisor))

        print("Executing path: {}".format(path))
        

        for event in path:

            master_transitions[event]._run(supervisor)
            print(supervisor.current_state)

            if supervisor.current_state.value == "idle":                
                path1 = move_j(robot, previous_position, start)
                previous_position = start
                path_array.append(path1)
                print("Supervisor done!")

            if supervisor.current_state.value == "scan":                
                path1 = move_j(robot, previous_position, scan)
                previous_position = scan
                path_array.append(path1)

            if supervisor.current_state.value == "grip":                
                path1 = move_j(robot, previous_position, grip)
                previous_position = grip
                path_array.append(path1)

            if supervisor.current_state.value == "evaluate":                
                path1 = move_j(robot, previous_position, evaluate)
                previous_position = evaluate
                path_array.append(path1)

            if supervisor.current_state.value == "trash":                
                path1 = move_j(robot, previous_position, trash)
                previous_position = trash
                path_array.append(path1)

            if supervisor.current_state.value == "transport_a":                
                path1 = move_j(robot, previous_position, transport_a)
                previous_position = transport_a
                path_array.append(path1)

            if supervisor.current_state.value == "transport_b":                
                path1 = move_j(robot, previous_position, transport_b)
                previous_position = transport_b
                path_array.append(path1)

            if supervisor.current_state.value == "detach":
                if previous_position == trash:  
                    path1 = move_j(robot, previous_position, detach)
                    previous_position = detach

                elif previous_position == transport_a:                    
                    path1 = move_j(robot, previous_position, detach_a)
                    previous_position = detach_a

                elif previous_position == transport_b:                    
                    path1 = move_j(robot, previous_position, detach_b)
                    previous_position = detach_b
                path_array.append(path1)

            if random.randint(0, 100) > 90:
                idx = options_idx[supervisor.current_state.value]
                master_transitions[f'm_{idx}_9']._run(supervisor)
                print(supervisor.current_state)
                master_transitions['m_9_10']._run(supervisor)
                print(supervisor.current_state)
                print("Monkeys are repairing machine...")
                n = 100
                for i in range(n):
                    if i % 10 == 0:
                        print("Repairing machine ({}%)".format(100 * i // n))
                        time.sleep(0.01)

                master_transitions[f'm_{10}_{idx}']._run(supervisor)
                print("Recovered from fatal crash!")
                print(supervisor.current_state)

    path = np.concatenate(path_array, axis=0)

    model.animate(stances=path, frame_rate=30, unit='deg')

if __name__ == '__main__':
    run()
