class TuringMachine:
    def __init__(self, states, symbols, transitions, initial_state, final_states):
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        self.current_state = initial_state
        self.final_states = final_states
        self.tape = []
        self.head_position = 0

    def initialize_tape(self, input_sequence):
        self.tape = list(input_sequence)
        self.head_position = 0

    def run(self):
        try:
            while self.current_state not in self.final_states:
                if self.head_position >= len(self.tape):
                    self.tape.append('_')  # Blank symbol if we reach the end of the tape

                current_symbol = self.tape[self.head_position]

                if (self.current_state, current_symbol) not in self.transitions:
                    raise ValueError("Transition not defined. Turing machine rejects.")

                next_state, write_symbol, action, new_state = self.transitions[(self.current_state, current_symbol)]

                # Modification du contenu du ruban si la troisième position est 0 ou 1
                if action in {'0', '1'}:
                    self.tape[self.head_position] = action

                # Mise à jour de l'état et de la position de la tête de lecture
                self.current_state = new_state
                if action == 'R':
                    self.head_position += 1
                elif action == 'L':
                    self.head_position -= 1

                self.print_tape()

            if self.current_state in self.final_states:
                print("Turing machine accepted.")
        except Exception as e:
            print(f"Error: {e}")

    def print_tape(self):
        print("State: {}, Tape: {}".format(self.current_state, ''.join(self.tape)))


def parse_transition(transition_input):
    parts = transition_input.split(',')
    if len(parts) != 4:
        raise ValueError("Invalid transition format.")
    current_state, read_symbol, action, new_state = parts
    if action not in {'L', 'R', '0', '1'}:
        raise ValueError("Invalid action. Use 'L', 'R', '0', or '1'.")
    return current_state, read_symbol, action, new_state


def main():
    try:
        states = input("Enter states (comma-separated): ").split(',')
        symbols = input("Enter tape symbols (comma-separated): ").split(',')
        final_states = input("Enter final states (comma-separated): ").split(',')
        if not set(final_states).issubset(set(states)):
            raise ValueError("Final states must be included in the list of states.")

        transitions = {}
        while True:
            transition_input = input("Enter transition (or type 'exit' to finish): ")
            if transition_input.lower() == 'exit':
                break
            current_state, read_symbol, action, new_state = parse_transition(transition_input)

            if current_state not in states or new_state not in states:
                raise ValueError("Transition states must be included in the list of states.")
            if read_symbol not in symbols:
                raise ValueError("Read symbol must be included in the list of tape symbols.")

            transitions[(current_state, read_symbol)] = (new_state, read_symbol, action, new_state)

        initial_state = input("Enter initial state: ")
        if initial_state not in states:
            raise ValueError("Initial state must be included in the list of states.")

        input_sequence = input("Enter input sequence on the tape: ")

        turing_machine = TuringMachine(states, symbols, transitions, initial_state, final_states)
        turing_machine.initialize_tape(input_sequence)
        turing_machine.run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
