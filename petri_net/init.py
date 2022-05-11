from xml.dom.minicompat import NodeList
from pip import main
from snakes.nets import * 


def create_net():
    net = PetriNet('MyNet')

    for i in list(range(1,5)):
        p = Place(i, 1)
        net.add_place(p)

    for i in list(range(1,8)):
        t = Transition(i)
        net.add_transition
    
    # connect places with transitions 
    


def main():
    create_net


if __name__ == "__main__":
    main()