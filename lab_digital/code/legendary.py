from pylab import *


class Legendary(dict):
    def draw(self, **style):
        labels = []
        lines = []
        for _, qualities in sorted(self.items()):
            kwargs = dict(qualities.items())
            label = kwargs.pop("label")
            lines.append(Line2D((0,1), (0,0), **kwargs))
            labels.append(label)
        self.legend = legend(lines, labels, **style)
        return self.legend

    def hide(self):
        self.legend.set_visible(False)

    def show(self):
        self.legend.set_visible(True)

