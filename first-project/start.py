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
        #     run_time=move_time*2,
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
        sheep1 = ImageMobject(sheep_path).scale(0.8).shift(LEFT * 2)
        sheep2 = ImageMobject(sheep_path).scale(0.8)
        sheep3 = ImageMobject(sheep_path).scale(0.8).shift(RIGHT * 2)

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
        apple1 = ImageMobject(apple_path).scale(0.8).shift(LEFT * 2)
        apple2 = ImageMobject(apple_path).scale(0.8)
        apple3 = ImageMobject(apple_path).scale(0.8).shift(RIGHT * 2)

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
