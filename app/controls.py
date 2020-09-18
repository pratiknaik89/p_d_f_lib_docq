
import utils


class Controls(object):
    def __init__(self, pdf):
        self.pdf = pdf

    def text(self, control):
        style = control['style']
        print(control)
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def note(self, control):
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def checkbox(self, control):
        style = control['style']
        if 'val' in control and control['val'] == True:
            self.pdf.image('icons/check.png', self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(20), self.pixel_to_mm(20), 'PNG', '')

    #Radio Button
    def radio(self, control):
        style = control['style']
        if 'val' in control and 'value' in control['dataset']  and control['val'] == control['dataset']['value']:
            self.pdf.image('icons/check.png', self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(20), self.pixel_to_mm(20), 'PNG', '')

    def ddl(self, control):
        style = control['style']
        pdf_style = self.font_style(style['fontStyle'], style['fontWeight'])
        self.pdf.set_font(style['fontFamily'],
                          style=pdf_style, size=style['fontSize'])
        self.pdf.set_xy(self.pixel_to_mm(
            style['left']), self.pixel_to_mm(self.top_fix(style['top'])))
        self.pdf.cell(0, 10, txt=control['val'], ln=0)

    def sign(self, control):
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def pic(self, control):
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def initial(self, control):
        style = control['style']
        newWidth = utils.imageReturnNewWidth(control['val'], style['height'])
        self.pdf.image(control['val'], self.pixel_to_mm(style['left']), self.pixel_to_mm(self.top_fix(style['top'])),
                       self.pixel_to_mm(newWidth), self.pixel_to_mm(style['height']), 'PNG', '')

    def pixel_to_mm(self, pixels):
        return pixels * 0.264583

    def top_fix(self, top):
        return top + 55

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
