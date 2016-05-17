# tox-easy-bootstrap

Simple util to create and update tox-bootstrapd.conf with public online and private node list and restart service if needed. Allows to simple configure and maintain up to date Tox node.

# Usage

Edit template config `/etc/tox-easy-bootstrap.conf` and run `/bin/tox-easy-bootstrap` to regenerate `/etc/tox-bootstrapd.conf` and restart `tox-bootstrapd` service (if needed and enabled in template config).
