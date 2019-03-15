import sys
import argparse
import util

if __name__ == "__main__":
    print("riff is for functions")

    print("Domino is FaaS Acceptance Test Suite for riff and PFS on Windows\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("--pfs", help="test using pfs CLI", action="store_true")
    parser.add_argument("--manifest", help="the manifest to test with", type=str)
    parser.add_argument("--skip-install", help="whether to skip the system install/uninstall", action="store_true")
    args = parser.parse_args()

    util.skip_install = args.skip_install
    if args.pfs:
        util.cli = "pfs"
    else:
        util.cli = "riff"
    if args.manifest is None or len(args.manifest) <= 0:
        if args.pfs:
            raise Exception("A manifest must be provided for PFS")
        util.manifest = "stable"
    else:
        util.manifest = args.manifest

    import setup, teardown, functions, eventing
    setup.run()
    functions.run()
    eventing.run()
    teardown.run()

    print("DONE!")
