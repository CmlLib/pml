class Event(list):
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


class MDownloadEventArgs:
    def __init__(self):
        self.filekind = ""
        self.filename = ""
        self.maxvalue = 1
        self.currentvalue = 1

