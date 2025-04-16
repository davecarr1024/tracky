from tracky.visuals import Visualizer
from tracky.sim import Sim
from tracky.track import Grid
from tracky.cars import CarManager

def main():
    grid = Grid()
    cars = CarManager()
    sim = Sim(grid, cars)
    visualizer = Visualizer(sim)
    visualizer.run()


if __name__ == "__main__":
    main()
