import util

def run():
    print("== namespace cleanup default")
    output = util.run_cmd(["riff", "namespace", "cleanup", "default"])
    completed = output[len(output)-1]
    assert completed == "riff namespace cleanup completed successfully"

    print("== uninstalling riff")
    if util.skip_install:
        print("skipping\n")
    else:
        output = util.run_cmd(["riff", "system", "uninstall", "--force", "--istio"])
        completed = output[len(output)-1]
        assert completed == "riff system uninstall completed successfully"
