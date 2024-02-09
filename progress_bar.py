import progressbar


def progress_bar(frame_count):
    widgets = [' [',
               progressbar.Timer(format= 'Upłynęło: %(elapsed)s'),'] ',
               progressbar.Bar('#'),' (',
               progressbar.ETA(), ') ',
              ]
    bar = progressbar.ProgressBar(max_value=frame_count, widgets=widgets).start()
    return bar