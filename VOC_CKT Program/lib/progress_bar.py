import math

class BarStyle():
  SOLID             = 0
  DIAGONAL_FORWARD  = 1
  DIAGONAL_BACKWARD = 2
  ARROW_FORWARD     = 3
  ARROW_BACKWARD    = 4

class BarBase():
  
  def __init__(self, x, y, width, height, oled, band_style=1, band_width=20, percent=100):
    self.inited = False
    
    self.x = x
    self.y = y
    self.height = height
    self.width = width
    self.oled = oled
    self.phase = 0
    self.band_width = band_width
    self.band_style = band_style
    self.percent = percent
    
    self._reverse = False
    
    self.text = None
    self.text_color = 1
    self.show_text_mask = True
    
    self.update()
    self.inited = True
  
  def update(self):
    x_range = range(1, math.floor(self.width * (self.percent / 100)))
    y_range = range(1, self.height)
    
    for i in x_range:
      for j in y_range:
        if 0 < i < self.width and 0 <j < self.height:
          # draw bar
          self.oled.pixel(
            self.x + i, 
            self.y + j,
            self._get_pixel_color(i, j)
          )
    
    # print the text out
    self.draw_text()
    
    # draw outline
    if not self.inited:
      self.oled.rect(
        self.x,
        self.y,
        self.width,
        self.height,
        1
      )
    
    # increase phase
    self._increase_phase()
  
  def _increase_phase(self):
    increment = 1
    if self._reverse:
      increment = -1
    self.phase = (self.phase - increment) % self.band_width
  
  def _get_pixel_color(self, x, y):
    if self.band_style == BarStyle.SOLID:
      return 1
    
    if self.band_style == BarStyle.DIAGONAL_FORWARD:
      return ((self.phase + x + y + 1) % self.band_width * 2) < self.band_width
  
  def _set_pixel(self, x, y):
    self.oled.pixel(
      self.x + x, 
      self.y + y,
      self._get_pixel_color(x, y)
    )
  
  def set_text(self, text, color=1, show_text_mask=True):
    self.text = text
    self.text_color = color
    self.show_text_mask = show_text_mask
  
  def reverse(self):
    self._reverse = not self._reverse
    
  def set_percent(self, percent=100):
    if self.percent > percent:
      # clear out previous percentage
      self.oled.fill_rect(
        self.x + 1 + math.ceil(self.width * (percent / 100)),
        self.y + 1,
        math.ceil((self.width - 2) * (self.percent - percent) / 100),
        self.height - 2,
        0
      )
    self.percent = percent
  
  def draw_text(self):
    if self.text == None:
      return
    
    # All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
    text_width = len(self.text) * 8
    block_padding = 1 # 1 pixel padding around text mask
    text_x = math.floor(self.x + (self.width - text_width) / 2)
    text_y = math.floor(self.y + (self.height - 6) / 2)
    
    if self.show_text_mask:
      self.oled.fill_rect(
        text_x - block_padding,
        text_y - block_padding,
        text_width + block_padding * 2,
        8 + block_padding * 2,
        not self.text_color
      )
    self.oled.text(self.text, text_x, text_y, self.text_color)

class ProgressBar(BarBase):
  def __init__(self, x, y, width, height, oled, band_style=1, band_width=20, percent=100):
    super().__init__(x, y, width, height, oled, band_style, band_width, percent)
    self.inited = True
  
  def redraw(self):
    self.inited = False
    super().update()
    self.inited = True
  
  def update(self):
    if not self.inited:
      # update unoptimized the first time (paint all pixels)
      return super().update()
    
    bar_count = math.ceil((self.width * (self.percent / 100)) / self.band_width * 2)
    for i in range(bar_count):
      for j in range(0, self.height - 2):
        x = i * self.band_width - j - self.phase
        if 0 < x < self.width * (self.percent / 100) - 1:
          # draw left side
          self.oled.pixel(
            self.x + x, 
            self.y + j + 1,
            self._get_pixel_color(x, j+1)
          )
        x = x + math.floor(self.band_width / 2)
        if 0 < x < self.width * (self.percent / 100) - 1:
          # draw right side
          self.oled.pixel(
            self.x + x, 
            self.y + j + 1,
            self._get_pixel_color(x, j+1)
          )
    
    # print the text out
    self.draw_text()
    
    # increase phase
    self._increase_phase()