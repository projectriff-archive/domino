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
- creates functions, channels and subscriptions for "Hello 49" test
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
PS C:\Users\trisberg\workspace\domino> python .\domino.py
riff is for functions
Domino is FaaS Acceptance Test Suite for riff on Windows

***[ setup ]***
== checking riff version
domino> riff version
Version
  riff cli: 0.3.0-snapshot (13a8bca1d350c27121258c0a1c45990aee700759)

== installing riff
domino> riff system install --force
Installing Istio components
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/istio.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/istio/istio-riff-knative-serving-v0-4-0-patch.yaml
Istio components installed

Waiting for the Istio components to start .. all components are 'Running'

Installing Knative components
Applying resources defined in: https://storage.googleapis.com/knative-releases/build/previous/v0.4.0/build.yaml
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"
unable to recognize "STDIN": no matches for kind "Image" in version "caching.internal.knative.dev/v1alpha1"

Applying resources defined in: https://storage.googleapis.com/knative-releases/build/previous/v0.4.0/build.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/serving/previous/v0.4.0/serving.yaml
Applying resources defined in: https://raw.githubusercontent.com/knative/serving/v0.4.0/third_party/config/build/clusterrole.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/eventing.yaml
Applying resources defined in: https://storage.googleapis.com/knative-releases/eventing/previous/v0.4.0/in-memory-channel.yaml
Applying resources defined in: https://storage.googleapis.com/projectriff/riff-buildtemplate/riff-cnb-clusterbuildtemplate-0.2.0-snapshot-ci-a974b8e885d3.yaml
Knative components installed


riff system install completed successfully

== namespace init default
domino> riff namespace cleanup default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

domino> riff namespace init default --gcr ./push-image.json
Initializing namespace "default"

Creating secret "push-credentials" with basic authentication to server "https://gcr.io" for user "_json_key"
Creating serviceaccount "riff-build" using secret "push-credentials" in namespace "default"
Setting default image prefix to "gcr.io/cf-sandbox-trisberg" for namespace "default"

riff namespace init completed successfully

***[ functions ]***
== create function squarew
domino> riff function create squarew --git-repo https://github.com/projectriff-samples/node-square.git --artifact square.js --wait

riff function create completed successfully

domino> riff service invoke squarew --json -- -w \n -d 7
curl 35.238.161.31/ -H 'Host: squarew.default.example.com' -H 'Content-Type: application/json' -w '\n' -d 7
49

== delete service squarew
domino> riff service delete squarew

riff service delete completed successfully

== create function hellow
domino> riff function create hellow --git-repo https://github.com/projectriff-samples/java-hello.git --handler functions.Hello --wait

riff function create completed successfully

domino> riff service invoke hellow --text -- -w \n -d windows
curl 35.238.161.31/ -H 'Host: hellow.default.example.com' -H 'Content-Type: text/plain' -w '\n' -d windows
Hello windows

== delete service hellow
domino> riff service delete hellow

riff service delete completed successfully

***[ eventing ]***
== create channel numbers as in-memory-channel
domino> riff channel create numbers --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create channel squares as in-memory-channel
domino> riff channel create squares --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create channel replies as in-memory-channel
domino> riff channel create replies --cluster-provisioner in-memory-channel

riff channel create completed successfully

== create function square-1
domino> riff function create square-1 --git-repo https://github.com/projectriff-samples/node-square.git --artifact square.js --wait

riff function create completed successfully

== create function hello-2
domino> riff function create hello-2 --git-repo https://github.com/projectriff-samples/java-hello.git --handler functions.Hello --wait

riff function create completed successfully

== create subscription square-1 for numbers
domino> riff subscription create square-1 --channel numbers --reply squares --subscriber square-1

riff subscription create completed successfully

== create subscription hello-2 for squares
domino> riff subscription create hello-2 --channel squares --reply replies --subscriber hello-2

riff subscription create completed successfully

== create service correlator using image trisberg/correlator:v0.3.0
domino> riff service create correlator --image trisberg/correlator:v0.3.0

riff service create completed successfully

== create subscription correlator for replies
domino> riff subscription create correlator --channel replies --subscriber correlator

riff subscription create completed successfully

== invoking correlator with 7 for numbers
domino> riff service invoke correlator /default/numbers-channel-szzpr --json -- -H knative-blocking-request:true -w \n -d 7
curl 35.238.161.31/default/numbers-channel-szzpr -H 'Host: correlator.default.example.com' -H 'Content-Type: application/json' -H knative-blocking-request:true -w '\n' -d 7
Hello 49

== delete subscription correlator
domino> riff subscription delete correlator

riff subscription delete completed successfully

== delete subscription hello-2
domino> riff subscription delete hello-2

riff subscription delete completed successfully

== delete subscription square-1
domino> riff subscription delete square-1

riff subscription delete completed successfully

== delete service correlator
domino> riff service delete correlator

riff service delete completed successfully

== delete service hello-2
domino> riff service delete hello-2

riff service delete completed successfully

== delete service square-1
domino> riff service delete square-1

riff service delete completed successfully

== delete channel numbers
domino> riff channel delete numbers

riff channel delete completed successfully

== delete channel squares
domino> riff channel delete squares

riff channel delete completed successfully

== delete channel replies
domino> riff channel delete replies

riff channel delete completed successfully

***[ teardown ]***
== namespace cleanup default
domino> riff namespace cleanup default
Deleting serviceaccounts matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"
Deleting secrets matching label keys [projectriff.io/installer projectriff.io/version] in namespace "default"

riff namespace cleanup completed successfully

== uninstalling riff
domino> riff system uninstall --force --istio
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
