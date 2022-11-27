from manim import Scene, Write, Text, FadeIn, FadeOut, ImageMobject, UP, DOWN, LEFT, RIGHT, Ellipse, Rectangle, VGroup, DrawBorderThenFill, BLUE_D, BLUE_B, BLUE, ORANGE


class CreateCircle(Scene):
    def construct(self):
        self.WriteQuestion()
        self.PoseMotivation()
        self.ListGoals()

    def WriteQuestion(self):
        text = Text("What is a 🐔 filter?", font_size=100)
        self.play(Write(text))
        self.play(FadeOut(text))

    def PoseMotivation(self):
        kirby = ImageMobject("images/8-bit-kirby.png")
        food_pile = ImageMobject("images/8-bit-food-pile.jpg")
        cherry_text = Text("I hate cherries", font_size=30)
        bubble = Ellipse(width=3.0, height=2.0, color=BLUE_D)
        bubble.set_fill(BLUE, opacity=0.5)
        speech_bubble = VGroup()
        speech_bubble.add(bubble, cherry_text).shift(5*LEFT).shift(0.5 * UP)
        self.play(FadeIn(kirby))
        self.play(kirby.animate.shift(5*LEFT).shift(2*DOWN))
        self.play(FadeIn(food_pile))
        self.wait(5)
        self.play(FadeIn(speech_bubble))
        self.wait(3)
        self.play(FadeOut(speech_bubble))
        self.play(FadeOut(kirby))
        self.play(FadeOut(food_pile))

    def ListGoals(self):
        background = Rectangle(
            height=3, width=6, fill_opacity=1, fill_color=BLUE)
        goals = Text('First_line\nSecond_line\nThird_line')
        background_goals = VGroup()
        background_goals.add(background, goals)
        self.play(DrawBorderThenFill(background))
        self.play(Write(goals))
        self.play(background_goals.animate.shift(4*LEFT).shift(2*UP))
