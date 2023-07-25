from PIL import ImageDraw, Image, ImageFont

class RenderFont: # we love stackoverflow
    def __init__(self, filename, fill=(0, 0, 0)):
        """
        constructor for RenderFont
        filename: the filename to the ttf font file
        fill: the color of the text
        """
        self._file = filename
        self._fill = fill
        self._image = None
        
    def get_render(self, font_size, txt, type_="normal"):
        """
        returns a transparent PIL image that contains the text
        font_size: the size of text
        txt: the actual text
        type_: the type of the text, "normal" or "bold"
        """
        if type(txt) is not str:
            raise TypeError("text must be a string")

        if type(font_size) is not int:
            raise TypeError("font_size must be a int")

        width = len(txt)*font_size
        height = font_size+5

        font = ImageFont.truetype(font=self._file, size=font_size)
        self._image = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255))

        rgba_data = self._image.getdata()
        newdata = []

        for item in rgba_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newdata.append((255, 255, 255, 0))

            else:
                newdata.append(item)

        self._image.putdata(newdata)

        draw = ImageDraw.Draw(im=self._image)

        if type_ == "normal":
            draw.text(xy=(width/2, height/2), text=txt, font=font, fill=self._fill, anchor='mm')
        elif type_ == "bold":
            draw.text(xy=(width/2, height/2), text=txt, font=font, fill=self._fill, anchor='mm', 
            stroke_width=1, stroke_fill=self._fill)

        return self._image