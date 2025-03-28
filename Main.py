from Mediator import Mediator


class Main:
    # returns 1 if the input is a movie name and 2 if it's a imdb-ID
    def getInputType(input):
        prefix = input[:2]
        suffix = input[2:]
        if prefix == "tt":
            try:
                int(suffix)
                return "2"
            except ValueError:
                return "1"
        else:
            return "1"

    if __name__ == '__main__':
        mediator = Mediator()
        print("------------------------------------")
        print("Welcome to the Movie Integrator 3000")
        print("")
        while 1:
            print("Please enter your movie name or imdb-ID")
            print("Enter 'stop' to leave")
            print("")

            user_input = input()
            user_input = user_input.lstrip()
            if user_input == "stop":
                break
            dir = getInputType(user_input)

            if dir == "1":
                print("Processing..")
                mediator.showData(user_input, "1")

            elif dir == "2":
                print("Processing..")
                mediator.showData(user_input, "2")
