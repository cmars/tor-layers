# tor-layers

This project builds Juju charms that deploy [Tor](https://www.torproject.org/):

- [tor-relay](tor-relay/README.md), which just operates a relay to support the network
- [tor-hidden](tor-hidden/README.md), which is used to publish hidden services
- [tor-bridge](tor-bridge/README.md), which operates a bridge

# Requirements

- charm-tools 1.8.0
- Juju 1.24 or newer recommended

# Building

`make all` will build the charms at `../trusty` from this directory.

Use `make REPO=/path/to/repo all` to build the charms somewhere else.

# Usage

See the README files:
- [tor-relay](tor-relay/README.md)
- [tor-hidden](tor-hidden/README.md)
- [tor-bridge](tor-bridge/README.md)

# Known Issues

The charm fails the install hook in network environments where torproject.org
is blocked. For example, OpenDNS does not resolve the domain properly.

If this happens, you can `juju resolved --retry` on the unit after fixing the
DNS/networking issue.

# TODO

- subordinate charm to route all traffic through Tor
- obfuscation proxy support?

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

