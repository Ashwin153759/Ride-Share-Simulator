
from event import create_event_list
from simulation import Simulation

if __name__ == '__main__':
    event_list = create_event_list("a1_my_events.txt")

    sim = Simulation()

    results = sim.run(event_list)
    print(results)
