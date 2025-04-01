#!/usr/bin/env python

from manimlib import *
from src.mobject.clock import Clock
from functools import partial
import math


class Test(Scene):
    def construct(self):
        import matplotlib.font_manager as fm

        text = Text("한글 테스트", font="BM Hanna 11yrs Old")
        self.add(text)
        # for font in fm.fontManager.ttflist:
        #     if "B" in font.name:
        #         print(font.name)


class Intro(Scene):
    def construct(self):
        import matplotlib.font_manager as fm

        t1 = Text("학교에서 안가르쳐주는 ", font="BM Hanna 11yrs Old").scale(1.5)
        t2 = Text("더하기", font="BM Hanna 11yrs Old").scale(2.2)

        t3 = Text(" 곱하기!", font="BM Hanna 11yrs Old").scale(2.2)

        img = ImageMobject("/Users/eugenekim/projects/dance-with/first-project/g.jpg")
        img.shift(DOWN * 2).scale(1.5)
        self.add(img)

        t2.set_color(RED)

        group = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.2).shift(2 * UP)
        t4 = Tex(r"+").scale(2).next_to(t2, DOWN)
        t5 = Tex(r"\times").scale(2).next_to(t3, DOWN)

        self.add(group)
        self.add(t4)
        self.add(t5)


class NonCommutative(Scene):
    def construct(self):
        import matplotlib.font_manager as fm

        t1 = Text("퇴근 ", font="BM Hanna 11yrs Old").scale(2)
        t2 = Tex(r"+").scale(2)
        t3 = Text("식사", font="BM Hanna 11yrs Old").scale(2)

        t4 = Text("식사", font="BM Hanna 11yrs Old").scale(2)
        t5 = Tex(r"+").scale(2)
        t6 = Text("퇴근", font="BM Hanna 11yrs Old").scale(2)

        group = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.2).shift(UP * 0.7)
        group2 = VGroup(t4, t5, t6).arrange(RIGHT, buff=0.2).shift(DOWN * 0.7)

        self.play(Write(group))
        self.play(Write(group2))

        self.wait()

        eq = Tex(r" = ").scale(2).next_to(group2, LEFT)
        q = Text(" ? ").scale(2).next_to(group2, RIGHT)

        self.play(Write(eq))
        self.play(Write(q))
        self.wait()


class NonCommutative2(Scene):
    def construct(self):
        # Word Pairs
        t1 = Text("퇴근", font="BM Hanna 11yrs Old").scale(1.5)
        t2 = Tex("+").scale(1.5)
        t3 = Text("식사", font="BM Hanna 11yrs Old").scale(1.5)

        t4 = Text("식사", font="BM Hanna 11yrs Old").scale(1.5)
        t5 = Tex("+").scale(1.5)
        t6 = Text("퇴근", font="BM Hanna 11yrs Old").scale(1.5)

        group = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.2).shift(UP * 0.7)
        group2 = VGroup(t4, t5, t6).arrange(RIGHT, buff=0.2).shift(DOWN * 0.7)

        self.play(Write(group))
        self.play(Write(group2))

        self.wait(2)

        self.play(
            group.animate.move_to(LEFT * 3 + UP * 2),
            group2.animate.move_to(RIGHT * 3 + UP * 2),
            run_time=1.5,
        )

        self.wait(2)

        # Axes for time 1 and time 2
        axes_left_1 = Axes(x_range=[0, 3], y_range=[0, 3], height=2, width=2).shift(
            LEFT * 4 + DOWN * 1
        )
        axes_left_2 = Axes(x_range=[0, 3], y_range=[0, 3], height=2, width=2).shift(
            LEFT * 2 + DOWN * 1
        )
        axes_right_1 = Axes(x_range=[0, 3], y_range=[0, 3], height=2, width=2).shift(
            RIGHT * 2 + DOWN * 1
        )
        axes_right_2 = Axes(x_range=[0, 3], y_range=[0, 3], height=2, width=2).shift(
            RIGHT * 4 + DOWN * 1
        )

        time1_label_left = (
            Text("Time = 1", font="BM Hanna 11yrs Old")
            .scale(0.6)
            .next_to(axes_left_1, DOWN)
            .set_color(ORANGE)
        )
        time2_label_left = (
            Text("Time = 2", font="BM Hanna 11yrs Old")
            .scale(0.6)
            .next_to(axes_left_2, DOWN)
            .set_color(GREEN)
        )
        time1_label_right = (
            Text("Time = 1", font="BM Hanna 11yrs Old")
            .scale(0.6)
            .next_to(axes_right_1, DOWN)
            .set_color(ORANGE)
        )
        time2_label_right = (
            Text("Time = 2", font="BM Hanna 11yrs Old")
            .scale(0.6)
            .next_to(axes_right_2, DOWN)
            .set_color(GREEN)
        )

        self.play(
            ShowCreation(axes_left_1),
            FadeIn(time1_label_left),
            ShowCreation(axes_left_2),
            FadeIn(time2_label_left),
            ShowCreation(axes_right_1),
            FadeIn(time1_label_right),
            ShowCreation(axes_right_2),
            FadeIn(time2_label_right),
        )
        self.wait(1)

        # Vector Transformations
        # Left Side: 퇴근 -> time 1, 식사 -> time 2
        t1_vec = Arrow(
            start=axes_left_1.c2p(0, 0), end=axes_left_1.c2p(1.5, 1), buff=0, color=BLUE
        )
        t1_label = (
            Text("퇴근", font="BM Hanna 11yrs Old")
            .scale(0.8)
            .next_to(t1_vec.get_end(), RIGHT, buff=0.1)
        )

        t3_vec = Arrow(
            start=axes_left_2.c2p(0, 0),
            end=axes_left_2.c2p(1, 2.8),
            buff=0,
            color=GREEN,
        )
        t3_label = (
            Text("식사", font="BM Hanna 11yrs Old")
            .scale(0.8)
            .next_to(t3_vec.get_end(), RIGHT, buff=0.1)
        )

        self.play(TransformFromCopy(t1, t1_vec), FadeIn(t1_label))
        self.play(TransformFromCopy(t3, t3_vec), FadeIn(t3_label))
        self.wait(1)

        # Right Side: 식사 -> time 1, 퇴근 -> time 2
        t4_vec = Arrow(
            start=axes_right_1.c2p(0, 0),
            end=axes_right_1.c2p(1, 2.8),
            buff=0,
            color=GREEN,
        )
        t4_label = (
            Text("식사", font="BM Hanna 11yrs Old")
            .scale(0.8)
            .next_to(t4_vec.get_end(), RIGHT, buff=0.1)
        )

        t6_vec = Arrow(
            start=axes_right_2.c2p(0, 0),
            end=axes_right_2.c2p(1.5, 1),
            buff=0,
            color=BLUE,
        )
        t6_label = (
            Text("퇴근", font="BM Hanna 11yrs Old")
            .scale(0.8)
            .next_to(t6_vec.get_end(), RIGHT, buff=0.1)
        )

        self.play(TransformFromCopy(t4, t4_vec), FadeIn(t4_label))
        self.play(TransformFromCopy(t6, t6_vec), FadeIn(t6_label))
        self.wait(2)

        self.play(Indicate(time1_label_left))
        self.play(Indicate(time2_label_left))

        self.wait(1.5)

        self.play(Indicate(time1_label_right))
        self.play(Indicate(time2_label_right))
        self.wait(2)

        # --- Highlight left group (words + vectors) ---
        left_words_box = SurroundingRectangle(group, color=YELLOW, buff=0.4)
        left_coords_group = VGroup(
            axes_left_1,
            axes_left_2,
            t1_vec,
            t1_label,
            t3_vec,
            t3_label,
            time1_label_left,
            time2_label_left,
        )
        left_coords_box = SurroundingRectangle(
            left_coords_group, color=YELLOW, buff=0.4
        )

        self.play(FadeIn(left_words_box))
        self.play(FadeIn(left_coords_box))
        self.wait(1)

        # --- Highlight right group (words + vectors) ---
        right_words_box = SurroundingRectangle(group2, color=RED, buff=0.4)
        right_coords_group = VGroup(
            axes_right_1,
            axes_right_2,
            t4_vec,
            t4_label,
            t6_vec,
            t6_label,
            time1_label_right,
            time2_label_right,
        )
        right_coords_box = SurroundingRectangle(right_coords_group, color=RED, buff=0.4)

        self.play(FadeIn(right_words_box))
        self.play(FadeIn(right_coords_box))
        self.wait(2)


class Addition(Scene):

    def construct(self):
        eq3 = Tex(r"a + b = b + a").scale(1.5)

        # Group and arrange vertically

        self.play(FadeIn(eq3))


class AddPolygon(Scene):
    def construct(self):
        # Basic Polygon

        polys_l = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=RED,
                    fill_opacity=0.5,
                )
                for j in range(3)
            ],
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(2)
            ],
        ).arrange(RIGHT, buff=0.2)
        # polys_l.shift(3 * LEFT)
        polys_l.shift(UP * 2)

        self.play(DrawBorderThenFill(polys_l), run_time=1)
        self.wait(0.5)

        polys = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(2)
            ],
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=RED,
                    fill_opacity=0.5,
                )
                for j in range(3)
            ],
        ).arrange(RIGHT, buff=0.2)
        polys.shift(0.5 * DOWN)

        equal_sign = Text("=").scale(1.5)
        point = polys.get_left() + 0.5 * LEFT
        equal_sign.move_to(point)

        self.add(equal_sign)  # Add without animation (ManimGL optimized)

        self.play(DrawBorderThenFill(polys), run_time=1)

        self.wait(0.5)
        # equation
        equation = Tex(r"3 + 2 = 2 + 3").scale(1.5)
        equation.shift(DOWN * 2.5)

        self.play(Write(equation))
        self.wait(0.5)


class BarAddition(Scene):
    def construct(self):

        # Create x-axis
        sc = 1.5
        x_axis = NumberLine((0, 5, 1), tick_size=0.05).scale(sc)

        numbers = x_axis.add_numbers(range(0, 6, 1), font_size=30, buff=0.15)

        x_axis.shift(UP * 2.8)
        self.add(x_axis)

        # Create bar of length 3 (Blue) - Align left to tick 0
        bar_3 = Rectangle(
            height=1, width=3, fill_color=BLUE, fill_opacity=0.8, stroke_width=0
        ).scale(sc)
        # bar_3.move_to(x_axis.get_left() + RIGHT * 1.5 + DOWN)  # Align left to 0

        bar_3.next_to(x_axis, DOWN, aligned_edge=LEFT)

        # Label "3" above the blue bar
        label_3 = Tex("3").scale(1.2).move_to(bar_3.get_center())

        # Animate showing the "3" bar
        self.play(FadeIn(bar_3), Write(label_3), run_time=0.5)
        self.wait(0.5)

        # Create bar of length 2 (Red) - Align to right of the blue bar
        bar_2 = Rectangle(
            height=1, width=2, fill_color=RED, fill_opacity=0.8, stroke_width=0
        ).scale(sc)
        bar_2.next_to(bar_3, RIGHT, buff=0)  # Place next to blue bar

        # Label "2" above the red bar
        label_2 = Tex("2").scale(1.2).move_to(bar_2.get_center())

        # Animate showing the "2" bar
        self.play(FadeIn(bar_2), Write(label_2), run_time=0.5)
        self.wait(0.5)

        # Create the final bar of length 5 (Green) - Align left to tick 0
        bar_5 = Rectangle(
            height=1, width=5, fill_color=GREEN, fill_opacity=0.8, stroke_width=0
        ).scale(sc)
        bar_5.next_to(bar_3, DOWN, aligned_edge=LEFT, buff=0)
        # Label "3" above the blue bar
        label_5 = Tex("5").scale(1.2).move_to(bar_5.get_center())

        # Animate the transition into the final green bar
        self.play(
            Transform(bar_3.copy(), bar_5),  # Merge blue into green
            Transform(bar_2.copy(), bar_5),  # Merge red into green
            run_time=0.5,
        )
        self.play(
            Write(label_5),
        )

        self.wait(0.5)

        bar_2b = bar_2.copy()
        # bar_2b.move_to(bar_5.get_left() + RIGHT + DOWN * 1)

        bar_2b.next_to(bar_5, DOWN, aligned_edge=LEFT, buff=0)

        self.play(
            Transform(bar_2.copy(), bar_2b, run_time=0.5),  # Merge red into green
        )

        # Label "2" above the red bar
        label_2 = Tex("2").scale(1.2).move_to(bar_2b.get_center())
        self.play(Write(label_2))

        self.wait(0.5)

        bar_3b = bar_3.copy()
        # bar_3b.move_to(bar_2b.get_right() + RIGHT * 1.5)
        bar_3b.next_to(bar_2b, RIGHT, buff=0)

        self.play(
            Transform(bar_3.copy(), bar_3b, run_time=0.5),  # Merge red into green
        )

        # Label "3" above the blue bar
        label_3 = Tex("3").scale(1.2).move_to(bar_3b.get_center())

        # Animate showing the "3" bar
        self.play(Write(label_3))

        self.wait(0.5)

        # Show "3 + 2 = 5" text at the bottom
        equation = Tex("3 + 2 = 2 + 3").scale(1.5)
        equation.next_to(bar_5, DOWN * 3.8, buff=0.5)

        self.play(Write(equation))
        self.wait()


class AddClockAnimation(Scene):
    def construct(self):
        # clock_face
        def clock_face():
            # Create clock face (circle)
            clock_face = Circle(radius=2, color=WHITE)

            # Create 6-hour marks
            hour_marks = VGroup()
            labels = VGroup()
            for i in range(6):
                angle = i * 60 * DEGREES * (-1)  # 360° / 6 = 60° per hour
                mark = Line(UP * 2, UP * 1.8, color=WHITE)  # Tick marks

                num_label = Text(str(i)).scale(0.7)
                num_label.next_to(mark, UP)

                mark.rotate(angle, about_point=ORIGIN)
                num_label.rotate(angle, about_point=ORIGIN)  # Keep numbers upright

                hour_marks.add(mark)
                labels.add(num_label)

            # Create clock hand (initially pointing up)
            hand = Line(ORIGIN, UP * 1.5, color=YELLOW)

            # Group the clock components
            clock = VGroup(clock_face, hour_marks, labels, hand)

            return clock

        def animate_hand(hand_origin, start_angle, angle_delta, fill_color):
            # Create the first 3-hour pie slice (starts at 0° angle)
            pie_3 = AnnularSector(
                inner_radius=0,
                outer_radius=2,
                angle=0,  # Start with no visible pie slice
                start_angle=start_angle,  # Starts from the top
                fill_color=GREEN,
                fill_opacity=0.5,  # Keep it visible but initially empty
            )
            # self.add(pie_3)  # Add it first so we can update its angle

            self.add(pie_3)
            pie_3.move_to(hand_origin)

            # c1 = Circle()
            # c1.move_to(hand_origin)
            # self.play(FadeIn(c1))

            # Use a ValueTracker to animate the sector's angle
            angle_tracker = ValueTracker(0)

            def update_pie(m):
                new_pie = AnnularSector(
                    inner_radius=0,
                    outer_radius=2,
                    angle=-angle_tracker.get_value(),  # Negative to rotate clockwise
                    start_angle=start_angle,
                    fill_color=fill_color,
                    fill_opacity=0.5,
                )
                new_pie.shift(
                    (ORIGIN[0] - hand_origin[0]) * LEFT
                )  # Keep the pie centered at hand origin
                new_pie.shift(
                    (ORIGIN[1] - hand_origin[1]) * DOWN
                )  # Keep the pie centered at hand origin
                m.become(new_pie)

            pie_3.add_updater(update_pie)
            # Rotate hand 3 hours (180°) + grow the sector together
            self.play(
                Rotate(hand, angle=angle_delta, about_point=hand_origin),
                angle_tracker.animate.set_value(
                    -angle_delta
                ),  # Gradually expand the sector
            )

        clock = clock_face()
        clock.shift(3 * LEFT + UP)
        hand = clock[3]
        hand_origin = hand.get_start()

        # Animate showing the clock
        self.play(FadeIn(clock))

        self.wait(0.5)

        animate_hand(hand_origin, start_angle=PI / 2, angle_delta=-PI, fill_color=GREEN)

        self.wait(0.5)
        animate_hand(
            hand_origin, start_angle=-PI / 2, angle_delta=-2 * PI / 3, fill_color=RED
        )

        clock = clock_face()
        clock.shift(3 * RIGHT + UP)
        hand = clock[3]
        hand_origin = hand.get_start()

        # Animate showing the clock
        self.play(FadeIn(clock))

        self.wait(0.5)

        animate_hand(
            hand_origin, start_angle=PI / 2, angle_delta=-2 * PI / 3, fill_color=RED
        )

        self.wait(0.5)
        animate_hand(
            hand_origin, start_angle=-1 * PI / 6, angle_delta=-PI, fill_color=GREEN
        )

        # equation
        equation = Tex(r"3 + 2 = 2 + 3").scale(1.5)
        equation.shift(DOWN * 2.5)

        self.play(Write(equation))
        self.wait(0.5)


class CommutativeAddition(Scene):
    def construct(self):
        # Define two abstract closed-loop shapes

        shape_a = VMobject()
        shape_a.set_points_as_corners(
            [
                [-1.5, -0.5, 0],
                [-1.0, 0.5, 0],
                [0, 1.0, 0],
                [1.0, 0.5, 0],
                [1.5, -0.5, 0],
                [0, -1.0, 0],
                [-1.5, -0.5, 0],
            ]
        )
        shape_a.set_fill(BLUE, opacity=0.8)
        shape_a.set_stroke(WHITE, width=2)

        # Define shape_b (elongated shape)
        shape_b = VMobject()
        shape_b.set_points_as_corners(
            [
                [-2.0, -0.6, 0],
                [-1.5, 0.5, 0],
                [-0.5, 0.8, 0],
                [0.5, 0.7, 0],
                [1.8, 0.3, 0],
                [2.0, -0.5, 0],
                [1.2, -0.8, 0],
                [-2.0, -0.6, 0],
            ]
        )
        shape_b.set_fill(RED, opacity=0.8)
        shape_b.set_stroke(WHITE, width=2)

        # Position shapes for a + b
        shape_a.move_to(LEFT * 2)
        shape_b.next_to(shape_a, RIGHT, buff=0.5)

        # Create text labels
        text_a = Text("a").scale(1).next_to(shape_a, UP, buff=0.3)
        text_b = Text("b").scale(1).next_to(shape_b, UP, buff=0.4)

        a_group = VGroup(shape_a, text_a)
        b_group = VGroup(shape_b, text_b)

        # Show first equation (a + b)
        self.play(FadeIn(a_group))
        self.play(FadeIn(b_group))
        self.wait(1)

        # Transition to b + a by swapping positions
        shape_a_target = a_group.copy().shift(RIGHT * 4)
        shape_b_target = b_group.copy().shift(LEFT * 4)

        # Animate swap
        self.play(
            Transform(a_group, shape_a_target), Transform(b_group, shape_b_target)
        )
        self.wait(0.5)

        equation = Tex(r"a + b = b + a").scale(1.5)
        equation.shift(DOWN * 2)

        self.play(Write(equation))
        self.wait(0.5)


class Distributive(Scene):
    def construct(self):
        eq = Tex(r"m \cdot (a + b) = m \cdot b + m \cdot a").scale(1.5)
        self.play(FadeIn(eq))
        self.wait(1)

        # Get references to letters
        m1 = eq.get_part_by_tex("m")[0]  # left m
        a = eq.get_part_by_tex("a")[0]  # left a
        b = eq.get_part_by_tex("b")[0]  # left b

        # Create labels (π, π, √2)
        m_val = Tex(r"\pi").scale(1.5).set_color(YELLOW)
        a_val = Tex(r"\pi").scale(1.5).set_color(BLUE)
        b_val = Tex(r"\sqrt{2}").scale(1.2).set_color(GREEN)

        # Position them somewhere below
        m_val.next_to(m1, DOWN, buff=1)
        a_val.next_to(a, DOWN, buff=1)
        b_val.next_to(b, DOWN, buff=1)

        # Arrows
        m_arrow = Arrow(
            start=m_val.get_top(), end=m1.get_bottom(), buff=0.1, color=YELLOW
        )
        a_arrow = Arrow(start=a_val.get_top(), end=a.get_bottom(), buff=0.1, color=BLUE)
        b_arrow = Arrow(
            start=b_val.get_top(), end=b.get_bottom(), buff=0.1, color=GREEN
        )

        # Group them
        subs = VGroup(m_val, a_val, b_val, m_arrow, a_arrow, b_arrow)

        self.play(Write(subs), run_time=2)
        self.wait(2)


class DistributiveSingle(Scene):
    def construct(self):
        # Title
        title = (
            Tex("2(3+4) = 2 \\times 3 + 2 \\times 4")
            .shift(UP * 1.5 + LEFT * 0.5)
            .scale(1.2)
        )

        box_2_3 = SurroundingRectangle(title[7:10], color=YELLOW)
        box_3_2 = SurroundingRectangle(title[11:14], color=RED)
        self.play(FadeIn(title))

        # Function to create a fixed grid structure with empty placeholders
        def create_grid(rows, cols):
            grid = VGroup()
            for row in range(rows):
                row_cells = VGroup()
                for col in range(cols):
                    cell = Square(side_length=0.3, stroke_opacity=0, fill_opacity=0)
                    row_cells.add(cell)
                row_cells.arrange(RIGHT, buff=0.3).shift(DOWN * row * 0.5)
                grid.add(row_cells)

            return grid

        # Function to fill specific cells in the grid with circles
        def fill_circles(grid, filled_counts):
            for row, pair in enumerate(filled_counts):
                count, color = pair
                for col in range(count):
                    circle = Circle(radius=0.12, fill_color=color, stroke_color=color)
                    circle.move_to(grid[row][col].get_center())
                    grid[row][col].add(circle)

        # LHS Representation
        lhs_grid = create_grid(2, 4)
        fill_circles(lhs_grid, [[3, BLUE], [4, ORANGE]])
        lhs_grid.shift(LEFT * 2)

        lhs_boundary = SurroundingRectangle(lhs_grid, color=GREY_A, stroke_width=2)

        self.play(FadeIn(lhs_boundary), FadeIn(lhs_grid))

        # Splitting into two groups (3 and 4 per row)
        lhs_group_3_1 = VGroup(*lhs_grid[0])
        lhs_group_3_2 = VGroup(*lhs_grid[0]).copy()
        lhs_group_4_1 = VGroup(*lhs_grid[1])
        lhs_group_4_2 = VGroup(*lhs_grid[1]).copy()

        lhs_boundary_c = lhs_boundary.copy()

        lhs_group = VGroup(lhs_group_3_2, lhs_group_4_2, lhs_boundary_c)
        self.play(lhs_group.animate.shift(DOWN), run_time=1.5)
        self.wait(0.5)
        rhs_group_3_1 = lhs_group_3_1.copy()
        rhs_group_3_2 = lhs_group_3_2.copy()
        rhs_group_3 = VGroup(rhs_group_3_1, rhs_group_3_2)

        rhs_group_3_1.shift(RIGHT * 3)
        rhs_group_3_2.next_to(rhs_group_3_1, DOWN, buff=0.2)

        rhs3_boundary = SurroundingRectangle(rhs_group_3, color=YELLOW, stroke_width=2)

        rhs_group_4_1 = lhs_group_4_1.copy()
        rhs_group_4_2 = lhs_group_4_2.copy()

        rhs_group_4_1.next_to(rhs_group_3_2, DOWN, buff=0.2)
        rhs_group_4_2.next_to(rhs_group_4_1, DOWN, buff=0.2)

        rhs_group_4 = VGroup(rhs_group_4_1, rhs_group_4_2)
        rhs4_boundary = SurroundingRectangle(rhs_group_4, color=RED, stroke_width=2)
        # self.add(rhs_group_3)
        # self.add(rhs_group_3c)

        self.play(
            Transform(lhs_group_3_1.copy(), rhs_group_3_1),
            Transform(lhs_group_3_2.copy(), rhs_group_3_2),
            run_time=1.5,
        )
        self.play(
            FadeIn(rhs3_boundary),
            FadeIn(box_2_3),
        )
        self.play(
            Transform(lhs_group_4_1.copy(), rhs_group_4_1),
            Transform(lhs_group_4_2.copy(), rhs_group_4_2),
            run_time=1.5,
        )

        self.play(FadeIn(rhs4_boundary), FadeIn(box_3_2))

        self.wait(2)


class Distributive3232Area(Scene):
    def construct(self):
        # distributive area
        eq1 = Tex("(3+2) \\times (3+2)").shift(LEFT * 4 + UP)
        bc = BLUE
        box_3_3_1 = SurroundingRectangle(eq1[1], color=bc)
        box_3_3_2 = SurroundingRectangle(eq1[7], color=bc)

        box_3_2_1 = SurroundingRectangle(eq1[1], color=bc)
        box_3_2_2 = SurroundingRectangle(eq1[9], color=bc)

        box_2_3_1 = SurroundingRectangle(eq1[3], color=bc)
        box_2_3_2 = SurroundingRectangle(eq1[7], color=bc)

        box_2_2_1 = SurroundingRectangle(eq1[3], color=bc)
        box_2_2_2 = SurroundingRectangle(eq1[9], color=bc)

        self.play(FadeIn(eq1))

        # Show the x-axis

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_2 = Rectangle(width=2, height=0.3, color=GREEN, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.copy().move_to(RIGHT + UP * 2)
        top_2 = bar_2.copy().next_to(top_3, RIGHT, buff=0)
        corner = top_3.get_left()

        tick_marks = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=GREY_E)
            tick.move_to(top_3.get_left() + RIGHT * i)
            tick_marks.add(tick)

        # Position vertical bars
        left_3 = top_3.copy().rotate(-PI / 2, about_point=corner)
        left_2 = (
            top_2.copy()
            .rotate(PI / 2, about_point=corner)
            .next_to(left_3, DOWN, buff=0)
        )

        left_bar = VGroup(left_3, left_2)
        top_bar = VGroup(top_3, top_2)

        tick_marks_v = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=GREY_E)
            tick.move_to(top_3.get_left() + RIGHT * i)
            tick.rotate(-PI / 2, about_point=corner)

            tick_marks_v.add(tick)

        self.play(FadeIn(top_3), FadeIn(top_2), FadeIn(tick_marks))

        self.play(FadeIn(left_3), FadeIn(left_2), FadeIn(tick_marks_v))
        self.wait(1)

        # Define rectangles for areas
        rect_3x3 = Rectangle(width=3, height=3, color=WHITE, fill_opacity=0.5)
        rect_3x2 = Rectangle(width=2, height=3, color=YELLOW, fill_opacity=0.5)
        rect_2x3 = Rectangle(width=3, height=2, color=ORANGE, fill_opacity=0.5)
        rect_2x2 = Rectangle(width=2, height=2, color=RED, fill_opacity=0.5)

        # Align rectangles properly
        rect_3x3.next_to(top_3, DOWN, buff=0, aligned_edge=UP)
        rect_3x2.next_to(rect_3x3, RIGHT, buff=0, aligned_edge=UP)
        rect_2x3.next_to(rect_3x3, DOWN, buff=0, aligned_edge=LEFT)
        rect_2x2.next_to(rect_3x2, DOWN, buff=0, aligned_edge=LEFT)

        self.play(FadeIn(rect_3x3))
        self.play(FadeIn(rect_3x2))
        self.play(FadeIn(rect_2x3))
        self.play(FadeIn(rect_2x2))

        # Add labels inside rectangles
        label_3x3 = Tex("3 \\cdot 3").move_to(rect_3x3)
        box_3_3 = SurroundingRectangle(label_3x3, color=bc)

        # 3x2
        label_3x2 = Tex("3 \\cdot 2").move_to(rect_3x2)
        box_3_2 = SurroundingRectangle(label_3x2, color=bc)

        # 2x3
        label_2x3 = Tex("2 \\cdot 3").move_to(rect_2x3)
        box_2_3 = SurroundingRectangle(label_2x3, color=bc)

        label_2x2 = Tex("2 \\cdot 2").move_to(rect_2x2)
        box_2_2 = SurroundingRectangle(label_2x2, color=bc)

        label_3_l = Brace(left_3, LEFT)
        text_3_l = Tex("3").next_to(label_3_l, LEFT, buff=0.2)

        label_2_l = Brace(left_2, LEFT)
        text_2_l = Tex("2").next_to(label_2_l, LEFT, buff=0.2)

        label_3_u = Brace(top_3, UP)
        text_3_u = Tex("3").next_to(label_3_u, UP, buff=0.2)

        label_2_u = Brace(top_2, UP)
        text_2_u = Tex("2").next_to(label_2_u, UP, buff=0.2)

        self.play(
            FadeIn(label_3x3),
            FadeIn(box_3_3),
            FadeIn(box_3_3_1),
            FadeIn(box_3_3_2),
            FadeIn(label_3_l),
            FadeIn(label_3_u),
            FadeIn(text_3_l),
            FadeIn(text_3_u),
        )
        self.play(
            FadeOut(box_3_3),
            FadeOut(box_3_3_1),
            FadeOut(box_3_3_2),
            FadeOut(label_3_l),
            FadeOut(label_3_u),
            FadeOut(text_3_l),
            FadeOut(text_3_u),
        )

        self.play(
            FadeIn(label_3x2),
            FadeIn(box_3_2),
            FadeIn(box_3_2_1),
            FadeIn(box_3_2_2),
            FadeIn(label_3_l),
            FadeIn(label_2_u),
            FadeIn(text_3_l),
            FadeIn(text_2_u),
        )

        self.play(
            FadeOut(box_3_2),
            FadeOut(box_3_2_1),
            FadeOut(box_3_2_2),
            FadeOut(label_3_l),
            FadeOut(label_2_u),
            FadeOut(text_3_l),
            FadeOut(text_2_u),
        )

        self.play(
            FadeIn(label_2x3),
            FadeIn(box_2_3),
            FadeIn(box_2_3_1),
            FadeIn(box_2_3_2),
            FadeIn(label_2_l),
            FadeIn(label_3_u),
            FadeIn(text_2_l),
            FadeIn(text_3_u),
        )

        self.play(
            FadeOut(box_2_3),
            FadeOut(box_2_3_1),
            FadeOut(box_2_3_2),
            FadeOut(label_2_l),
            FadeOut(label_3_u),
            FadeOut(text_2_l),
            FadeOut(text_3_u),
        )

        self.play(
            FadeIn(label_2x2),
            FadeIn(box_2_2),
            FadeIn(box_2_2_1),
            FadeIn(box_2_2_2),
            FadeIn(label_2_l),
            FadeIn(label_2_u),
            FadeIn(text_2_l),
            FadeIn(text_2_u),
        )

        self.play(
            FadeOut(box_2_2),
            FadeOut(box_2_2_1),
            FadeOut(box_2_2_2),
            FadeOut(label_2_l),
            FadeOut(label_2_u),
            FadeOut(text_2_l),
            FadeOut(text_2_u),
        )

        self.wait(0.5)

        # Labels for lengths
        left_label = Brace(left_bar, LEFT)
        left_text = Tex("5").next_to(left_label, LEFT, buff=0.2)

        self.play(FadeIn(left_label), FadeIn(left_text))

        top_label = Brace(top_bar, UP)
        top_text = Tex("5").next_to(top_label, UP, buff=0.2)

        self.play(FadeIn(top_label), FadeIn(top_text))

        eq2 = Tex("= 5 \\cdot 5").next_to(eq1, DOWN, buff=0.3)

        self.play(Write(eq2))


class MultiplicationLaw2Visualization(Scene):
    def construct(self):
        # Create equation
        eq1 = Tex(r"(a+b) \cdot (a^2 - ab + b^2) = a^3 + b^3").scale(1.2)

        # Display equation
        self.play(Write(eq1))
        self.wait(0.5)

        # Underline for the second term in LHS ("a^2 - ab + b^2")
        underline = Line(eq1[6].get_left(), eq1[15].get_right(), color=BLUE).shift(
            DOWN * 0.4
        )
        self.play(FadeIn(underline))
        self.wait(2)

        # Surrounding box for the minus sign (indexing finds '-')
        minus_box = SurroundingRectangle(eq1[9], color=RED, buff=0.1)
        self.play(FadeIn(minus_box))
        self.wait(1)


class Distributive321Visualization(Scene):
    def construct(self):
        # 3+2 * 3+2+1
        title = Tex("(3+2) \cdot (3+2+1)").shift(UP * 3)
        self.play(FadeIn(title))

        # Define colors
        bc = BLUE

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_2 = Rectangle(width=2, height=0.3, color=GREEN, fill_opacity=1)
        bar_1 = Rectangle(width=1, height=0.3, color=RED, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.copy().move_to(LEFT * 2 + UP * 2)
        top_2 = bar_2.copy().next_to(top_3, RIGHT, buff=0)
        top_1 = bar_1.copy().next_to(top_2, RIGHT, buff=0)
        corner = top_3.get_left()

        # Position vertical bars
        left_3 = (
            bar_3.copy().rotate(PI / 2, about_point=corner).move_to(corner + DOWN * 1.5)
        )
        left_2 = bar_2.copy().rotate(PI / 2).next_to(left_3, DOWN, buff=0)
        left_1 = bar_1.copy().rotate(PI / 2).next_to(left_2, DOWN, buff=0)

        self.play(FadeIn(top_3), FadeIn(top_2), FadeIn(top_1))
        self.play(FadeIn(left_3), FadeIn(left_2))

        # Define rectangles for areas
        rect_3x3 = Rectangle(width=3, height=3, color=WHITE, fill_opacity=0.5)
        rect_3x2 = Rectangle(width=2, height=3, color=YELLOW, fill_opacity=0.5)
        rect_3x1 = Rectangle(width=1, height=3, color=PURPLE, fill_opacity=0.5)
        rect_2x3 = Rectangle(width=3, height=2, color=ORANGE, fill_opacity=0.5)
        rect_2x2 = Rectangle(width=2, height=2, color=RED, fill_opacity=0.5)
        rect_2x1 = Rectangle(width=1, height=2, color=GREEN, fill_opacity=0.5)

        # Align rectangles properly
        rect_3x3.move_to(corner + RIGHT * 1.5 + DOWN * 1.5)
        rect_3x2.next_to(rect_3x3, RIGHT, buff=0, aligned_edge=UP)
        rect_3x1.next_to(rect_3x2, RIGHT, buff=0, aligned_edge=UP)
        rect_2x3.next_to(rect_3x3, DOWN, buff=0, aligned_edge=LEFT)
        rect_2x2.next_to(rect_3x2, DOWN, buff=0, aligned_edge=LEFT)
        rect_2x1.next_to(rect_3x1, DOWN, buff=0, aligned_edge=LEFT)

        self.play(FadeIn(rect_3x3), run_time=0.3)
        self.play(FadeIn(rect_3x2), run_time=0.3)
        self.play(FadeIn(rect_3x1), run_time=0.3)
        self.play(FadeIn(rect_2x3), run_time=0.3)
        self.play(FadeIn(rect_2x2), run_time=0.3)
        self.play(FadeIn(rect_2x1), run_time=0.3)
        self.wait(2)


class DistributiveNegativeLaw(Scene):
    def construct(self):
        # minus dis
        title = Tex("4 \\times (3 - 2)").shift(LEFT * 3.5 + UP).scale(1.5)
        self.play(FadeIn(title))
        custom_dark_grey = "#444444"  # Hex color for a darker grey
        # Define colors
        bc = BLUE

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_neg_2 = Rectangle(width=2, height=0.3, color=RED, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.copy().move_to(RIGHT * 2 + UP * 2)
        top_neg_2 = bar_neg_2.copy().next_to(top_3, RIGHT, buff=0)
        corner = top_3.get_left()

        # Position vertical bars
        left_4 = Rectangle(width=0.3, height=4, color=GREEN, fill_opacity=1).move_to(
            corner, aligned_edge=UP
        )

        # Define rectangles for areas
        rect_4x3 = Rectangle(width=3, height=4, color=BLUE, fill_opacity=0.9)
        rect_4x2 = Rectangle(width=2, height=4, color=RED, fill_opacity=0.9)

        rect_4x1 = Rectangle(width=1, height=4, color=GREEN, fill_opacity=0.5)

        # Align rectangles properly
        rect_4x3.move_to(corner + RIGHT * 1.5 + DOWN * 2)
        rect_4x2.next_to(rect_4x3, RIGHT, buff=0, aligned_edge=UP)

        rect_4x1.move_to(rect_4x3.get_left(), aligned_edge=LEFT)
        label_1 = Brace(rect_4x1, UP)
        text_1 = Tex("1").next_to(label_1, UP, buff=0.2)

        rect_4x2_copy = rect_4x2.copy().move_to(rect_4x2.get_left(), aligned_edge=RIGHT)
        # Move the yellow rectangle from the red one to its new position

        label_4 = Brace(rect_4x3, LEFT)
        text_4 = Tex("4").next_to(label_4, LEFT, buff=0.2)

        label_3 = Brace(rect_4x3, UP)
        text_3 = Tex("3").next_to(label_3, UP, buff=0.2)

        self.play(
            FadeIn(rect_4x3),
            FadeIn(label_4),
            FadeIn(text_4),
            FadeIn(label_3),
            FadeIn(text_3),
        )

        eq1 = Tex("4 \\cdot 3").scale(1.5)
        eq2 = Tex("4 \\cdot 2").scale(1.5)
        minus = Tex(" - ").scale(1.5)
        eq3 = Tex(" = 4 \\cdot 1").scale(1.5)
        eq1.shift(DOWN * 3 + LEFT * 2)
        eq2.next_to(eq1, RIGHT * 3)
        eq3.next_to(eq2, RIGHT * 1)

        minus.move_to((eq1.get_right() + eq2.get_left()) / 2)
        self.play(Write(eq1))
        self.wait(0.5)

        label_2 = Brace(rect_4x2, UP)
        text_2 = Tex("2").next_to(label_2, UP, buff=0.2)

        rect_4x2_group = VGroup(rect_4x2, label_2, text_2)

        label_2c = Brace(rect_4x2_copy, UP)
        text_2c = Tex("2").next_to(label_2c, UP, buff=0.2)

        rect_4x2_group_copy = VGroup(rect_4x2_copy, label_2c, text_2c)

        self.play(
            FadeIn(rect_4x2_group),
            Write(eq2),
        )

        # Grey out the negative parts to show subtraction
        grey_rect = rect_4x2.copy().set_color("#333333").set_opacity(1)
        grey_rect_copy = rect_4x2_copy.copy().set_color("#444444").set_opacity(1)

        self.play(
            FadeOut(label_3),
            FadeOut(text_3),
            # Transform(rect_4x2, rect_4x2_copy),
            Transform(rect_4x2_group, rect_4x2_group_copy),
            Write(minus),
            run_time=2,
        )

        grey_rect_4x2 = rect_4x2.copy().set_color(custom_dark_grey).set_opacity(1)

        self.wait(1)

        self.play(
            # Transform(rect_4x2, grey_rect),
            Transform(rect_4x2_copy, grey_rect_copy),
            FadeOut(label_2),
            FadeOut(text_2),
            FadeIn(label_1),
            FadeIn(text_1),
            Write(eq3),
        )

        self.wait()


class MultiplicationLawVisualization(Scene):
    def construct(self):
        # Create equation
        eq1 = Tex(r"(a+b) \cdot (a^2 - ab + b^2) = a^3 + b^3").scale(1.2)

        # Display equation
        self.play(Write(eq1))
        self.wait(0.5)


class ComplexNumber(Scene):
    def construct(self):
        equation = Tex("(3+4i)(2+3i) = 6 + 9i + 8i + 12i^2").scale(1.2).shift(UP * 2)
        self.play(FadeIn(equation))
        self.wait(2)
        sc = 1.5

        plane = (
            NumberPlane(
                x_range=[0, 3, 1],
                y_range=[0, 2, 1],
                faded_line_ratio=3,
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },
            )
            .set_opacity(0.8)
            .shift(DOWN)
            .scale(1.5)
        )

        origin = plane.c2p(0.0)

        def create_rectangle(x1, y1, x2, y2, color):
            """FadeIns a rectangle aligned to the NumberPlane."""
            rect = Rectangle(
                width=abs(x2 - x1) * sc,
                height=abs(y2 - y1) * sc,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.5,
            ).move_to(
                [origin[0] + (x1 + x2) / 2 * sc, origin[1] + (y1 + y2) / 2 * sc, 0]
            )
            return rect

        rect1 = create_rectangle(0, 0, 2, 1, BLUE)  # 2 x 1
        rect2 = create_rectangle(0, 1, 2, 2, GREEN)  # 2 x 2/3
        rect3 = create_rectangle(2, 0, 3, 1, ORANGE)  # 1/4 x 1
        rect4 = create_rectangle(2, 1, 3, 2, RED)  # 1/4 x 2/3
        self.play(FadeIn(plane))

        self.play(
            FadeIn(rect1), FadeIn(rect2), FadeIn(rect3), FadeIn(rect4), run_time=0.5
        )

        self.wait()


class MultiplicationFraction(Scene):
    def construct(self):
        # Display multiplication expression

        # Create individual numbers
        num_2 = Tex("2")
        num_1 = Tex("1")
        num_1_4 = Tex(r"\frac{1}{4}")
        num_2_3 = Tex(r"\frac{2}{3}")

        # Construct the equation dynamically using VGroup
        equation = (
            VGroup(
                Tex("("),
                num_2,
                Tex("+"),
                num_1_4,
                Tex(") \\cdot ("),
                num_1,
                Tex("+"),
                num_2_3,
                Tex(")"),
            )
            .arrange(RIGHT)
            .scale(1.2)
        )

        # Position the equation at the top
        equation.shift(UP * 2.2)

        # Animate the equation appearance
        self.play(Write(equation))

        self.wait()
        sc = 2.3  # Scaling factor

        # Main number plane (integer grid)
        big_plane = (
            NumberPlane(
                x_range=[0, 3, 1],
                y_range=[0, 2, 1],
                faded_line_ratio=0,
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },
            )
            .scale(sc)
            .set_opacity(0.8)
        ).shift(DOWN)

        big_plane.add_coordinate_labels()
        self.add(big_plane)

        # Finer grid for fractions
        big_plane2 = (
            NumberPlane(
                x_range=[0, 3, 1 / 4],  # Smaller step for finer grid
                y_range=[0, 2, 1 / 3],
                faded_line_ratio=1,
                axis_config={"stroke_width": 0},
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },
            )
            .scale(sc)
            .set_opacity(0.8)
        ).shift(DOWN)

        self.add(big_plane2)

        origin = big_plane.c2p(0, 0)  # Get origin for proper alignment

        # Define function to create rectangles
        def create_rectangle(x1, y1, x2, y2, color):
            """FadeIns a rectangle aligned to the NumberPlane."""
            rect = Rectangle(
                width=abs(x2 - x1) * sc,
                height=abs(y2 - y1) * sc,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.5,
            ).move_to(
                [origin[0] + (x1 + x2) / 2 * sc, origin[1] + (y1 + y2) / 2 * sc, 0]
            )
            return rect

        # Function to animate multiplication step
        def animate_multiplication(num1, num2, rect, x_pos, y_pos, color):
            """Animates the multiplication process with braces."""

            # Copy numbers from equation
            num1_copy = num1.copy()
            num2_copy = num2.copy()

            # Get rectangle side lines as braces
            brace_x = Line(
                big_plane.c2p(x_pos, y_pos),
                big_plane.c2p(x_pos + rect.get_width() / sc, y_pos),
                color=ORANGE,
            )
            brace_y = Line(
                big_plane.c2p(x_pos, y_pos),
                big_plane.c2p(x_pos, y_pos + rect.get_height() / sc),
                color=ORANGE,
            )

            # Move numbers near the braces
            num1_dest = Tex(str(num1.get_tex())).next_to(brace_x, DOWN)
            num2_dest = Tex(str(num2.get_tex())).next_to(brace_y, LEFT)

            # Fade in rectangle
            # rect.set_opacity(0)

            self.play(
                Transform(num1_copy, num1_dest),
                Transform(num2_copy, num2_dest),
                FadeIn(brace_x),
                FadeIn(brace_y),
            )
            # self.play()

            # Move numbers inside rectangle and form product
            product = Tex(num1.get_tex() + " \\times " + num2.get_tex()).move_to(
                rect.get_center()
            )
            self.play(
                FadeIn(rect),
                Transform(num1_copy, product),
                Transform(num2_copy, product),
                FadeOut(brace_x),
                FadeOut(brace_y),
            )

        # FadeIn rectangles for each term in the multiplication
        rect1 = create_rectangle(0, 0, 2, 1, BLUE)  # 2 x 1
        rect2 = create_rectangle(0, 1, 2, 1 + 2 / 3, GREEN)  # 2 x 2/3
        rect3 = create_rectangle(2, 0, 2 + 1 / 4, 1, ORANGE)  # 1/4 x 1
        rect4 = create_rectangle(2, 1, 2 + 1 / 4, 1 + 2 / 3, RED)  # 1/4 x 2/3

        animate_multiplication(num_2, num_1, rect1, 0, 0, BLUE)  # 2 * 1
        animate_multiplication(num_2, num_2_3, rect2, 0, 1, GREEN)  # 2 * 2/3
        animate_multiplication(num_1_4, num_1, rect3, 2, 0, ORANGE)  # 1/4 * 1
        animate_multiplication(num_1_4, num_2_3, rect4, 2, 1, RED)  # 1/4 * 2/3

        self.wait(2)


class MultiplicationPiEquation(Scene):
    def construct(self):
        # Display title
        title = Tex(r" \pi \times \pi").scale(1.5)
        title.shift(UP * 2)
        self.play(Write(title))

        eq1 = Tex(r"3.1415926535897932\ldots")
        m = Tex(r"\times").next_to(eq1, DOWN)
        eq2 = Tex(r"3.1415926535897932\ldots").next_to(m, DOWN)

        self.play(Write(eq1), Write(m), Write(eq2))
        self.wait(2)

        self.play(FadeOut(eq1), FadeOut(m), FadeOut(eq2))

        eq1 = Tex(r"3").set_color(BLUE).scale(1.2)
        mul = Tex(r"\times")
        eq2 = Tex(r"3.1415926535897932\ldots")

        group = VGroup(eq1, mul, eq2).arrange(RIGHT, buff=0.2).shift(UP * 0.5)

        self.play(Write(group))
        self.wait()

        t1 = Text("끝나면 다음 수를 곱하자", font="BM Hanna 11yrs Old").scale(1)

        t1.next_to(group, DOWN * 1.3)
        self.play(Write(t1))
        self.wait(2)

        eq1 = Tex(r"3.1").set_color(BLUE).scale(1.2)
        mul = Tex(r"\times")
        eq2 = Tex(r"3.1415926535897932\ldots")

        group = VGroup(eq1, mul, eq2).arrange(RIGHT, buff=0.2)
        group.next_to(t1, DOWN * 1.3)
        self.play(Write(group))

        self.wait(2)


class PiMultiplication(Scene):
    def construct(self):
        # Initial scale factor
        sc = 1.5

        # Step 2: Iterate through finer grids
        pi_approximations = [
            3,
            3.1,
            3.14,
            3.141,
            3.1415,
            3.14159,
            3.141592,
        ]  # Refinement levels
        # pi_approximations = [3, 3.1]  # Refinement levels

        colors = [RED, YELLOW, GREEN, ORANGE, BLUE, RED, YELLOW] * 2
        faded_ratio = 0
        self.camera.frame.save_state()

        pi_text = Tex(r"\pi \cdot \pi").scale(1.5)
        pi_text.shift(UP * 2.1)
        pi_text.fix_in_frame()
        self.play(Write(pi_text))

        self.wait()

        big_plane = (
            NumberPlane(
                x_range=[0, 4, 1],
                y_range=[0, 4, 1],
                faded_line_ratio=100,
                axis_config={
                    "stroke_width": 0,
                },
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },  # Lower opacity
            )
            .scale(sc)
            .set_opacity(0.8)
        )
        big_plane.z_index = -3 * 1 + 2
        self.add(big_plane)

        for i in range(0, len(pi_approximations)):
            ap = pi_approximations[i]

            color = colors[i]

            if i > 0:
                point = big_plane.c2p(
                    pi_approximations[i - 1], pi_approximations[i - 1]
                )
            else:
                point = big_plane.c2p(ap, ap)
            zoom_factor = 0.5**i

            point = big_plane.c2p(ap, ap)
            p31 = Dot().move_to(point).scale(zoom_factor)

            pi_text_ap = Tex(f"{ap} \cdot {ap}")
            pi_text_ap.move_to(pi_text).fix_in_frame()

            width = ap * sc
            refined_background = Rectangle(
                width=width,
                height=width,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,  # Removes border
            ).set_z_index(-3 * i + 1)

            refined_background.next_to(big_plane, RIGHT).align_to(
                big_plane, DOWN + LEFT
            )

            if i > 1:
                # if True:
                # self.play(self.camera.frame.animate.set_width(4 / (3**i)).move_to(p31))
                animations = [
                    self.camera.frame.animate.move_to(p31).scale(zoom_factor),
                    Transform(pi_text, pi_text_ap),
                    FadeIn(refined_background),
                ]
                self.play(
                    # self.camera.frame.animate.set_width(zoom_factor).move_to(p31),
                    *animations
                )
                self.wait(1)
            else:
                self.play(Transform(pi_text, pi_text_ap), FadeIn(refined_background))

                self.wait(1)

        pi_text_ap = Tex(f"{ap}... \cdot {ap}...")
        pi_text_ap.move_to(pi_text).fix_in_frame()
        self.play(
            Transform(pi_text, pi_text_ap),
        )

        self.wait()

        pi_text_ap = Tex(r"\pi \cdot \pi").scale(1.5)
        pi_text_ap.move_to(pi_text).fix_in_frame()

        self.play(
            # FadeOut(pi_text_ap),
            Restore(self.camera.frame),
            Transform(pi_text, pi_text_ap),
            run_time=5,
        )
        self.play(self.camera.frame.animate.move_to(p31).scale(zoom_factor), run_time=6)
        self.wait(0.5)
        self.play(Restore(self.camera.frame), run_time=3)

        self.wait()


class PiApproximation(Scene):
    def construct(self):
        # Step 1: Start high with π · π
        eq = Tex(r"\pi \cdot \pi").scale(2)
        self.play(Write(eq))
        self.wait(1)

        # Step 2: Move to center while changing to 3 · 3

        # Step 3: In-place morphs
        approximations = [
            r"3 \cdot 3",
            r"3.1 \cdot 3.1",
            r"3.14 \cdot 3.14",
            r"3.141 \cdot 3.141",
            r"3.1415 \cdot 3.1415",
            r"3.14159 \cdot 3.14159",
            r"3.141592 \cdot 3.141592",
        ]

        for approx in approximations:
            next_eq = Tex(approx).scale(2)
            self.play(Transform(eq, next_eq), run_time=0.8)
            self.wait(0.2)

        self.wait(1)
        eq_lim = (
            Tex(r"\lim a_n \times \lim b_n = \lim (a_n \times b_n)")
            .shift(DOWN * 1.5)
            .scale(1.2)
        ).set_color(GREY)
        eq2 = Tex(r"\pi \cdot \pi").scale(2)

        self.play(Write(eq_lim), Transform(eq, eq2))
        self.wait()


class InfiniteDecimalGeometricEq(Scene):
    def construct(self):
        # Step 1: Introduce s = 0.99999...
        equation_s = Tex(r"s = 0.99999\ldots").scale(1.5)

        self.play(Write(equation_s))
        self.wait(1)

        # Geometric series visual proof
        r = 0.1  # Updated ratio value
        shift_amount = LEFT * 6 + DOWN * 3  # Shift entire graph to the left

        equation_s10 = (
            Tex(r"10s = 9.99999\ldots")
            .scale(1.5)
            .next_to(equation_s, DOWN, aligned_edge=LEFT)
            .shift(LEFT * 0.65)
        )
        self.play(Write(equation_s10))
        self.wait(1)

        self.play(
            equation_s.animate.shift(UP * 1),
            equation_s10.animate.shift(UP * 2.5),
        )

        self.wait()

        minus = (
            Tex(r" - ")
            .scale(1.5)
            .next_to(equation_s, LEFT * 1.8, aligned_edge=LEFT)
            .set_color(GREY)
        )

        equation = Tex(r"9s = 9").scale(1.5).shift(LEFT * 1.65)

        # Extract parts for individual animation
        s9 = equation[0:2]  # "10s"
        equal = equation[2]  # "="
        res = equation[3]  # "9"

        # self.play(Indicate(equation_s10, color=WHITE))

        self.play(FadeIn(minus))

        # self.play(Indicate(equation_s, color=WHITE))

        self.play(
            Write(s9),
        )
        self.wait()
        # self.play(
        #     FadeIn(strike_line1),
        #     FadeIn(strike_line2),
        # )
        self.play(Write(equal), Write(res))

        self.wait(2)

        equation2 = Tex(r"s = 1").scale(1.5).shift(LEFT * 1.45)

        self.play(
            Transform(equation, equation2),
        )

        self.wait()

        self.play(
            # FadeOut(strike_line1),
            # FadeOut(strike_line2),
            FadeOut(minus)
        )

        framebox1 = SurroundingRectangle(equation_s[2:], buff=0.1)
        framebox2 = SurroundingRectangle(equation2[2], buff=0.1)

        equation3 = Tex(r"0.99999\ldots = 1").shift(DOWN * 1).scale(1.8)

        self.play(FadeIn(framebox1), Write(equation3[0:10]))
        self.wait()

        self.play(FadeIn(framebox2), Write(equation3[-1]), Write(equation3[-2]))
        self.play(Indicate(equation3, color=WHITE))

        self.wait()


class InfiniteRepeatingNineBlowup(Scene):
    def construct(self):
        # Define the colors for emphasis
        color_s = BLUE

        color_ten = GREEN
        sc = 1.2

        # First equation: s = ...99999999
        lhs1 = Tex("s").scale(sc)
        eq1 = Tex("=").scale(sc)
        rhs1 = Tex("...", "99999999").scale(sc)

        lhs1.set_color(color_s)

        # Second equation: 10s = ...99999990
        lhs2 = Tex("10s").scale(sc)
        eq2 = Tex("=").scale(sc)
        rhs2 = Tex("...", "99999990").scale(sc)

        lhs2.set_color(color_s)
        rhs2.set_color_by_tex("0", YELLOW)

        # Third equation: 10s - s = -9
        lhs3 = Tex("10s", "-", "s").scale(sc)
        eq3 = Tex("=").scale(sc)
        rhs3 = Tex("-9").scale(sc)

        lhs3.set_color_by_tex("s", color_s)
        lhs3.set_color_by_tex("10s", color_s)

        # Fourth equation: 9s = -9
        lhs4 = Tex("9s").scale(sc)
        eq4 = Tex("=").scale(sc)
        rhs4 = Tex("-9").scale(sc)

        lhs4.set_color_by_tex("9s", color_s)

        # Fifth equation: s = -1
        lhs5 = Tex("s").scale(sc)
        eq5 = Tex("=").scale(sc)
        rhs5 = Tex("-1").scale(sc)

        lhs5.set_color(color_s)

        # Align all equal signs
        eq_x_pos = -1  # Set common x-coordinate for equal signs

        eq1.move_to([eq_x_pos, 2.5, 0])
        eq2.move_to([eq_x_pos, 1.5, 0])
        eq3.move_to([eq_x_pos, 0.5, 0])
        eq4.move_to([eq_x_pos, -0.5, 0])
        eq5.move_to([eq_x_pos, -1.5, 0])

        # Position LHS and RHS relative to equal sign
        lhs1.next_to(eq1, LEFT, buff=0.3)
        rhs1.next_to(eq1, RIGHT, buff=0.3)

        lhs2.next_to(eq2, LEFT, buff=0.3)
        rhs2.next_to(eq2, RIGHT, buff=0.3)

        lhs3.next_to(eq3, LEFT, buff=0.3)
        rhs3.next_to(eq3, RIGHT, buff=0.3)

        lhs4.next_to(eq4, LEFT, buff=0.3)
        rhs4.next_to(eq4, RIGHT, buff=0.3)

        lhs5.next_to(eq5, LEFT, buff=0.3)
        rhs5.next_to(eq5, RIGHT, buff=0.3)

        # Arrows to show transition
        arrow1 = Arrow(eq1.get_bottom(), eq2.get_top(), buff=0.2)
        arrow2 = Arrow(eq2.get_bottom(), eq3.get_top(), buff=0.2)
        arrow3 = Arrow(eq3.get_bottom(), eq4.get_top(), buff=0.2)
        arrow4 = Arrow(eq4.get_bottom(), eq5.get_top(), buff=0.2)

        # Display everything
        self.play(Write(lhs1), Write(eq1), Write(rhs1))
        self.wait(1)
        self.play(GrowArrow(arrow1))
        self.play(Write(lhs2), Write(eq2), Write(rhs2))
        self.wait(1)
        self.play(GrowArrow(arrow2))
        self.play(Write(lhs3), Write(eq3), Write(rhs3))
        self.wait(1)
        self.play(GrowArrow(arrow3))
        self.play(Write(lhs4), Write(eq4), Write(rhs4))
        self.wait(1)
        self.play(GrowArrow(arrow4))
        self.play(Write(lhs5), Write(eq5), Write(rhs5))

        self.wait(2)


class DualClock12WithAnimation(Scene):
    def construct(self):
        # FadeIn first clock (left) with red hand
        clock1 = Clock()
        clock1.move_to(LEFT * 3.5)

        # FadeIn second clock (right) with yellow hand
        clock2 = Clock()
        clock2.move_to(RIGHT * 3.5)

        # Add both clocks to the scene
        self.add(clock1, clock2)

        # Animate first clock: Clockwise from 12 to 11
        ani1 = clock1.animate_hand(PI / 2, -TAU / 12 * 11, fill_color=GREY_A)
        ani2 = clock2.animate_hand(PI / 2, TAU / 12, fill_color=GREY_A)

        self.play(*ani1, *ani2, run_time=2)

        self.wait()

        eq = Tex(r"11 = -1").scale(1.5)
        eq.shift(DOWN * 3)

        self.play(Write(eq))

        self.wait(2)

        # eq2 = Tex(r"11^2 + 11 = -1").scale(1.5)
        # eq2.shift(DOWN * 3)

        # self.play(Transform(eq, eq2))


class DualClockWithAnimation10(Scene):
    def construct(self):
        # FadeIn first clock (left) with red hand
        clock1 = Clock(num_hours=10)
        clock1.move_to(LEFT * 3.5)

        # FadeIn second clock (right) with yellow hand
        clock2 = Clock(num_hours=10)
        clock2.move_to(RIGHT * 3.5)

        # Add both clocks to the scene
        self.add(clock1, clock2)

        # Animate first clock: Clockwise from 12 to 11
        ani1 = clock1.animate_hand(PI / 2, -TAU / 10 * 9, fill_color=GREY_A)
        ani2 = clock2.animate_hand(PI / 2, TAU / 10, fill_color=GREY_A)

        self.play(*ani1, *ani2, run_time=2)

        eq = Tex("9 = -1").scale(1.5)
        eq.shift(DOWN * 3)

        self.play(Write(eq))

        self.wait()

        eq2 = Tex("99 = -1").scale(1.5)
        eq2.shift(DOWN * 3)

        self.play(Transform(eq, eq2))

        ani1 = clock1.animate_hand(TAU / 10, -TAU * 6, fill_color=None)

        self.play(*ani1, run_time=2)

        self.wait()

        eq2 = Tex("999 = -1").scale(1.5)
        eq2.shift(DOWN * 3)

        self.play(Transform(eq, eq2))

        ani1 = clock1.animate_hand(TAU / 10, -TAU * 10, fill_color=None)

        self.play(*ani1, run_time=2)

        self.wait()

        eq2 = Tex("...99999 = -1").scale(1.5)
        eq2.shift(DOWN * 3)

        self.play(Transform(eq, eq2))
        ani1 = clock1.animate_hand(TAU / 10, -TAU * 15, fill_color=None)

        self.play(*ani1, run_time=3)

        self.wait(2)


class FlatAnt(Scene):
    def construct(self):
        sc = 2
        move_time = 1  # Time for the ant to move up by 1 unit in global frame
        move_speed = 1 / move_time * 2

        left_plane = NumberPlane(
            x_range=[-1, 2, 1],
            y_range=[-1, 2, 1],
            faded_line_ratio=0,
            axis_config={
                "stroke_opacity": 0.5,
            },
            background_line_style={
                "stroke_opacity": 0.2,
                "stroke_width": 2,
                "stroke_color": GREY,
            },  # Lower opacity
        ).scale(sc)

        def update_ant_north(mob, alpha, plane):
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time

            ant_pos = mob.get_center()
            pos = ant_pos + [0, move_speed * dt, 0]
            mob.move_to(pos)
            up_arrow.next_to(mob, UP, aligned_edge=UP)

            plane.add(mob.copy().set_fill(RED))

        def update_ant_east(mob, alpha, plane):
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time

            ant_pos = mob.get_center()
            pos = ant_pos + [move_speed * dt, 0, 0]
            mob.move_to(pos)
            right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

            plane.add(mob.copy().set_fill(GREEN))

        self.play(FadeIn(left_plane))
        ant = Dot(color=WHITE)

        starting_pos = left_plane.c2p(0, 0)
        up_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + UP,
            fill_color=BLUE,
        )
        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)
        ant.move_to(starting_pos)

        right_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + RIGHT,
            fill_color=BLUE,
        )
        times = [0]

        self.add(up_arrow)
        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_north, plane=left_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.play(FadeOut(up_arrow))

        times = [0]
        starting_pos = ant.get_center()

        right_arrow.next_to(starting_pos, RIGHT, aligned_edge=RIGHT)
        self.add(right_arrow)

        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_east, plane=left_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )
        self.remove(right_arrow)

        self.wait()

        self.play(left_plane.animate.shift(LEFT * 3.5), ant.animate.shift(LEFT * 3.5))

        # right plane
        right_plane = (
            NumberPlane(
                x_range=[-1, 2, 1],
                y_range=[-1, 2, 1],
                faded_line_ratio=0,
                axis_config={
                    "stroke_opacity": 0.5,
                },
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },  # Lower opacity
            )
            .scale(sc)
            .shift(RIGHT * 3.5)
        )

        self.play(FadeIn(right_plane))

        starting_pos = right_plane.c2p(0, 0)

        ant2 = Dot(color=WHITE)
        ant2.move_to(starting_pos)

        times = [0]

        right_arrow.next_to(starting_pos, RIGHT, aligned_edge=RIGHT)
        self.add(right_arrow)

        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(update_ant_east, plane=left_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )
        self.remove(right_arrow)

        times = [0]
        starting_pos = ant2.get_center()

        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)
        self.add(up_arrow)

        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(update_ant_north, plane=right_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )
        self.remove(up_arrow)

        # glow
        glow = Dot(ant.get_center(), color=BLUE, radius=0.3, fill_opacity=0.2)

        glow2 = Dot(ant2.get_center(), color=BLUE, radius=0.3, fill_opacity=0.2)

        self.play(FadeIn(glow), FadeIn(glow2))

        self.wait()

        left_plane.set_opacity(0.03)
        right_plane.set_opacity(0.03)

        up_arrow = Arrow(
            start=ORIGIN,
            end=UP * 2,
            stroke_color=BLUE_D,
            fill_color=BLUE_D,
            stroke_width=10,
            fill_opacity=1,
        )
        right_arrow = Arrow(
            start=ORIGIN,
            end=RIGHT * 2,
            stroke_color=BLUE_D,
            fill_color=BLUE_D,
            stroke_width=10,
            fill_opacity=1,
        )

        up_arrow.move_to(left_plane.c2p(0.5, 0.5)).shift(LEFT * 0.8)
        left_plus = Tex(r" + ").scale(1.5)

        right_arrow.move_to(left_plane.c2p(0.5, 0.5)).shift(RIGHT * 1.3)
        left_plus.move_to(left_plane.c2p(0.5, 0.5))

        self.play(FadeIn(up_arrow), FadeIn(right_arrow), Write(left_plus))

        up_arrow_c = up_arrow.copy()
        up_arrow_c.move_to(right_plane).shift(RIGHT * 0.8)
        right_plus = Tex(r" + ").scale(1.5)

        right_arrow_c = right_arrow.copy()
        right_arrow_c.move_to(right_plane).shift(LEFT * 1.3)
        right_plus.move_to(right_plane)

        self.play(FadeIn(right_arrow_c), FadeIn(up_arrow_c), Write(right_plus))

        neq = Tex(r"=").scale(2.0)

        self.play(Write(neq))


class RotatingDiskAntIntro(Scene):
    def construct(self):
        # Disk properties

        move_time = 1  # Time for the ant to move up by 1 unit in global frame
        move_speed = 1 / move_time * 1
        sc = 1.5

        left_plane = NumberPlane(
            x_range=[-1, 2, 1],
            y_range=[-1, 2, 1],
            faded_line_ratio=0,
            axis_config={
                "stroke_opacity": 0.5,
            },
            background_line_style={
                "stroke_opacity": 0.2,
                "stroke_width": 2,
                "stroke_color": GREY,
            },  # Lower opacity
        ).scale(sc)

        def update_ant_north_plane(mob, alpha, plane):
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time

            ant_pos = mob.get_center()
            pos = ant_pos + [0, move_speed * dt, 0]
            mob.move_to(pos)
            up_arrow.next_to(mob, UP, aligned_edge=UP)

            plane.add(mob.copy().set_fill(RED))

        def update_ant_east_plane(mob, alpha, plane):
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time

            ant_pos = mob.get_center()
            pos = ant_pos + [move_speed * dt, 0, 0]
            mob.move_to(pos)
            right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

            plane.add(mob.copy().set_fill(GREEN))

        left_plane.set_opacity(0)
        self.play(FadeIn(left_plane))

        # self.play(left_plane.animate.shift(RIGHT * 3.5))

        t1 = Text("회전하는 판위에서", font="BM Hanna 11yrs Old").scale(1.2)

        t2 = Text("움직인다면?", font="BM Hanna 11yrs Old").scale(1.2)

        t1.shift(RIGHT * 2.5)
        t2.next_to(t1, DOWN)
        self.play(Write(t1))
        self.play(Write(t2))

        ant = Dot(color=WHITE)

        starting_pos = left_plane.c2p(0, 0)
        up_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + UP,
            fill_color=BLUE,
        )
        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)
        ant.move_to(starting_pos)

        right_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + RIGHT,
            fill_color=BLUE,
        )

        disk_radius = 2.5
        omega = 2 * PI / 9  # Angular velocity (full rotation in 5 sec)
        rotate_time = 4  # Time for the ant to move up by 1 unit in global frame
        rotate_speed = 1 / rotate_time * 1.5

        def create_disc():
            # Create the rotating disk
            disk = Circle(radius=disk_radius, fill_opacity=0.1)

            # Create polar coordinate lines
            polar_lines = VGroup()
            for angle in np.linspace(0, 2 * PI, 12, endpoint=False):
                line = DashedLine(
                    ORIGIN,
                    disk_radius * np.array([np.cos(angle), np.sin(angle), 0]),
                    stroke_color=GREY_A,
                    dash_length=0.2,
                    stroke_width=0.5,
                )
                polar_lines.add(line)

            # Create radial circles
            radial_circles = VGroup()
            for r in np.linspace(0.5, disk_radius, 4):
                circle = Circle(radius=r, stroke_color=GREY_A, stroke_opacity=0.3)
                radial_circles.add(circle)

            group = VGroup(disk, polar_lines, radial_circles)
            return group

        disc = create_disc()

        rotating_group = disc

        ant = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all = VGroup(rotating_group, ant)

        rotating_all.shift(LEFT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all))

        # Animate ant moving along trajectory while rotating the disk

        def update_ant_north(mob, alpha, disc, starting_pos=ORIGIN):
            origin = disc.get_center()
            time_prev = times[0]
            time = rotate_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=origin)

        def update_ant_east(mob, alpha, disc, starting_pos=ORIGIN):
            origin = disc.get_center()
            time_prev = times[0]
            time = rotate_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=origin)

        times = [0]

        starting_pos = rotating_all.copy().get_center()

        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_north, disc=rotating_all, starting_pos=starting_pos),
            ),
            run_time=rotate_time,
            rate_func=linear,
        )

        self.wait(1)
        # plane

        times = [0]

        self.add(up_arrow)
        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_north_plane, plane=left_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.play(FadeOut(up_arrow))

        times = [0]
        starting_pos = ant.get_center()

        right_arrow.next_to(starting_pos, RIGHT, aligned_edge=RIGHT)
        self.add(right_arrow)

        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_east_plane, plane=left_plane),
            ),
            run_time=move_time,
            rate_func=linear,
        )
        self.remove(right_arrow)

        self.wait()


class RotatingDiskAnt(Scene):
    def construct(self):
        # Disk properties

        disk_radius = 2.5
        omega = 2 * PI / 9  # Angular velocity (full rotation in 5 sec)
        move_time = 4  # Time for the ant to move up by 1 unit in global frame
        move_speed = 1 / move_time * 1.5

        def create_disc():
            # Create the rotating disk
            disk = Circle(radius=disk_radius, fill_opacity=0.1)

            # Create polar coordinate lines
            polar_lines = VGroup()
            for angle in np.linspace(0, 2 * PI, 12, endpoint=False):
                line = DashedLine(
                    ORIGIN,
                    disk_radius * np.array([np.cos(angle), np.sin(angle), 0]),
                    stroke_color=GREY_A,
                    dash_length=0.2,
                    stroke_width=0.5,
                )
                polar_lines.add(line)

            # Create radial circles
            radial_circles = VGroup()
            for r in np.linspace(0.5, disk_radius, 4):
                circle = Circle(radius=r, stroke_color=GREY_A, stroke_opacity=0.3)
                radial_circles.add(circle)

            group = VGroup(disk, polar_lines, radial_circles)
            return group

        disc = create_disc()

        rotating_group = disc

        ant = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all = VGroup(rotating_group, ant)

        rotating_all.shift(LEFT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all))

        self.wait(1)

        # Animate ant moving along trajectory while rotating the disk

        def update_ant_north(mob, alpha, disc, starting_pos=ORIGIN):
            origin = disc.get_center()
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=origin)

            ant_pos = mob.get_center()
            pos = ant_pos + [0, move_speed * dt, 0]
            mob.move_to(pos)
            up_arrow.next_to(mob, UP, aligned_edge=UP)

            disc.add(mob.copy().set_fill(RED))

        def update_ant_east(mob, alpha, disc, starting_pos=ORIGIN):
            origin = disc.get_center()
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=origin)

            ant_pos = mob.get_center()
            pos = ant_pos + [move_speed * dt, 0, 0]
            mob.move_to(pos)
            right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

            disc.add(mob.copy().set_fill(GREEN))

        times = [0]

        starting_pos = rotating_all.copy().get_center()
        up_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + UP,
            fill_color=BLUE,
        )
        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)

        right_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + RIGHT,
            fill_color=BLUE,
        )

        self.play(FadeIn(up_arrow))
        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_north, disc=rotating_all, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]
        starting_pos = ant.copy().get_center()

        right_arrow.next_to(starting_pos, RIGHT, aligned_edge=RIGHT)
        self.play(FadeOut(up_arrow), FadeIn(right_arrow))

        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_east, disc=rotating_all, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        # second disc
        disc2 = create_disc()

        rotating_group2 = disc2

        ant2 = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all2 = VGroup(rotating_group2, ant2)

        rotating_all2.shift(RIGHT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all2))

        self.wait(1)

        times = [0]

        starting_pos = rotating_all2.copy().get_center()
        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(update_ant_east, disc=rotating_all2, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]
        starting_pos = ant2.copy().get_center()
        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)

        self.play(FadeOut(right_arrow), FadeIn(up_arrow))

        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(
                    update_ant_north, disc=rotating_all2, starting_pos=starting_pos
                ),
            ),
            run_time=move_time,
            rate_func=linear,
        )
        self.remove(up_arrow)
        self.remove(right_arrow)
        # show equation
        rotating_all.set_opacity(0.03)
        rotating_all2.set_opacity(0.03)

        # glow
        glow = Dot(ant.get_center(), color=BLUE, radius=0.3, fill_opacity=0.2)

        ant.set_opacity(1)
        self.play(FadeIn(glow))

        glow2 = Dot(ant2.get_center(), color=BLUE, radius=0.3, fill_opacity=0.2)

        ant2.set_opacity(1)
        self.play(FadeIn(glow2))

        self.wait(1)

        up_arrow = Arrow(
            start=ORIGIN,
            end=UP * 2,
            stroke_color=BLUE_D,
            fill_color=BLUE_D,
            stroke_width=10,
            fill_opacity=1,
        )
        right_arrow = Arrow(
            start=ORIGIN,
            end=RIGHT * 2,
            stroke_color=BLUE_D,
            fill_color=BLUE_D,
            stroke_width=10,
            fill_opacity=1,
        )

        up_arrow.move_to(rotating_all).shift(LEFT * 0.8)
        left_plus = Tex(r" + ").scale(1.5)

        right_arrow.move_to(rotating_all).shift(RIGHT * 1.3)
        left_plus.move_to(rotating_all)

        self.play(FadeIn(up_arrow), FadeIn(right_arrow), Write(left_plus))

        up_arrow_c = up_arrow.copy()
        up_arrow_c.move_to(rotating_all2).shift(RIGHT * 0.8)
        right_plus = Tex(r" + ").scale(1.5)

        right_arrow_c = right_arrow.copy()
        right_arrow_c.move_to(rotating_all2).shift(LEFT * 1.3)
        right_plus.move_to(rotating_all2)

        self.play(FadeIn(right_arrow_c), FadeIn(up_arrow_c), Write(right_plus))

        neq = Tex(r"\neq").set_color(RED).scale(2.0)

        self.play(Write(neq))


class RotatingDiskAntInAbs(Scene):
    def construct(self):
        # Disk properties

        disk_radius = 2.5
        omega = 4 * PI / 9  # Angular velocity (full rotation in 5 sec)

        move_time = 5  # Time for the ant to move up by 1 unit in global frame
        move_speed = 2
        sc = 1.5

        def create_disc():
            # Create the rotating disk
            disk = Circle(radius=disk_radius, fill_opacity=0.1)

            # Create polar coordinate lines
            polar_lines = VGroup()
            for angle in np.linspace(0, 2 * PI, 12, endpoint=False):
                line = DashedLine(
                    ORIGIN,
                    disk_radius * np.array([np.cos(angle), np.sin(angle), 0]),
                    stroke_color=GREY_A,
                    dash_length=0.2,
                    stroke_width=0.5,
                )
                polar_lines.add(line)

            # Create radial circles
            radial_circles = VGroup()
            for r in np.linspace(0.5, disk_radius, 4):
                circle = Circle(radius=r, stroke_color=GREY_A, stroke_opacity=0.3)
                radial_circles.add(circle)

            group = VGroup(disk, polar_lines, radial_circles)
            return group

        disc = create_disc()

        rotating_group = disc

        ant = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all = VGroup(rotating_group, ant)

        rotating_all.shift(LEFT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all))

        self.wait(1)

        # Animate ant moving along trajectory while rotating the disk

        def update_ant_north(mob, alpha, disc, starting_pos=ORIGIN):

            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=starting_pos)

            ant_pos = mob.get_center()
            pos = ant_pos + [0, move_speed * dt, 0]
            mob.move_to(pos)
            up_arrow.next_to(mob, UP, aligned_edge=UP)

            disc.add(mob.copy().set_fill(RED))

        def update_ant_east(mob, alpha, disc, starting_pos=ORIGIN):

            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=starting_pos)

            ant_pos = mob.get_center()
            pos = ant_pos + [move_speed * dt, 0, 0]
            mob.move_to(pos)
            right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

            disc.add(mob.copy().set_fill(GREEN))

            positions.append(pos)

        times = [0]
        positions = []

        starting_pos = rotating_all.copy().get_center()
        up_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + UP,
            fill_color=BLUE,
        )
        up_arrow.next_to(starting_pos, UP, aligned_edge=UP)

        right_arrow = Arrow(
            start=starting_pos,
            end=starting_pos + RIGHT,
            fill_color=BLUE,
        )

        self.play(FadeIn(up_arrow))
        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_north, disc=rotating_all, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]

        right_arrow.next_to(ant.copy().get_center(), RIGHT, aligned_edge=RIGHT)
        self.play(FadeOut(up_arrow), FadeIn(right_arrow))

        self.play(
            UpdateFromAlphaFunc(
                ant,
                partial(update_ant_east, disc=rotating_all, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        # second disc
        disc2 = create_disc()

        rotating_group2 = disc2

        ant2 = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all2 = VGroup(rotating_group2, ant2)

        rotating_all2.shift(RIGHT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all2))

        self.wait(1)

        times = [0]
        positions = []

        starting_pos = rotating_all2.copy().get_center()
        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(update_ant_east, disc=rotating_all2, starting_pos=starting_pos),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]

        up_arrow.next_to(ant2.copy().get_center(), UP, aligned_edge=UP)

        self.play(FadeOut(right_arrow), FadeIn(up_arrow))

        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(
                    update_ant_north, disc=rotating_all2, starting_pos=starting_pos
                ),
            ),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(2)
        up_arrow.set_opacity(0.1)
        right_arrow.set_opacity(0)

        rotating_all.set_opacity(0.1)
        rotating_all2.set_opacity(0.1)

        self.wait(2)

        right_plane = (
            NumberPlane(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                faded_line_ratio=0,
                axis_config={
                    "stroke_opacity": 1,
                    "stroke_width": 3,
                },
                background_line_style={
                    "stroke_opacity": 1,
                    "stroke_width": 2,
                    "stroke_color": GREY,
                },  # Lower opacity
            ).scale(sc)
        ).move_to(disc2)

        self.play(FadeIn(right_plane))

        self.wait()

        # self.play(up_arrow.animate.set_opacity(1))

        # First index

        # omega = 4 * PI / 9  # Angular velocity (full rotation in 5 sec)

        # move_time = 5  # Time for the ant to move up by 1 unit in global frame

        times = [0]

        def update_ant_east_withv(mob, alpha, disc, starting_pos=ORIGIN):

            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            disc.rotate(omega * dt, about_point=starting_pos)

            ant_pos = mob.get_center()
            pos = ant_pos + [move_speed * dt, 0, 0]
            mob.move_to(pos)
            # right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

            disc.add(mob.copy().set_fill(GREEN))

            rel_pos = pos - starting_pos
            x, y, z = rel_pos
            scale = 1

            dxdt = (move_speed - omega * y) * scale
            dydt = omega * x * scale

            new_arrow_x = Arrow(
                start=pos, end=pos + np.array([dxdt, 0, 0]), fill_color=BLUE, buff=0
            )
            new_arrow_y = Arrow(
                start=pos,
                end=pos + np.array([0, dydt, 0]),
                fill_color=BLUE,
                buff=0,
            )
            arrow_x.become(new_arrow_x)
            arrow_y.become(new_arrow_y)

        pos = [0, 0, 0]
        arrow_x = Arrow(
            start=pos, end=pos + np.array([0, 0, 0]), fill_color=BLUE, buff=0
        )

        arrow_y = Arrow(
            start=pos,
            end=pos + np.array([0, 0, 0]),
            fill_color=BLUE,
            buff=0,
        )
        self.add(arrow_x)
        self.add(arrow_y)

        ant2.move_to(starting_pos)

        remaining = 2 * PI - omega * move_time * 2

        self.play(
            Rotate(rotating_all2, angle=remaining, about_point=starting_pos), run_time=2
        )
        self.wait()

        self.play(
            UpdateFromAlphaFunc(
                ant2,
                partial(
                    update_ant_east_withv, disc=rotating_all2, starting_pos=starting_pos
                ),
            ),
            run_time=move_time * 2,
            rate_func=linear,
        )

        # Step through every nth frame

        self.play(FadeOut(arrow_x), FadeOut(arrow_y))

        self.wait(1)

        def get_polar_grid(
            max_radius=3,
            num_circles=3,
            num_radial_lines=12,
            color=WHITE,
            stroke_opacity=0.2,
        ):
            # Circles
            circles = VGroup(
                *[
                    Circle(radius=r, color=color, stroke_opacity=stroke_opacity)
                    for r in np.linspace(1, max_radius, num_circles)
                ]
            )

            # Radial lines
            lines = VGroup(
                *[
                    Line(ORIGIN, RIGHT * max_radius)
                    .rotate(i * TAU / num_radial_lines, about_point=ORIGIN)
                    .set_stroke(color=color, opacity=stroke_opacity)
                    for i in range(num_radial_lines)
                ]
            )

            # Axes: horizontal and vertical
            h_line = Line(
                LEFT * max_radius,
                RIGHT * max_radius,
                color=color,
                stroke_opacity=stroke_opacity,
            )
            v_line = Line(
                DOWN * max_radius,
                UP * max_radius,
                color=color,
                stroke_opacity=stroke_opacity,
            )

            axes = VGroup(h_line, v_line)

            return VGroup(circles, lines, axes)

        remaining = 2 * PI - omega * move_time * 1

        self.play(
            Rotate(rotating_all2, angle=remaining, about_point=starting_pos), run_time=2
        )

        self.wait()

        #  if you want to animate the polar coordinate perspective..
        # wip

        # polar = get_polar_grid()
        # polar.scale(0.2)
        # polar.move_to(starting_pos)
        # ant2.move_to(starting_pos)

        # self.play(FadeOut(right_plane))
        # self.play(FadeIn(polar))

        # # ant2.move_to(starting_pos)

        # arrow_x = Arrow(
        #     start=pos, end=pos + np.array([0, 0, 0]), fill_color=BLUE, buff=0
        # )

        # arrow_y = Arrow(
        #     start=pos,
        #     end=pos + np.array([0, 0, 0]),
        #     fill_color=BLUE,
        #     buff=0,
        # )

        # self.add(arrow_x)
        # self.add(arrow_y)

        # def update_ant_east_with_polar(mob, alpha, disc, polar, starting_pos=ORIGIN):

        #     time_prev = times[0]
        #     time = move_time * alpha
        #     dt = time - time_prev
        #     times[0] = time
        #     disc.rotate(omega * dt, about_point=starting_pos)

        #     ant_pos = mob.get_center()
        #     pos = ant_pos + [move_speed * dt, 0, 0]
        #     mob.move_to(pos)
        #     # right_arrow.next_to(mob, RIGHT, aligned_edge=RIGHT)

        #     polar.move_to(pos)
        #     polar.rotate(omega * dt, about_point=polar.get_center())

        #     disc.add(mob.copy().set_fill(GREEN))

        #     rel_pos = pos - starting_pos
        #     x, y, z = rel_pos
        #     scale = 1

        #     theta = math.atan2(y, x)
        #     dadt = math.cos(theta) * scale
        #     drdt = -math.sin(theta) * scale

        #     new_arrow_x = Arrow(
        #         start=pos, end=pos + np.array([dadt + 1, 0, 0]), fill_color=BLUE, buff=0
        #     )
        #     new_arrow_x.rotate(theta, about_point=pos)
        #     new_arrow_y = Arrow(
        #         start=pos,
        #         end=pos + np.array([0, drdt, 0]),
        #         fill_color=BLUE,
        #         buff=0,
        #     )
        #     new_arrow_y.rotate(theta, about_point=pos)

        #     arrow_x.become(new_arrow_x)
        #     arrow_y.become(new_arrow_y)

        # times = [0]

        # self.play(
        #     UpdateFromAlphaFunc(
        #         ant2,
        #         partial(
        #             update_ant_east_with_polar,
        #             disc=rotating_all2,
        #             polar=polar,
        #             starting_pos=starting_pos,
        #         ),
        #     ),
        #     run_time=move_time * 2,
        #     rate_func=linear,
        # )

        # # Step through every nth frame

        # self.wait(1)
        # self.remove(arrow_x)
        # self.remove(arrow_y)
        # self.remove(polar)


class GeometricSeriesVisualization(Scene):
    def construct(self):
        # Geometric series visual proof
        r = 0.8  # Updated ratio value
        scale_factor = 2.3  # Rescale the entire image
        shift_amount = LEFT * 5  # Shift entire graph to the left

        # Base lines
        left_line = Line([0, 0, 0], [0, 1 * scale_factor, 0], color=WHITE).shift(
            shift_amount
        )

        origin = left_line.get_start()
        # bottom_line = Line(
        #     origin + [0, 0, 0], origin + [1 / (1 - r) * scale_factor, 0, 0], color=WHITE
        # )

        # Vertical segment lines at positions 1, 1+r, 1+r+r^2, ...
        x_pos = 1 * scale_factor
        x_pos_prev = 0

        vertical_lines = []
        segment_labels = []
        vertical_line = None
        vertical_line_prev = left_line
        cnt = 0
        while x_pos < (1 / (1 - r)) * scale_factor - 0.1:
            cnt += 1
            run_time = 1
            if cnt > 5:
                run_time = 0.1

            vertical_line = Line(
                origin + [x_pos, 0, 0],
                origin + [x_pos, r ** (len(vertical_lines) + 1) * scale_factor, 0],
                color=WHITE,
            )
            vertical_lines.append(vertical_line)

            horizontal_line = Line(
                origin + [x_pos_prev, 0, 0],
                origin + [x_pos, 0, 0],
            )
            x_pos_prev = x_pos

            len_v = len(vertical_lines)
            if len_v <= 6:
                if len_v == 1:
                    len_t = 1
                elif len_v == 2:
                    len_t = "r"
                elif len_v == 6:
                    len_t = "..."
                else:
                    len_t = f"r^{len_v-1}"
                text = Tex(f"{len_t}").next_to(
                    horizontal_line, DOWN, buff=0.3, aligned_edge=DOWN
                )
            else:
                text = None

            if text is not None:
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    FadeIn(text),
                    run_time=run_time,
                )
            else:
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    run_time=run_time,
                )

            x_pos += r ** len(vertical_lines) * scale_factor
            vertical_line_prev = vertical_line

        self.wait(2)
        bottom_line = Line(
            origin + [0, 0, 0], origin + [1 / (1 - r) * scale_factor, 0, 0], color=WHITE
        )
        diagonal_line = Line(
            origin + [0, 1 * scale_factor, 0],
            origin + [(1 / (1 - r)) * scale_factor, 0, 0],
            color=WHITE,
        )
        self.play(FadeIn(diagonal_line), FadeIn(bottom_line), run_time=3)

        # Upper similar triangle
        upper_triangle = Polygon(
            origin + [0, 1 * scale_factor, 0],
            origin + [1 * scale_factor, 1 * scale_factor, 0],
            origin + [1 * scale_factor, r * scale_factor, 0],
            color=WHITE,
        )

        upper_triangle.set_fill(BLUE, opacity=0.7)
        self.play(FadeIn(upper_triangle))

        # Labels for lengths
        left_label = Brace(left_line, LEFT)
        left_text = Tex("1").next_to(left_label, LEFT, buff=0.2)

        top_line = Line(
            origin[:2] + [0, 1 * scale_factor],
            origin[:2] + [1 * scale_factor, 1 * scale_factor],
        )

        top_label = Brace(top_line, UP)
        top_text = Tex("1").next_to(top_label, UP, buff=0.2)

        right_line = Line(
            origin + [1 * scale_factor, 1 * scale_factor, 0],
            origin + [1 * scale_factor, r * scale_factor, 0],
        )
        right_label = Brace(right_line, RIGHT)
        right_text = Tex("1 - r").next_to(right_label, RIGHT, buff=0.2)

        self.play(
            FadeIn(left_label),
            FadeIn(left_text),
            FadeIn(top_label),
            FadeIn(top_text),
            FadeIn(right_label),
            FadeIn(right_text),
        )

        self.wait()

        # Lower similar triangle
        lower_triangle = Polygon(
            origin + [0, 1 * scale_factor, 0],
            origin + [0, r * scale_factor, 0],
            origin + [1 * scale_factor, r * scale_factor, 0],
            color=WHITE,
        )

        lower_triangle.set_fill(RED, opacity=0.7)
        self.play(FadeIn(lower_triangle))

        # Animation to grow lower triangle into the bottom big triangle
        def update_triangle(triangle, alpha):
            if alpha < 1 - r:
                return
            new_bottom_right = origin + [
                (1 / (1 - r)) * scale_factor * alpha,
                (1 - alpha) * scale_factor,
                0,
            ]
            new_polygon = Polygon(
                origin + [0, 1 * scale_factor, 0],
                origin + [0, (1 - alpha) * scale_factor, 0],
                new_bottom_right,
                color=WHITE,
            )
            new_polygon.set_fill(RED, opacity=0.7)

            triangle.become(new_polygon)

        self.play(UpdateFromAlphaFunc(lower_triangle, update_triangle))
        self.wait()

        # equation
        equation = Tex(r"\frac{1}{1 - r} = \frac{1 + r + r^2 + \dots}{1}")
        equation.move_to(bottom_line.get_center() + DOWN * 2).scale(
            1.3
        )  # Make it slightly larger
        self.play(Write(equation))  # Animate the equation appearing
        self.wait()

        # Lower similar triangle
        middle_triangle = Polygon(
            origin + [1 * scale_factor, r * scale_factor, 0],
            origin + [1 * scale_factor, r * r * scale_factor, 0],
            origin + [(1 + r) * scale_factor, r * r * scale_factor, 0],
            color=WHITE,
        )

        left_line = Line(
            middle_triangle.get_vertices()[0], middle_triangle.get_vertices()[1]
        )

        b_label = Brace(left_line, LEFT)
        b_text = Tex("r - r^2").next_to(b_label, LEFT, buff=0.2)

        middle_triangle.set_fill(YELLOW, opacity=0.7)
        self.play(FadeIn(middle_triangle))
        self.play(FadeIn(b_label), FadeIn(b_text))

        middle_line = Line(
            origin + [1 * scale_factor, 0, 0],
            origin + [1 * scale_factor, r * r * scale_factor, 0],
            color=WHITE,
        )

        b_label = Brace(middle_line, LEFT)
        b_text = Tex("r^2").next_to(b_label, LEFT, buff=0.2)
        self.play(FadeIn(b_label), FadeIn(b_text))

        self.wait()


class GeometricSeriesVisualization2(Scene):
    def construct(self):
        # Geometric series visual proof
        r = 0.8  # Updated ratio value
        scale_factor = 2.3  # Rescale the entire image
        shift_amount = LEFT * 5  # Shift entire graph to the left

        # Base lines
        left_line = Line([0, 0, 0], [0, 1 * scale_factor, 0], color=WHITE).shift(
            shift_amount
        )

        origin = left_line.get_start()
        # bottom_line = Line(
        #     origin + [0, 0, 0], origin + [1 / (1 - r) * scale_factor, 0, 0], color=WHITE
        # )

        # Vertical segment lines at positions 1, 1+r, 1+r+r^2, ...
        x_pos = 1 * scale_factor
        x_pos_prev = 0

        vertical_lines = []
        segment_labels = []
        vertical_line = None
        vertical_line_prev = left_line
        cnt = 0
        while x_pos < (1 / (1 - r)) * scale_factor - 0.1:
            cnt += 1
            run_time = 0.1

            vertical_line = Line(
                origin + [x_pos, 0, 0],
                origin + [x_pos, r ** (len(vertical_lines) + 1) * scale_factor, 0],
                color=WHITE,
            )
            vertical_lines.append(vertical_line)

            horizontal_line = Line(
                origin + [x_pos_prev, 0, 0],
                origin + [x_pos, 0, 0],
            )
            x_pos_prev = x_pos

            len_v = len(vertical_lines)
            if len_v <= 6:
                if len_v == 1:
                    len_t = 1
                elif len_v == 2:
                    len_t = "r"
                elif len_v == 6:
                    len_t = "..."
                else:
                    len_t = f"r^{len_v-1}"
                text = Tex(f"{len_t}").next_to(
                    horizontal_line, DOWN, buff=0.3, aligned_edge=DOWN
                )
            else:
                text = None

            if text is not None:
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    FadeIn(text),
                    run_time=run_time,
                )
            else:
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    run_time=run_time,
                )

            x_pos += r ** len(vertical_lines) * scale_factor
            vertical_line_prev = vertical_line

        self.wait(2)
        bottom_line = Line(
            origin + [0, 0, 0], origin + [1 / (1 - r) * scale_factor, 0, 0], color=WHITE
        )

        end = origin + [(1 / (1 - r)) * scale_factor, 0, 0]
        diagonal_line = Line(
            origin + [0, 1 * scale_factor, 0],
            end,
            color=WHITE,
        )
        self.play(FadeIn(diagonal_line), FadeIn(bottom_line), run_time=3)

        self.wait()

        # Dot at bottom-right point

        glow = Dot(point=end, color=BLUE, radius=0.3, fill_opacity=0.2)

        # Add dot + glow
        self.play(FadeIn(glow))
        self.wait()


class PandaNoiseIllustration(Scene):
    def construct(self):
        # Step 1: Show the washed out panda

        washed_out = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/new_panda_more_washed_out.png"
        )

        ws2 = washed_out.copy().shift(LEFT * 3.2)

        self.play(FadeIn(washed_out), FadeIn(ws2))

        self.wait(1)
        # noise_layer = ImageMobject("/Users/eugenekim/projects/dance-with/first-project/coarse_noise_overlay.png"
        #                            )

        noise_layer = Rectangle(
            width=washed_out.get_width(),
            height=washed_out.height,
            fill_color=GREY_D,
            fill_opacity=0.6,
            stroke_opacity=0,
        )

        noise_layer_top = Rectangle(
            width=washed_out.get_width(),
            height=washed_out.height,
            fill_color=GREY_D,
            fill_opacity=0.4,
            stroke_opacity=0,
        )

        noise_layer.next_to(washed_out, RIGHT * 2)

        t1 = Text("노이즈", font="BM Hanna 11yrs Old")
        t1.next_to(noise_layer, DOWN)
        t2 = t1.copy().next_to(washed_out, DOWN)

        gr_noise = VGroup(noise_layer, t1)

        self.play(FadeIn(gr_noise))

        self.wait()

        # Step 3: Transition to the moderately noisy image (sharper)
        sharper_panda = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/new_panda_noise_1.png"
        )
        sharper_panda.move_to(washed_out.get_center())

        self.play(
            # noise_layer.animate.move_to(washed_out),
            Transform(noise_layer, noise_layer_top),
            Transform(t1, t2),
        )
        self.play(
            noise_layer.animate.move_to(washed_out),
            FadeOut(washed_out),
            FadeOut(gr_noise),
            FadeIn(sharper_panda),
            FadeOut(t2),
        )

        self.wait(2)

        # self.play(
        #     FadeOut(washed_out), FadeOut(noise_layer), FadeIn(sharper_panda), run_time=2
        # )

        t1 = Text("원본", font="BM Hanna 11yrs Old")
        t1.next_to(ws2, DOWN)

        t2 = Text("원본 + 노이즈", font="BM Hanna 11yrs Old").set_color(YELLOW)
        t2.next_to(sharper_panda, DOWN)

        self.play(FadeIn(t1), FadeIn(t2))
        self.wait(2)

        noise2 = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/new_panda_noise_3.png"
        )

        noise2.next_to(sharper_panda, RIGHT * 2)

        t3 = Text("노이즈 * 5", font="BM Hanna 11yrs Old")
        t3.next_to(noise2, DOWN)

        self.play(FadeIn(noise2), FadeIn(t3))

        self.wait()

        t1 = Tex(r"a + b").scale(1.2)
        t1.shift(UP * 2.7)

        self.play(Write(t1))
        self.wait()


class AbstractNumberScene(Scene):
    def construct(self):
        # ----------------------------
        # 🐑 3-SHEEP ADDITION
        # ----------------------------
        sheep_path = "/Users/eugenekim/projects/dance-with/first-project/sheep.png"
        sheep1 = ImageMobject(sheep_path).scale(0.6).shift(LEFT * 2)
        sheep2 = ImageMobject(sheep_path).scale(0.6)
        sheep3 = ImageMobject(sheep_path).scale(0.6).shift(RIGHT * 2)

        plus1 = Tex("+").scale(1.2).next_to(sheep1, RIGHT, buff=0.2)
        plus2 = Tex("+").scale(1.2).next_to(sheep2, RIGHT, buff=0.2)

        self.play(FadeIn(sheep1))
        self.wait(0.3)
        self.play(FadeIn(sheep2))
        self.wait(0.3)
        self.play(FadeIn(sheep3))
        self.wait(0.5)

        sheep_eq = Tex("= 3").scale(1.2).next_to(sheep3, RIGHT, buff=0.4)
        self.play(Write(sheep_eq))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [sheep1, sheep2, sheep3, sheep_eq]])

        # ----------------------------
        # 🍎 3-APPLE ADDITION
        # ----------------------------
        apple_path = "/Users/eugenekim/projects/dance-with/first-project/apple.png"
        apple1 = ImageMobject(apple_path).scale(0.6).shift(LEFT * 2)
        apple2 = ImageMobject(apple_path).scale(0.6)
        apple3 = ImageMobject(apple_path).scale(0.6).shift(RIGHT * 2)

        plus3 = Tex("+").scale(1.2).next_to(apple1, RIGHT, buff=0.2)
        plus4 = Tex("+").scale(1.2).next_to(apple2, RIGHT, buff=0.2)

        self.play(FadeIn(apple1))
        self.wait(0.3)
        self.play(FadeIn(apple2))
        self.wait(0.3)
        self.play(FadeIn(apple3))
        self.wait(0.5)

        apple_eq = Tex("= 3").scale(1.2).next_to(apple3, RIGHT, buff=0.4)
        self.play(Write(apple_eq))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [apple1, apple2, apple3, apple_eq]])

        # ----------------------------
        # 📄 ABSTRACT INTEGER ADDITION
        # ----------------------------
        # self.play(FadeOut(self.mobjects))  # Clear screen

        int_expr = Tex("1 + 1 + 1 = 3").scale(2)

        # Extract number indices from the expression
        number_indices = [0, 2, 4, 6]  # positions of '1', '1', '1', '3'

        # Create glow circles for each number
        glows = [
            Circle(radius=0.4, color=WHITE, fill_opacity=0.3, stroke_opacity=0).move_to(
                int_expr[i].get_center()
            )
            for i in number_indices
        ]

        self.play(Write(int_expr))
        self.wait(0.5)
        self.play(*[FadeIn(glow) for glow in glows])
        self.wait(2)

        self.play(FadeOut(int_expr), *[FadeOut(glow) for glow in glows])

        self.wait()

        # ----------------------------
        # 📏 REAL NUMBER ADDITION (LENGTHS)
        # ----------------------------

        origin = LEFT * 4

        # Make lines longer and distinguishable
        seg1 = Line(origin, origin + RIGHT * 3.0, color=BLUE, stroke_width=10)
        seg1_label = Tex("1.5", font_size=50).next_to(seg1, DOWN)

        seg2 = Line(
            seg1.get_end(), seg1.get_end() + RIGHT * 4.6, color=GREEN, stroke_width=10
        )
        seg2_label = Tex("2.3", font_size=50).next_to(seg2, DOWN)

        # Total line (faint white), placed below
        sum_seg = Line(origin, origin + RIGHT * 7.6, color=YELLOW, stroke_width=10)
        sum_seg.shift(DOWN * 1.0)

        sum_label = Tex("= 3.8", font_size=50).next_to(sum_seg, DOWN)

        # Animate additions
        self.play(FadeIn(seg1), FadeIn(seg1_label))
        self.wait(0.5)
        self.play(FadeIn(seg2), FadeIn(seg2_label))
        self.wait(1)
        self.play(FadeIn(sum_seg), FadeIn(sum_label))
        self.wait(1.5)

        # Fade out everything
        self.play(
            *[
                FadeOut(mob)
                for mob in [seg1, seg2, seg1_label, seg2_label, sum_seg, sum_label]
            ]
        )

        # ----------------------------
        # 🧭 VECTOR ADDITION
        # ----------------------------
        # Bigger and colorful vector addition

        start = ORIGIN

        # Extend the vector lengths
        v1 = Arrow(
            start, start + RIGHT * 4, buff=0, color=ORANGE, stroke_width=8
        ).shift(LEFT * 2.8 + DOWN)
        v2 = Arrow(
            v1.get_end(), v1.get_end() + UP * 3, buff=0, color=GREEN, stroke_width=8
        )
        v_sum = Arrow(
            v1.get_start(), v1.get_end() + UP * 3, buff=0, color=WHITE, stroke_width=8
        )

        # Bigger, clearer labels
        v_label = Tex("\\vec{v}_1", font_size=42).next_to(v1, DOWN)
        u_label = Tex("\\vec{v}_2", font_size=42).next_to(v2, RIGHT)
        sum_label = Tex("\\vec{v}_1 + \\vec{v}_2", font_size=44).next_to(
            v_sum, UP + RIGHT * 0.3
        )

        self.play(GrowArrow(v1), FadeIn(v_label))
        self.play(GrowArrow(v2), FadeIn(u_label))
        self.wait(0.5)
        self.play(GrowArrow(v_sum), FadeIn(sum_label))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [v1, v2, v_sum, v_label, u_label, sum_label]])

        self.wait()

        # ----------------------------
        # ➕ FINAL ABSTRACTION: a + b
        # ----------------------------

        expr = Tex("a + b").scale(2.5)
        plus_part = expr[1]

        # Create glow: white circle behind +
        glow = Circle(
            radius=0.5, color=WHITE, fill_opacity=0.3, stroke_opacity=0
        ).move_to(plus_part.get_center())

        self.play(Write(expr))
        self.wait(0.5)
        self.play(FadeIn(glow), plus_part.animate.set_color(YELLOW).scale(1.2))
        self.wait(2)


class MemoryConceptScene(Scene):
    def construct(self):
        # Load images
        animals_path = "/Users/eugenekim/projects/dance-with/first-project/animals.png"
        face_path = "/Users/eugenekim/projects/dance-with/first-project/face.png"

        # Image Mobjects
        animals = ImageMobject(animals_path).scale(1)
        face = ImageMobject(face_path).scale(1)

        # Reduce distance: shift slightly less than full screen
        animals.shift(LEFT * 3 + UP)
        face.shift(RIGHT * 3 + UP)

        # Text under animal
        episodic_desc = Text("여러번의 구체적인 경험", font="BM Hanna 11yrs Old").scale(
            1.2
        )
        episodic_desc.next_to(animals, DOWN, buff=0.3)

        # Text under face
        semantic_desc = Text("얼굴이라는 개념", font="BM Hanna 11yrs Old").scale(1.2)
        semantic_desc.next_to(face, DOWN, buff=0.3)
        semantic_desc.set_color_by_text("얼굴", GREEN)
        semantic_desc.set_color_by_text("개념", ORANGE)

        # STEP 1: Show left image and its description
        self.play(FadeIn(animals))
        self.wait(0.5)
        self.play(Write(episodic_desc))
        self.wait(1)

        # STEP 2: Show right image and its description
        self.play(FadeIn(face))
        self.wait(0.5)
        self.play(Write(semantic_desc))
        self.wait(1.5)

        # STEP 4: Arrow from left to right
        arrow = Arrow(start=animals.get_right(), end=face.get_left(), buff=0.3)

        self.play(GrowArrow(arrow))
        self.wait(2)

        # STEP 3: Show memory labels
        episodic_kr = Text("(에피소드 기억)", font="BM Hanna 11yrs Old", font_size=32)
        semantic_kr = Text("(의미 기억)", font="BM Hanna 11yrs Old", font_size=32)
        episodic_kr.next_to(episodic_desc, DOWN, buff=0.3)
        semantic_kr.next_to(semantic_desc, DOWN, buff=0.3)

        self.play(Write(episodic_kr))
        self.wait(0.5)
        self.play(Write(semantic_kr))
        self.wait(1)


class DateScene(Scene):
    def construct(self):

        dating_path = "/Users/eugenekim/projects/dance-with/first-project/dating.png"

        # Image Mobjects
        dating = ImageMobject(dating_path).scale(1)

        pick_path = "/Users/eugenekim/projects/dance-with/first-project/datepick.png"

        # Image Mobjects
        pick = ImageMobject(pick_path).scale(1)

        dad_path = "/Users/eugenekim/projects/dance-with/first-project/dad.png"

        # Image Mobjects
        dad = ImageMobject(dad_path).scale(0.5)

        dating.shift(UP)
        pick.shift(UP)

        # Step 1: Show girl evaluating candidates
        self.play(FadeIn(dating))
        self.wait(2)

        # Step 2: Transition to picked candidate

        self.play(FadeOut(dating), FadeIn(pick))

        self.wait(2)

        # Step 3: Reveal dad image (implying resemblance)

        dad.move_to(dating)
        dad.shift(UP + RIGHT * 1.8)
        dad.set_opacity(0)  # start transparent
        self.play(FadeIn(dad.set_opacity(1)))
        self.wait(2)

        # Step 4: Text: "여러번의 구체적인 경험 → 이상적인 파트너"
        text1 = Text(
            "여러번의 구체적인 경험 ---> 이상적인 파트너",
            font="BM Hanna 11yrs Old",
            font_size=36,
        )
        text1.next_to(pick, DOWN)
        self.play(Write(text1))
        self.wait(2)

        # Step 5: Cross it out with red X line
        x_line1 = Line(
            text1.get_corner(UL), text1.get_corner(DR), color=RED, stroke_width=5
        )
        x_line2 = Line(
            text1.get_corner(UR), text1.get_corner(DL), color=RED, stroke_width=5
        )
        self.play(ShowCreation(x_line1), ShowCreation(x_line2))
        self.wait(1.5)

        # Step 6: New Text: "각인 → 여러번의 경험"
        text2 = Text("각인 ---> 재경험", font="BM Hanna 11yrs Old", font_size=36)
        text2.next_to(text1, DOWN)
        self.play(Write(text2))
        self.wait(3)


class CreateOrFoundScene(Scene):
    def construct(self):

        int_expr = Tex("1 + 1 + 1 = 3").scale(2)
        int_expr.shift(UP * 1.5)

        # Extract number indices from the expression
        number_indices = [0, 2, 4, 6]  # positions of '1', '1', '1', '3'

        # Create glow circles for each number
        glows = [
            Circle(radius=0.4, color=WHITE, fill_opacity=0.3, stroke_opacity=0).move_to(
                int_expr[i].get_center()
            )
            for i in number_indices
        ]

        self.play(Write(int_expr))
        self.wait(1)
        self.play(*[FadeIn(glow) for glow in glows])

        expr = Tex("a + b").scale(2)
        expr.next_to(int_expr, DOWN * 2)
        plus_part = expr[1]

        # Create glow: white circle behind +
        glow = Circle(
            radius=0.5, color=WHITE, fill_opacity=0.3, stroke_opacity=0
        ).move_to(plus_part.get_center())

        self.play(Write(expr))
        self.wait(0.5)
        self.play(FadeIn(glow), plus_part.animate.set_color(YELLOW).scale(1.2))
        self.wait(2)

        # Step 4: Text: "여러번의 구체적인 경험 → 이상적인 파트너"
        text1 = Text(
            "여러번의 경험을 개념화 ---> 발명",
            font="BM Hanna 11yrs Old",
            font_size=40,
        )
        text1.next_to(expr, DOWN * 2)
        text1.set_color_by_text("발명", GREEN)

        self.play(Write(text1))
        self.wait(2)

        # Step 6: New Text: "각인 → 여러번의 경험"
        text2 = Text("원래 있던것 ---> 발견", font="BM Hanna 11yrs Old", font_size=40)
        text2.set_color_by_text("발견", ORANGE)

        text2.next_to(text1, DOWN)
        self.play(Write(text2))
        self.wait(3)


class UniverseAndN(Scene):
    def construct(self):
        # Step 1: Universe illustration
        universe = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/universe.png"
        )
        universe.scale(1.8).set_opacity(0.4)
        self.play(FadeIn(universe))
        self.wait(2)

        # Step 2: Pose the universe question
        # q1 = Text("우주는 무한할까?", font="BM Hanna 11yrs Old").scale(1.5)

        # q1.to_edge(UP, buff=1)
        # self.play(Write(q1))
        # self.wait(1)
        # self.play(FadeOut(q1))

        particle_text = Text(
            "무한한 수의 입자가 존재할까?",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)
        # particle_text.next_to(q1, DOWN)
        particle_text.shift(UP * 2)
        self.play(Write(particle_text))
        self.wait(2)

        # Step 3: Fade to dark

        # Step 4: Show ℕ
        n_text = Text(
            "ℕ = {1, 2, 3, 4, 5, ...}",
            font="BM Hanna 11yrs Old",
        ).scale(2.0)

        self.play(Write(n_text))
        self.wait(2)

        text2 = Text("발견 or 발명?", font="BM Hanna 11yrs Old").scale(2.0)
        text2.set_color_by_text("발명", GREEN)
        text2.set_color_by_text("발견", ORANGE)
        n_text.set_color_by_text("ℕ", YELLOW)

        text2.next_to(n_text, DOWN * 3)

        self.play(Write(text2))
        self.wait(3)

        self.play(
            FadeOut(text2), FadeOut(n_text), FadeOut(particle_text), FadeOut(universe)
        )

        corpus = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/corpus.png"
        )
        corpus.scale(1.2).to_edge(LEFT, buff=1.3)
        # courpus.shift(UP)
        self.play(FadeIn(corpus))
        self.wait(1)

        embedding = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/embedding.png"
        )
        embedding.scale(1.2).to_edge(RIGHT, buff=1.3)
        # embedding.shift(UP)
        self.play(FadeIn(embedding))
        self.wait(2)

        # q1 = Text("각각의 단어를 숫자로 표현함", font="BM Hanna 11yrs Old").scale(1.5)

        # q1.shift(3 * DOWN)
        # self.play(Write(q1))
        # self.wait(1)

        # # Step 7: Fade to insight
        # self.play(FadeOut(particle_text))
        # insight = Text(
        #     "ℕ은 어쩌면, 우리의 '창조물'일지도 모른다.",
        #     font="BM Hanna 11yrs Old",
        #     font_size=44,
        # )
        # self.play(Write(insight))
        # self.wait(3)


class PiTablesManimGL(Scene):
    def construct(self):
        # First table: 200 billion digits of pi

        pi = Tex(r"\pi ").scale(2).set_color(GREEN)
        t2 = Text(
            "의 랜덤성",
            font="BM Hanna 11yrs Old",
            font_size=44,
        ).scale(1.5)
        pi_g = VGroup(pi, t2).arrange(RIGHT, buff=0.2).shift(UP * 3.1)

        self.play(FadeIn(pi_g))

        im1 = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/pi_frequency.png"
        )
        im1.scale(1.2).to_edge(LEFT, buff=1)
        self.play(FadeIn(im1))
        self.wait(1)

        im2 = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/pi_card.png"
        )
        im2.scale(1.2).to_edge(RIGHT, buff=1)

        l2 = Text(
            "연속 5자리를 포커패로 구분",
            font="BM Hanna 11yrs Old",
            font_size=44,
        )
        l2.next_to(im2, DOWN)

        self.play(FadeIn(im2))
        self.play(Write(l2))
        self.wait(2)

        g = VGroup(pi_g, l2)

        self.play(FadeOut(g), FadeOut(im1), FadeOut(im2))

        l2 = (
            Text(
                "랜덤한 수가 나오는데,",
                font="BM Hanna 11yrs Old",
            )
            .shift(UP)
            .scale(1.5)
        )

        l3 = Text(
            "뭐가 나올지는 이미 정해져 있음",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)
        l3.next_to(l2, DOWN)

        l4 = Text(
            "정해진 랜덤?",
            font="BM Hanna 11yrs Old",
            font_size=50,
        ).scale(2.0)

        l4.next_to(l3, DOWN)

        l4.set_color_by_text("정해진", GREEN)
        l4.set_color_by_text("랜덤", ORANGE)

        self.play(Write(l2))
        self.wait(0.5)
        self.play(Write(l3))
        self.wait(0.5)
        self.play(Write(l4))

        self.wait(2)

        g = VGroup(l2, l3, l4)

        self.play(FadeOut(g))

        l1 = (
            Text(
                "양자얽힘",
                font="BM Hanna 11yrs Old",
            )
            .shift(UP * 3)
            .scale(2)
        )

        self.play(Write(l1))

        both = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/updown.png"
        )

        up = ImageMobject("/Users/eugenekim/projects/dance-with/first-project/up.png")
        down = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/down.png"
        )

        bl = both.copy().scale(1).shift(LEFT * 4)

        br = both.copy().scale(1).shift(RIGHT * 4)
        self.play(FadeIn(br), FadeIn(bl))
        self.wait()

        up = up.move_to(bl)
        down = down.move_to(br)
        self.play(ReplacementTransform(br, down))
        self.wait(2)

        self.play(ReplacementTransform(bl, up))

        self.wait(2)

        self.play(ReplacementTransform(up, bl), ReplacementTransform(down, br))

        self.wait(2)
        up = up.move_to(br)
        down = down.move_to(bl)

        self.play(ReplacementTransform(br, up))

        self.wait(2)
        self.play(ReplacementTransform(bl, down))

        self.wait(2)

        self.play(ReplacementTransform(up, br), ReplacementTransform(down, bl))
        self.wait(2)
        self.play(ReplacementTransform(br, up))

        self.wait(1)

        l2 = Text(
            "랜덤한데,",
            font="BM Hanna 11yrs Old",
            font_size=48,
        ).shift(DOWN)

        l3 = Text(
            "뭐가 나올지는 이미 정해져 있음",
            font="BM Hanna 11yrs Old",
            font_size=48,
        )
        l3.next_to(l2, DOWN)

        l4 = Text(
            "정해진 랜덤",
            font="BM Hanna 11yrs Old",
            font_size=52,
        )

        l4.next_to(l3, DOWN)

        l4.set_color_by_text("정해진", GREEN)
        l4.set_color_by_text("랜덤", ORANGE)

        self.play(Write(l2))
        self.wait(0.5)
        self.play(Write(l3))
        self.wait(0.5)
        self.play(Write(l4))

        self.wait(2)


class GaltonHistogram(Scene):
    def construct(self):
        # Histogram config

        num_bins = 13
        bin_range = (-4, 4)
        bin_width = (bin_range[1] - bin_range[0]) / num_bins
        bin_edges = [bin_range[0] + i * bin_width for i in range(num_bins + 1)]
        bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(num_bins)]

        # Axes
        axes = Axes(
            x_range=(bin_range[0], bin_range[1]),
            y_range=(0, 24),
            axis_config={"include_tip": False},
        )
        axes.to_edge(DOWN)

        self.add(axes)

        # Bars (initially height 0)
        bars = VGroup()
        bar_width = bin_width * 0.9
        for center in bin_centers:
            bar = Rectangle(
                width=bar_width,
                height=0.01,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0,
            )
            bar.move_to(axes.c2p(center, 0), DOWN)
            bars.add(bar)

        self.add(bars)

        # Histogram bin counts
        counts = [0 for _ in range(num_bins)]
        max_height = 20

        # Animation loop: drop samples and grow bars
        for i in range(200):
            sample = random.gauss(0, 1.5)  # Normal distribution
            # Bin it
            for j in range(num_bins):
                if bin_edges[j] <= sample < bin_edges[j + 1]:
                    counts[j] += 1
                    break
            else:
                # Clip to edge bins
                if sample < bin_edges[0]:
                    counts[0] += 1
                elif sample >= bin_edges[-1]:
                    counts[-1] += 1

            # Update bars visually
            updated_bars = VGroup()
            for j, count in enumerate(counts):
                # height = min(count, max_height)
                height = count
                bar = Rectangle(
                    width=bar_width,
                    height=height * 0.2,  # Scale to fit y axis
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_width=0,
                )
                bar.move_to(axes.c2p(bin_centers[j], 0), DOWN)
                updated_bars.add(bar)

            self.play(Transform(bars, updated_bars), run_time=0.02)

        self.wait(2)
        self.play(bars.animate.set_fill(opacity=0.2), run_time=1)

        # Add normal distribution curve (yellow)
        curve_points = []
        scale_y = 6.0  # Scaling factor for visual height
        for x in np.linspace(bin_range[0], bin_range[1], 300):
            y = math.exp(-((x / 1.5) ** 2) / 2) * scale_y
            curve_points.append(axes.c2p(x, y))

        curve = VMobject(color=YELLOW)
        curve.set_points_smoothly(curve_points)
        self.play(FadeIn(curve), run_time=2)
        self.wait(0.5)

        # Add explanation text
        l5 = Text("확률 분포라는 것도", font="BM Hanna 11yrs Old", font_size=52)
        l6 = Text(
            "전체의 그림은 정해져 있다는 것", font="BM Hanna 11yrs Old", font_size=52
        )
        l5.shift(UP)
        l6.next_to(l5, DOWN)

        self.play(Write(l5))
        self.play(Write(l6))
        self.wait(2)

        l5 = Text(
            "확률 분포라는 것도",
            font="BM Hanna 11yrs Old",
            font_size=52,
        )

        l6 = Text(
            "전체의 그림은 정해져 있다는 것",
            font="BM Hanna 11yrs Old",
            font_size=52,
        )
        l5.shift(UP)

        l6.next_to(l5, DOWN)

        self.play(Write(l5))
        self.play(Write(l6))


class RiemannScene(Scene):
    def construct(self):
        # 1. Complex Plane Setup
        plane = (
            ComplexPlane(
                x_range=[-2, 6, 1],
                y_range=[-1, 6, 1],
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_opacity": 0.8,
                    "stroke_width": 1,
                },
            )
            .scale(1)
            .shift(RIGHT * 2)
        )
        self.add(plane)

        zeta_tex = (
            Tex(
                r"""\begin{aligned}
                \zeta(s) &= \frac{1}{1^s} + \frac{1}{2^s} + \frac{1}{3^s} + \frac{1}{4^s} + \cdots \\
                &= 0
                \end{aligned}""",
                tex_to_color_map={"s": YELLOW},
            )
            .scale(0.8)
            .to_corner(UL)
            .shift(DOWN * 0.3)
        )

        self.add(zeta_tex)

        # 3. Prime number label (top-right)
        prime_tex = Tex("").to_corner(UR).shift(DOWN * 0.3)
        self.add(prime_tex)

        # 4. Actual imaginary parts of first non-trivial zeros
        zeros_actual = [
            14.134725,
            21.022040,
            25.010857,
            30.424876,
            32.935061,
            37.586178,
            40.918719,
        ]
        scale = 0.12  # compress vertically for visibility
        visual_ys = [z * scale for z in zeros_actual]

        # 5. Dots on critical line
        x_pos = 0.5
        primes = [2, 3, 5, 7, 11, 13, 17]  # same number of items as zeros
        zero_dots = []

        for i, y in enumerate(visual_ys):
            dot = Dot(plane.n2p(complex(x_pos, y)), color=WHITE)
            zero_dots.append(dot)

            new_prime_tex = Tex(",".join(str(p) for p in primes[: i + 1]) + ",\\dots")
            new_prime_tex.to_corner(UR).shift(DOWN * 0.3)

            self.play(FadeIn(dot), Transform(prime_tex, new_prime_tex), run_time=0.5)

        # 6. Vertical yellow strip (optional, aesthetic)
        highlight_strip = Rectangle(
            height=6, width=0.1, fill_color=YELLOW, fill_opacity=0.3, stroke_width=0
        ).move_to(plane.n2p(complex(x_pos, 3)))
        self.wait()
        self.add(highlight_strip)

        # 7. Yellow vertical line (grows after dots)
        line_origin = plane.n2p(complex(x_pos, 0))
        line_up = plane.n2p(complex(x_pos, 6))
        line_down = plane.n2p(complex(x_pos, -1))

        critical_line_up = Line(
            start=line_origin,
            end=line_origin,
            color=YELLOW,
            stroke_width=4,
        )
        critical_line_down = Line(
            start=line_origin,
            end=line_origin,
            color=YELLOW,
            stroke_width=4,
        )

        self.add(critical_line_up, critical_line_down)

        self.play(
            critical_line_up.animate.put_start_and_end_on(line_origin, line_up),
            critical_line_down.animate.put_start_and_end_on(line_origin, line_down),
            run_time=1.2,
        )

        self.wait()


class RandomImpossible(Scene):
    def construct(self):

        t1 = (
            Text(
                "수학적으로",
                font="BM Hanna 11yrs Old",
            )
            .scale(1.3)
            .shift(UP)
        )

        t2 = Text(
            "Random 을 구현할 수 없음",
            font="BM Hanna 11yrs Old",
        ).scale(1.3)
        t2.set_color_by_text("Random", ORANGE)

        t2.next_to(t1, DOWN)

        self.play(Write(t1))
        self.play(Write(t2))
        self.wait(2)

        t3 = Text(
            "Random 은 발견했지만",
            font="BM Hanna 11yrs Old",
        ).scale(1.4)
        t3.set_color_by_text("발견", GREEN)

        t3.next_to(t2, DOWN * 2)

        t4 = Text(
            "표현할 수 없는 것인가?",
            font="BM Hanna 11yrs Old",
        ).scale(1.4)

        t4.next_to(t3, DOWN)

        self.play(Write(t3))
        self.play(Write(t4))
        self.wait(2)


class ZenoStep1(Scene):
    def construct(self):
        # Define points
        title = Text(
            "Zeno 역설",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)
        title.shift(UP * 3)

        self.add(title)

        start = LEFT * 6 + UP * 0.7
        end = RIGHT * 5 + UP * 0.7

        # Generate key points by halving repeatedly
        halfway = (start + end) / 2
        quarter = (halfway + end) / 2
        eighth = (quarter + end) / 2
        sixteenth = (eighth + end) / 2
        t32 = (sixteenth + end) / 2

        up_s = UP * 1  # vertical offset for dog image

        # Draw line

        line = Line(start, end, color=YELLOW, stroke_width=7)
        bones = (
            ImageMobject("/Users/eugenekim/projects/dance-with/first-project/bones.png")
            .scale(0.3)
            .next_to(end, RIGHT)
        )

        self.play(FadeIn(line), FadeIn(bones))

        # Goal label and dog bones

        # Load transparent dog image
        character = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/dog-zeno.png"
        ).scale(0.3)
        character.set_opacity(0.8)  # make dog slightly transparent
        character.move_to(start + up_s)
        self.add(character)

        # Function to create step animation
        def do_step(start_pt, end_pt, label_text):
            line_seg = Line(start_pt, end_pt)
            brace = Brace(line_seg, DOWN)
            label = brace.get_text(label_text)
            self.play(GrowFromCenter(brace), Write(label))
            self.play(character.animate.move_to(end_pt + up_s), run_time=1)
            self.wait(0.3)

        # Do four steps: 1/2, 1/4, 1/8, 1/16
        do_step(start, halfway, "1/2")
        do_step(halfway, quarter, "1/4")
        do_step(quarter, eighth, "1/8")
        do_step(eighth, sixteenth, "1/16")
        do_step(sixteenth, t32, "...")

        # Add "..." to imply infinity
        # dots = Text("...", font_size=60).move_to((sixteenth + end) / 2 )
        # self.play(FadeIn(dots))
        self.wait(1.5)

        lp = Tex(r"L_p = 1.616\,199 \times 10^{-35} \ \mathrm{m}")
        lp.shift(DOWN)
        self.play(Write(lp))

        t1 = (
            Text(
                "물리적으로 이보다 짧은 거리는 이동불가",
                font="BM Hanna 11yrs Old",
            )
            .scale(1.2)
            .next_to(lp, DOWN)
        )
        self.play(Write(t1))

        self.wait(2)

        question = Text(
            "ℝ 은 발명 or 발견?",
            font="BM Hanna 11yrs Old",
        ).scale(2.0)
        question.set_color_by_text("발명", GREEN)
        question.set_color_by_text("발견", ORANGE)
        question.set_color_by_text("ℝ", YELLOW)

        question.next_to(t1, DOWN * 1.3)
        self.play(Write(question))


class ShowCube(ThreeDScene):
    def construct(self):
        # Camera
        frame = self.camera.frame
        light = self.camera.light_source
        light.move_to([-10, -10, 20])

        # Plane and axes
        plane = NumberPlane(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            height=15,
            width=15,
            faded_line_ratio=3,
            axis_config={"include_tip": False},
        )
        plane.add_coordinate_labels()
        plane.coordinate_labels.set_stroke(width=0)

        axes = ThreeDAxes(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            z_range=(-2, 2, 1),
            height=15,
            width=15,
            depth=15,
        )
        axes.apply_depth_test()

        # Vertices and edges
        vert_coords = [(n % 2, (n // 2) % 2, (n // 4) % 2) for n in range(8)]
        verts = [axes.c2p(*coords) for coords in vert_coords]

        # Vertex spheres (removed later)
        spheres = SGroup()
        for vert in verts:
            sphere = Sphere(radius=0.1, resolution=(9, 9), color=GREY)
            sphere.move_to(vert)
            spheres.add(sphere)

        # Edges of the cube
        edge_indices = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]
        edges = VGroup(
            *[Line(verts[i], verts[j], color=WHITE) for i, j in edge_indices]
        )

        # 2D cube
        frame.move_to(1.5 * UP)
        self.add(plane)
        self.play(
            LaggedStartMap(GrowFromCenter, edges[:4]),
        )
        self.wait()

        # Transition to 3D
        frame.generate_target()
        frame.target.set_euler_angles(-25 * DEGREES, 70 * DEGREES)
        frame.target.move_to([1, 2, 0])
        frame.target.set_height(10)

        to_grow = Group(*edges[4:], *spheres[4:])
        to_grow.save_state()
        to_grow.set_depth(0, about_edge=IN, stretch=True)

        rf = squish_rate_func(smooth, 0.5, 1)
        self.play(
            MoveToTarget(frame),
            # REMOVE: ShowCreation(axes.z_axis),  # << this is the vertical bar you wanted to remove
            Restore(to_grow, rate_func=rf),
            run_time=3,
        )

        # Keep 3D camera rotating
        # frame.start_time = self.time
        # frame.scene = self
        # frame.add_updater(
        #     lambda m: m.set_theta(
        #         -25 * DEGREES * math.cos((m.scene.time - m.start_time) * PI / 60)
        #     )
        # )

        self.add(axes)  # full coordinate axes
        self.remove(spheres)  # no corner vertex spheres

        # --- Add particles inside the cube
        particles = Group()
        for _ in range(15):
            x = random.uniform(0.1, 0.9)
            y = random.uniform(0.1, 0.9)
            z = random.uniform(0.1, 0.9)
            pos = axes.c2p(x, y, z)
            p = Sphere(radius=0.05, resolution=(6, 6), color=YELLOW)
            p.move_to(pos)
            particles.add(p)

        self.play(LaggedStartMap(GrowFromCenter, particles, lag_ratio=0.1))
        self.wait(3)
        self.play(LaggedStartMap(FadeOut, particles, lag_ratio=0.1))
        self.wait(2)

        # --- 3D vector field using Arrow (ManimGL-compatible)
        vector_field = VGroup()
        grid_steps = [0.2, 0.4, 0.6, 0.8]  # Controls density of arrows

        for x in grid_steps:
            for y in grid_steps:
                for z in grid_steps:
                    start = axes.c2p(x, y, z)
                    direction = normalize(ORIGIN - start)  # inward pointing
                    end = start + 0.3 * direction
                    arrow = Arrow(
                        start=start,
                        end=end,
                        buff=0,
                        color=BLUE_E,
                        stroke_width=2,
                        # preserve_tip_size_when_scaling=False
                    )
                    vector_field.add(arrow)

        # vector_field.set_shade_in_3d(True)

        self.play(LaggedStartMap(GrowArrow, vector_field, lag_ratio=0.01), run_time=2)
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, vector_field, lag_ratio=0.3))
        self.wait(2)

        # --- Collapse cube: animate height dropping to the plane
        flatten_group = Group(*edges)
        self.play(
            flatten_group.animate.stretch(
                0.01, dim=2, about_point=ORIGIN
            ),  # dim=2 = Z-axis
            run_time=2,
        )
        self.wait(0.3)
        self.play(FadeOut(flatten_group), run_time=1)
        self.wait(2)

        self.play(Write(plane))

        self.wait(1)

        # --- Representing "nothingness" outside the universe
        nothing_pos = axes.c2p(0.5, 0.5, 0.4)
        nothing_dot = Sphere(radius=0.2, resolution=(6, 6), color=BLUE)
        nothing_dot.move_to(nothing_pos)

        # Arrow pointing to the dot (from the right side)
        arrow_start = axes.c2p(0.8, 0.8, 0.6)
        arrow = Arrow(
            start=arrow_start, end=nothing_pos, buff=0.05, stroke_width=3, color=WHITE
        )

        self.play(FadeIn(nothing_dot), GrowArrow(arrow))
        self.wait()


class ZeroPhilosophy(Scene):
    def construct(self):
        # Title (가운데 정렬, 크게)
        title = Text("없다는 것을 표현하는 0", font="BM Hanna 11yrs Old").scale(1.6)
        title.to_edge(UP).shift(DOWN * 0.8)

        # 자연수 줄
        line1 = Text("자연수: 1, 2, 3 이 아니다", font="BM Hanna 11yrs Old").scale(1.2)
        line1.set_color_by_text("자연수", RED)
        line1.shift(LEFT * 2.5 + UP)

        # 실수 줄 (with \pi)
        keyword2 = Text("실수:", font="BM Hanna 11yrs Old").scale(1.2).set_color(GREEN)
        pre2 = Text("0.23,", font="BM Hanna 11yrs Old").scale(1.2)
        pi = Tex(r"\pi").scale(1.2)
        post2 = Text(", 5 가 아니다.", font="BM Hanna 11yrs Old").scale(1.2)

        line2 = VGroup(keyword2, pre2, pi, post2).arrange(RIGHT, buff=0.15)
        line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.8)

        # 복소수 줄
        line3 = Text(
            "복소수: 3 + 4i 가 아니다.   0 + 0i 이다.", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        line3.set_color_by_text("복소수", BLUE)
        line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.8)

        # 애니메이션
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeIn(line1))
        self.wait(1)
        self.play(FadeIn(line2))
        self.wait(1)
        self.play(FadeIn(line3))
        self.wait(2)


class PhysicsScene(Scene):
    def construct(self):
        # Title
        title = Text("Physics", font="BM Hanna 11yrs Old").scale(1.6)
        title.to_edge(UP)

        # Content lines
        line1 = Text("빛은 입자이고 파동이다", font="BM Hanna 11yrs Old").scale(1)
        line2 = Text("물질은 에너지이다", font="BM Hanna 11yrs Old").scale(1)
        line3 = Text(
            "고양이는 죽어있고 살아있다 (중첩)", font="BM Hanna 11yrs Old"
        ).scale(1)
        line4 = Text(
            "수는 쪼개져있고 (quantum) 이어져있다 (continuous)",
            font="BM Hanna 11yrs Old",
        ).scale(1)

        lines = [line1, line2, line3, line4]

        # Position lines
        line1.shift(LEFT * 3 + UP * 1.5)
        for i in range(1, len(lines)):
            lines[i].next_to(lines[i - 1], DOWN, aligned_edge=LEFT, buff=0.2)

        # Final sentence
        final = Text(
            "물리적 세계는 이해하기 어려울정도로 이상하다.", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        final.next_to(line4, DOWN, aligned_edge=LEFT, buff=1.3)

        # Optional: image next to final sentence (e.g., 당황한 얼굴)
        face = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/confused_face2.png"
        ).scale(0.4)
        face.next_to(final, RIGHT)

        # Animate
        self.play(FadeIn(title))
        self.wait(1)

        for line in lines:
            self.play(FadeIn(line))
            self.wait(1)

        self.play(FadeIn(final))
        self.wait(0.5)
        self.play(FadeIn(face))
        self.wait(2)


class MathematicsScene(Scene):
    def construct(self):
        # Title
        title = Text("Mathematics", font="BM Hanna 11yrs Old").scale(1.6)
        title.to_edge(UP)

        # Line 1
        line1 = Text("0 은 있는 것의 그림자이다.", font="BM Hanna 11yrs Old").scale(1.2)

        # Line 2 (π만 Tex)
        line2 = Text(
            "random 은 불확실하지만, 이를 담는 그릇은 정해져있다",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)

        # Line 3
        line3 = Text(
            "무한한 것으로 유한한 것을 감쌀 수 없다.", font="BM Hanna 11yrs Old"
        ).scale(1.2)

        # Line 4 (강조)
        line4 = Text(
            "N, R 이 발견인것도 같고 발명인것도 같다", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        line4.set_color_by_text("발견", YELLOW)
        line4.set_color_by_text("발명", ORANGE)

        # Line positions (left aligned)
        line1.shift(LEFT * 3 + UP * 1.5)
        line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.2)
        line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.2)
        line4.next_to(line3, DOWN, aligned_edge=LEFT, buff=0.2)

        # Final two lines (centered + 강조)
        final1 = (
            Text("수학적 개념도, 이상하다.", font="BM Hanna 11yrs Old")
            .scale(1.3)
            .set_color(GREY_A)
        )
        final2 = (
            Text("상반되는 A 와 B 가 함께 존재한다.", font="BM Hanna 11yrs Old")
            .scale(1.3)
            .set_color(GREY_A)
        )
        # final
        final1.next_to(line4, DOWN, aligned_edge=LEFT, buff=1.3)
        final2.move_to(final1, aligned_edge=LEFT)

        face = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/confused_face2.png"
        ).scale(0.4)
        face.next_to(final2, RIGHT)

        # Animation
        self.play(FadeIn(title))
        self.wait(1)

        for line in [line1, line2, line3, line4]:
            self.play(FadeIn(line))
            self.wait(1)

        self.play(FadeIn(final1, run_time=1.5))

        self.play(ReplacementTransform(final1, final2))
        self.wait(0.5)
        self.play(FadeIn(face))

        self.wait(2)


class NegativeNegativeEueler(Scene):
    def construct(self):
        # Step 1: Show "-1 × -1" in the center
        question = Tex(r"-1 \times -1", font_size=96)
        self.play(FadeIn(question))
        self.wait(1)

        # Step 2: Move it up
        self.play(question.animate.shift(UP * 3))
        self.wait(0.5)

        euler_label = Text("Euler", font="BM Hanna 11yrs Old").scale(0.8)
        euler_label.set_color_by_text("Euler", GREY_A)

        euler_label.next_to(question, RIGHT * 4)
        self.play(FadeIn(euler_label))

        # Step 3: First explanation (Euler-like logic)
        step1 = Text(
            "-1 x -1 은 1 혹은 -1 일 수 있다", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        step2 = Text("하지만 -1 x 1 = -1 이다", font="BM Hanna 11yrs Old").scale(1.2)
        step3 = Text(
            "따라서 -1 x -1 은 -1 일 수 없다", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        step4 = (
            Text("결국, -1 x -1 = 1 이다", font="BM Hanna 11yrs Old")
            .scale(1.2)
            .set_color(YELLOW)
        )

        # Positioning steps under the question
        step1.next_to(question, DOWN, buff=1.0)
        step2.next_to(step1, DOWN, aligned_edge=LEFT, buff=0.5)
        step3.next_to(step2, DOWN, aligned_edge=LEFT, buff=0.5)
        step4.next_to(step3, DOWN, aligned_edge=LEFT, buff=0.7)

        # Animate explanation step-by-step
        self.play(FadeIn(step1))
        self.wait(1)
        self.play(FadeIn(step2))
        self.wait(1)
        self.play(FadeIn(step3))
        self.wait(1)
        self.play(FadeIn(step4))
        self.wait(2)


class DeriveNegative(Scene):
    def construct(self):
        # Step 1
        step1 = Tex(r"-1 \times (1 - 1) = -1 \times 1 + (-1) \times (-1)").scale(1.2)
        step1.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(step1))
        self.wait(1)

        # Step 2: copy full line and animate it appearing below
        step2 = step1.copy()
        step2.next_to(step1, DOWN, aligned_edge=LEFT, buff=0.6)
        # self.add(step2)  # <== important!
        self.play(TransformFromCopy(step1, step2))
        self.wait(0.5)

        # Step 2: replace (1 - 1) → 0
        new_lhs = (
            Tex(r"-1 \times 0 ")
            .scale(1.2)
            .move_to(
                step2[4:7],
            )
        )
        self.play(Transform(step2[0:8], new_lhs))
        self.wait(1)

        # Step 3: copy again
        step3 = step2.copy()
        step3.next_to(step2, DOWN, aligned_edge=LEFT, buff=0.6)
        # self.add(step3)
        self.play(TransformFromCopy(step2, step3))
        self.wait(0.5)

        # Step 3: replace whole LHS with just 0
        final_lhs = (
            Tex(r"0 ")
            .scale(1.2)
            .move_to(
                step3[6:7],
            )
        )
        self.play(Transform(step3[0:8], final_lhs))
        self.wait(1)

        # Step 4: copy again
        step4 = step3.copy()
        step4.next_to(step3, DOWN, aligned_edge=LEFT, buff=0.6)
        self.play(TransformFromCopy(step3, step4))
        self.wait(0.5)

        # Transform "-1 \times 1" to "-1"
        minus_one = Tex(r"-1 ").scale(1.2).move_to(step4[11:12])
        self.play(Transform(step4[9:13], minus_one))  # "-1 × 1" becomes "-1"
        self.wait(1)

        # Step 5: final form (-1) × (-1) = 1
        final_eq = Tex(r"(-1) \times (-1) = 1").scale(1.4).set_color(YELLOW)
        final_eq.next_to(step4, DOWN, aligned_edge=LEFT, buff=0.8)
        self.play(Write(final_eq))
        self.wait(2)


class MultiplyNegativeOneTwice(Scene):
    def construct(self):
        # --- Number plane
        plane = (
            NumberPlane(
                x_range=[-1, 1, 1],
                y_range=[-1, 1, 1],
                background_line_style={"stroke_opacity": 0.3},
            )
            .scale(3)
            .shift(RIGHT * 3)
        )
        self.add(plane)

        # --- Title label (shows × (-1) at each stage)
        # title = Tex(r"\times (-1)").scale(1.1).to_edge(UP)
        # self.play(FadeIn(title))

        # --- Step 1: base arrow from origin to +1
        origin = plane.c2p(0, 0)
        right = plane.c2p(1, 0)

        arrow = Arrow(origin, right, buff=0, fill_color=GREEN)
        self.play(GrowArrow(arrow))

        # --- Copy to right side (reference +1 arrow)
        base_copy = arrow.copy()
        base_copy.next_to(plane, LEFT, aligned_edge=LEFT).shift(LEFT * 3 + UP * 2)
        base_label = Tex("+1").scale(0.8).next_to(base_copy.get_end(), RIGHT)

        self.play(GrowArrow(base_copy), FadeIn(base_label))
        self.wait(1)

        # --- Step 2: Rotate origin arrow 180° (× -1)
        self.play(
            Rotate(arrow, angle=PI, about_point=origin),
            arrow.animate.set_fill(ORANGE),
            run_time=1,
        )

        # --- Copy downward with label -1
        arrow.set_fill(ORANGE)
        neg_arrow = arrow.copy()
        neg_arrow.next_to(base_copy, DOWN)
        label_minus1 = (
            Tex(r"1 \times (-1)").scale(0.8).next_to(neg_arrow.get_end(), LEFT)
        )

        self.play(
            GrowArrow(neg_arrow), FadeIn(label_minus1), arrow.animate.set_fill(GREEN)
        )
        arrow.set_fill(GREEN)

        self.wait(1)

        # --- Step 3: Show title × (-1) again

        # --- Rotate again (× -1)
        self.play(Rotate(arrow, angle=PI, about_point=origin), run_time=1)

        # --- Final: Copy downward with label (-1) × (-1) = 1
        pos_arrow = arrow.copy()
        pos_arrow.next_to(neg_arrow, DOWN)
        label_result = (
            Tex(r"(-1) \times (-1) = 1").scale(0.8).next_to(pos_arrow.get_end(), RIGHT)
        )

        self.play(GrowArrow(pos_arrow), FadeIn(label_result))
        self.wait(2)


class WhichExplanation(Scene):
    def construct(self):
        # Title
        title = Text("어느 설명이 맞는 것일까?", font="BM Hanna 11yrs Old").scale(1.5)
        title.shift(UP * 2.5)

        # Lines of thought
        line1 = Text("다 맞다고 볼 수도 있지 않나?", font="BM Hanna 11yrs Old").scale(
            1.2
        )
        line2 = Text("그럴듯한 story 가 있으니까", font="BM Hanna 11yrs Old").scale(1.2)
        line3 = (
            Text(
                "이해한다는 것은, story 를 만들어내는 것 아닐까",
                font="BM Hanna 11yrs Old",
            )
            .scale(1.2)
            .set_color(GREY_A)
        )

        # Align lines left under each other
        line1.shift(LEFT * 2.5 + UP)
        line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.5)
        line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.5)

        # Animation
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeIn(line1))
        self.wait(1)
        self.play(FadeIn(line2))
        self.wait(1.2)
        self.play(Write(line3), run_time=1.5)
        self.wait(2)


class EntropyBoxExpansion(Scene):
    def construct(self):
        radius = 0.08
        init_width = 3
        height = 4
        expanded_width = 5.5
        num_particles = 15

        # --- 왼쪽 박스
        box_left = Rectangle(width=init_width, height=height, color=WHITE)
        box_left.shift(LEFT * 4)

        # --- 오른쪽 박스 (처음엔 동일)
        box_right = Rectangle(width=init_width, height=height, color=WHITE)
        box_right.shift(RIGHT * 2)

        self.add(box_left, box_right)

        # --- 입자 생성 함수
        def create_particles(center_shift, box_width):
            particles = VGroup()
            velocities = []
            for _ in range(num_particles):
                x = random.uniform(-box_width / 2 + radius, box_width / 2 - radius)
                y = random.uniform(-height / 2 + radius, height / 2 - radius)
                pos = np.array([x, y, 0]) + center_shift
                dot = Dot(point=pos, radius=radius, color=YELLOW)
                particles.add(dot)
                vx = random.uniform(-0.05, 0.05)
                vy = random.uniform(-0.05, 0.05)
                velocities.append(np.array([vx, vy, 0]))
            return particles, velocities

        # 왼쪽 입자
        particles_left, vels_left = create_particles(LEFT * 4, init_width)
        self.add(particles_left)

        # 오른쪽 입자 (복사)
        particles_right, vels_right = create_particles(RIGHT * 2, init_width)
        self.add(particles_right)

        # --- 업데이트 함수
        def make_updater(velocities, center_shift, width):
            def updater(mob, dt):
                for i, dot in enumerate(mob):
                    dot.shift(velocities[i])
                    pos = dot.get_center() - center_shift

                    # Bounce X
                    if abs(pos[0]) > (width / 2 - radius):
                        velocities[i][0] *= -1
                        dot.shift(velocities[i])
                    # Bounce Y
                    if abs(pos[1]) > (height / 2 - radius):
                        velocities[i][1] *= -1
                        dot.shift(velocities[i])

            return updater

        particles_left.add_updater(make_updater(vels_left, LEFT * 4, init_width))
        particles_right.add_updater(make_updater(vels_right, RIGHT * 2, init_width))
        self.wait(2)

        # --- 오른쪽 박스 확장 애니메이션
        new_box_right = Rectangle(width=expanded_width, height=height, color=WHITE)
        new_box_right.shift(RIGHT * 2)

        self.play(Transform(box_right, new_box_right), run_time=5)

        self.wait(2)

        # 업데이트된 우측 입자 경계 반영
        particles_right.clear_updaters()
        particles_right.add_updater(make_updater(vels_right, RIGHT * 2, expanded_width))

        self.wait(4)


class ReversibleParticles(Scene):
    def construct(self):
        radius = 0.08
        box_width = 6
        box_height = 4
        num_particles = 15
        duration = 6  # seconds forward + reverse

        # --- 박스 경계
        boundary = Rectangle(width=box_width, height=box_height, color=WHITE)
        self.add(boundary)

        # --- 입자 생성
        particles = VGroup()
        velocities = []

        for _ in range(num_particles):
            x = random.uniform(-box_width / 2 + radius, box_width / 2 - radius)
            y = random.uniform(-box_height / 2 + radius, box_height / 2 - radius)
            dot = Dot(point=np.array([x, y, 0]), radius=radius, color=YELLOW)
            particles.add(dot)

            vx = random.uniform(-0.05, 0.05)
            vy = random.uniform(-0.05, 0.05)
            velocities.append(np.array([vx, vy, 0]))

        self.add(particles)

        original_velocities = velocities.copy()

        # --- 카메라 줌인 (한 입자 추적)
        tracked = particles[0]
        frame = self.camera.frame
        frame.save_state()
        self.play(frame.animate.scale(0.2).move_to(tracked.get_center()), run_time=2)
        # 추적용 updater 저장
        track_updater = lambda m: m.move_to(tracked.get_center())
        frame.add_updater(track_updater)

        # --- 입자 업데이트 함수 (전진)
        def forward_update(mob, dt):
            for i, dot in enumerate(mob):
                dot.shift(velocities[i])
                pos = dot.get_center()

                if abs(pos[0]) > (box_width / 2 - radius):
                    velocities[i][0] *= -1
                    dot.shift(velocities[i])
                if abs(pos[1]) > (box_height / 2 - radius):
                    velocities[i][1] *= -1
                    dot.shift(velocities[i])

        # --- Play icon (▶)
        play_icon = Text("▶", font="Arial").scale(1.5)
        play_icon.to_corner(DR).shift(LEFT * 0.3 + UP * 0.3)
        play_icon.fix_in_frame()
        self.play(FadeIn(play_icon))

        particles.add_updater(forward_update)
        self.wait(duration)

        # ...

        # 제거할 때
        frame.remove_updater(track_updater)

        # --- 멈추고 카메라 줌아웃
        particles.remove_updater(forward_update)
        self.play(Restore(frame), run_time=2)
        self.wait(0.5)

        # --- 되감기: 속도 반전
        for i in range(num_particles):
            velocities[i] = -original_velocities[i]

        def reverse_update(mob, dt):
            for i, dot in enumerate(mob):
                dot.shift(velocities[i])
                pos = dot.get_center()

                if abs(pos[0]) > (box_width / 2 - radius):
                    velocities[i][0] *= -1
                    dot.shift(velocities[i])
                if abs(pos[1]) > (box_height / 2 - radius):
                    velocities[i][1] *= -1
                    dot.shift(velocities[i])

        particles.remove_updater(forward_update)
        rewind_icon = Text("⏪", font="Arial").scale(1.5)
        rewind_icon.fix_in_frame()

        rewind_icon.move_to(play_icon)

        self.play(Transform(play_icon, rewind_icon))

        frame = self.camera.frame
        frame.save_state()
        self.play(frame.animate.scale(0.2).move_to(tracked.get_center()), run_time=2)
        # 추적용 updater 저장
        track_updater = lambda m: m.move_to(tracked.get_center())
        frame.add_updater(track_updater)

        particles.add_updater(reverse_update)
        self.wait(duration)
        particles.remove_updater(reverse_update)
        frame.remove_updater(track_updater)

        self.wait(1)
        self.play(Restore(frame), run_time=2)
        self.wait(0.5)


class StoryPerspectiveQuestion(Scene):
    def construct(self):

        # 문장 1
        line1 = Text(
            "입자의 스토리에는 (물리법칙)", font="BM Hanna 11yrs Old", color=WHITE
        ).scale(1.2)
        line1_2 = Text(
            "시간의 방향이 없다.", font="BM Hanna 11yrs Old", color=WHITE
        ).scale(1.2)

        # 문장 2
        line2 = Text(
            "공간을 바라봐야만 스토리에, 시간의 방향이 생긴다.",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)
        line2.set_fill(GREY)

        # 문장 3 (질문)
        line3 = Text(
            "그렇다면, 중요한 질문은,", font="BM Hanna 11yrs Old", color=WHITE
        ).scale(1.2)
        line3_2 = Text(
            "하나의 story 에서, 다른 스토리로", font="BM Hanna 11yrs Old", color=WHITE
        ).scale(1.2)
        line3_3 = Text(
            "어떻게 우리가 관점을 이동할 수 있는가 이다.",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)
        line3_3.set_color_by_text("관점을 이동", ORANGE)

        # 배치
        line1.move_to(UP * 2.5)
        line1_2.next_to(line1, DOWN, buff=0.3)
        line2.next_to(line1_2, DOWN, buff=0.7)
        line3.next_to(line2, DOWN, buff=1)
        line3_2.next_to(line3, DOWN, buff=0.3)
        line3_3.next_to(line3_2, DOWN, buff=0.3)

        # 애니메이션
        self.play(FadeIn(line1))
        self.play(FadeIn(line1_2))
        self.wait(1)

        self.play(FadeIn(line2))
        self.wait(1.5)

        self.play(FadeIn(line3))
        self.play(FadeIn(line3_2))
        self.play(FadeIn(line3_3))
        self.wait(2)


class ZenoStep2(Scene):
    def construct(self):
        # Define points
        title = Text(
            "Zeno 역설",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)
        title.shift(UP * 3)

        self.add(title)

        start = LEFT * 6 + UP * 0.7
        end = RIGHT * 5 + UP * 0.7

        # Generate key points by halving repeatedly
        halfway = (start + end) / 2
        quarter = (halfway + end) / 2
        eighth = (quarter + end) / 2
        sixteenth = (eighth + end) / 2
        t32 = (sixteenth + end) / 2

        up_s = UP * 1  # vertical offset for dog image

        # Draw line

        line = Line(start, end, color=YELLOW, stroke_width=7)
        bones = (
            ImageMobject("/Users/eugenekim/projects/dance-with/first-project/bones.png")
            .scale(0.3)
            .next_to(end, RIGHT)
        )

        self.play(FadeIn(line), FadeIn(bones))

        # Goal label and dog bones

        # Load transparent dog image
        character = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/dog-zeno.png"
        ).scale(0.3)
        character.set_opacity(0.8)  # make dog slightly transparent
        character.move_to(start + up_s)
        self.add(character)

        # Function to create step animation
        def do_step(start_pt, end_pt, label_text):
            line_seg = Line(start_pt, end_pt)
            brace = Brace(line_seg, DOWN)
            label = brace.get_text(label_text)
            self.play(GrowFromCenter(brace), Write(label))
            self.play(character.animate.move_to(end_pt + up_s), run_time=1)
            self.wait(0.3)

        # Do four steps: 1/2, 1/4, 1/8, 1/16
        do_step(start, halfway, "1/2")
        do_step(halfway, quarter, "1/4")
        do_step(quarter, eighth, "1/8")
        do_step(eighth, sixteenth, "1/16")
        do_step(sixteenth, t32, "...")

        # Add "..." to imply infinity
        # dots = Text("...", font_size=60).move_to((sixteenth + end) / 2 )
        # self.play(FadeIn(dots))
        self.wait(1.5)

        t1 = Text(
            "이동하는 입장이 아니라 밖에서 바라보면",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)
        t1.shift(DOWN)
        self.play(Write(t1))

        self.wait(2)

        t2 = Text(
            "몇번을 가든, 시간도 그만큼 잘게 쪼개 보겠다는 것이다",
            font="BM Hanna 11yrs Old",
        ).scale(1)
        t2.set_fill(GREY)

        t2.next_to(t1, DOWN * 1.3)

        self.play(Write(t2))
        self.wait(1)

        t3 = Text(
            "몇번을 쪼개서 보든, 전체 시간은 정해져 있다",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)

        t3.next_to(t2, DOWN * 1.3)
        t3.set_color_by_text("전체 시간", BLUE)

        self.play(Write(t3))
        self.wait(1)


class Scene01_MathAndPhysicsSplit(Scene):

    def construct(self):
        math_b = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/math_f.png"
        ).scale(1.2)

        math_b.shift(LEFT * 3 + DOWN * 0.5)

        self.play(FadeIn(math_b))

        physics_b = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/physics_f.png"
        ).scale(1.2)

        physics_b.shift(RIGHT * 3 + DOWN * 0.5)

        self.play(FadeIn(physics_b))

        t1 = Text(
            "수학",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)

        t1.next_to(math_b, UP)

        self.play(Write(t1))

        t2 = Text(
            "물리",
            font="BM Hanna 11yrs Old",
        ).scale(1.5)

        t2.next_to(physics_b, UP)

        self.play(Write(t2))


class CircleNetwork(Scene):
    def construct(self):
        # Parameters
        num_outer = 20
        num_inner = 30
        radius = 3
        jitter_amount = 0.002
        connection_threshold = 2.0

        # Circle base
        circle = Circle(radius=radius, color=GREY)
        self.add(circle)

        # Dot positions
        outer_dots = []
        inner_dots = []

        for i in range(num_outer):
            angle = 1 * i
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            dot = Dot(point=np.array([x, y, 0]), radius=0.07, color=BLUE)
            outer_dots.append(dot)

        for _ in range(num_inner):
            angle = random.uniform(0, 2 * PI)
            r = random.uniform(0, radius)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            dot = Dot(point=np.array([x, y, 0]), radius=0.07, color=GREEN)
            inner_dots.append(dot)

        all_dots = outer_dots + inner_dots
        self.add(*all_dots)

        # Connect close dots
        # Connect all pairs (complete graph)
        lines = VGroup()
        dot_pairs = []

        for i in range(len(all_dots)):
            for j in range(i + 1, len(all_dots)):
                p1 = all_dots[i].get_center()
                p2 = all_dots[j].get_center()
                line = Line(p1, p2, stroke_opacity=0.1)
                lines.add(line)
                dot_pairs.append((i, j))  # Store the pair for updates

        self.add(lines)

        # --- Jitter animation
        def jitter_update(mobj, dt):

            for i, dot in enumerate(all_dots):
                if i < num_outer:
                    # Move slightly along tangent (circular motion)
                    pos = dot.get_center()
                    angle = math.atan2(pos[1], pos[0])
                    delta_angle = random.uniform(-0.002, 0.002)
                    new_angle = angle + delta_angle
                    new_x = radius * math.cos(new_angle)
                    new_y = radius * math.sin(new_angle)
                    dot.move_to([new_x, new_y, 0])
                else:
                    shift_x = random.uniform(-jitter_amount, jitter_amount)
                    shift_y = random.uniform(-jitter_amount, jitter_amount)
                    dot.shift([shift_x, shift_y, 0])

            # Update line positions (using dot_pairs list)
            for k, (i, j) in enumerate(dot_pairs):
                lines[k].put_start_and_end_on(
                    all_dots[i].get_center(), all_dots[j].get_center()
                )

        tracker = ValueTracker(0)

        # Dummy mobject just to use add_updater
        dummy = VectorizedPoint()
        dummy.add_updater(lambda m, dt: tracker.increment_value(dt))
        self.add(dummy)

        dummy.add_updater(jitter_update)
        self.wait(6)
        dummy.remove_updater(jitter_update)


class SiddharthaScene(Scene):
    def construct(self):

        def make_wave_curve():
            # Simple sinusoidal wave line
            points = []
            for x in np.linspace(-7, 7, 200):
                y = 0.2 * math.sin(x * 2)
                points.append(np.array([x, y, 0]))

            return VMobject().set_points_as_corners(points)

        # --- 명언 본문
        quote = (
            Text("강은 어디에나 동시에 존재한다.", font="BM Hanna 11yrs Old")
            .scale(1.4)
            .set_color(BLUE_A)
        )

        # --- 물결형 라인 (곡선 흐름 애니메이션)
        wave = make_wave_curve()
        wave.set_color(BLUE_D).set_opacity(0.5)
        wave.shift(DOWN * 2)

        # --- 애니메이션
        self.add(quote)

        self.add(wave)
        self.play(wave.animate.shift(LEFT * 1), run_time=10, rate_func=linear)

        self.wait(3)


class SurvivalOfFittest(Scene):
    def construct(self):

        # 생명체 점 10개 생성
        num = 15
        dots = VGroup()
        for _ in range(num):
            x = random.uniform(-5, 5)
            y = random.uniform(-2.5, 2.5)
            dot = Dot(point=[x, y, 0], color=BLUE, radius=0.15)
            dots.add(dot)

        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait(1)

        # 하나씩 제거 (생존 경쟁)

        for i in range(num - 1):
            if i < num - 5:  # First phase: speed up
                t = i / (num - 6)  # normalize to [0, 1]
                speed = interpolate(0.6, 0.2, t)
            else:  # Second phase: slow down
                t = (i - (num - 5)) / 4  # normalize last 4 steps
                speed = interpolate(0.2, 0.6, t)

            self.play(FadeOut(dots[i]), run_time=speed)
        # 마지막 남은 하나 강조
        survivor = dots[-1]
        self.play(survivor.animate.set_color(RED).scale(1.6))
        self.wait(0.5)

        self.wait(2)


class PrisonerDilemmaWithHighlight(Scene):
    def construct(self):
        cell_size = 2

        # Grid base: 2x2 payoff matrix
        grid = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size)
                cell.move_to(RIGHT * (j * cell_size) + DOWN * (i * cell_size))
                grid.add(cell)
        grid.move_to(ORIGIN)
        self.add(grid)

        # Diagonal lines in each cell
        for i in range(2):
            for j in range(2):
                start = grid[i * 2 + j].get_corner(UL)
                end = grid[i * 2 + j].get_corner(DR)
                line = Line(start, end, stroke_opacity=0.4)
                self.add(line)

        # Payoff labels
        payoffs = [
            ("5", "5"),
            ("1", "10"),
            ("10", "1"),
            ("2", "2"),
        ]
        a_texts = []
        b_texts = []

        for idx, (a, b) in enumerate(payoffs):
            cell = grid[idx]
            a_text = Text(a, fill_color=YELLOW).scale(1)
            b_text = Text(b, fill_color=GREEN).scale(1)
            a_text.next_to(cell.get_corner(DL), direction=UP + RIGHT, buff=0.2)
            b_text.next_to(cell.get_corner(UR), direction=DOWN + LEFT, buff=0.2)
            a_texts.append(a_text)
            b_texts.append(b_text)
            self.add(a_text, b_text)

        # Titles and actions
        a_title = Text("죄수 A", fill_color=YELLOW, font="BM Hanna 11yrs Old").scale(
            1.1
        )
        a_actions = (
            VGroup(
                Text("배신", font="BM Hanna 11yrs Old"),
                Text("협력", font="BM Hanna 11yrs Old"),
            )
            .arrange(DOWN, buff=1)
            .next_to(grid, LEFT)
        )
        self.add(a_title.next_to(a_actions, LEFT), a_actions)

        b_title = Text("죄수 B", fill_color=GREEN, font="BM Hanna 11yrs Old").scale(1.1)
        b_actions = (
            VGroup(
                Text("배신", font="BM Hanna 11yrs Old"),
                Text("협력", font="BM Hanna 11yrs Old"),
            )
            .arrange(RIGHT, buff=2)
            .next_to(grid, UP)
        )
        self.add(b_title.next_to(b_actions, UP * 1.5), b_actions)

        # --- Add highlight rectangles for rows and columns ---
        row_highlights = [
            Rectangle(
                width=4, height=2, fill_color=BLACK, fill_opacity=0, stroke_opacity=0
            ).move_to(grid[0].get_center() + RIGHT * cell_size / 2),
            Rectangle(
                width=4, height=2, fill_color=BLACK, fill_opacity=0, stroke_opacity=0
            ).move_to(grid[2].get_center() + RIGHT * cell_size / 2),
        ]
        col_highlights = [
            Rectangle(
                width=2, height=4, fill_color=BLACK, fill_opacity=0, stroke_opacity=0
            ).move_to(grid[0].get_center() + DOWN * cell_size / 2),
            Rectangle(
                width=2, height=4, fill_color=BLACK, fill_opacity=0, stroke_opacity=0
            ).move_to(grid[1].get_center() + DOWN * cell_size / 2),
        ]

        self.add(*row_highlights, *col_highlights)

        # --- Player B's best response animation

        # Case 1: A 배신 — dim other row (row 1), highlight payoff on row 0
        self.wait(1)
        self.play(row_highlights[1].animate.set_fill(opacity=0.7))
        highlight_b0 = SurroundingRectangle(b_texts[0], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b0))
        self.wait(1)
        self.play(FadeOut(highlight_b0), row_highlights[1].animate.set_fill(opacity=0))

        # Case 2: A 협력 — dim other row (row 0), highlight payoff on row 1
        self.wait(1)
        self.play(row_highlights[0].animate.set_fill(opacity=0.7))
        highlight_b3 = SurroundingRectangle(b_texts[2], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b3))
        self.wait(1)
        self.play(FadeOut(highlight_b3), row_highlights[0].animate.set_fill(opacity=0))

        highlight_b = SurroundingRectangle(b_actions[0], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b))

        # --- Player A's best response animation

        # Case 1: B 배신 — dim other col (col 1), highlight payoff on col 0
        self.wait(1)
        self.play(col_highlights[1].animate.set_fill(opacity=0.7))
        highlight_a0 = SurroundingRectangle(a_texts[0], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a0))
        self.wait(1)
        self.play(FadeOut(highlight_a0), col_highlights[1].animate.set_fill(opacity=0))

        # Case 2: B 협력 — dim other col (col 0), highlight payoff on col 1
        self.wait(1)
        self.play(col_highlights[0].animate.set_fill(opacity=0.7))
        highlight_a3 = SurroundingRectangle(a_texts[1], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a3))
        self.wait(1)
        self.play(FadeOut(highlight_a3), col_highlights[0].animate.set_fill(opacity=0))

        highlight_a = SurroundingRectangle(a_actions[0], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a))

        self.wait(2)

        eq = SurroundingRectangle(grid[0], color=RED, buff=0)
        self.play(FadeIn(eq))

        self.wait(1)

        opt = SurroundingRectangle(grid[3], color=BLUE, buff=0)
        self.play(FadeIn(opt))

        self.wait(2)

        # self.play(grid.animate.set_opacity(0.2))

        for m in self.mobjects:
            m.set_opacity(0.1)

        eq = Tex(r"1 + 1 = -1").scale(2)
        self.play(Write(eq))
        self.wait(2)


class DilemmaTopics(Scene):
    def construct(self):
        # Title
        title = Tex(r"1 + 1 = -1").scale(1.5)

        title[4:7].set_color(RED)

        title.to_edge(UP)
        self.play(FadeIn(title))

        # List of examples
        items = [
            "1. 기후위기",
            "2. 환경오염",
            "3. 핵",
            "4. AI",
            "5. 마케팅 / 정치 / 뉴스 / sns",
            "6. 비만 / 사교육 / 금융",
            "7. ...",
        ]

        text_lines = VGroup()
        for i, item in enumerate(items):
            line = Text(item, font="BM Hanna 11yrs Old").scale(1.1)
            if i % 2 == 1:
                line.set_fill(GREY_C)
            text_lines.add(line)

        text_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        text_lines.next_to(title, DOWN * 2, aligned_edge=LEFT).shift(LEFT)

        # Animate each line appearing
        for line in text_lines:
            self.play(Write(line), run_time=0.5)

        self.wait(2)

        # 기존 텍스트들 왼쪽으로 밀고 흐리게
        self.play(
            text_lines.animate.to_edge(LEFT, buff=0.5).set_opacity(0.5), run_time=1
        )

        # 새 문장들
        quotes = [
            "문제를 예방하는 건 돈이 안되고",
            "문제를 만들면, 누군가 해결하면서 돈이 되곤 한다.",
            "문제가 커질때까지는 대응을 못한다.",
        ]

        quote_texts = VGroup()
        for i, q in enumerate(quotes):
            quote = Text(q, font="BM Hanna 11yrs Old").scale(1.0)
            if i == 1:
                quote.set_color(GREY_B)  # 강조 색상

            if i == 2:
                quote.set_color(YELLOW_E)  # 강조 색상
            quote_texts.add(quote)

        # 기존 텍스트 기준으로 오른쪽에 정렬
        quote_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        # quote_texts.next_to(text_lines, RIGHT, buff=1)
        quote_texts.shift(UP + RIGHT * 2)

        for qt in quote_texts:
            self.play(FadeIn(qt), run_time=2)

        self.wait(2)


class FinalScene(Scene):
    def construct(self):
        import math

        # 👾 1. Function to generate wave points with a phase shift
        def generate_wave_points(phase=0):
            points = []
            for x in np.linspace(-7, 7, 200):
                y = 0.2 * math.sin(2 * x + phase)
                points.append(np.array([x, y, 0]))
            return points

        # 👾 2. Create the wave VMobject
        wave = VMobject()
        wave.set_points_as_corners(generate_wave_points())
        wave.set_color(BLUE_D).set_opacity(0.5).shift(DOWN * 1.5)

        # 👾 3. Phase tracker
        phase = ValueTracker(0)

        # 👾 4. Updater for the wave
        def update_wave(mob):
            mob.set_points_as_corners(generate_wave_points(phase.get_value()))

        wave.add_updater(update_wave)

        # 🧠 5. Text animations
        # text1 = Text("Don't look up", font="BM Hanna 11yrs Old").scale(1.2).move_to(UP * 2)
        # text2 = Text("Don't add up", font="BM Hanna 11yrs Old").scale(1.2).move_to(text1)
        text3 = Tex("1 + 1 = -1").scale(1.5)
        text3.shift(UP * 1.5)

        # self.play(FadeIn(text1, run_time=2))
        # self.wait(1.5)
        # self.play(ReplacementTransform(text1, text2),FadeIn(text3))

        self.play(Write(text3))

        self.wait(1)

        # self.play(FadeOut(text2))

        # Add wave and phase tracker to scene
        self.add(wave)
        self.add(phase)  # ⬅️ This makes phase update with dt
        phase.add_updater(lambda m, dt: m.increment_value(2 * dt))

        self.wait(2)
        # Let wave move while we show final text
        final_text = Tex("1 + 1 = 2").scale(1.5).shift(DOWN * 1.5)
        self.play(Write(final_text), run_time=2)

        self.wait(9)

        # Cleanup
        wave.remove_updater(update_wave)
        phase.clear_updaters()

        self.wait(1)


class GabrielHorn(ThreeDScene):
    def construct(self):
        eq = Tex(r"y = \frac{1}{x}").scale(1.2)
        eq.shift(UP * 2.5)
        eq.fix_in_frame()
        self.play(Write(eq))

        # === 1. Axes ===
        axes = ThreeDAxes(
            x_range=[0, 16, 2],
            y_range=[-1, 2, 0.5],
            z_range=[-2, 2, 0.5],
        )
        self.add(axes)

        class Graph1OverX(VMobject):
            def __init__(self, axes, x_min=1, x_max=15, **kwargs):
                super().__init__(**kwargs)
                points = []
                for x in np.linspace(x_min, x_max, 200):
                    point = axes.c2p(x, 0, 1 / x)
                    points.append(point)
                self.set_points_as_corners(points)

        # Optional: label 2D curve
        # label = Text("y = 1/x", font_size=32)
        # label.move_to(axes.c2p(4, 0.6, 0) + 0.5 * UP)
        # self.add(label)

        # === 2. Camera Setup ===
        frame = self.camera.frame

        frame.set_euler_angles(
            theta=0, phi=PI / 2.5
        )  # φ = π/2.5 ≈ 72° (slightly tilted)
        frame.move_to(axes.c2p(6, 0, 0))  # center on curve

        # === 3. 2D Curve y = 1/x from x = 1 to 15 ===
        curve = Graph1OverX(axes)
        curve.set_color(YELLOW)

        self.play(ShowCreation(curve), run_time=2)
        self.wait(0.5)

        # === 4. Rotate camera for 3D view ===
        # self.play(
        #     frame.animate.set_euler_angles(theta=-PI/4, phi=PI/6).move_to(axes.c2p(6, 0, 0)),
        #     run_time=2
        # )

        # === 5. Animate surface sweep (rotation) ===
        sweep = ValueTracker(0)

        def get_rotating_surface():
            return (
                ParametricSurface(
                    lambda u, v: axes.c2p(
                        u, (1 / u) * np.cos(v + PI / 2), (1 / u) * np.sin(v + PI / 2)
                    ),
                    u_range=[1, 15],
                    v_range=[0, sweep.get_value()],
                    resolution=(60, 20),
                )
                .set_color(BLUE_A)
                .set_opacity(0.6)
            )

        rotating_horn = always_redraw(get_rotating_surface)

        self.add(rotating_horn)

        self.play(sweep.animate.set_value(TAU), run_time=1)
        self.remove(rotating_horn)

        # === 6. Add full horn after rotation completes ===
        full_horn = ParametricSurface(
            lambda u, v: axes.c2p(u, (1 / u) * np.cos(v), (1 / u) * np.sin(v)),
            u_range=[1, 15],
            v_range=[0, TAU],
            resolution=(100, 30),
        )
        full_horn.set_color(BLUE_A)
        full_horn.set_opacity(0.7)

        self.add(full_horn)
        self.play(Restore(self.camera.frame))

        self.wait(1)

        # for m in self.mobjects:
        #     self.remove(m)

        self.play(FadeOut(curve), FadeOut(axes))

        # Axes

        max_x = 15
        axes = ThreeDAxes(
            x_range=[0, max_x, 1],
            y_range=[-1.5, 1.5, 0.5],
            z_range=[-1.5, 1.5, 0.5],
        )
        axes.shift(LEFT)
        # axes.add_coordinate_labels()

        # self.add(axes)

        # Horn surface using .c2p()
        horn = ParametricSurface(
            lambda u, v: axes.c2p(u, (1 / u) * np.cos(v), (1 / u) * np.sin(v)),
            u_range=[1, max_x + 2],
            v_range=[0, TAU],
            resolution=(100, 30),
        )
        horn.set_color(BLUE_A)
        horn.set_opacity(0.7)
        self.play(ReplacementTransform(full_horn, horn), run_time=1.5)
        # self.add(horn)

        # Camera setup
        frame = self.camera.frame
        frame.move_to(axes.c2p(2, 0, 0))  # move camera focus near horn base

        frame.save_state()

        self.play(
            frame.animate.set_euler_angles(theta=-PI / 6, gamma=PI / 2), run_time=1
        )
        # frame.set_euler_angles(theta=-PI / 6, gamma=PI / 2)

        self.camera.light_source.move_to([-10, -10, 20])

        # Fill the horn with solid disks
        num_disks = 100
        height = max_x / num_disks  # to fill x from 1 to 10
        disks = Group()

        # new_eq = Text("부피",font="BM Hanna 11yrs Old").scale(1.2)
        new_eq = Tex(r"\text{volume} = \pi").scale(1.2)
        new_eq.fix_in_frame()
        new_eq.move_to(eq.get_center())  # or wherever you want

        self.play(ReplacementTransform(eq, new_eq), run_time=1)

        # Start filling
        for i in reversed(range(num_disks)):
            u = 1 + i * height
            r = 1 / u
            center = axes.c2p(u, 0, 0)
            scene_hvec = 0.5 * height * RIGHT

            # Make the disk cap
            bottom = Circle(radius=r)
            bottom.rotate(PI / 2, axis=UP)
            bottom.move_to(center)
            bottom.set_color(BLUE_C)
            bottom.set_opacity(0.8)

            disks.add(bottom)

            # Add the disk after droplet
            # self.add(bottom)

            # Slightly rotate the horn each time

        # Animate fill
        visible_disks = Group()
        self.add(visible_disks)

        previous_i = 0
        for i in range(45, num_disks + 1, 3):
            if i > num_disks - 3:
                i = num_disks
            new_disks = Group(*disks[previous_i:i])
            self.add(new_disks)

            # Droplet
            droplet = Sphere(radius=0.15, resolution=(16, 16))
            droplet.set_color(BLUE_D)
            start_point = axes.c2p(-1, 0, 0)
            end_point = axes.c2p(1.5, 0, 0)
            droplet.move_to(start_point)
            self.add(droplet)

            self.play(
                droplet.animate.move_to(end_point), run_time=0.3, rate_func=linear
            )
            self.remove(droplet)

        # horn.set_color(BLUE_A)

        self.wait(2)
        self.play(Restore(self.camera.frame))

        # new_eq2 = Text("표면적",font="BM Hanna 11yrs Old").scale(1.2)
        new_eq2 = Tex(r"\text{area} = \infty").scale(1.2)

        new_eq2.fix_in_frame()
        new_eq2.move_to(eq.get_center())  # or wherever you want

        self.play(ReplacementTransform(new_eq, new_eq2), run_time=1)

        self.wait(1)

        self.play(FadeOut(disks))
        self.wait(1)

        num_rings = 100
        ring_width = max_x / num_rings  # from x = 1 to 10

        for i in range(num_rings):
            u_min = 1 + i * ring_width
            u_max = u_min + ring_width

            ring = ParametricSurface(
                lambda u, v: axes.c2p(
                    u, (1 / u) * np.cos(v) * 1.01, (1 / u) * np.sin(v) * 1.01
                ),
                u_range=[u_min, u_max],
                v_range=[0, TAU],
                resolution=(10, 30),
            )
            ring.set_color(ORANGE)
            ring.set_opacity(0.6)

            self.add(ring)
            self.wait(0.03)

        self.wait(1)


class NormalCurveScene(ThreeDScene):
    def construct(self):

        plane_g = VGroup()

        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[0, 1, 1],
            faded_line_ratio=2,
            background_line_style={"stroke_opacity": 0.3},
        ).scale(1.8)
        # plane.add_coordinate_labels()

        self.play(FadeIn(plane))
        self.wait()

        plane_g.add(plane)

        # === 2. Normal distribution function ===
        mu = 0
        sigma = 0.5

        def normal_pdf(x):
            return (1 / (sigma * np.sqrt(2 * PI))) * np.exp(
                -((x - mu) ** 2) / (2 * sigma**2)
            )

        # Partial curve (will grow outward from center)
        full_curve = VMobject()
        full_curve.set_color(BLUE)
        points = []

        for x in np.linspace(0, 3, 200):
            y = normal_pdf(x)
            points.append(plane.c2p(x, y))
        for x in np.linspace(-3, 0, 200):
            y = normal_pdf(x)
            points.insert(0, plane.c2p(x, y))

        full_curve.set_points_smoothly(points)

        # Draw the curve symmetrically
        curve_left = VMobject(color=BLUE)
        curve_right = VMobject(color=BLUE)

        curve_left.set_points_smoothly(points[:200])
        curve_right.set_points_smoothly(points[200:])

        self.play(ShowCreation(curve_right), ShowCreation(curve_left), run_time=2)

        self.wait()

        plane_g.add(curve_left, curve_right)

        # === 3. Shading under the curve ===
        def get_area(x_min, x_max):
            resolution = 50
            xs = np.linspace(x_min, x_max, resolution)
            verts = [plane.c2p(x, normal_pdf(x)) for x in xs]
            verts += [plane.c2p(x_max, 0), plane.c2p(x_min, 0)]
            area = Polygon(*verts)
            area.set_fill(BLUE_E, opacity=0.4)
            area.set_stroke(width=0)
            # plane_g.add(area)
            return area

        # Animate area shading from center outward

        prev_i = 0
        areas_g = VGroup()
        for i in np.linspace(0, 2, 40):
            area_left = get_area(-i, prev_i)
            area_right = get_area(prev_i, i)
            areas_g.add(area_left, area_right)
            self.play(FadeIn(area_right), FadeIn(area_left), run_time=0.1)
            prev_i = i

        plane.get_x_axis().set_stroke(BLUE)

        t1 = Tex(r"\text{area} = 1").scale(1.2)
        t1.shift(UP * 2.5)
        t1.fix_in_frame()
        self.play(Write(t1))

        self.wait(1)
        plane_g.add(areas_g)
        # self.play(FadeOut(areas_g))

        self.play(
            plane_g.animate.rotate(
                angle=PI / 6,  # rotation angle
                axis=UP,  # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
                about_point=plane.c2p(0, 0, 0),  # pivot point
            )
        )

        new_eq = Tex(r"\text{length = ?}").scale(1.2)
        new_eq.fix_in_frame()
        new_eq.move_to(t1.get_center())  # or wherever you want
        self.play(ReplacementTransform(t1, new_eq), run_time=1)

        line_length = 10
        num_segments = 50
        segment_length = line_length / num_segments

        # Create segments with gradient color
        segments = VGroup()

        for i in range(num_segments):
            start_x = i * segment_length
            end_x = (i + 1) * segment_length
            line = Line(
                plane.c2p(start_x, 0),
                plane.c2p(end_x, 0),
                stroke_width=6,
                color=interpolate_color(ORANGE, BLACK, i / num_segments),
            )
            segments.add(line)
            plane_g.add(segments)

            self.play(FadeIn(line, run_time=0.1))

        new_eq2 = Tex(r"\text{length} = \infty").scale(1.2)
        new_eq2.fix_in_frame()
        new_eq2.move_to(new_eq.get_center())  # or wherever you want
        self.play(ReplacementTransform(new_eq, new_eq2), run_time=1)

        self.wait(2)


class StickManWalkScene(ThreeDScene):
    def construct(self):

        class StickMan(VGroup):
            def __init__(
                self,
                axes: ThreeDAxes,
                radius=0.3,
                height=1.2,
                leg_length=0.5,
                color=WHITE,
                **kwargs,
            ):
                super().__init__(**kwargs)
                self.axes = axes
                self.facing_right = True
                self.rotation_angle = 0

                # Build stickman upright in axes coordinates

                self.unit_x = axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)
                self.unit_y = axes.c2p(0, 1, 0) - axes.c2p(0, 0, 0)
                self.unit_z = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)

                self.up = up = self.unit_y
                self.down = down = -self.unit_y
                self.left = left = -self.unit_z
                self.right = right = -left

                self.body_top = ORIGIN + up * (height / 2)
                self.body_bottom = ORIGIN + down * (height / 2)

                self.head = Circle(radius=radius, color=color)
                self.head.shift(self.body_top + up * radius)

                self.body = Line(self.body_top, self.body_bottom, color=color)

                self.left_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + down * leg_length + left * leg_length * 0.5,
                    color=color,
                )
                self.right_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + down * leg_length + right * leg_length * 0.5,
                    color=color,
                )

                self.add(self.head, self.body, self.left_leg, self.right_leg)

            def get_body_bottom(self):
                return self.body.get_end()

            def move_to_feet(self, point):
                shift = np.array(point) - self.get_body_bottom()
                self.shift(shift)

            def face_point(self, point):
                my_x = self.axes.p2c(self.get_center())[0]
                target_x = self.axes.p2c(point)[0]
                should_face_right = target_x >= my_x

                if self.facing_right != should_face_right:
                    self.rotate(
                        PI,
                        axis=self.axes.y_axis.get_vector(),
                        about_point=self.get_body_bottom(),
                    )
                    self.facing_right = should_face_right

            def walk_to(self, scene, point, duration=2):
                start = self.get_body_bottom()
                end = self.axes.c2p(*point)

                self.face_point(end)

                up = self.up
                down = self.down
                left = self.left
                right = self.right

                bounce = lambda t: 0.05 * np.sin(8 * PI * t)
                swing_angle = lambda t: 0.4 * np.sin(8 * PI * t)

                dummy = VMobject()

                def update_mob(mob, alpha):
                    foot_pos = interpolate(start, end, alpha)
                    bounce_offset = bounce(alpha) * up

                    lean_dir = 1 if self.facing_right else -1
                    lean_angle = lean_dir * interpolate(0, -PI / 16, np.sin(PI * alpha))

                    self.move_to(foot_pos + up * 0.6 + bounce_offset)
                    self.rotate(
                        lean_angle - self.rotation_angle,
                        axis=self.axes.z_axis.get_vector(),
                        about_point=self.get_body_bottom(),
                    )
                    self.rotation_angle = lean_angle

                    body_bottom = self.get_body_bottom()

                    leg_len = 0.5
                    horiz = 0.25

                    self.left_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + down * leg_len + left * horiz,
                            color=self.left_leg.get_color(),
                        )
                    )
                    self.right_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + down * leg_len + right * horiz,
                            color=self.right_leg.get_color(),
                        )
                    )
                    self.left_leg.rotate(swing_angle(alpha), about_point=body_bottom)
                    self.right_leg.rotate(-swing_angle(alpha), about_point=body_bottom)

                scene.play(
                    UpdateFromAlphaFunc(dummy, update_mob),
                    run_time=duration,
                    rate_func=linear,
                )

        axes = ThreeDAxes(
            x_range=[-7, 9, 1],
            y_range=[-2, 5, 0.5],
            z_range=[-10, 8, 0.5],
        )

        axes.x_axis.set_color(GREY_A)
        axes.y_axis.set_color(GREY_A)
        axes.z_axis.set_color(GREY_A)
        axes.x_axis.set_opacity(0.4)
        axes.y_axis.set_opacity(0.4)
        axes.z_axis.set_opacity(0.4)

        self.add(axes)

        axes.rotate(
            angle=PI / 6,
            axis=UP,
            about_point=axes.c2p(0, 0, 0),
        )

        axes.rotate(
            angle=PI / 12,  # rotation angle
            axis=RIGHT,  # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
            about_point=axes.c2p(0, 0, 0),  # pivot point
        )

        man = StickMan(axes)
        man.move_to_feet(axes.c2p(10, 0, -10))
        self.add(man)

        frame = self.camera.frame
        frame.save_state()

        # frame.set_euler_angles(
        #     theta=0, phi=PI / 12, gamma=0
        # )  # φ = π/2.5 ≈ 72° (slightly tilted)

        man.walk_to(self, point=(6, 0, 5), duration=2)
        self.wait(0.1)

        # Walk left
        man.walk_to(self, point=(-3, 0, 0), duration=2)
        self.wait(0.1)

        man.walk_to(self, point=(5, 0, -5), duration=2)
        self.wait(2)

        # Animate in-between grid lines

        # Add bounding box

        bounding_lines = VGroup(
            Line(axes.c2p(-7, -2, -10), axes.c2p(9, -2, -10)),
            Line(axes.c2p(9, -2, -10), axes.c2p(9, 5, -10)),
            Line(axes.c2p(9, 5, -10), axes.c2p(-7, 5, -10)),
            Line(axes.c2p(-7, 5, -10), axes.c2p(-7, -2, -10)),
            Line(axes.c2p(-7, -2, 8), axes.c2p(9, -2, 8)),
            Line(axes.c2p(9, -2, 8), axes.c2p(9, 5, 8)),
            Line(axes.c2p(9, 5, 8), axes.c2p(-7, 5, 8)),
            Line(axes.c2p(-7, 5, 8), axes.c2p(-7, -2, 8)),
            Line(axes.c2p(-7, -2, -10), axes.c2p(-7, -2, 8)),
            Line(axes.c2p(9, -2, -10), axes.c2p(9, -2, 8)),
            Line(axes.c2p(9, 5, -10), axes.c2p(9, 5, 8)),
            Line(axes.c2p(-7, 5, -10), axes.c2p(-7, 5, 8)),
        )
        bounding_lines.set_stroke(opacity=0.7, color=WHITE)
        self.play(FadeIn(bounding_lines))

        self.wait(1)

        world_g = VGroup()
        world_g.add(axes, man, bounding_lines)

        world_g_up = world_g.copy()
        shift_up = axes.c2p(0, 7.5, 0) - axes.c2p(0, 0, 0)
        world_g_up.shift(shift_up)
        self.play(Write(world_g_up))

        world_g_down = world_g.copy()
        shift_down = axes.c2p(0, 0, 0) - axes.c2p(0, 7.5, 0)
        world_g_down.shift(shift_down)
        self.play(Write(world_g_down), run_time=0.5)

        world_g_x1 = world_g.copy()
        shift_x1 = axes.c2p(0, 0, 0) - axes.c2p(16.5, 0, 0)
        world_g_x1.shift(shift_x1)
        self.play(Write(world_g_x1), run_time=0.5)

        world_g_x2 = world_g.copy()
        shift_x2 = axes.c2p(16.5, 0, 0) - axes.c2p(0, 0, 0)
        world_g_x2.shift(shift_x2)
        self.play(Write(world_g_x2), run_time=0.5)

        world_g_z1 = world_g.copy()
        shift_z1 = axes.c2p(0, 0, 0) - axes.c2p(0, 0, 18.5)
        world_g_z1.shift(shift_z1)
        self.play(Write(world_g_z1), run_time=0.5)

        world_g_z2 = world_g.copy()
        shift_z2 = axes.c2p(0, 0, 18.5) - axes.c2p(0, 0, 0)
        world_g_z2.shift(shift_z2)
        self.play(Write(world_g_z2), run_time=0.5)

        self.wait(1)
