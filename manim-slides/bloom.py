from manim import *
# or: from manimlib import *
from manim_slides import Slide
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
import random
from BloomFilter import BloomFilter


class Bloom(Slide):
    def construct(self):
        # Add a plane for visualization
        # plane = NumberPlane(background_line_style={
        #     "stroke_color": TEAL,
        #     "stroke_width": 4,
        #     "stroke_opacity": 0.6
        # })
        # self.add(plane)
        ## Define input parameters
        
        array_len = 10
        num_hash = 5
        sample_keys = ["Ben", "Langmead"]
        non_keys = ["Aidan", "Aug"]
        box_size = array_len / (array_len + 5)
        bloom_filter = BloomFilter(num_hash = num_hash, size=array_len)

        # Slide 1: Initialize array of zeros
        array = Array(array_len=array_len, box_size=box_size, fill_color=DARK_GRAY, color=LIGHT_GRAY, indices=True)
        array.set_indices()

        # Create Pseudocode Block
        self.arrow = Arrow(buff=0.2, start=ORIGIN, end=RIGHT, stroke_width=8, max_stroke_width_to_length_ratio=10)
        self.create_function()

        self.slide1(array)
        self.highlight(self.code_lines, 0, 1)
        
        ## Slide 2: Shift and move hash functions above the array
        hash = []
        for i in range(num_hash):
            mathText = MathTex(f"h{i}")
            mathText.shift(array.get_center() + RIGHT*(i-num_hash//2) + UP*2)
            hash.append(mathText)

        self.slide2(array, hash, num_hash)
        self.highlight(self.code_lines, 1, 2)

        #Slide 3: Map each key to the block
        self.slide3(array, num_hash, hash, sample_keys, bloom_filter)

        self.highlight(self.code_lines, 2, 3)
        #self.slide4(array, num_hash, hash, sample_keys, bloom_filter)

        self.highlight(self.code_lines, 3, 4)
        self.slide5(array, num_hash, hash, non_keys, bloom_filter)
        self.wait()


    
    def create_function(self):
        title = Text("Bloom Filter", color=WHITE)
        title.scale(0.75)

        # Process for Bloom Filter
        t1 = Text("     Initialize array of zeros")
        t2 = Text("     Define hash functions")
        t3 = Text("     Pass key into hash functions and map to array")
        t4 = Text("     Check existing key in array")
        t5 = Text("     Check non-existing key in array")

        code_lines = VGroup(t1, t2, t3, t4, t5).next_to(title,0.5*DOWN)
        self.code_lines = code_lines
        code_lines.set_color(WHITE).scale(0.3).set_opacity(0.5)

        all_code = VGroup(title, t1, t2, t3, t4, t5).arrange(direction=DOWN, aligned_edge=LEFT).next_to(ORIGIN, 2*UP)
        box = SurroundingRectangle(all_code, color=YELLOW, buff=MED_LARGE_BUFF)
        box.move_to(all_code.get_center())

        self.play(Create(box), Write(all_code))
        box.add_updater(lambda x: x.move_to(all_code.get_center()))

        self.arrow.move_to(code_lines.submobjects[0].get_left() + 0.4 * LEFT)
        self.play(all_code.animate.to_corner(UR))
        self.highlight(code_lines, 0, 0)


    def highlight(self, code_lines, prev_line_num, line_num):
        self.code_lines.submobjects[prev_line_num].set_opacity(0.5)
        self.code_lines.submobjects[line_num].set_opacity(1)
        self.play(Circumscribe(code_lines.submobjects[line_num]), 
            self.arrow.animate.move_to(code_lines.submobjects[line_num].get_left() + 0.4 * LEFT))


    def slide1(self, array):
        self.play(DrawBorderThenFill(array), array.animate.shift(DOWN*2).shift(LEFT*2).scale(0.7), run_time=1)
        self.pause() # Waits user to press continue to go to the next slide
    
    #Shift
    def slide2(self, array, hash, num_hash):
        #all_hash = VGroup()
            #all_hash.add(mathText)
        #all_hash.add_updater(lambda x: x.move_to(array.get_center()+UP*2))
        all_hash = VGroup(*hash).add_updater(lambda x: x.move_to(array.get_center()+UP*2))
        self.play(FadeIn(all_hash))
        self.pause()
            

    def map_arrows(self, array, num_hash, hash, bloom_indices, key):
            # Pass in values that map to different place
            self.play(Write(key))
            in_arrows_list = []
            for i in range(num_hash):
                radius = 1 if i < i//2 else -1
                arrow = CurvedArrow(key.get_center() + 0.5 *
                                    DOWN, hash[i].get_center(), radius=10*radius)
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
            
    # Animate the updating of values
    def slide3(self, array, num_hash, hash, sample_keys, bloom_filter):
        # Animate the hash functions
        for key in sample_keys:
            bloom_indices = bloom_filter.store_return_indices(key)
            key = Tex(key).move_to(array.get_center() + 4 * UP)
            out_arrows_list = self.map_arrows(array, num_hash, hash, bloom_indices, key)
            
            animate_out_arrows = []
            nums = array.get_indices()
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            for i in set(bloom_indices):
                animate_out_arrows.append(Write(nums[i].set_value(1)))
            self.play(*animate_out_arrows)


            self.pause()
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key), run_time=1)
            

    def slide4(self, array, num_hash, hash, sample_keys, bloom_filter):
        for key in sample_keys:
            bloom_indices = bloom_filter.check_return_indices(key)
            key = Tex(key).move_to(array.get_center() + 4 * UP)

            out_arrows_list = self.map_arrows(array, num_hash, hash, bloom_indices, key)
            
            if bloom_filter.check(key) == 0:
                output = f"Key {key} does not exist in the data structure!"
                color = PURE_RED
            else:
                output = f"Key {key} probably exists in the data structure!"
                color = PURE_GREEN

            animate_out_arrows = []
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            self.play(*animate_out_arrows)

            confirm = Text(output).set_color(color).next_to(array,DOWN).scale(0.5)
            self.play(Write(confirm), run_time=1)
            self.pause()
            self.play(Unwrite(confirm), run_time=1)
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key), run_time=1)

    def slide5(self, array, num_hash, hash, non_keys, bloom_filter):
        for key in non_keys:
            bloom_indices = bloom_filter.check_return_indices(key)
            key_tex = Tex(key).move_to(array.get_center() + 4 * UP)
            out_arrows_list = self.map_arrows(array, num_hash, hash, bloom_indices, key_tex)

            if bloom_filter.check(key) == 0:
                output = f"Key {key} does not exist in the data structure!"
                color = PURE_RED
            else:
                output = f"Key {key} probably exists in the data structure!"
                color = PURE_GREEN

        
            animate_out_arrows = []
            for i in (out_arrows_list):
                animate_out_arrows.append(Create(i))
            self.play(*animate_out_arrows)

            confirm = Text(output).set_color(color).next_to(array,DOWN).scale(0.5)
            self.play(Write(confirm), run_time=1)
            self.pause()
            self.play(Unwrite(confirm), run_time=1)
            self.play(Unwrite(VGroup(*out_arrows_list)), run_time=1)
            self.play(Unwrite(key_tex), run_time=1)
        



class Array(VMobject):
    def __init__(self, array_len, box_size, color=WHITE, indices=False, **kwargs):
        # Set properties
        self.array_len = array_len
        self.box_size = box_size
        self.squares = []
        self.nums= []
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


    def get_squares(self):
        return self.squares
    
    # Add the indices
    def set_indices(self):
        next_num = Integer()
        # Fill indices with value
        for i in range(self.array_len):
            next_num = Integer().move_to(self.squares[i].get_center())
            next_num.move_to(self.squares[i].get_center())
            self.nums.append(next_num)
            self.add(next_num)
    
    def get_indices(self):
        return self.nums


class CodeFromString(Scene):
    def construct(self, input, non_input):
        code = f'''import BloomFilter

'''

class CodeFromString():
    def construct(self, input, non_input):
        code = f'''import BloomFilter
input_items = {input}
non_input_items = {non_input}

bloom = BloomFilter()
for key in input_items:
    bloom.store(key)

for key in input_items:
    bloom.check(key)

for key in non_input:
    bloom.check(key)
'''