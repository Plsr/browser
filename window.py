import tkinter
import browser

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def layout(text, width):
  display_list = []
  cursor_x, cursor_y = HSTEP, VSTEP

  for c in text:
    # New line on line breaks
    if c == '\n':
       cursor_y += VSTEP
       cursor_x = 0

    display_list.append((cursor_x, cursor_y, c))
    cursor_x += HSTEP

    if cursor_x >= width:
      cursor_y += VSTEP
      cursor_x = HSTEP

  return display_list

class Browser:
  def __init__(self):
    self.width = 800
    self.height= 600
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
      self.window,
      width=self.width,
      height=self.height
    )
    self.canvas.pack(fill="both", expand=True)
    self.scroll = 0

    self.window.bind("<Down>", self.scrolldown)
    self.window.bind("<Up>", self.scrollup)
    self.window.bind("<MouseWheel>", self.mousewheel)
    self.window.bind("<Configure>", self.resize)
  
  def resize(self, e):
    self.width = e.width
    self.height = e.height

    self.display_list = layout(self.text, self.width)
    self.draw()


  def scrolldown(self, e):
    if self.scroll - SCROLL_STEP + self.height >= self.display_list[-1][1]: return
    self.scroll += SCROLL_STEP
    self.draw()

  def scrollup(self, e):
    if self.scroll <= 0: return

    self.scroll -= SCROLL_STEP
    self.draw()
  
  # TODO: Add windows & linux support
  def mousewheel(self, e):
    delta = e.delta
    
    if delta % 120 == 0:
      delta = delta / 120

    if delta < 0 and self.scroll + delta * SCROLL_STEP + self.height >= self.display_list[-1][1]: 
      self.scroll = self.display_list[-1][1] - self.height
      self.draw()
      return
    if delta > 0 and self.scroll + delta * SCROLL_STEP <= 0: return

    self.scroll += delta * SCROLL_STEP * -1
    self.draw()
  
  def draw(self):
    self.canvas.delete("all")
    for x, y, c in self.display_list:
      if y > self.scroll + self.height: continue
      if y + VSTEP < self.scroll: continue
      self.canvas.create_text(x, y - self.scroll, text=c)
      
    # Scrollbar
    y_max = self.display_list[-1][1]
    y_curr = self.scroll + self.height
    pct_scrl = y_curr / y_max
    if pct_scrl > 1: pct_scrl = 1
    if pct_scrl < 0: pct_scrl = 0
    y0 = (self.height - 30) * pct_scrl 
    self.canvas.create_rectangle(self.width - 10, y0, self.width, y0 + 30 , fill="#eee")
    
  
  def load(self, text):
    self.text = text
    self.display_list = layout(text, self.width)
    self.draw()

if __name__ == "__main__":
    import sys
    Browser().load(browser.URL(sys.argv[1]).load())
    tkinter.mainloop()


