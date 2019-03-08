import sys
import util

if __name__ == "__main__":
    print("riff is for functions")
    print("Domino is FaaS Acceptance Test Suite for riff on Windows\n")

    util.skip_install = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--skip-install":
            util.skip_install = True

    import setup, teardown, functions, eventing
    setup.run()
    functions.run()
    eventing.run()
    teardown.run()

    print("DONE!")
