import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import (  # nets from loading plugins, found at runtime
    PetriNet,
    Transition,
    Variable,
    Value,
    Place
)


def create_net():
    net = PetriNet('MyNet')

    # create places
    for i in list(range(1, 5)):
        p = Place(str(i), [1])
        net.add_place(p)

    # create transitions
    t1 = Transition('t1')
    t2 = Transition('t2')
    net.add_transition(t1)
    net.add_transition(t2)

    # connect places with transitions
    net.add_input('1', 't1', Variable('x'))
    net.add_input('1', 't2', Value(1))
    net.add_output('2', 't1', Value(2))
    net.add_input('3', 't2', Value(1))
    net.add_output('2', 't2', Value(1))
    net.add_output('3', 't1', Value(2))

    print(net.transition('t1').modes())

    return net


def draw_place(place, attr):
    attr['label'] = place.name.upper()
    attr['color'] = '#FF0000'


def draw_transition(trans, attr):
    if str(trans.guard) == 'True':
        attr['label'] = trans.name
    else:
        attr['label'] = '%s\n%s' % (trans.name, trans.guard)


def main():
    net = create_net()
    net.draw('my_net.png', place_attr=draw_place, trans_attr=draw_transition)


if __name__ == "__main__":
    main()
