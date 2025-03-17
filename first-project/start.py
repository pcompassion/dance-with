#!/usr/bin/env python

from manimlib import *

import os
import time
import ctypes


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
            ]
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
            ]
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
        x_axis = Line(start=LEFT * 2.5, end=RIGHT * 2.5, color=WHITE)
        x_axis.move_to(UP * 2.5)  # Position above

        # Create tick marks and labels at 0,1,2,3,4,5
        tick_marks = VGroup()
        number_labels = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=WHITE)
            tick.move_to(x_axis.get_left() + RIGHT * i)
            tick_marks.add(tick)

            if i > 0:  # Avoid placing a "0" label
                num = Text(str(i)).scale(0.8)
                num.next_to(tick, DOWN * 0.3)
                number_labels.add(num)

        # Show the x-axis
        self.play(ShowCreation(x_axis), FadeIn(tick_marks), FadeIn(number_labels))
        self.wait(0.5)

        # Create bar of length 3 (Blue) - Align left to tick 0
        bar_3 = Rectangle(height=1, width=3, fill_color=BLUE, fill_opacity=0.8)
        bar_3.move_to(x_axis.get_left() + RIGHT * 1.5 + DOWN * 1.5)  # Align left to 0

        # Label "3" above the blue bar
        label_3 = Text("3").scale(1.2).move_to(bar_3.get_center())

        # Animate showing the "3" bar
        self.play(FadeIn(bar_3), Write(label_3))
        self.wait(0.5)

        # Create bar of length 2 (Red) - Align to right of the blue bar
        bar_2 = Rectangle(height=1, width=2, fill_color=RED, fill_opacity=0.8)
        bar_2.next_to(bar_3, RIGHT, buff=0)  # Place next to blue bar

        # Label "2" above the red bar
        label_2 = Text("2").scale(1.2).move_to(bar_2.get_center())

        # Animate showing the "2" bar
        self.play(FadeIn(bar_2), Write(label_2))
        self.wait(0.5)

        # Create the final bar of length 5 (Green) - Align left to tick 0
        bar_5 = Rectangle(height=1, width=5, fill_color=GREEN, fill_opacity=0.8)
        bar_5.move_to(x_axis.get_left() + RIGHT * 2.5 + DOWN * 2.5)  # Align left

        # Label "3" above the blue bar
        label_5 = Text("5").scale(1.2).move_to(bar_5.get_center())

        # Animate the transition into the final green bar
        self.play(
            Transform(bar_3.copy(), bar_5),  # Merge blue into green
            Transform(bar_2.copy(), bar_5),  # Merge red into green
        )
        self.play(
            Write(label_5),
        )

        self.wait(0.5)

        bar_2b = bar_2.copy()
        bar_2b.move_to(bar_5.get_left() + RIGHT + DOWN * 1)

        self.play(
            Transform(bar_2.copy(), bar_2b),  # Merge red into green
        )

        # Label "2" above the red bar
        label_2 = Text("2").scale(1.2).move_to(bar_2b.get_center())
        self.play(Write(label_2))

        self.wait(0.5)

        bar_3b = bar_3.copy()
        bar_3b.move_to(bar_2b.get_right() + RIGHT * 1.5)

        self.play(
            Transform(bar_3.copy(), bar_3b),  # Merge red into green
        )

        # Label "3" above the blue bar
        label_3 = Text("3").scale(1.2).move_to(bar_3b.get_center())

        # Animate showing the "3" bar
        self.play(Write(label_3))

        self.wait(0.5)

        # Show "3 + 2 = 5" text at the bottom
        equation = Text("3 + 2 = 2 + 3").scale(1.5)
        equation.next_to(bar_5, DOWN * 3, buff=0.5)

        self.play(Write(equation))
        self.wait()


class ClockAnimation(Scene):
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
                fill_color=BLUE,
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

        animate_hand(hand_origin, start_angle=PI / 2, angle_delta=-PI, fill_color=BLUE)

        self.wait(0.5)
        animate_hand(
            hand_origin, start_angle=-PI / 2, angle_delta=-2 * PI / 3, fill_color=GREY_A
        )

        clock = clock_face()
        clock.shift(3 * RIGHT + UP)
        hand = clock[3]
        hand_origin = hand.get_start()

        # Animate showing the clock
        self.play(FadeIn(clock))

        self.wait(0.5)

        animate_hand(
            hand_origin, start_angle=PI / 2, angle_delta=-2 * PI / 3, fill_color=BLUE
        )

        self.wait(0.5)
        animate_hand(
            hand_origin, start_angle=-1 * PI / 6, angle_delta=-PI, fill_color=GREY_A
        )

        # equation
        equation = Tex(r"3 + 2 = 2 + 3").scale(1.5)
        equation.shift(DOWN * 2.5)

        self.play(Write(equation))
        self.wait(0.5)


class BallDrop(Scene):
    def construct(self):
        # Create a three-sided box (open top)
        floor = Line(LEFT * 3, RIGHT * 3, color=WHITE)
        left_wall = Line(UP * 2, DOWN * 2, color=WHITE)
        right_wall = Line(UP * 2, DOWN * 2, color=WHITE)

        # Position the walls correctly
        left_wall.move_to(LEFT * 3 + DOWN * 1)
        right_wall.move_to(RIGHT * 3 + DOWN * 1)
        box = VGroup(floor, left_wall, right_wall)

        # Create three balls (circles)
        balls = VGroup(
            *[
                Dot(radius=0.2, fill_color=BLUE).move_to(UP * 2 + LEFT * (1 - i))
                for i in range(2)
            ]
        )

        gravity = 3
        min_velocity = 1

        for ball in balls:
            velocity = ValueTracker(0)  # Initial velocity
            time_tracker = ValueTracker(0)  # Track time

            def update_ball(m, dt, time_tracker=time_tracker, velocity=velocity):
                damping_factor = 0.7  # Bounce energy loss

                time_tracker.increment_value(dt)
                v = velocity.get_value() + gravity * dt  # Apply gravity
                m.shift(DOWN * v * dt)  # Move the ball
                velocity.set_value(v)

                # Collision with floor (bouncing effect)
                if m.get_bottom()[1] <= floor.get_center()[1]:
                    new_v = -damping_factor * v  # Reduce bounce velocity
                    velocity.set_value(new_v)
                    m.move_to(
                        [m.get_x(), floor.get_center()[1] + 0.2, 0]
                    )  # Keep ball on floor

                    # Stop updating if the bounce velocity is too low or time exceeds 2 sec
                    if abs(new_v) < min_velocity:  # or time_tracker.get_value() > 2:
                        velocity.set_value(-1 * v)

            ball.add_updater(update_ball)

        # Animate dropping balls
        self.play(FadeIn(box), FadeIn(balls))
        self.wait(10)  # Let the balls bounce and settle
        # Acceleration due to gravity

        # # Stop updates to freeze the scene
        # for ball in balls:
        #     ball.clear_updaters()


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
        text_b = Text("b").scale(1).next_to(shape_b, UP, buff=0.3)

        a_group = VGroup(shape_a, text_a)
        b_group = VGroup(shape_b, text_b)

        # Show first equation (a + b)
        self.play(FadeIn(a_group))
        self.play(FadeIn(b_group))
        self.wait(1)

        # Transition to b + a by swapping positions
        shape_a_target = a_group.copy().move_to(RIGHT * 2)
        shape_b_target = b_group.copy().move_to(LEFT * 2)

        # Animate swap
        self.play(
            Transform(a_group, shape_a_target), Transform(b_group, shape_b_target)
        )
        self.wait(0.5)

        equation = Tex(r"a + b = b + a").scale(1.5)
        equation.shift(DOWN * 2)

        self.play(Write(equation))
        self.wait(0.5)


class DistributiveProperty(Scene):
    def construct(self):
        # Step 1: Define M, A, B in a single line
        M_text = Tex("M").scale(1.5)
        l_text = Tex("(")
        A_text = Tex("A").scale(1.5)
        m_text = Tex("*")
        B_text = Tex("B").scale(1.5)
        r_text = Tex(")")

        # Arrange M, A, B in a line
        M_text.move_to(LEFT * 3)
        A_text.move_to(LEFT * 2)

        B_text.move_to(LEFT * 1)
        l_text.move_to((M_text.get_right() + A_text.get_left()) / 2)
        m_text.move_to((A_text.get_right() + B_text.get_left()) / 2)
        r_text.move_to(B_text.get_right() + RIGHT * 0.2)

        # Step 2: Draw curved arrows from M to A and M to B
        arc_to_A = Arrow(
            M_text.get_top(), A_text.get_top(), color=YELLOW, path_arc=-PI / 3
        )
        arc_to_B = Arrow(
            M_text.get_bottom(), B_text.get_bottom(), color=YELLOW, path_arc=PI / 3
        )

        # Step 3: Animate the elements appearing
        self.play(
            FadeIn(M_text),
            FadeIn(l_text),
            FadeIn(A_text),
            FadeIn(m_text),
            FadeIn(B_text),
            FadeIn(r_text),
        )
        self.play(GrowArrow(arc_to_A))

        equal_sign = Tex(r"=")

        equation_rhs1 = Tex(r"MA").scale(1.5)
        equation_rhs1.move_to(equal_sign.get_right() + RIGHT)

        self.play(FadeIn(equal_sign), FadeIn(equation_rhs1))

        plus_sign = Tex(r"+").scale(1.5)
        equation_rhs2 = Tex(r"MB").scale(1.5)

        plus_sign.move_to(equation_rhs1.get_right() + RIGHT * 0.5)
        equation_rhs2.move_to(plus_sign.get_right() + RIGHT * 0.8)

        self.play(GrowArrow(arc_to_B))
        self.play(FadeIn(plus_sign), FadeIn(equation_rhs2))

        self.wait(0.5)


class DistributivePropertyBasic(Scene):
    def construct(self):
        # Step 1: Write initial equation M(A + B)
        equation_lhs = Tex(r"M(A + B)").scale(1.5)
        equation_lhs.move_to(LEFT * 3)

        # Step 2: Write transformed equation MA + MB
        equation_rhs = Tex(r"MA + MB").scale(1.5)
        equation_rhs.move_to(RIGHT * 3)

        # Step 3: Draw curved arrows to indicate distribution
        M_text = Tex("M").scale(1.5)
        A_text = Tex("A").scale(1.5)
        B_text = Tex("B").scale(1.5)

        M_text.move_to(LEFT * 3.5 + UP)
        A_text.move_to(LEFT * 2.5 + DOWN * 0.5)
        B_text.move_to(LEFT * 1.5 + DOWN * 0.5)

        arc_to_A = Arrow(
            M_text.get_bottom(), A_text.get_top(), color=YELLOW, path_arc=-PI / 3
        )
        arc_to_B = Arrow(
            M_text.get_bottom(), B_text.get_top(), color=YELLOW, path_arc=PI / 3
        )

        # Step 4: Animate the distribution
        self.play(Write(equation_lhs))
        self.wait(0.5)
        self.play(FadeIn(M_text), FadeIn(A_text), FadeIn(B_text))
        self.wait(0.5)
        self.play(GrowArrow(arc_to_A), GrowArrow(arc_to_B))
        self.wait(0.5)
        self.play(Transform(equation_lhs, equation_rhs))  # Morph into MA + MB
        self.wait()


class DistributiveProperty(Scene):
    def construct(self):
        # Title
        title = Tex("2(3+4) = 2 \\cdot 3 + 2 \\cdot 4").shift(UP * 1.5 + LEFT * 0.5)

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


class DistributiveArea(Scene):
    def construct(self):
        # Title
        title = Tex("(3+2) \\cdot (3+2)").shift(UP * 3)
        bc = BLUE
        box_3_3_1 = SurroundingRectangle(title[1], color=bc)
        box_3_3_2 = SurroundingRectangle(title[7], color=bc)

        box_3_2_1 = SurroundingRectangle(title[1], color=bc)
        box_3_2_2 = SurroundingRectangle(title[9], color=bc)

        box_2_3_1 = SurroundingRectangle(title[3], color=bc)
        box_2_3_2 = SurroundingRectangle(title[7], color=bc)

        box_2_2_1 = SurroundingRectangle(title[3], color=bc)
        box_2_2_2 = SurroundingRectangle(title[9], color=bc)

        self.play(FadeIn(title))

        # Show the x-axis

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_2 = Rectangle(width=2, height=0.3, color=GREEN, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.copy().move_to(LEFT + UP * 2)
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
        rect_3x3.move_to(LEFT * 1 + UP * 0.5)
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
        label_3x2 = Tex("3 \\cdot 2").move_to(rect_3x2)
        box_3_2 = SurroundingRectangle(label_3x2, color=bc)
        label_2x3 = Tex("2 \\cdot 3").move_to(rect_2x3)
        box_2_3 = SurroundingRectangle(label_2x3, color=bc)
        label_2x2 = Tex("2 \\cdot 2").move_to(rect_2x2)
        box_2_2 = SurroundingRectangle(label_2x2, color=bc)

        self.play(
            FadeIn(label_3x3),
            FadeIn(box_3_3),
            FadeIn(box_3_3_1),
            FadeIn(box_3_3_2),
        )
        self.play(
            FadeOut(box_3_3),
            FadeOut(box_3_3_1),
            FadeOut(box_3_3_2),
        )

        self.play(
            FadeIn(label_3x2),
            FadeIn(box_3_2),
            FadeIn(box_3_2_1),
            FadeIn(box_3_2_2),
        )

        self.play(
            FadeOut(box_3_2),
            FadeOut(box_3_2_1),
            FadeOut(box_3_2_2),
        )

        self.play(
            FadeIn(label_2x3),
            FadeIn(box_2_3),
            FadeIn(box_2_3_1),
            FadeIn(box_2_3_2),
        )

        self.play(
            FadeOut(box_2_3),
            FadeOut(box_2_3_1),
            FadeOut(box_2_3_2),
        )

        self.play(
            FadeIn(label_2x2),
            FadeIn(box_2_2),
            FadeIn(box_2_2_1),
            FadeIn(box_2_2_2),
        )

        self.play(
            FadeOut(box_2_2),
            FadeOut(box_2_2_1),
            FadeOut(box_2_2_2),
        )

        self.wait(2)


class DistributiveArea(Scene):
    def construct(self):
        # Title
        title = Tex("(3+2) \\cdot (4+1)").shift(UP * 3)
        bc = BLUE
        box_3_3_1 = SurroundingRectangle(title[1], color=bc)
        box_3_3_2 = SurroundingRectangle(title[7], color=bc)

        box_3_2_1 = SurroundingRectangle(title[1], color=bc)
        box_3_2_2 = SurroundingRectangle(title[9], color=bc)

        box_2_3_1 = SurroundingRectangle(title[3], color=bc)
        box_2_3_2 = SurroundingRectangle(title[7], color=bc)

        box_2_2_1 = SurroundingRectangle(title[3], color=bc)
        box_2_2_2 = SurroundingRectangle(title[9], color=bc)

        self.play(FadeIn(title))

        # Show the x-axis

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_2 = Rectangle(width=2, height=0.3, color=GREEN, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.move_to(LEFT + UP * 2)
        top_2 = bar_2.next_to(top_3, RIGHT, buff=0)
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

        tick_marks_v = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=GREY_E)
            tick.move_to(top_3.get_left() + RIGHT * i)
            tick.rotate(-PI / 2, about_point=corner)

            tick_marks_v.add(tick)

        bar_4 = Rectangle(width=4, height=0.3, color=BLUE, fill_opacity=1)
        bar_1 = Rectangle(width=1, height=0.3, color=GREEN, fill_opacity=1)
        top_4 = bar_4.copy().move_to(corner + RIGHT * 4 / 2)
        top_1 = bar_1.copy().next_to(top_4, RIGHT, buff=0)

        self.play(FadeIn(top_4), FadeIn(top_1), FadeIn(tick_marks))

        self.play(FadeIn(left_3), FadeIn(left_2), FadeIn(tick_marks_v))
        self.wait(1)

        # Define rectangles for areas
        rect_3x3 = Rectangle(width=4, height=3, color=WHITE, fill_opacity=0.5)
        rect_3x2 = Rectangle(width=1, height=3, color=YELLOW, fill_opacity=0.5)
        rect_2x3 = Rectangle(width=4, height=2, color=ORANGE, fill_opacity=0.5)
        rect_2x2 = Rectangle(width=1, height=2, color=RED, fill_opacity=0.5)

        # Align rectangles properly
        rect_3x3.move_to(LEFT * 0.5 + UP * 0.5)
        rect_3x2.next_to(rect_3x3, RIGHT, buff=0, aligned_edge=UP)
        rect_2x3.next_to(rect_3x3, DOWN, buff=0, aligned_edge=LEFT)
        rect_2x2.next_to(rect_3x2, DOWN, buff=0, aligned_edge=LEFT)

        self.play(FadeIn(rect_3x3))
        self.play(FadeIn(rect_3x2))
        self.play(FadeIn(rect_2x3))
        self.play(FadeIn(rect_2x2))

        # Add labels inside rectangles
        label_3x3 = Tex("3 \\cdot 4").move_to(rect_3x3)
        box_3_3 = SurroundingRectangle(label_3x3, color=bc)
        label_3x2 = Tex("3 \\cdot 1").move_to(rect_3x2)
        box_3_2 = SurroundingRectangle(label_3x2, color=bc)
        label_2x3 = Tex("2 \\cdot 4").move_to(rect_2x3)
        box_2_3 = SurroundingRectangle(label_2x3, color=bc)
        label_2x2 = Tex("2 \\cdot 1").move_to(rect_2x2)
        box_2_2 = SurroundingRectangle(label_2x2, color=bc)

        self.play(
            FadeIn(label_3x3),
            FadeIn(box_3_3),
            FadeIn(box_3_3_1),
            FadeIn(box_3_3_2),
        )
        self.play(
            FadeOut(box_3_3),
            FadeOut(box_3_3_1),
            FadeOut(box_3_3_2),
        )

        self.play(
            FadeIn(label_3x2),
            FadeIn(box_3_2),
            FadeIn(box_3_2_1),
            FadeIn(box_3_2_2),
        )

        self.play(
            FadeOut(box_3_2),
            FadeOut(box_3_2_1),
            FadeOut(box_3_2_2),
        )

        self.play(
            FadeIn(label_2x3),
            FadeIn(box_2_3),
            FadeIn(box_2_3_1),
            FadeIn(box_2_3_2),
        )

        self.play(
            FadeOut(box_2_3),
            FadeOut(box_2_3_1),
            FadeOut(box_2_3_2),
        )

        self.play(
            FadeIn(label_2x2),
            FadeIn(box_2_2),
            FadeIn(box_2_2_1),
            FadeIn(box_2_2_2),
        )

        self.play(
            FadeOut(box_2_2),
            FadeOut(box_2_2_1),
            FadeOut(box_2_2_2),
        )

        self.wait(2)


class GeometricSeries(Scene):
    def construct(self):
        # Define equations
        eq1 = Tex("S = 0.999999\\dots")
        eq2 = Tex("10S = 9.999999\\dots")

        eq3 = Tex("10S - S = 9.999999\\dots - 0.999999\\dots")
        eq4 = Tex("9S = 9")
        eq5 = Tex("S = 1")

        # Position equations
        eq1.shift(UP * 2)
        left_margin = LEFT * 3  # Adjust as needed
        eq1.move_to(left_margin + UP * 2)
        eq2.next_to(eq1, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq3.next_to(eq2, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq4.next_to(eq3, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq5.next_to(eq4, DOWN, buff=0.5).align_to(eq1, LEFT)

        # Animate equations step by step
        self.play(FadeIn(eq1))
        self.wait(1)
        self.play(FadeIn(eq2))
        self.wait(1)
        self.play(FadeIn(eq3))
        self.wait(1)
        self.play(FadeIn(eq4))
        self.wait(1)
        self.play(FadeIn(eq5))
        self.wait(2)

        self.clear()

        # 9999
        eq1 = Tex("S = \dots999999")
        eq2 = Tex("10S = \dots999990")

        eq3 = Tex("10S - S = \dots999990 - \dots999999")

        eq4 = Tex("9S = -9")
        eq5 = Tex("S = -1")

        # Position equations
        eq1.shift(UP * 2)
        left_margin = LEFT * 3  # Align to left margin
        eq1.move_to(left_margin + UP * 2)
        eq2.next_to(eq1, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq3.next_to(eq2, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq4.next_to(eq3, DOWN, buff=0.5).align_to(eq1, LEFT)
        eq5.next_to(eq4, DOWN, buff=0.5).align_to(eq1, LEFT)

        # Animate equations step by step
        self.play(FadeIn(eq1))
        self.wait(1)
        self.play(FadeIn(eq2))

        self.wait(1)
        self.play(FadeIn(eq3))

        self.wait(1)
        self.play(FadeIn(eq4))
        self.wait(1)
        self.play(FadeIn(eq5))
        self.wait(2)

        self.clear()

        equation = Tex("(3+4i)(2+3i) = 6 + 9i + 8i + 12i^2")
        self.play(FadeIn(equation))
        self.wait(2)


class DistributiveLawVisualization(Scene):
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
        self.wait(1)

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

        self.play(FadeIn(rect_3x3))
        self.play(FadeIn(rect_3x2))
        self.play(FadeIn(rect_3x1))
        self.play(FadeIn(rect_2x3))
        self.play(FadeIn(rect_2x2))
        self.play(FadeIn(rect_2x1))
        self.wait(2)


class DistributiveLawVisualization(Scene):
    def construct(self):
        # minus dis
        title = Tex("4 \\cdot (3 - 2)").shift(UP * 3).scale(1.5)
        self.play(FadeIn(title))
        custom_dark_grey = "#444444"  # Hex color for a darker grey
        # Define colors
        bc = BLUE

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_neg_2 = Rectangle(width=2, height=0.3, color=RED, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.copy().move_to(LEFT + UP * 2)
        top_neg_2 = bar_neg_2.copy().next_to(top_3, RIGHT, buff=0)
        corner = top_3.get_left()

        # Position vertical bars
        left_4 = Rectangle(width=0.3, height=4, color=GREEN, fill_opacity=1).move_to(
            corner, aligned_edge=UP
        )

        # self.play(FadeIn(top_3), FadeIn(top_neg_2))
        # self.play(FadeIn(left_4))

        # Define rectangles for areas
        rect_4x3 = Rectangle(width=3, height=4, color=BLUE, fill_opacity=0.9)
        rect_4x_neg2 = Rectangle(width=2, height=4, color=RED, fill_opacity=0.9)
        rect_4x2 = Rectangle(width=2, height=4, color=RED, fill_opacity=0.9)

        # Align rectangles properly
        rect_4x3.move_to(corner + RIGHT * 1.5 + DOWN * 2)
        rect_4x_neg2.next_to(rect_4x3, RIGHT, buff=0, aligned_edge=UP)
        rect_4x2_copy = rect_4x2.copy().move_to(
            rect_4x_neg2.get_left(), aligned_edge=RIGHT
        )
        # Move the yellow rectangle from the red one to its new position

        self.play(FadeIn(rect_4x3))

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

        self.play(FadeIn(rect_4x_neg2), Write(eq2))

        # Grey out the negative parts to show subtraction
        grey_rect_neg2 = rect_4x_neg2.copy().set_color("#333333").set_opacity(1)

        self.play(
            # rect_4x2.animate.move_to(rect_4x_neg2.get_left(), aligned_edge=RIGHT),
            Transform(rect_4x2, rect_4x2_copy),
            Write(minus),
            run_time=2,
        )
        grey_rect_4x2 = rect_4x2.copy().set_color(custom_dark_grey).set_opacity(1)

        self.play(
            Transform(rect_4x_neg2, grey_rect_neg2),
            Transform(rect_4x2, grey_rect_4x2),
            Write(eq3),
        )

        self.wait()
