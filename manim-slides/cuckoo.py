from manim import MathTex, Scene, Write, Text, FadeIn, FadeOut, ImageMobject, ArcBetweenPoints, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, Ellipse, Rectangle, Circle, Line, Arrow, CurvedArrow, GrowArrow, ArrowSquareTip, Group, VGroup, Circumscribe, DrawBorderThenFill, BLUE_D, BLUE_B, BLUE, ORANGE, DARK_GRAY, LIGHT_GRAY, WHITE, VMobject, Square
import numpy as np

class CuckooFilter(Scene):
    def construct(self):
        #self.WriteQuestion()
        #self.PoseMotivation()
        #self.ListGoals()
        self.MakeDataStructure()
        '''self.ExplainFinger()
        self.ExplainHashes()
        self.Cycles()
        self.LookUpAndDelete()
        self.FalsePositive()
        self.Future()
        self.WriteQuestion()'''
        

    def WriteQuestion(self):
        text = Text("What is a 🐔 filter?", font_size=100)
        self.play(Write(text), run_time=3)
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
        self.wait(1.5)
        self.play(kirby.animate.shift(5*LEFT).shift(2*DOWN))
        self.play(FadeIn(food_pile))
        self.wait(14)
        self.play(FadeIn(speech_bubble))
        self.wait(3)
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
        self.wait(13)
        self.play(Write(g_2))
        self.wait(13)
        self.play(Write(g_3))
        self.wait(10)
        self.play(background_goals.animate.shift(4*LEFT).shift(2.5*UP))

        bloom_text = "Bloom Filter"
        bloom = Text(bloom_text, font_size=70).shift(4*DOWN)
        bloom_pic = ImageMobject("images/Bloom-Filter.png")
        bloom_filter = Group()
        bloom_filter.add(bloom, bloom_pic).scale(.5).shift(DOWN)
        self.play(FadeIn(bloom_filter))
        self.wait(5)
        self.play(bloom_filter.animate.shift(3.3*UP).shift(4*RIGHT))
        self.wait(5)
        self.play(Circumscribe(g_3))

        kirby = ImageMobject("images/8-bit-kirby.png").shift(2.4*DOWN)
        cherry_text = Text("I STILL hate cherries", font_size=30)
        bubble = Ellipse(width=4.0, height=2.0, color=BLUE_D)
        bubble.set_fill(BLUE, opacity=0.5)
        kirby_speech_bubble = Group()
        kirby_speech_bubble.add(kirby, bubble, cherry_text).shift(
            5*LEFT).shift(0.5 * DOWN)
        self.wait(10)
        self.play(FadeIn(kirby_speech_bubble))
        self.wait(10)

        self.play(FadeOut(Group(*self.mobjects)))

    def MakeDataStructure(self, play_cherry=True):

        middle_group = VGroup()
        for i in range(0, 8, 1):
            middle_group += Arrow(max_stroke_width_to_length_ratio=5).shift(i*.8 * DOWN + .2*RIGHT)

        numEntries = 2
        cuckooFilter = Group()
        for i in range(numEntries):
            cuckooFilter.add(Vert_Array(8, 0.8, fill_color=DARK_GRAY,
                                        color=LIGHT_GRAY, indices=True).shift(2.2*i*RIGHT))
        self.play(FadeIn(cuckooFilter.shift(2*RIGHT)))
        self.play(FadeIn(middle_group.shift(2.8*UP).shift(3*RIGHT)))
        #9 secs pass
        self.wait(15)

        if play_cherry:
            self.hashCherry()
            self.play(FadeOut(Group(*self.mobjects)))

    def hashCherry(self):
        cherry = ImageMobject(
            "images/8-bit-cherry.png").scale(.4).shift(5.3*LEFT)
        self.play(FadeIn(cherry.shift(.5*UP)))
        self.wait(5)
        self.play(Circumscribe(cherry, shape=Circle))
        self.wait(5)
        # self.play(FadeOut(cherry))

        all_hash = VGroup()
        for i in range(1, -1, -1):
            mathText = MathTex(f"h{i}")
            mathText.shift(UP*(i*1.2))
            all_hash.add(mathText)
        self.play(FadeIn(all_hash.shift(LEFT*2)))
        self.wait(5)

        h1Arr = Arrow(LEFT, RIGHT).shift(1.2*UP + 3.5*LEFT)
        h2Arr = Arrow(LEFT, RIGHT).shift(3.5*LEFT)
        self.play(GrowArrow(h1Arr))
        self.play(GrowArrow(h2Arr))
        self.wait(5)
        index1Arr = Arrow(LEFT, 2*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 2.2*DR)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.3*LEFT)))
        self.wait(15)
        self.play(FadeOut(cherry))
        self.play(FadeOut(h1Arr))
        self.play(FadeOut(h2Arr))
        self.play(FadeIn(cherry.scale(.2).shift(UP*2.3 + RIGHT*7.3)))
        self.play(FadeOut(index1Arr))
        self.play(FadeOut(index2Arr))
        self.wait(15)
        self.hashPineapple(cherry)

    def hashPineapple(self, cherry):
        pineapple = ImageMobject(
            "images/8-bit-pineapple.png").scale(.8).shift(5.3*LEFT)
        self.play(FadeIn(pineapple.shift(.5*UP)))
        self.wait(5)
        self.play(Circumscribe(pineapple, shape=Circle))
        self.wait(5)
        h1Arr = Arrow(LEFT, RIGHT).shift(1.2*UP + 3.5*LEFT)
        h2Arr = Arrow(LEFT, RIGHT).shift(3.5*LEFT)
        self.play(GrowArrow(h1Arr))
        self.play(GrowArrow(h2Arr))
        self.wait(15)

        index1Arr = Arrow(LEFT, 2*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 2.2*DR)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.3*LEFT)))
        self.wait(15)

        # self.play(cherry.animate.shift(RIGHT*2.2))
        self.play(FadeOut(pineapple))
        self.play(FadeOut(h1Arr, h2Arr))
        self.play(FadeIn(pineapple.scale(.2).shift(UP*2.3 + RIGHT*9.5)))
        self.play(FadeOut(index1Arr, index2Arr))
        self.wait(15)

        x_string1 = Text("X", font_size=40)
        x_string2 = Text("X", font_size=40)
        self.play(Write(x_string1.shift(UP*1.2 + RIGHT*2)))
        self.play(Write(x_string2.shift(UP*1.2 + RIGHT*4.2)))
        self.wait(15)

        self.hashApple(cherry, pineapple)

    def hashApple(self, cherry, pineapple):
        apple = ImageMobject(
            "images/8-bit-apple.png").scale(.6).shift(5.3*LEFT + .5*UP)
        self.play(FadeIn(apple))
        self.wait(5)
        h1Arr = Arrow(LEFT, RIGHT).shift(1.2*UP + 3.5*LEFT)
        h2Arr = Arrow(LEFT, RIGHT).shift(3.5*LEFT)
        self.play(GrowArrow(h1Arr))
        self.play(GrowArrow(h2Arr))
        self.wait(5)

        index1Arr = Arrow(LEFT, 2*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 1.5*UP+2*RIGHT).shift(.3*DOWN)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.2*UP + .3*LEFT)))
        self.wait(5)
        
        self.play(Circumscribe(cherry, shape=Circle))
        self.wait(5)
        self.play(cherry.animate.shift(DOWN*4.8))
        self.play(FadeOut(apple))
        self.play(FadeIn(apple.scale(.3).shift(UP*2.3 + RIGHT*7.3)))
        self.play(FadeOut(h1Arr, h2Arr, index1Arr, index2Arr))
        self.play(Circumscribe(cherry, shape=Circle))
        self.wait(5)

    def ExplainFinger(self):
        fingerprint = Text("Fingerprint", font_size=100)
        self.play(Write(fingerprint))
        self.play(FadeOut(fingerprint))

        cherry = ImageMobject(
            "images/8-bit-cherry.png").scale(.4).shift(5.3*LEFT)
        self.play(FadeIn(cherry))

        sendCherry = Arrow(max_stroke_width_to_length_ratio=5).shift(3.3*LEFT)
        self.play(FadeIn(sendCherry))

        fingerprint_func = Text("FP( )", font_size=80).shift(1.3*LEFT)
        self.play(Write(fingerprint_func))

        sendResult = Arrow(max_stroke_width_to_length_ratio=5).shift(RIGHT)
        self.play(FadeIn(sendResult))

        fingerprint_bits = Text("0101", font_size=80).shift(3*RIGHT)
        self.play(Write(fingerprint_bits))

        self.play(FadeOut(Group(*self.mobjects)))
        self.play(FadeIn(cherry.shift(.5*UP)))
        self.play(Write(fingerprint_bits.shift(8.2*LEFT + 2.5*UP)))

        self.MakeDataStructure(play_cherry=False)

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

        self.play(FadeOut(fingerprint_bits))
        self.play(FadeIn(fingerprint_bits.scale(.2).shift(7.2*RIGHT + .2*UP)))

        self.play(FadeOut(Group(*self.mobjects)))

    def ExplainHashes(self):
        h1 = MathTex("h1( ) = hash(input object)").shift(4*LEFT+3*UP)
        h2 = MathTex("h0( ) = h1( ) \oplus hash(fingerprint)").shift(
            3.2*LEFT+2*UP)
        self.play(FadeIn(h1))
        self.play(FadeIn(h2))

        h1_val = MathTex("h1( ) = 11010").shift(5.4*LEFT+1*UP)
        hf_val = MathTex("hash(fingerprint) = 10011").shift(3.8*LEFT)
        self.play(FadeIn(h1_val))
        self.play(FadeIn(hf_val))

        bit_one = MathTex("11010").shift(5*RIGHT+3*UP)
        bit_two = MathTex("10011").shift(5*RIGHT+2.5*UP)
        bit_three = MathTex("01001").shift(5*RIGHT+1.5*UP)
        self.play(FadeIn(bit_one))
        self.play(FadeIn(bit_two))

        l = Line((0, 0, 0), (2, 0, 0)).shift(2*UP + 4*RIGHT)
        self.play(FadeIn(l))
        self.play(Write(bit_three))

        h2_val = MathTex("h0( ) = 01001").shift(5.4*LEFT + DOWN)
        self.play(FadeIn(h2_val))
        
        self.play(FadeOut(h1, h2, bit_two, bit_one, l, bit_three))
        move_group = VGroup(h1_val, hf_val, h2_val)
        self.play(move_group.animate.shift(2*UP))
        
        cur_index_num = MathTex("firstIndex = h0( ) = 01001").shift(1*UP)
        first_index = Square(side_length=1.5)
        fingerprint_num = MathTex("010")
        orig_storage = VGroup(cur_index_num, first_index, fingerprint_num).shift(4*RIGHT + 2*UP)
        self.play(FadeIn(orig_storage))
        
        self.play(Circumscribe(cur_index_num, shape=Rectangle))
        self.play(Circumscribe(hf_val, shape=Rectangle))
        
        newMath = VGroup(bit_three.shift(.5*UP), bit_two, l.shift(.5*DOWN), bit_one.shift(2*DOWN)).shift(2.5*DOWN + 11*LEFT)
        self.play(FadeIn(newMath))
        
        self.play(Circumscribe(bit_one), shape=Rectangle)
        self.play(Circumscribe(h1_val), shape=Rectangle)
        
        self.play(FadeOut(Group(*self.mobjects)))
    
    def LookUpAndDelete(self):
        function_title = Text("Perform Lookup", font_size=40).shift(3.5*UP + 4*LEFT)
        self.play(Write(function_title))
        
        self.MakeDataStructure(play_cherry=False)
        first_bit_one = MathTex("000")
        first_bit_two = MathTex("001").shift(.75*DOWN)
        first_bit_three = MathTex("110").shift(1.5*DOWN)
        firstEntry = VGroup(first_bit_one, first_bit_two, first_bit_three).shift(2.8*UP + 2*RIGHT)
        self.play(FadeIn(firstEntry))
        
        second_bit_one = MathTex("111")
        second_bit_two = MathTex("101").shift(.75*DOWN)
        second_bit_three = MathTex("110").shift(1.5*DOWN)
        secondEntry = VGroup(second_bit_one, second_bit_two, second_bit_three).shift(2.8*UP + 4.2*RIGHT)
        self.play(FadeIn(secondEntry))
        
        cherry_finger = MathTex("111").shift(5.5*LEFT + 1.8*UP)
        cherry = ImageMobject(
            "images/8-bit-cherry.png").scale(.4).shift(5.3*LEFT + .5*UP)
        self.play(FadeIn(cherry))
        self.play(FadeIn(cherry_finger))
        
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
        index2Arr = Arrow(LEFT, 1.5*UP+2*RIGHT).shift(.3*DOWN)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.2*UP + .3*LEFT)))
        
        self.play(Circumscribe(cherry_finger), shape=Rectangle)
        self.play(Circumscribe(first_bit_three), shape=Rectangle)
        self.play(Circumscribe(second_bit_three), shape=Rectangle)
        self.play(Circumscribe(first_bit_one), shape=Rectangle)
        self.play(Circumscribe(second_bit_one), shape=Rectangle)
        
        self.play(FadeOut(function_title))
        function_title = Text("Perform Deletion", font_size=40).shift(3.5*UP + 4*LEFT)
        self.play(Write(function_title))
        
        self.play(FadeOut(cherry_finger))
        cherry_finger = MathTex("110").shift(5.5*LEFT + 1.8*UP)
        self.play(FadeIn(cherry_finger))
        
        self.play(Circumscribe(cherry_finger), shape=Rectangle)
        self.play(Circumscribe(first_bit_one), shape=Rectangle)
        self.play(Circumscribe(second_bit_one), shape=Rectangle)
        self.play(Circumscribe(first_bit_three), shape=Rectangle)
        self.play(Circumscribe(second_bit_three), shape=Rectangle)
        
        self.play(FadeOut(first_bit_three))
        
        apple_finger = MathTex("110").shift(5.5*LEFT + DOWN)
        apple = ImageMobject(
            "images/8-bit-apple.png").scale(.5).shift(5.3*LEFT + 2*DOWN)
        self.play(FadeIn(apple_finger, apple))
        
        self.play(FadeOut(Group(*self.mobjects)))
    
    def FalsePositive(self):
        fp_title = Text("False Positive (How Bad?)", font_size=40).shift(3.5*UP + 3.6*LEFT)
        self.play(Write(fp_title))
        
        firstFinger = Text("1st Fingerprint:", font_size=20)
        onebitfinger = Text("1", font_size=40).shift(1.5*RIGHT)
        combinedOne = VGroup(firstFinger, onebitfinger)
        self.play(Write(combinedOne))
        
        self.play(combinedOne.animate.shift(2.5*UL + 2.5*LEFT))
        
        secondFinger = Text("2nd Fingerprint:", font_size=20)
        secondonebitfinger = Text("1", font_size=40).shift(1.5*RIGHT)
        combinedSecond = VGroup(secondFinger, secondonebitfinger)
        self.play(Write(combinedSecond))
        
        self.play(combinedSecond.animate.shift(2.5*UL + 2.5*LEFT + .5*DOWN))
        
        prob_tex = Text("Probablity:", font_size=40)
        probability = MathTex("1 \over 2").shift(2*RIGHT)
        prob_sen = VGroup(prob_tex, probability)
        self.play(Write(prob_sen))
        self.play(prob_sen.animate.shift(2.5*UR + 1.5*RIGHT + .3*DOWN))
        
        self.play(FadeOut(onebitfinger, secondonebitfinger))
        onebitfinger = Text("10", font_size=40).shift(1.5*RIGHT + 2.5*UL + 2.5*LEFT)
        secondonebitfinger = Text("10", font_size=40).shift(1.5*RIGHT + 2.5*UL + 2.5*LEFT + .5*DOWN)
        self.play(FadeIn(onebitfinger, secondonebitfinger))
        
        self.play(FadeOut(probability))
        probability = MathTex("{1 \over 2}^2").shift(2*RIGHT + 2.5*UR + 1.5*RIGHT + .3*DOWN)
        self.play(FadeIn(probability))
        
        
        self.play(FadeOut(onebitfinger, secondonebitfinger, firstFinger, secondFinger))
        self.play(FadeOut(probability))
        probability = MathTex("({1 \over 2})^f").shift(2*RIGHT + 2.5*UR + 1.5*RIGHT + .3*DOWN)
        self.play(FadeIn(probability))
        
        self.play(FadeOut(prob_tex))
        prob_tex = Text("Probablity:", font_size=40).shift(LEFT + 2.5*UR + 1.5*RIGHT + .3*DOWN)
        self.play(FadeOut(probability))
        probability = MathTex("{2 \over m} \cdot ({1 \over 2})^f").shift(1.8*RIGHT + 2.5*UR + 1.5*RIGHT + .3*DOWN)
        prob_sen = VGroup(prob_tex, probability).shift(4.3*LEFT + 1.5*DOWN)
        self.play(FadeIn(prob_sen))
        
        self.play(FadeOut(Group(*self.mobjects)))
        
    def Cycles(self):
        self.MakeDataStructure(play_cherry=False)
        
        first_bit_one = MathTex("000")
        first_bit_two = MathTex("001").shift(.75*DOWN)
        first_bit_three = MathTex("110").shift(1.5*DOWN)
        firstEntry = VGroup(first_bit_one, first_bit_two, first_bit_three).shift(2.8*UP + 2*RIGHT)
        self.play(FadeIn(firstEntry))
        
        second_bit_one = MathTex("111")
        second_bit_two = MathTex("101").shift(.75*DOWN)
        second_bit_three = MathTex("110").shift(1.5*DOWN)
        secondEntry = VGroup(second_bit_one, second_bit_two, second_bit_three).shift(2.8*UP + 4.2*RIGHT)
        self.play(FadeIn(secondEntry))
        
        cherry_finger = MathTex("111").shift(5.5*LEFT + 1.8*UP)
        cherry = ImageMobject(
            "images/8-bit-cherry.png").scale(.4).shift(5.3*LEFT + .5*UP)
        self.play(FadeIn(cherry))
        self.play(FadeIn(cherry_finger))
        
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

        index1Arr = Arrow(LEFT, 1.8*UR).shift(1.2*UP)
        index2Arr = Arrow(LEFT, 1.5*UP+1.6*RIGHT).shift(.3*DOWN)
        self.play(GrowArrow(index1Arr.shift(.1*DOWN + .3*LEFT)))
        self.play(GrowArrow(index2Arr.shift(.2*UP + .3*LEFT)))
        
        self.play(Circumscribe(first_bit_three), shape=Rectangle)
        self.play(Circumscribe(second_bit_three), shape=Rectangle)
        self.play(Circumscribe(first_bit_one), shape=Rectangle)
        self.play(Circumscribe(second_bit_one), shape=Rectangle)
        
        #self.play(FadeOut(index1Arr, index2Arr))
        
        firstCyc = ArcBetweenPoints(start=UP + RIGHT, end=DOWN + RIGHT, radius=2, angle=90).shift(2*UP + .5*RIGHT)
        firstCyc.add_tip()
        self.play(FadeIn(firstCyc))
        
        secondCyc = ArcBetweenPoints(start=DOWN + LEFT, end=UP + LEFT, radius=2, angle=90).shift(2*UP + 5.8*RIGHT)
        secondCyc.add_tip()
        self.play(FadeIn(secondCyc))
        
        cycText = Text("max_cycles=200").shift(2*DOWN + 2*LEFT)
        self.play(Write(cycText))
        
        self.play(FadeOut(Group(*self.mobjects)))
    
    def Future(self):
        len_fp = Text("How long should the finger print be?", font_size=50).shift(2*UP)
        len_bucket = Text("How large should the table be?", font_size=50)
        xor_hash = Text("Why did we hash the fingerprint before the XOR?", font_size=40).shift(2*DOWN)
        self.play(Write(len_fp))
        self.play(Write(len_bucket))
        self.play(Write(xor_hash))
        self.play(FadeOut(len_fp, len_bucket, xor_hash))


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
