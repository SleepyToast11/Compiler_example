import pathlib
import sys

from satelite import ROVER_COMMAND_FILES


def main():
    # Get the command from the file given and move it
    # to the file the rover is watching (default is Rover1)
    rover_name = "Rover1"
    if len(sys.argv) < 1:
        raise Exception("Missing file path to parse.")


    fcontent = None
    filepath = pathlib.Path(sys.argv[1])
    with filepath.open() as f:
        fcontent = f.read()

    with pathlib.Path(pathlib.Path(__file__).parent.resolve(), "Rover1.txt").open("w") as f:
        f.write(fcontent)

    print("Command sent successfully! See the rover for more details")


if __name__ == "__main__":
    main()
