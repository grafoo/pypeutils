from os import linesep
from unittest.mock import patch, call
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


def test_util_reuse_pipe_printf_grep_cut():
    printf = Util("printf")
    grep = Util("grep")
    cut = Util("cut")
    assert str(
        printf("'cat,dog,kraken\ncat,ape,kraken\n'") | grep("dog") | cut("-d ',' -f 3")
    ) == "kraken{}".format(linesep)
    assert str(
        printf("'tent;house;space station\ntent;trailer;space station\n'")
        | grep("trailer")
        | cut("-d; -f3")
    ) == "space station{}".format(linesep)


def test_pipe_printf_grep_cut_cut():
    printf = Util("printf")
    grep = Util("grep")
    cut = Util("cut")
    assert str(
        printf("'cat,dog,kraken\ncat,ape,kraken\n'") | grep("dog") | cut("-d ',' -f 3")
    ) == "kraken{}".format(linesep)
    assert str(
        printf("'tent;house;space station\ntent;trailer;space station\n'")
        | grep("trailer")
        | cut("-d; -f3")
        | cut("-d ' ' -f 1")
    ) == "space{}".format(linesep)


@patch("sys.stdout")
def test_quick_print(mock_stdout):
    echo = Util("echo")
    -echo("Kwik-E-Mart")
    assert mock_stdout.mock_calls == [call.write("Kwik-E-Mart{}".format(linesep))]
