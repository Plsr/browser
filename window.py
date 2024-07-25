import tkinter
import browser

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def layout(text):
  display_list = []
  cursor_x, cursor_y = HSTEP, VSTEP

  for c in text:
    # New line on line breaks
    if c == '\n':
       cursor_y += VSTEP
       cursor_x = 0

    display_list.append((cursor_x, cursor_y, c))
    cursor_x += HSTEP

    if cursor_x >= WIDTH:
      cursor_y += VSTEP
      cursor_x = HSTEP

  return display_list

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
      self.window,
      width=WIDTH,
      height=HEIGHT
    )
    self.canvas.pack()
    self.scroll = 0

    self.window.bind("<Down>", self.scrolldown)
    self.window.bind("<Up>", self.scrollup)
    self.window.bind("<MouseWheel>", self.mousewheel)
  
  def scrolldown(self, e):
    if self.scroll >= HEIGHT: return

    self.scroll += SCROLL_STEP
    self.draw()

  def scrollup(self, e):
    if self.scroll == 0: return

    self.scroll -= SCROLL_STEP
    self.draw()
  
  # TODO: Add windows & linux support
  def mousewheel(self, e):
    delta = e.delta
    
    if delta % 120 == 0:
      delta = delta / 120

    if delta < 0 and self.scroll + delta * SCROLL_STEP <= 0: return
    if delta > 0 and self.scroll + delta * SCROLL_STEP >= HEIGHT: return

    self.scroll += delta * SCROLL_STEP
    self.draw()
  
  def draw(self):
     self.canvas.delete("all")
     for x, y, c in self.display_list:
        if y > self.scroll + HEIGHT: continue
        if y + VSTEP < self.scroll: continue
        self.canvas.create_text(x, y - self.scroll, text=c)
  
  def load(self, text):
     self.display_list = layout(text)
     self.draw()

if __name__ == "__main__":
    import sys
    Browser().load(browser.URL(sys.argv[1]).load())
    tkinter.mainloop()


