import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

from mazegenerator import Maze
from wall_follower import WallFollower


def update(frame, follower_obj, img, maze):
    SOLUTION = [0, 255, 0]
    CURRENT = [255, 0, 0]
    maze[follower_obj.coords] = SOLUTION
    follower_obj.move()
    maze[follower_obj.coords] = CURRENT
    img.set_data(maze)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', '--mazesize', type=int, default=20)
    parser.add_argument('-L', '--followleft', action='store_true', default=False)
    args = parser.parse_args()

    maze = Maze(args.mazesize)

    copy_maze = maze.maze.copy()

    follower = WallFollower(maze, args.followleft)

    fig, ax = plt.subplots(figsize=(8, 8))
    img = plt.imshow(copy_maze)
    try:
        ani = FuncAnimation(fig, update, fargs=(follower, img, copy_maze), interval=1)
    except IndexError:
        pass
    plt.show()


if __name__ == '__main__':
    main()
