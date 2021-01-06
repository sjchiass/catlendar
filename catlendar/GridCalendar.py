from datetime import date
import calendar
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import math

class GridCalendar():
    """Instantiates a drawing area for PIL polygons"""
    def __init__(self, width=500, height=300, title_size=0.1, header_size=0.05, padding=0.1, rows=6, columns=7, background=0, mode="RGBA"):
        """PIL Image and ImageDraw objects are initialized, with an
        optional grid.
        """
        # Making inputs acceptable
        height = int(height)
        width = int(width)
        
        # Creating the Image and the ImageDraw
        self.image = Image.new(mode=mode, size=(width, height), color=background)
        self.draw = ImageDraw.Draw(self.image)
        
        # Saving the height and width
        self.H = height
        self.head = height * header_size
        self.h = height * (1 - title_size - header_size - 2*padding)
        self.W = width
        self.w = width * (1 - 2*padding)
        self.title_size = title_size
        self.header_size = header_size
        self.padding = padding
        
        # Grid offsets
        self.top = height * (title_size + header_size + padding)
        self.bottom = height * (1 - padding)
        self.left = width * padding
        self.right = width * (1 - padding)
        
        # Saving the rows and columns
        self.rows = rows
        self.columns = columns
        
        # Calculating the units
        self.r = self.h / self.rows
        self.c = self.w / self.columns
    def draw_grid(self, width_factor = 0.2, color="black", background=0):
        width = self.convert_size(width_factor)
        x = self.left
        
        # Fill the background
        self.draw.rectangle([self.left, self.top, self.right, self.bottom], fill=background)
        
        while x < self.right:
            self.draw.line(((x, self.top), (x, self.bottom)),
                           fill=color,
                           width=width)
            x += self.c
        
        # Final vertical line
        self.draw.line(((self.right, self.top), (self.right, self.bottom)),
                       fill=color,
                       width=width)
        y = self.top
        while y < self.bottom:
            self.draw.line(((self.left, y), (self.right, y)),
                           fill=color,
                           width=width)
            y += self.r
        
        # Final horizontal line
        self.draw.line(((self.left, self.bottom), (self.right, self.bottom)),
                       fill=color,
                       width=width)
    def number_cells(self,
                     year=2020,
                     month=10,
                     x_offset=-0.4,
                     y_offset=-0.4,
                     firstweekday=6,
                     font_file="DejaVuSans.ttf",
                     font_factor=1.0,
                     other_month_color=None):
        font_size = self.convert_size(font_factor)
        font = ImageFont.truetype(font_file, font_size)
        c = calendar.Calendar()
        c.setfirstweekday(firstweekday)
        
        # From the calendar module, itermonthdays3() will return tuples
        # of (year, month, day). We can use this to know which days are
        # from other months.
        numbers = list(c.itermonthdays3(year, month))
        
        # We can keep adding days until the full calendar is filled out
        # Since the first items of each itermonthdays3() generator will
        # overlap the previous months, we only admit them if they're
        # not already present. It would be cleaner to just get a date
        # generator and have it output a new (year, month, day) tuple
        # until the limits is reached.
        if len(numbers) < self.rows*self.columns:
            m = month
            y = year
            while len(numbers) < self.rows*self.columns:
                y = y + m // 12
                m = 1 if m == 12 else m + 1
                numbers += [x for x in c.itermonthdays3(y, m) if x not in numbers]
        
        # Calculate all of the centerpoints of the cells
        points = [(self.left + (self.c / 2) + (self.c * (x % self.columns) + x_offset*self.c),
                        self.top + (self.r / 2) + (self.r * (x // self.columns)) + y_offset*self.r)
                       for x in range(self.rows * self.columns)]
        for n, i in enumerate(numbers[0:self.rows*self.columns]):
            if i[1] == month:
                self.draw.text(points[n], str(i[2]), fill="black", font=font)
            elif other_month_color is not None:
                self.draw.text(points[n], str(i[2]), fill=other_month_color, font=font)
    def label_days(self,
                   x_offset=0.05,
                   y_offset=0.5,
                     firstweekday=6,
                   background=0,
                   font_color="black",
                   font_file="DejaVuSans.ttf",
                   font_factor=1.0,
                  abbreviate=False):
        font_size = self.convert_size(font_factor)
        font = ImageFont.truetype(font_file, font_size)
        if abbreviate is True:
            days = [calendar.day_abbr[i] for i in [(x + firstweekday) % 7 for x in range(7)]]
        else:
            days = [calendar.day_name[i] for i in [(x + firstweekday) % 7 for x in range(7)]]
        for n, day in enumerate(days):
            self.draw.rectangle([(self.left + n*self.c, self.top-self.head),
                                (self.left + (n+1)*self.c, self.top)],
                               fill=background)
            self.draw.text((self.left + (n+x_offset)*self.c,
                            self.top - self.head*(1+y_offset)/2),
                           text=str(day),
                           fill=font_color,
                          font=font)
    def label_month(self,
                    year,
                    month,
                    background=0,
                    color="black",
                    font_file="DejaVuSans.ttf",
                    font_factor=3.2):            
        # Fill the background
        self.draw.rectangle([self.left,
              self.top - (self.header_size+self.title_size)*self.H,
              self.right,
              self.top - self.header_size*self.H],
            fill=background)
        
        months = calendar.month_name
        font_size = self.convert_size(font_factor)
        font = ImageFont.truetype(font_file, font_size)
        self.draw.text((self.padding*self.W, (self.title_size + self.padding)*self.H/5), text=f"{months[month]} {year}", fill=color, font=font)
    def convert_size(self, factor):
        return int(factor * (self.H+self.W)/100)
    def display(self):
        """Returns the image object, which renders the image in Jupyter."""
        return self.image
