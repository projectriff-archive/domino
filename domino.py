import sys
import time
import argparse
import util

if __name__ == "__main__":
    start_time = time.time()
    print("riff is for functions")

    print("Domino is FaaS Acceptance Test Suite for riff and PFS on Windows\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("--pfs", help="test using pfs CLI", action="store_true")
    parser.add_argument("--manifest", help="the manifest to test with", type=str)
    parser.add_argument("--push-secret", help="the push secret to use for builds", type=str)
    parser.add_argument("--pull-secret", help="an optional pull secret to use for builds", type=str)
    parser.add_argument("--image-prefix", help="the image prefix to use", type=str)
    parser.add_argument("--skip-install", help="whether to skip the system install/uninstall", action="store_true")
    args = parser.parse_args()

    util.skip_install = args.skip_install
    if args.pfs:
        util.cli = "pfs"
    else:
        util.cli = "riff"
    if args.push_secret is None or len(args.push_secret) <= 0:
        util.push_secret = ""
    else:
        if args.image_prefix is None or len(args.image_prefix) <= 0:
            raise Exception("An --image-prefix must be provided when using --push-secret")
        util.push_secret = args.push_secret
        util.image_prefix = args.image_prefix
    if args.pull_secret is None or len(args.pull_secret) <= 0:
        util.pull_secret = ""
    else:
        util.pull_secret = args.pull_secret
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

    elapsed_time = time.time() - start_time
    elapsed_min = int(elapsed_time / 60)
    elapsed_sec = int(elapsed_time - (elapsed_min * 60))
    print("DONE in {m} min {s} sec".format(m=elapsed_min, s=elapsed_sec))
