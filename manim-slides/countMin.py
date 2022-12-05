from manim import *
# or: from manimlib import *
from manim_slides import Slide
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
from BloomFilter import BloomFilter
import random
import math


class CountMinIntro(Slide):
    def construct(self):
        # Define input parameters

        array_len = 10
        num_hash = 3
        sample_keys = ["AAA", "GGG"] #"AAA", "AAA", "GGG", "ATA"
        test_keys = ["AAA", "GGG", "TTT"]
        box_size = 8 / (array_len)

        # Create the array
        array = TwoDArray(array_len=array_len, num_hash=num_hash, box_size=box_size,
                      fill_color=DARK_GRAY, color=LIGHT_GRAY, indices=True)
        array.shift(ORIGIN, DOWN * 1.5 + RIGHT * 4).scale(0.5)
        squares = array.get_squares()

        ################# Title: #################
        count_min = VGroup(array)
        hash = []
        

        # Create text
        for i in reversed(range(num_hash)):
            mathText = MathTex(f"h{i + 1}")
            mathText.shift(array.get_center())
            hash.append(mathText)

        for i, hash_mobj in enumerate(hash):
            hash_mobj.next_to(array.get_left() + LEFT * 3 + (num_hash//2 - i) * DOWN)
            count_min.add(hash_mobj)
            
        # Text for title slide
        title = Title(f"Count Min Sketch")
        subtitle1 = Text(f"Computational Genomics: Final Project",
                         slant=ITALIC).next_to(title, DOWN)
        subtitle2 = Text(f"Team 42", slant=ITALIC).next_to(subtitle1, DOWN)
        subtitle3 = Text(f"Aidan Aug, Karen He, Mark Tiavises, Alan Zhang",
                         slant=ITALIC).next_to(subtitle2, DOWN)
        self.play(Write(title), run_time=1)
        self.play(Write(subtitle1.scale(0.6)), run_time=0.5)
        self.play(Write(subtitle2.scale(0.5)), Write(
            subtitle3.scale(0.5)), run_time=0.5)
        title_text = VGroup(subtitle1, subtitle2, subtitle3)
        self.play(Write(count_min))

        # Generate the stream
        self.start_loop()

        d1 = Dot().set_color(ORANGE)
        l1 = Line(3 * LEFT, RIGHT).to_edge(LEFT).set_y(count_min.get_y())
        l2 = VMobject()
        self.add(d1, l1, l2)
        l2.add_updater(lambda x: x.become(Line(l1.get_left(), d1.get_center()).set_color(ORANGE)))
        self.play(MoveAlongPath(d1, l1), rate_func=linear)
        
        in_arrows_list = []
        for i in range(num_hash):
            arrow = Arrow(d1.get_center(), hash[i].get_center())
            in_arrows_list.append(arrow)

        out_arrows_list = []
        for i in range(num_hash):
            radius = 1 if i < i//2 else -1
            rand_m = random.randint(0, array_len - 1)
            arrow = CurvedArrow(hash[i].get_center(), squares[num_hash-i-1][rand_m].get_center(), radius=10*radius
                                ).set_color_by_gradient(random_bright_color(), random_bright_color())
            out_arrows_list.append(arrow)

        animate_in_arrows = []
        for i in (in_arrows_list):
            animate_in_arrows.append(GrowArrow(i))
        delete_in_arrows = []
        for i in (in_arrows_list):
            delete_in_arrows.append(Unwrite(i))

        animate_out_arrows = []
        for i in (out_arrows_list):
            animate_out_arrows.append(Create(i))
        delete_out_arrows = []
        for i in (out_arrows_list):
            delete_out_arrows.append(Unwrite(i))

        self.play(*animate_in_arrows, run_time=1)
        self.play(*delete_in_arrows, run_time=0.5)
        self.play(*animate_out_arrows, run_time=1)
        self.play(*delete_out_arrows, run_time=0.5)
        self.remove(d1)
    
        
        self.end_loop()
        self.play(Unwrite(d1), Unwrite(l1), Unwrite(title_text))
        self.pause()
        self.wait()
        

        ############### Slide 1: Initialize array of zeros ###############
        # # Create Pseudocode Block
        blist1_title = Text("About").next_to(title, DOWN).to_edge(LEFT).scale(0.5)
        blist1 = BulletedList(
          "Prob. Data Struct.", 
          "Similar to Bloom, but with input\ndata stream", 
          "Estimates frequency of input", 
          height=2, width=5).next_to(blist1_title, DOWN).to_edge(LEFT)
        self.play(Write(blist1_title))
        self.play(Write(blist1))
        blist1_all = VGroup(blist1_title, blist1)

        blist2_title = Text("How to Use:").scale(0.5)
        blist2 = BulletedList(
          "Initialize 2D array of 0", 
          "Pass input through each hash + map to indices", 
          "Query: take min of mapped indices", 
          height=2, width=5).next_to(blist2_title, DOWN)
        blist2_all = VGroup(blist2_title, blist2).next_to(title, DOWN).to_edge(RIGHT)
        self.play(Write(blist2_title))
        self.play(Write(blist2))
        self.play(blist2.animate.set_color_by_tex("Initialize 2D array of 0", YELLOW), run_time=2)
        array.init_val_zero()
        array.show_indices()

        self.show_input(sample_keys, test_keys)

        d1.move_to(l1.get_left())
        all_m_vals = [
          [0, 4, 9],
          [1, 3, 9],
          [0, 4, 9],
          [0, 4, 9],
          [1, 3, 9],
          [2, 3, 8]
          ]
        for i, key in enumerate(sample_keys):
          key_mobj = Tex(key).scale(0.75)
          key_mobj.add_updater(lambda x: x.move_to(d1.get_center() + UP * 0.5))
          self.play(Write(key_mobj))
          d1 = Dot().set_color(ORANGE)
          l1 = Line(3 * LEFT, RIGHT).to_edge(LEFT).set_y(count_min.get_y())
          d1.move_to(l1.get_left())
          l2 = VMobject()
          self.add(d1, l1, l2)
          l2.add_updater(lambda x: x.become(Line(l1.get_left(), d1.get_center()).set_color(ORANGE)))
          self.play(MoveAlongPath(d1, l1), rate_func=linear, run_time=3)
          self.play(Unwrite(key_mobj), run_time=0.5)

          ## Arrows
          self.map_arrows(num_hash, hash, d1, squares, all_m_vals[i], array)



          d1.move_to(l1.get_left())

          
    def map_arrows(self, num_hash, hash, d1, squares, m_vals, array):
        in_arrows_list = []
        for i in range(num_hash):
            arrow = Arrow(d1.get_center(), hash[i].get_center())
            in_arrows_list.append(arrow)

        out_arrows_list = []
        for i in range(num_hash):
            radius = 1 if i < i//2 else -1
            
            arrow = CurvedArrow(hash[i].get_center(), squares[num_hash-i-1][m_vals[i]].get_center(), radius=10*radius
                                ).set_color_by_gradient(random_bright_color(), random_bright_color())
            out_arrows_list.append(arrow)

        animate_in_arrows = []
        for i in (in_arrows_list):
            animate_in_arrows.append(GrowArrow(i))
        delete_in_arrows = []
        for i in (in_arrows_list):
            delete_in_arrows.append(Unwrite(i))

        animate_out_arrows = []
        for i in (out_arrows_list):
            animate_out_arrows.append(Create(i))
        delete_out_arrows = []
        for i in (out_arrows_list):
            delete_out_arrows.append(Unwrite(i))
        
        self.play(*animate_in_arrows, run_time=1)
        self.play(*delete_in_arrows, run_time=0.5)
        self.play(*animate_out_arrows, run_time=1)
        nums = array.get_values()
        for i in range(num_hash):
          self.play(Write(nums[i][m_vals[num_hash - i - 1]].set_value(1)), run_time=0.5)


        self.play(*delete_out_arrows, run_time=0.5)

    # Animates the input strings and output strings
    def show_input(self, sample_keys, test_keys):
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
        t1 = Text(input_string).scale(0.35).set_color(GREEN_A)

        non_input_string = "Not in input:\n["
        for i in range(len(test_keys)):
            non_input_string += f"{test_keys[i]}"
            if i != len(test_keys) - 1:
                non_input_string += ", "
            else:
                non_input_string += "]"
                break
            if i % 20 == 19:
                non_input_string += "\n"
        t2 = Text(non_input_string).scale(
            0.35).next_to(t1, DOWN).set_color(BLUE_A)
        
        all_input = VGroup(t1, t2).to_corner(LEFT + DOWN)
        self.play(Write(all_input))

    # Moves the yellow arrow in the function block from create_function

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
class TwoDArray(VMobject):
    def __init__(self, array_len, num_hash, box_size, color=WHITE, indices=False, **kwargs):
        # Set properties
        self.array_len = array_len
        self.num_hash = num_hash
        self.box_size = box_size
        self.squares = []
        self.nums = []
        self.indices = []
        VMobject.__init__(self, **kwargs)
        square = Square(side_length=box_size, color=color)

        # Create the squares in array
        for i in range(num_hash): # k
          row = []
          for j in range(array_len): # m
            if j != 0:
                square1 = Square(side_length=box_size, color=color).next_to(
                  square, RIGHT, buff=0).set_style(fill_color=DARK_GRAY, fill_opacity=1)
            else:
                square1 = Square(side_length=box_size, color=color).next_to(
                  square, DOWN, buff=0).set_style(fill_color=DARK_GRAY, fill_opacity=1)

            square = square1
            self.add(square)
            row.append(square)
          self.squares.append(row)
          square = self.squares[i][0]

        self.center()

    # Return the MObject related to each square in a list
    def get_squares(self):
        return self.squares

    # Add the indices
    def init_val_zero(self):
        next_num = Integer()
        # Fill indices with value
        for i in range(self.num_hash):
          new_list = []
          for j in range(self.array_len):
            next_num = Integer().move_to(self.squares[i][j].get_center()).scale(self.box_size)
            next_num.move_to(self.squares[i][j].get_center())
            new_list.append(next_num)
            self.add(next_num)
          self.nums.append(new_list)

    # Returns the actual number values inside each box
    def get_values(self):
        return self.nums

    # Creates indices beneath the array
    def show_indices(self):
        # Horizontal
        for i in range(self.array_len):
              index = Integer(number=i).scale(
                  self.box_size).next_to(self.nums[self.num_hash - 1][i], DOWN * 1.5)
              self.add(index)
        # Vertical
        for i in range(self.num_hash):
              index = Integer(number=i).scale(
                  self.box_size).next_to(self.nums[i][self.array_len - 1], RIGHT * 1.5)
              self.add(index)

