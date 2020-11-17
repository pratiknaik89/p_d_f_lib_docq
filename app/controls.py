
import utils


class Controls(object):
    def __init__(self, pdf, format):
        self.pdf = pdf
        self.format = format

    def text(self, control):
        if 'val' not in control:
            return
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def note(self, control):
        if 'val' not in control:
            return
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.multi_cell(0, 4, txt=control['val'])

    def checkbox(self, control):
        if 'val' not in control:
            return
        style = control['style']
        if 'val' in control and control['val'] == True:
            self.pdf.image('icons/check.png', self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                           self.pixel_to_mm(20), self.pixel_to_mm(20), 'PNG', '')

    # Radio Button
    def radio(self, control):
        if 'val' not in control:
            return
        style = control['style']
        if 'val' in control and 'value' in control['dataset'] and control['val'] == control['dataset']['value']:
            self.pdf.image('icons/check.png', self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                           self.pixel_to_mm(20), self.pixel_to_mm(20), 'PNG', '')

    def ddl(self, control):
        if 'val' not in control:
            return
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def sign(self, control):
        if 'val' not in control:
            return
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def pic(self, control):
        if 'val' not in control:
            return
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def initial(self, control):
        if 'val' not in control:
            return
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def signdate(self, control):
        if 'val' not in control:
            return
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def pixel_to_mm(self, pixels):
        return pixels * 0.264583

    def top_fix(self, top):
        if self.format == "legal":
            return top - 10

        return top - 7

    def font_style(self, style, weight):
        if style == "normal":
            style = ""
        if weight == "normal":
            weight = ""
        style = style.replace(" ", "")
        weight = weight.replace(" ", "")
        _style = {
            "": "",
            "bold": "B",
            "italic": "I",
            "italicunderline": "IU",
            "italicunderlinebold": "IUB",
            "underline": "U",
            "italicbold": "IB",
            "underlinebold": "UB"

        }

        return _style[style+""+weight]
