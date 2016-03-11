# -*- coding: utf-8 -*-


import sshrc.core.lexer
import sshrc.core.parser


def process(content):
    content = content.split("\n")
    content = sshrc.core.lexer.lex(content)
    content = sshrc.core.parser.parse(content)
    content = generate(content)
    content = "\n".join(content)

    return content


def generate(tree):
    for host in flat(tree):
        yield "Host {}".format(host.fullname)
        for option, value in sorted(host.options.items()):
            yield "    {} {}".format(option, value)
        yield ""


def flat(tree):
    for host in sorted(tree.childs, key=lambda h: (h.name == "*", h.name)):
        yield from flat_host_data(host)


def flat_host_data(tree):
    for host in tree.hosts:
        yield from flat_host_data(host)
    if tree.trackable:
        yield tree
