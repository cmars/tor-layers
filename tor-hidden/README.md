# tor-hidden

tor-hidden implements the http interface with a reverseproxy endpoint. Relating
to a website endpoint will publish that website as a
[Tor](https://www.torproject.org/) [hidden service](https://tor.eff.org/docs/tor-hidden-service.html.en).

For security reasons, this instance of Tor does not operate as a relay.

# Example

## Deploying your own "hidden wiki"

Turn that wiki:

```
$ juju deploy mediawiki
$ juju deploy mysql
$ juju add-relation mediawiki:db mysql:db
```

into a hidden wiki:

```
$ juju deploy local:trusty/tor-hidden
$ juju add-relation mediawiki:website tor-hidden:reverseproxy
```

Get the hidden service hostname with:

```
$ juju run --service mediawiki 'cat /var/lib/tor/mediawiki/hostname'
at4rj2khrro462we.onion
```

# Disclaimer

This charm is experimental. Use at your own risk.

# License

Copyright 2015 Casey Marshall.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

