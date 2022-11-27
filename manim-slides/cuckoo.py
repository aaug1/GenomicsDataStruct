from manim import Scene, Write, Text, FadeIn, FadeOut, ImageMobject, UP, DOWN, LEFT, RIGHT, Ellipse, Rectangle, Group, VGroup, DrawBorderThenFill, BLUE_D, BLUE_B, BLUE, ORANGE


class CuckooFilter(Scene):
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
        self.play(FadeIn(speech_bubble))
        self.play(FadeOut(Group(*self.mobjects)))

    def ListGoals(self):
        background = Rectangle(
            height=2, width=6, fill_opacity=1, fill_color=BLUE)
        goal_text_1 = "1.Store large amounts of data\n"
        goal_text_2 = "2.Fast Searching\n"
        goal_text_3 = "3.Remove Items"
        g_1 = Text(goal_text_1, font_size=30).shift(0.5*UP)
        g_2 = Text(goal_text_2, font_size=30)
        g_3 = Text(goal_text_3, font_size=30).shift(0.5*DOWN)
        background_goals = VGroup()
        background_goals.add(background, g_1, g_2, g_3)
        self.play(DrawBorderThenFill(background))
        self.play(Write(g_1))
        self.play(Write(g_2))
        self.play(Write(g_3))
        self.play(background_goals.animate.shift(4*LEFT).shift(2.5*UP))

        bloom_text = "Bloom Filter"
        bloom = Text(bloom_text, font_size=70).shift(4*DOWN)
        bloom_pic = ImageMobject("images/Bloom-Filter.png")
        bloom_filter = Group()
        bloom_filter.add(bloom, bloom_pic).scale(.5).shift(DOWN)
        self.play(FadeIn(bloom_filter))
        self.play(bloom_filter.animate.shift(3.3*UP).shift(4*RIGHT))

        kirby = ImageMobject("images/8-bit-kirby.png").shift(2.4*DOWN)
        cherry_text = Text("I STILL hate cherries", font_size=30)
        bubble = Ellipse(width=4.0, height=2.0, color=BLUE_D)
        bubble.set_fill(BLUE, opacity=0.5)
        kirby_speech_bubble = Group()
        kirby_speech_bubble.add(kirby, bubble, cherry_text).shift(
            5*LEFT).shift(0.5 * DOWN)
        self.play(FadeIn(kirby_speech_bubble))

        self.play(FadeOut(Group(*self.mobjects)))
