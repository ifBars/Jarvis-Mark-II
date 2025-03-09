from localization import _
exit = False

def exit_program():
    print(_("Exiting the program"))
    global exit
    exit = True

def should_exit():
    return exit