from .GridCalendar import GridCalendar

def month_calendar(year, month, width=1100, height=850):
    large = GridCalendar(width=width, height=height, padding=0.01, background="white")
    large.label_days(background="grey")
    large.draw_grid(background="white")
    large.number_cells(year=year, month=month, other_month_color="grey")
    large.label_month(year, month, background="white")
        
    previous_year = year - int(month == 1)
    next_year = year + month // 12
    previous_month = 12 if month == 1 else month - 1
    next_month = 1 if month == 12 else month + 1
    
    small1 = GridCalendar(width=large.c, height=large.r, title_size=0.15, padding=0.05, header_size=0.1)
    small1.draw_grid(color="white", background="white")
    small1.label_days(abbreviate=True, background="white", font_factor=3.2, font_color="black")
    small1.number_cells(year=previous_year, month=previous_month, font_factor=4.8, font_file="DejaVuSans.ttf")
    small1.label_month(previous_year, previous_month, background="white")
    
    small2 = GridCalendar(width=large.c, height=large.r, title_size=0.15, padding=0.05, header_size=0.1)
    small2.draw_grid(color="white", background="white")
    small2.label_days(abbreviate=True, background="white", font_factor=3.2, font_color="black")
    small2.number_cells(year=next_year, month=next_month, font_factor=4.8, font_file="DejaVuSans.ttf")
    small2.label_month(next_year, next_month, background="white")
    
    large.image.paste(small1.image, (int(large.right-2*large.c), int(large.bottom-large.r)), small1.image)
    large.image.paste(small2.image, (int(large.right-large.c), int(large.bottom-large.r)), small2.image)
    
    return large
