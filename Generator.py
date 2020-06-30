from statemachine import StateMachine, State, Transition
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
