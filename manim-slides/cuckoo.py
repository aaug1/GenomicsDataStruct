from manim import MathTex, Scene, Write, Text, FadeIn, FadeOut, ImageMobject, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, Ellipse, Rectangle, Circle, Arrow, GrowArrow, ArrowSquareTip, Group, VGroup, Circumscribe, DrawBorderThenFill, BLUE_D, BLUE_B, BLUE, ORANGE, DARK_GRAY, LIGHT_GRAY, WHITE, VMobject, Square


class CuckooFilter(Scene):
    def construct(self):
        #self.WriteQuestion()
        #self.PoseMotivation()
        #self.ListGoals()
        self.MakeDataStructure()

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
        self.play(Circumscribe(g_3))

        kirby = ImageMobject("images/8-bit-kirby.png").shift(2.4*DOWN)
        cherry_text = Text("I STILL hate cherries", font_size=30)
        bubble = Ellipse(width=4.0, height=2.0, color=BLUE_D)
        bubble.set_fill(BLUE, opacity=0.5)
        kirby_speech_bubble = Group()
        kirby_speech_bubble.add(kirby, bubble, cherry_text).shift(
            5*LEFT).shift(0.5 * DOWN)
        self.play(FadeIn(kirby_speech_bubble))

        self.play(FadeOut(Group(*self.mobjects)))

    def MakeDataStructure(self):

        middle_group = VGroup()
        #middle_group2 = VGroup()
        # As max_stroke_width_to_length_ratio gets bigger,
        # the width of stroke increases.
        for i in range(0, 8, 1):
            middle_group += Arrow(max_stroke_width_to_length_ratio=5).shift(i*.8 * DOWN)
            #middle_group2 += Arrow(max_stroke_width_to_length_ratio=5).shift(i*.8 * DOWN)

        numEntries = 2
        cuckooFilter = Group()
        for i in range(numEntries):
            cuckooFilter.add(Vert_Array(8, 0.8, fill_color=DARK_GRAY,
                                        color=LIGHT_GRAY, indices=True).shift(2.2*i*RIGHT))
        self.play(FadeIn(cuckooFilter.shift(2*RIGHT)))
        self.play(FadeIn(middle_group.shift(2.8*UP).shift(3*RIGHT)))
        #self.play(FadeIn(middle_group2.shift(2.8*UP).shift(5.3*RIGHT)))

        self.hashCherry()

    def hashCherry(self):
        cherry = ImageMobject(
            "images/8-bit-cherry.png").scale(.4).shift(5.3*LEFT)
        self.play(FadeIn(cherry.shift(.5*UP)))

        self.play(Circumscribe(cherry, shape=Circle))
        #self.play(FadeOut(cherry))
        
        #fingerprint = Text("Fingerprint", font_size=50)
        #self.play(Write(fingerprint.shift(LEFT*2)))
        #self.play(FadeOut(fingerprint))
        
        #bit_string = Text("0101", font_size=50)
        #self.play(Write(bit_string.shift(LEFT*5 + DOWN*2)))
        #self.play(bit_string.animate.shift(LEFT*4))
        all_hash = VGroup()
        for i in range(1, -1, -1):
            mathText = MathTex(f"h{i}")
            mathText.shift(UP*(i*1.2))
            all_hash.add(mathText)
        self.play(FadeIn(all_hash.shift(LEFT*2)))
        
        h1Arr = Arrow(LEFT, RIGHT).shift(1.2*UP + 3.5*LEFT)
        h2Arr = Arrow(LEFT, RIGHT).shift(3.5*LEFT)
        self.play(GrowArrow(h1Arr))
        self.play(GrowArrow(h2Arr))
        
        index1Arr = Arrow(LEFT, 2*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 2.2*DR)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.3*LEFT)))
        
        self.play(FadeOut(cherry))
        self.play(FadeOut(h1Arr))
        self.play(FadeOut(h2Arr))
        self.play(FadeIn(cherry.scale(.2).shift(UP*2.3 + RIGHT*7.3)))
        self.play(FadeOut(index1Arr))
        self.play(FadeOut(index2Arr))
        self.hashPineapple(cherry)
        
    def hashPineapple(self, cherry):
        pineapple = ImageMobject(
            "images/8-bit-pineapple.png").scale(.8).shift(5.3*LEFT)
        self.play(FadeIn(pineapple.shift(.5*UP)))

        self.play(Circumscribe(pineapple, shape=Circle))
        
        h1Arr = Arrow(LEFT, RIGHT).shift(1.2*UP + 3.5*LEFT)
        h2Arr = Arrow(LEFT, RIGHT).shift(3.5*LEFT)
        self.play(GrowArrow(h1Arr))
        self.play(GrowArrow(h2Arr))
        
        index1Arr = Arrow(LEFT, 2*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 2.2*DR)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.3*LEFT)))
        
        #self.play(cherry.animate.shift(RIGHT*2.2))
        self.play(FadeOut(pineapple))
        self.play(FadeOut(h1Arr))
        self.play(FadeOut(h2Arr))
        self.play(FadeIn(pineapple.scale(.2).shift(UP*2.3 + RIGHT*9.5)))
        self.play(FadeOut(index1Arr))
        self.play(FadeOut(index2Arr))


class Vert_Array(VMobject):
    def __init__(self, array_len, box_size, color=WHITE, indices=False, **kwargs):
        # Set properties
        self.array_len = array_len
        self.box_size = box_size
        self.squares = []
        self.nums = []
        VMobject.__init__(self, **kwargs)
        square = Square(side_length=box_size, color=color)

        # Create the squares in array
        for i in range(array_len):
            square1 = Square(side_length=box_size, color=color).next_to(
                square, DOWN, buff=0).set_style(fill_color=DARK_GRAY, fill_opacity=1)
            square = square1
            self.add(square)
            self.squares.append(square)

        self.center()
