from manim import *
# or: from manimlib import *
from manim_slides import Slide
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
import math

# Parent class for all animations
class Bloom(Slide):
    def construct(self):
        # Define input parameters
        array_len = 15
        num_hash = 5
        sample_keys = ["AAA", "GGG", "Langmead"]
        non_keys = ["CCC", "TTT", "Lang"]
        box_size = 8 / (array_len)
        

        ################# Title: #################
        # Text for title slide
        title = Title(f"Bloom Filter")
        subtitle1 = Text(f"Computational Genomics: Final Project",
                         slant=ITALIC).next_to(title, DOWN)
        subtitle2 = Text(f"Team 42", slant=ITALIC).next_to(subtitle1, DOWN)
        subtitle3 = Text(f"Aidan Aug, Karen He, Mark Tiavises, Alan Zhang",
                         slant=ITALIC).next_to(subtitle2, DOWN)
        self.play(Write(title), run_time=1)
        self.play(Write(subtitle1.scale(0.6)), run_time=0.5)
        self.play(Write(subtitle2.scale(0.5)), Write(subtitle3.scale(0.5)), run_time=0.5)
        title_text = VGroup(title, subtitle1, subtitle2, subtitle3)

        # Create a Mobject array
        array = Array(array_len=array_len, box_size=box_size,
                      fill_color=DARK_GRAY, color=LIGHT_GRAY, indices=True)
        array.shift(ORIGIN, DOWN).scale(2)
        hash_text_group = []

        # Create hash-function names
        for i in range(num_hash):
            mathText = MathTex(f"h{i}")
            mathText.shift(array.get_center())
            hash_text_group.append(mathText)

        for i, hash_mobj in enumerate(hash_text_group):
            hash_mobj.shift(RIGHT*(i-num_hash//2) * 0.5 + UP*4)
        

        # Generate the flower animation and draw
        bloom_flower, all_bezier = self.flower_animation(array, hash_text_group, num_hash)

        self.play(Write(bloom_flower), run_time=2)

        self.pause()

        self.play(Unwrite(all_bezier), Unwrite(title_text))

        # Create Pseudocode Block
        self.function_arrow = Arrow(buff=0.2, start=ORIGIN, end=RIGHT,
                           stroke_width=8, max_stroke_width_to_length_ratio=10)
        box = self.create_function()
        input_mobject = self.show_input(box, sample_keys, non_keys)

        ############### Slide 1: Initialize array of zeros ###############
        array.init_val_zero()
        array.show_indices()
        self.slide1(array)
        self.highlight(self.code_lines, 0, 1)

        ############### Slide 2: Shift and move hash functions above the array###############
        self.slide2(array, hash_text_group, num_hash)
        self.highlight(self.code_lines, 1, 2)
        num_bloom_keys, math_prob_val = self.add_probability(num_hash, array_len, input_mobject)

        ############### Slide 3: Map each key to the block ###############
        self.slide3(array, num_hash, hash_text_group, sample_keys, num_bloom_keys, math_prob_val)
        self.highlight(self.code_lines, 2, 3)

        ############### Slide 4: Query keys we stored ###############
        self.slide4(array, num_hash, hash_text_group, sample_keys)
        self.highlight(self.code_lines, 3, 4)

        ############### Slide 5: Query keys not stored ###############
        self.slide5(array, num_hash, hash_text_group, non_keys)

        ################ Fade out everything ###############
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        ################ Conclsion slide ###############
        self.conclusion()
        self.wait()


    # Generates the flower animation on the title screen
    def flower_animation(self, array, hash_text_group, num_hash):
        bloom_flower = VGroup()
        all_bezier = VGroup() # For unwriting the generated curved lines

        hash_indices = np.arange(num_hash)

        bloom_flower.add(array)
        squares = array.get_squares()
        for i, square in enumerate(squares):
            p1 = square.get_center()
            p1b = p1 + [0, 0.75, 0]
            d1 = Dot(point=p1).set_color(BLUE)
            l1 = Line(p1b, p1)
            p2 = hash_text_group[hash_indices[i % num_hash]].get_center()
            p2b = p2 - [0, 0.75, 0]
            d2 = Dot(point=p2).set_color(RED)
            l2 = Line(p2, p2b)
            bezier = CubicBezier(p2b, p2b - UP, p1b + UP, p1b)
            total = VGroup(d2, l2, bezier, l1, d1)
            total.set_color(random_bright_color())
            all_bezier.add(total)
            bloom_flower.add(d1, d2, total)
        bloom_flower.scale(0.75).shift(DOWN * 2)

        return bloom_flower, all_bezier


    # Moves the yellow arrow in the function block from create_function
    def highlight(self, code_lines, prev_line_num, line_num):
        self.code_lines.submobjects[prev_line_num].set_opacity(0.5)
        self.code_lines.submobjects[line_num].set_opacity(1)
        self.play(Circumscribe(code_lines.submobjects[line_num]),
                  self.function_arrow.animate.move_to(code_lines.submobjects[line_num].get_left() + 0.4 * LEFT))


    # Creates the function for the video in the upper right corner
    def create_function(self):
        title = Text("Bloom Filter", color=WHITE)
        title.scale(0.75)

        # Function for Bloom Filter
        t1 = Text("Initialize array of zeros")
        t2 = Text("Define hash functions \n(universal hashing is a great choice)")
        t3 = Text("Pass key into hash functions and map to array")
        t4 = Text("Query existing key in array")
        t5 = Text("Check non-existing key in array")

        # Group each line for the function
        code_lines = VGroup(t1, t2, t3, t4, t5).next_to(title, 0.5*DOWN)
        self.code_lines = code_lines
        code_lines.set_color(WHITE).scale(0.3).set_opacity(0.5)

        # Put the entire function in a box
        all_code = VGroup(title, t1, t2, t3, t4, t5).arrange(
            direction=DOWN, aligned_edge=LEFT).next_to(ORIGIN, 2*UP)
        box = SurroundingRectangle(all_code, color=BLUE_C, buff=MED_LARGE_BUFF)
        box.move_to(all_code.get_center())

        self.play(Create(box), Write(all_code))
        box.add_updater(lambda x: x.move_to(all_code.get_center()))

        self.function_arrow.move_to(code_lines.submobjects[0].get_left() + 0.4 * LEFT)
        self.play(all_code.animate.to_corner(UR))
        self.highlight(code_lines, 0, 0)
        return box

    # Displays the input strings and output strings
    def show_input(self, box, sample_keys, non_keys):
        input_string = "Input keys:\n["
        for i in range(len(sample_keys)):
            input_string += f"{sample_keys[i]}"
            if i != len(sample_keys) - 1:
                input_string += ","
            else:
                input_string += "]"
                break
            if i % 20 == 19:
                input_string += "\n"
        t1 = Text(input_string).scale(0.35).next_to(
            box, DOWN).set_color(GREEN_A)
        t1.align_to(box, LEFT)
        self.play(Write(t1))

        non_input_string = "Not in input:\n["
        for i in range(len(non_keys)):
            non_input_string += f"{non_keys[i]}"
            if i != len(non_keys) - 1:
                non_input_string += ", "
            else:
                non_input_string += "]"
                break
            if i % 20 == 19:
                non_input_string += "\n"
        t2 = Text(non_input_string).scale(
            0.35).next_to(t1, RIGHT).set_color(RED_A)
        t2.align_to(box, RIGHT)
        self.play(Write(t2))
        return t1


    # Calculates the probability of a false positive
    def calc_probability(self, k, m, n):
      return (1 - math.exp((-k*n)/m))**k
    

    # Generates the text to denote probability and its calculation
    def add_probability(self, num_hash, input_len, input_mobject):
      text = Tex('Probability of a false positive:').scale(0.5).next_to(input_mobject, DOWN).align_to(input_mobject, LEFT)
      self.play(Write(text))

      math_prob = MathTex(r"\left( 1 - e^{- \frac{kn}{m}} \right)^{k}").scale(0.75).next_to(text, 0.5 * DOWN).align_to(text, LEFT)
      self.play(Write(math_prob))

      k_tex = Text(f"k = # indep. hash: {num_hash}").next_to(math_prob, 0.25 * RIGHT).scale(0.3).next_to(math_prob, 0.25 * RIGHT).shift(RIGHT * 0.25)
      m_tex = Text(f"m = table size: {input_len}").next_to(k_tex, 0.5 * DOWN).scale(0.3).align_to(k_tex, LEFT)
      n_tex = Text(f"n = # keys:    ").next_to(m_tex, 0.5 * DOWN).scale(0.3).align_to(k_tex, LEFT)
      num_bloom_keys = ValueTracker(0)
      n_tex_val = always_redraw(lambda: Integer(num_bloom_keys.get_value()).move_to(n_tex.get_right() + 0.25 * RIGHT).scale(0.75))

      all_variables = VGroup(k_tex, m_tex, n_tex)
      self.play(Write(all_variables))
      self.play(Write(n_tex_val))

      math_prob_val = ValueTracker(0)
      math_prob_calc = always_redraw(lambda: DecimalNumber(self.calc_probability(num_hash, input_len, num_bloom_keys.get_value()), num_decimal_places=3).scale(0.75).next_to(text, RIGHT))
      self.play(Write(math_prob_calc))

      return num_bloom_keys, math_prob_val


    # Draw the arrows when putting input or checking
    def map_arrows(self, array, num_hash, hash, bloom_indices, key):
        # Pass in values that map to different place
        self.play(Write(key))
        in_arrows_list = []
        for i in range(num_hash):
            arrow = Arrow(key.get_center() + 0.2 *
                          DOWN, hash[i].get_center())
            in_arrows_list.append(arrow)

        out_arrows = VGroup()
        out_arrows_list = []
        indices = array.get_squares()

        for i in range(num_hash):
            radius = 1 if i < i//2 else -1
            mapped_index = bloom_indices[i]
            arrow = CurvedArrow(hash[i].get_center(), indices[mapped_index].get_center(), radius=10*radius
                                ).set_color_by_gradient(random_bright_color(), random_bright_color())
            out_arrows_list.append(arrow)
            out_arrows.add(arrow)

        animate_in_arrows = []
        for i in (in_arrows_list):
            animate_in_arrows.append(ShowCreationThenFadeOut(i))

        self.play(*animate_in_arrows, run_time=2)

        return out_arrows_list


    # The first slide
    def slide1(self, array):
        self.play(array.animate.shift(
            UP*0.5).shift(LEFT*2).scale(0.7), run_time=1)
        self.pause()  # Waits user to press continue to go to the next slide


    # The second slide
    def slide2(self, array, hash, num_hash):
        for i, item in enumerate(hash):
            item.shift(array.get_center() + RIGHT * (i - num_hash//2))
        all_hash = VGroup(*hash)
        self.play(FadeIn(all_hash))
        self.pause()


    # The third slide
    def slide3(self, array, num_hash, hash, sample_keys, num_bloom_keys, math_prob_val):
        bloom_indices_all = [[0, 4, 9, 10, 13],
                             [0, 5, 9, 10, 11], [0, 1, 3, 8, 8]] # Preset values
        count = 0

        # Animate the arrows when inputting data
        for i, key in enumerate(sample_keys):
            bloom_indices = bloom_indices_all[i]
            key = Tex(key).move_to(array.get_center() + 5 * UP)
            out_arrows_list = self.map_arrows(
                array, num_hash, hash, bloom_indices, key)

            animate_out_arrows = []
            nums = array.get_values()
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            for i in set(bloom_indices):
                animate_out_arrows.append(Write(nums[i].set_value(1)))
            self.play(*animate_out_arrows)
            count += 1
            self.play(num_bloom_keys.animate.set_value(count), run_time = 2)
            self.play(math_prob_val.animate.set_value(math_prob_val.get_value()), run_time = 2)
            
            self.pause()
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key), run_time=1)


    # The 4th slide: Checking existing keys (mapped to same indices)
    def slide4(self, array, num_hash, hash, sample_keys):
        bloom_indices_all = [[0, 4, 9, 10, 13],
                             [0, 5, 9, 10, 11], [0, 1, 3, 8, 8]]
        for i, key in enumerate(sample_keys):
            bloom_indices = bloom_indices_all[i]
            key_tex = Tex(key).move_to(array.get_center() + 5 * UP)

            out_arrows_list = self.map_arrows(
                array, num_hash, hash, bloom_indices, key_tex)
            output = f"Key {key} might exist in the data structure!"
            color = PURE_GREEN

            animate_out_arrows = []
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            self.play(*animate_out_arrows)

            confirm = Text(output).set_color(
                color).next_to(array, DOWN).scale(0.5)
            self.play(Write(confirm), run_time=1)
            self.pause()
            self.play(Unwrite(confirm), run_time=1)
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key_tex), run_time=1)

    # The 5th slide: Checking non-input keys (mapped to same or different indices by chance)
    def slide5(self, array, num_hash, hash, non_keys):
       
        bloom_indices_all = [[0, 4, 7, 10, 14],
                             [0, 3, 9, 11, 13], [0, 2, 3, 8, 12]]
        yes_no = [0, 1, 0]
        for i, key in enumerate(non_keys):
            bloom_indices = bloom_indices_all[i]
            key_tex = Tex(key).move_to(array.get_center() + 5 * UP)
            out_arrows_list = self.map_arrows(
                array, num_hash, hash, bloom_indices, key_tex)

            if yes_no[i] == 0:
                output = f"Key {key} does not exist in the data structure!"
                color = RED_C
            else:
                output = f"Key {key} might exist in the data structure!"
                color = PURE_GREEN

            animate_out_arrows = []
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            self.play(*animate_out_arrows)

            confirm = Text(output).set_color(
                color).next_to(array, DOWN).scale(0.5)
            self.play(Write(confirm), run_time=1)
            self.pause()
            self.play(Unwrite(confirm), run_time=1)
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key_tex), run_time=1)


    # Conclusion
    def conclusion(self):
        # Text for conclusion slide
        title = Text(f"Thank you!")
        subtitle1 = Text(f"Computational Genomics: Final Project",
                         slant=ITALIC).next_to(title, DOWN)
        subtitle2 = Text(f"Team 42", slant=ITALIC).next_to(subtitle1, DOWN)
        subtitle3 = Text(f"Aidan Aug, Karen He, Mark Tiavises, Alan Zhang",
                         slant=ITALIC).next_to(subtitle2, DOWN)
        self.play(Write(title), run_time=1)
        self.play(Write(subtitle1.scale(0.6)), run_time=0.5)
        self.play(Write(subtitle2.scale(0.5)), Write(
            subtitle3.scale(0.5)), run_time=0.5)


# Creates an object that looks like an array
class Array(VMobject):
    def __init__(self, array_len, box_size, color=WHITE, indices=False, **kwargs):
        # Set properties
        self.array_len = array_len
        self.box_size = box_size
        self.squares = []
        self.nums = []
        self.indices = []
        VMobject.__init__(self, **kwargs)
        square = Square(side_length=box_size, color=color)

        # Create the squares in array
        for i in range(array_len):
            square1 = Square(side_length=box_size, color=color).next_to(
                square, RIGHT, buff=0).set_style(fill_color=DARK_GRAY, fill_opacity=1)
            square = square1
            self.add(square)
            self.squares.append(square)

        self.center()

    # Return the MObject related to each square in a list
    def get_squares(self):
        return self.squares

    # Add the indices
    def init_val_zero(self):
        next_num = Integer()
        # Fill indices with value
        for i in range(self.array_len):
            next_num = Integer().move_to(self.squares[i].get_center())
            next_num.move_to(self.squares[i].get_center())
            self.nums.append(next_num)
            self.add(next_num)

    # Returns the actual number values inside each box
    def get_values(self):
        return self.nums

    # Creates indices beneath the array
    def show_indices(self):
        for i in range(self.array_len):
            next_num = Integer()
            # Fill indices with value
            for i in range(len(self.nums)):
                index = Integer(number=i).scale(
                    0.5).next_to(self.nums[i], DOWN * 1.5)
                self.indices.append(next_num)
                self.add(index)

        return self.nums

