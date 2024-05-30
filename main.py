import pathlib
import sys



def main():
    # Get the command from the file given and move it
    # to the file the rover is watching (default is Rover1)



    rover_name = "Rover1"

    config_file_path = pathlib.Path("config")

    try:
        config_file_fd = open(config_file_path, "r")
        try:
            rover_communication_file_path = config_file_fd.readline()
        except:
            print("failed to read config file")

    except:
        config_file_fd = open(config_file_path, "w+")
        config_file_fd.write("Rover.txt")
        config_file_fd.close()

        config_file_fd = open(config_file_path, "r")
        rover_communication_file_path = config_file_fd.readline()

    finally:
        config_file_fd.close()

    fcontent = None
    filepath = pathlib.Path(rover_communication_file_path)
    with filepath.open() as f:
        fcontent = f.read()

    with pathlib.Path(pathlib.Path(__file__).parent.resolve(), "Rover.txt").open("w") as f:
        f.write(fcontent)

    print("Command sent successfully! See the rover for more details")


if __name__ == "__main__":
    main()
