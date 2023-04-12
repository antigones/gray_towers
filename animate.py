import urwid
from gray_hanoi import GrayHanoi
from gray_bucharest import GrayBucharest

frame = 0


def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()


def refresh(_loop, _data):
    outputTxt = gray_hanoi.pretty_print_configuration(
        configurations[_data % len(configurations)])

    txt.set_text(outputTxt)
    _data += 1
    loop.set_alarm_in(0.5, refresh, _data)


# gray_hanoi = GrayHanoi(n_pegs=3, n_disks=5)
gray_hanoi = GrayBucharest(n_pegs=3, n_disks=3)
configurations = gray_hanoi.solve(verbose=False)

outputTxt = gray_hanoi.pretty_print_configuration(
    configurations[frame])

txt = urwid.Text(outputTxt)
fill = urwid.Filler(txt, 'top')

loop = urwid.MainLoop(fill, unhandled_input=unhandled_input)
frame += 1
loop.set_alarm_in(2, refresh, frame)
loop.run()
