from manim import *


class CreateCircle(Scene):
    def construct(self):
      w = self.WriteQuestion()
      self.play(w)
      self.remove(w)
      self.play(self.PoseMotivation())
    
    def WriteQuestion(self):
      text = "What is a 🐔 filter?"
      return Write(Text(text, font_size=100))
    
    def PoseMotivation(self):
      text = "2nd slide please"
      return Write(Text(text, font_size=100))
      
