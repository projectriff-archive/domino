import util

def run():
    print("***[ setup ]***")

    print("== checking {cli} version".format(cli=util.cli))
    output = util.run_cmd([util.cli, "version"])
    assert len(output) == 2
    if util.cli == "pfs":
        assert "pfs cli: 0.2.0" in output[1]
    else:
        assert "riff cli: 0.3.0" in output[1]

    print("== installing {cli}".format(cli=util.cli))

    if util.skip_install:
        print("skipping")
        print("deleting any subscriptions")
        util.run_cmd(["kubectl", "delete", "subscriptions", "--all"])
        print("deleting any channels")
        util.run_cmd(["kubectl", "delete", "channels", "--all"])
        print("deleting any kservices")
        util.run_cmd(["kubectl", "delete", "kservice", "--all"])
        print("")
    else:
        output = util.run_cmd([util.cli, "system", "install", "--manifest", util.manifest, "--force"])
        completed = output[len(output)-1]
        assert completed == "{cli} system install completed successfully".format(cli=util.cli)
        util.wait_for_webhook()

    print("== namespace init default")
    util.run_cmd([util.cli, "namespace", "cleanup", "default"])
    if util.docker_secret > "":
        output = util.run_cmd([util.cli, "namespace", "init", "default", "--manifest", util.manifest, "--secret", util.docker_secret, "--image-prefix", util.docker_user])
    else:
        output = util.run_cmd([util.cli, "namespace", "init", "default", "--manifest", util.manifest, "--gcr", "./push-image.json"])
    completed = output[len(output)-1]
    assert completed == "{cli} namespace init completed successfully".format(cli=util.cli)
