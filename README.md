# domino

Domino is a FaaS Acceptance Test Suite for riff on Windows

What you need:

- a recent build of `riff` available on the system path
- a recent install of `kubectl` available on the system path
- a json key file for a service account with push credentials to the GCR repo you are using
- a Kubernetes cluster that can run riff running on GKE - see https://projectriff.io/docs/getting-started/gke/ 
- a recent version of Python 3

What it does:

- runs everything from a Windows PowerShell
- uses `riff` and `kubectl` commands for everything
- installs Istio, Knative and riff (optional)
- prepares the default namespace for GCR push
- creates and tests JavaScript and Java functions
- creates functioons, channels and subscriptions for "Hello 49" test
- cleans up the namespace
- uninstalls Istio, Knative and riff (optional)

## prepare

Clone the repo:

```[bash]
git clone https://github.com/trisberg/domino.git
cd domino
```

Create the json key file:

```[bash]
cp /path/to/my/key-file.json push-image.json
```

_NOTE_: It must be named `push-image.json` and located in the root directory of the cloned repo.

Run the tests:

```[bash]
python ./domino.py
```

_NOTE_: Depending on how Python is installed you should use either `python` or `python3`

_NOTE_: If you already have riff/Knative installed you can add the arg `--skip-install` to keep what you already have.

That's it.

## example run

```[bash]
Aruba:domino trisberg$ python3 ./domino.py
riff is for functions
Domino is FaaS Acceptance Test Suite for Windows

***[ setup ]***
== checking riff version
Version
  riff cli: 0.3.0-snapshot (d798e3b14403f0177f4cde2ad0dbff12396fbd22)

== installing riff
Installing Istio components
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/istio.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/istio/istio-riff-knative-serving-v0-4-0-patch.yaml
Istio components installed

Waiting for the Istio components to start ... all components are 'Running'

Installing Knative components
Applying resources defined in: https://storage.googleapis.com/knative-releases/build/previous/v0.4.0/build.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/serving.yaml
Applying resources defined in: https://raw.githubusercontent.com/knative/serving/v0.4.0/third_party/config/build/clusterrole.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/eventing.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/in-memory-channel.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/riff-buildtemplate/riff-cnb-clusterbuildtemplate-0.2.0-snapshot-ci-a974b8e885d3.yaml
Knative components installed


riff system install completed successfully

== namespace init default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

Initializing namespace "default"

Creating secret "push-credentials" with basic authentication to server "https://gcr.io" for user "_json_key"
Creating serviceaccount "riff-build" using secret "push-credentials" in namespace "default"
Setting default image prefix to "gcr.io/cf-sandbox-trisberg" for namespace "default"

riff namespace init completed successfully

***[ functions ]***
== create function squarew

riff function create completed successfully

curl 35.238.161.31/ -H 'Host: squarew.default.example.com' -H 'Content-Type: application/json' -w '\n' -d 7
49

== delete service squarew

riff service delete completed successfully

== create function hellow

riff function create completed successfully

curl 35.238.161.31/ -H 'Host: hellow.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d windows
Hello windows

== delete service hellow

riff service delete completed successfully

***[ eventing ]***
== create channel numbers as in-memory-channel

riff channel create completed successfully

== create channel squares as in-memory-channel

riff channel create completed successfully

== create channel replies as in-memory-channel

riff channel create completed successfully

== create function square-1

riff function create completed successfully

== create function hello-2

riff function create completed successfully

== create subscription square-1 for numbers

riff subscription create completed successfully

== create subscription hello-2 for squares

riff subscription create completed successfully

== create service correlator using image trisberg/correlator:v0.3.0

riff service create completed successfully

== create subscription correlator for replies

riff subscription create completed successfully

== invoking correlator with 7 for numbers
curl 35.238.161.31/default/numbers-channel-cxnww -H 'Host: correlator.default.example.com' -H 'Content-Type: application/json' -H knative-blocking-request:true -w '\n' -d 7
Hello 49

== delete subscription correlator

riff subscription delete completed successfully

== delete subscription hello-2

riff subscription delete completed successfully

== delete subscription square-1

riff subscription delete completed successfully

== delete service correlator

riff service delete completed successfully

== delete service hello-2

riff service delete completed successfully

== delete service square-1

riff service delete completed successfully

== delete channel numbers

riff channel delete completed successfully

== delete channel squares

riff channel delete completed successfully

== delete channel replies

riff channel delete completed successfully

***[ teardown ]***
== namespace cleanup default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

== uninstalling riff
Deleting Knative services
Removing Knative for riff components
Deleting CRDs for knative.dev
Deleting clusterrolebindings prefixed with knative-
Deleting clusterrolebindings prefixed with build-controller-
Deleting clusterrolebindings prefixed with eventing-controller-
Deleting clusterrolebindings prefixed with in-memory-channel-
Deleting clusterroles prefixed with in-memory-channel-
Deleting clusterroles prefixed with knative-
Deleting service/knative-ingressgateway resource in istio-system
Deleting horizontalpodautoscaler/knative-ingressgateway resource in istio-system
Deleting deployment/knative-ingressgateway resource in istio-system
Deleting resources defined in: knative-eventing
Deleting resources defined in: knative-serving
Deleting resources defined in: knative-build
Deleting resources defined in: knative-monitoring
Namespace "knative-monitoring" was not found
Removing Istio components
Deleting CRDs for istio.io
Deleting clusterrolebindings prefixed with istio-
Deleting clusterroles prefixed with istio-
Deleting mutatingwebhookconfigurations prefixed with istio-
Deleting resources defined in: istio-system

riff system uninstall completed successfully

DONE!
```
