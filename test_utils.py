from os import linesep
from .utils import Util


def test_call_echo():
    echo = Util("echo")
    assert str(
        echo("Patience you must have my young padawan.")
    ) == "Patience you must have my young padawan.{}".format(linesep)


def test_call_printf():
    printf = Util("printf")
    assert (
        str(printf("'Powerful you have become, the dark side I sense in you.'"))
        == "Powerful you have become, the dark side I sense in you."
    )


def test_pipe_echo_rev():
    echo = Util("echo")
    rev = Util("rev")
    assert str(echo("live") | rev()) == "evil{}".format(linesep)


def test_pipe_printf_grep_cut():
    printf = Util("printf")
    grep = Util("grep")
    cut = Util("cut")
    assert str(
        printf("'cat,dog,kraken\ncat,ape,kraken\n'") | grep("dog") | cut("-d ',' -f 3")
    ) == "kraken{}".format(linesep)
