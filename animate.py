import urwid
from gray_hanoi import GrayHanoi

frame = 0


def unhandled_input(key):
    if key == 'q':
        raise urwid.ExitMainLoop()


def refresh(_loop, _data):
    outputTxt = gray_hanoi.pretty_print_configuration(
        configurations[_data % len(configurations)])

    txt.set_text(outputTxt)
    _data += 1
    loop.set_alarm_in(0.2, refresh, _data)


gray_hanoi = GrayHanoi(n_rigs=3, n_disks=8)
configurations = gray_hanoi.solve(verbose=False)

outputTxt = gray_hanoi.pretty_print_configuration(
    configurations[frame])

txt = urwid.Text(outputTxt)
fill = urwid.Filler(txt, 'top')

loop = urwid.MainLoop(fill, unhandled_input=unhandled_input)
frame += 1
loop.set_alarm_in(2, refresh, frame)
loop.run()
