from manim import *
# or: from manimlib import *
from manim_slides import Slide
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
import random


class CountMinIntro(Slide):
    def construct(self):
        # Define input parameters
        array_len = 10
        num_hash = 3
        sample_keys = ["AAA", "GGG", "AAA", "AAA", "GGG", "ATA"]
        test_keys = ["AAA", "GGG", "TTT"]
        box_size = 8 / (array_len)

        # Create the array
        array = TwoDArray(array_len=array_len, num_hash=num_hash, box_size=box_size,
                      fill_color=DARK_GRAY, color=LIGHT_GRAY, indices=True)
        array.shift(ORIGIN, DOWN * 1.5 + RIGHT * 4).scale(0.5)
        squares = array.get_squares()

        ################# Title #################
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

        # Generate introductory animation on title slide
        count_min_intro, hash_text_group = self.count_min_intro_animation(array_len, num_hash, array)
        self.play(Unwrite(title_text))

        ################# Generate the description + pseudocode #################
        ## left-hand description
        blist1_title = Text("About").next_to(title, DOWN).scale(0.5)
        blist1 = BulletedList(
          "Probabilistic Data Structure", 
          "Similar to Bloom, but with input data stream", 
          "Estimates frequency of input", 
          height=2, width=5).next_to(blist1_title, DOWN)
        blist1_all = VGroup(blist1_title, blist1).to_edge(LEFT)
        self.play(Write(blist1_title))
        self.play(Write(blist1))

        ## right-hand pseudocode
        blist2_title = Text("How to Use:").scale(0.5)
        blist2 = BulletedList(
          "Initialize 2D array of 0", 
          "Pass input through each hash + map to indices", 
          "Query: take min of mapped indices", 
          height=2, width=5).next_to(blist2_title, DOWN)
        blist2_all = VGroup(blist2_title, blist2).next_to(title, DOWN).to_edge(RIGHT)
        self.play(Write(blist2_title))
        self.play(Write(blist2))
        self.pause()
        
        ############### Slide 1: Initialize array of zeros and show input ###############
        self.play(blist2.animate.set_color_by_tex("Initialize 2D array of 0", YELLOW), run_time=1)
        array.init_val_zero()
        array.show_indices()
        self.show_input(sample_keys, test_keys)
        
        ############### Slide 2: Pass in input into Count Min Sketch ###############
        self.play(blist2.animate.set_color_by_tex("Initialize 2D array of 0", WHITE), run_time=1)
        self.play(blist2.animate.set_color_by_tex("Pass input through each hash + map to indices", YELLOW), run_time=1)
        self.slide2(sample_keys, count_min_intro, num_hash, hash_text_group, array)
        
        ############### Slide 3: Make space for query procedure description ###############
        self.slide3(blist1_all, blist2_all, title)
        self.play(blist2.animate.set_color_by_tex("Pass input through each hash + map to indices", WHITE), run_time=1)
        self.play(blist2.animate.set_color_by_tex("Query: take min of mapped indices", YELLOW), run_time=1)
        self.pause()

        ############### Slide 4: Query the test strings ###############
        self.slide4(test_keys, count_min_intro, num_hash, hash_text_group, array)
        self.pause()

        # ################ Fade out everything ###############
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        ############### Conclusion ###############
        self.conclusion()


    def count_min_intro_animation(self, array_len, num_hash, array):
      # Create the introductory animation        
      count_min_intro = VGroup()
      count_min_intro.add(array)

      # Create and add hash function names
      hash_text_group = []
      for i in reversed(range(num_hash)):
          mathText = MathTex(f"h{i + 1}")
          mathText.shift(array.get_center())
          hash_text_group.append(mathText)

      for i, hash_mobj in enumerate(hash_text_group):
          hash_mobj.next_to(array.get_left() + LEFT * 3 + (num_hash//2 - i) * DOWN)
          count_min_intro.add(hash_mobj)

      self.play(Write(count_min_intro))

      # Generate the stream of data animation
      self.start_loop()

      d1 = Dot().set_color(ORANGE)
      l1 = Line(3 * LEFT, RIGHT).to_edge(LEFT).set_y(count_min_intro.get_y())
      l2 = VMobject()
      self.add(d1, l1, l2)
      l2.add_updater(lambda x: x.become(Line(l1.get_left(), d1.get_center()).set_color(ORANGE)))
      self.play(MoveAlongPath(d1, l1), rate_func=linear)
      
      # Map orange dot to the hash functions
      in_arrows_list = []
      for i in range(num_hash):
          arrow = Arrow(d1.get_center(), hash_text_group[i].get_center())
          in_arrows_list.append(arrow)

      # Map hash function values to indices in the 2D array
      out_arrows_list = []
      squares = array.get_squares()
      for i in range(num_hash):
          radius = 1 if i < i//2 else -1
          rand_m = random.randint(0, array_len - 1)
          arrow = CurvedArrow(hash_text_group[i].get_center(), squares[num_hash-i-1][rand_m].get_center(), radius=10*radius
                              ).set_color_by_gradient(random_bright_color(), random_bright_color())
          out_arrows_list.append(arrow)

      # Group animations for simultaneous animation
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

      # Play all animations
      self.play(*animate_in_arrows, run_time=1)
      self.play(*delete_in_arrows, run_time=0.5)
      self.play(*animate_out_arrows, run_time=1)
      self.play(*delete_out_arrows, run_time=0.5)
      
      self.remove(d1)
      self.end_loop()
      self.play(FadeOut(d1), FadeOut(l2), run_time=2)

      self.pause()
      self.wait(duration=1)

      return count_min_intro, hash_text_group

    # 1st slide: animate initial input and initialization of array
    def slide1(self, array, sample_keys, test_keys):
        array.init_val_zero()
        array.show_indices()
        self.show_input(sample_keys, test_keys)

    # 2nd slide: Pass in input as data stream, mapping to indices
    def slide2(self, sample_keys, count_min_intro, num_hash, hash_text_group, array):
        all_m_vals = [
          [0, 4, 9],
          [1, 3, 9],
          [0, 4, 8],
          [0, 4, 8],
          [1, 3, 9],
          [8, 2, 5]
          ]

        for i, key in enumerate(sample_keys):
          key_mobj = Tex(key).scale(0.75)
          d1 = Dot().set_color(ORANGE)
          key_mobj.add_updater(lambda x: x.move_to(d1.get_center() + UP * 0.5))
          
          l1 = Line(3 * LEFT, RIGHT).to_edge(LEFT).set_y(count_min_intro.get_y()) # white line
          d1.move_to(l1.get_left())
          self.play(Write(key_mobj))

          l2 = VMobject() # orange line
          self.add(d1, l1, l2)
          l2.add_updater(lambda x: x.become(Line(l1.get_left(), d1.get_center()).set_color(ORANGE)))
          self.play(MoveAlongPath(d1, l1), rate_func=linear, run_time=3)
          self.play(Unwrite(key_mobj), run_time=0.5)

          ## Arrows
          delete_out_arrows = self.map_arrows(num_hash, hash_text_group, d1, all_m_vals[i], array)
          d1.move_to(l1.get_left())
          nums = array.get_values()
          update_vals = []
          m_vals = all_m_vals[i]
          for i in range(num_hash):
            cur = nums[i][m_vals[num_hash - i - 1]].get_value() + 1
            update_vals.append(Write(nums[i][m_vals[num_hash - i - 1]].set_value(cur)))
          self.play(*update_vals, run_time = 1)
          self.play(*delete_out_arrows, run_time=0.5)

    # 3rd slide: Shift to make space for query procedure description
    def slide3(self, blist1_all, blist2_all, title):
        self.play(Unwrite(blist1_all))
        self.play(blist2_all.animate.to_edge(LEFT))
        self.wait(duration=1)

        blist3_title = Text("Query:").scale(0.5)
        blist3 = BulletedList(
          "Take min of values at mapped indices",
          "Provides an upper bound for frequency", 
          height=2, width=5).next_to(blist3_title, DOWN)
        blist3_all = VGroup(blist3_title, blist3).next_to(title, DOWN).to_edge(RIGHT)
        self.play(Write(blist3_all))

    # 4th slide: Query the strings in test_keys
    def slide4(self, test_keys, count_min_intro, num_hash, hash_text_group, array):
        squares = array.get_squares()
        all_m_vals = [
          [0, 4, 9],
          [1, 3, 9],
          [5, 2, 8],
          ]
        for i, key in enumerate(test_keys):
          key_mobj = Tex(key).scale(0.75)
          d1 = Dot().set_color(ORANGE)
          l1 = Line(3 * LEFT, RIGHT).to_edge(LEFT).set_y(count_min_intro.get_y())
          d1.move_to(l1.get_left())
          key_mobj.add_updater(lambda x: x.move_to(d1.get_center() + UP * 0.5))
          self.play(Write(key_mobj))
          l2 = VMobject()
          self.add(d1, l1, l2)
          l2.add_updater(lambda x: x.become(Line(l1.get_left(), d1.get_center()).set_color(ORANGE)))
          self.play(MoveAlongPath(d1, l1), rate_func=linear, run_time=3)
          self.play(Unwrite(key_mobj), run_time=0.5)

          ## Arrows
          delete_out_arrows = self.map_arrows(num_hash, hash_text_group, d1, all_m_vals[i], array)
          d1.move_to(l1.get_left())
          nums = array.get_values()
          update_vals = []
          m_vals = all_m_vals[i]
          all_hash_vals = []
          for i in range(num_hash):
            cur = str(nums[i][m_vals[num_hash - i - 1]].get_value())
            all_hash_vals.append(cur)

          self.play(*delete_out_arrows, run_time=0.5)

          # Display the equation underneath underneath
          min_val = MathTex(f'\min ( {",".join(all_hash_vals)} ) = {min(all_hash_vals)}').next_to(array, DOWN)
          self.play(Write(min_val))
          self.wait(duration=1)
          self.play(Unwrite(min_val))

    # Text for conclusion slide
    def conclusion(self):
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

    # Maps arrows to indices in array          
    def map_arrows(self, num_hash, hash, d1, m_vals, array):
        squares = array.get_squares()
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

        return delete_out_arrows

      
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

        non_input_string = "Query keys:\n["
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
            0.35).next_to(t1, DOWN).set_color(BLUE_A).align_to(t1, LEFT)
        
        all_input = VGroup(t1, t2).to_corner(LEFT + DOWN)
        self.play(Write(all_input))


# Creates a MObject that looks like a 2D array
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

