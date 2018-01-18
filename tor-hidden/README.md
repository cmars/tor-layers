# tor-hidden

tor-hidden implements the http interface with a reverseproxy endpoint. Relating
to a website endpoint will publish that website as a
[Tor](https://www.torproject.org/) [hidden service](https://tor.eff.org/docs/tor-hidden-service.html.en).

For security reasons, this instance of Tor does not operate as a relay.

# Example

## Deploying your own hidden website using the apache2 charm

Turn that website:

```
$ juju deploy apache2
```

into a hidden website:

```
$ juju deploy local:xenial/tor-hidden
$ juju add-relation apache2:website tor-hidden:reverseproxy
```

The hidden service hostname will be visible via juju status

```
$ juju status | grep \.onion
tor-hidden/0*  active    idle   1        192.168.2.60           tor service ready: service apache2 running on wl2f5pijubf33mjb.onio
```

# Source

This charm was built from [tor-layers](https://github.com/cmars/tor-layers).

# Disclaimer

Use at your own risk and peril.

This charm makes it easy to deploy a hidden service and attempts to do it well,
but it is no substitute for the flawless execution of operational security
needed to host things anonymously.

Know your threat model. Know and understand your potential exposure. _Any_
activity in your private service that correlates with external activity
(network traffic, resource consumption) reveals the true network location of
your deployment over time.

# License

Copyright 2015, 2016 Casey Marshall.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
