#!/usr/bin/env python

from manimlib import *


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
