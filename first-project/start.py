#!/usr/bin/env python

from manimlib import *

import os
import time
import ctypes


class AddPolygon(Scene):
    def construct(self):
        # Basic Polygon

        cnt = 3
        polys_l = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(cnt)
            ]
        ).arrange(RIGHT, buff=0.2)
        polys_l.shift(3 * LEFT)
        polys_l.shift(UP)

        self.play(DrawBorderThenFill(polys_l), run_time=1)
        self.wait(0.5)

        # second set of polygons
        cnt = 2
        polys_r = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(cnt)
            ]
        ).arrange(RIGHT, buff=0.2)
        polys_r.shift(4 * RIGHT)
        polys_r.shift(UP)

        # "+"

        plus_sign = Text("+").scale(1.5)
        midpoint = (polys_l.get_right() + polys_r.get_left()) / 2
        plus_sign.move_to(midpoint)

        self.add(plus_sign)  # Add without animation (ManimGL optimized)
        self.wait(0.5)

        self.play(DrawBorderThenFill(polys_r), run_time=1)

        self.wait()

        cnt = 5
        polys = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(cnt)
            ]
        ).arrange(RIGHT, buff=0.2)
        polys.shift(1.5 * DOWN)

        equal_sign = Text("=").scale(1.5)
        point = polys.get_left() + 0.5 * LEFT
        equal_sign.move_to(point)

        self.add(equal_sign)  # Add without animation (ManimGL optimized)

        self.play(DrawBorderThenFill(polys), run_time=1)


from manimlib import *


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
        clock.shift(3 * LEFT)
        hand_origin = hand.get_start()

        # Animate showing the clock
        self.play(FadeIn(clock))

        self.wait(0.5)

        # Create the first 3-hour pie slice (starts at 0° angle)
        pie_3 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=0,  # Start with no visible pie slice
            start_angle=PI / 2,  # Starts from the top
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
                start_angle=PI / 2,
                fill_color=BLUE,
                fill_opacity=0.5,
            )
            new_pie.shift(
                (ORIGIN - hand_origin) * LEFT
            )  # Keep the pie centered at hand origin
            m.become(new_pie)

        pie_3.add_updater(update_pie)
        # Rotate hand 3 hours (180°) + grow the sector together
        self.play(
            Rotate(hand, angle=-PI, about_point=hand_origin),
            angle_tracker.animate.set_value(PI),  # Gradually expand the sector
        )

        self.wait(0.5)

        #
        #
        # Create and fill the next 2-hour pie slice (120°)
        pie_2 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=-2 * PI / 3,
            start_angle=-PI / 2,
            fill_color=GREY_A,
            fill_opacity=0.5,
        )
        self.add(pie_2)  # Add it first so we can update its angle

        # Use a ValueTracker to animate the sector's angle
        angle_tracker2 = ValueTracker(0)

        def update_pie(m):
            new_pie = AnnularSector(
                inner_radius=0,
                outer_radius=2,
                angle=-angle_tracker2.get_value(),  # Negative to rotate clockwise
                start_angle=-PI / 2,
                fill_color=GREY_A,
                fill_opacity=0.5,
            )
            new_pie.shift(
                (ORIGIN - hand_origin) * LEFT
            )  # Keep the pie centered at hand origin
            m.become(new_pie)

        pie_2.add_updater(update_pie)

        # Rotate hand 3 hours (180°) + grow the sector together
        self.play(
            Rotate(hand, angle=-2 * PI / 3, about_point=hand_origin),
            angle_tracker2.animate.set_value(2 * PI / 3),  # Gradually expand the sector
        )

        # Final wait to show result
        self.wait()

        ###
        # Create clock face2 (circle)
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
        clock.shift(3 * RIGHT)
        hand_origin = hand.get_start()

        # Animate showing the clock
        self.play(FadeIn(clock))

        self.wait(0.5)

        # Create the first 3-hour pie slice (starts at 0° angle)
        pie_2 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=0,  # Start with no visible pie slice
            start_angle=PI / 2,  # Starts from the top
            fill_color=BLUE,
            fill_opacity=0.5,  # Keep it visible but initially empty
        )
        # self.add(pie_3)  # Add it first so we can update its angle

        self.add(pie_2)
        pie_2.move_to(hand_origin)

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
                start_angle=PI / 2,
                fill_color=BLUE,
                fill_opacity=0.5,
            )
            new_pie.shift(
                (ORIGIN - hand_origin) * LEFT
            )  # Keep the pie centered at hand origin
            m.become(new_pie)

        pie_2.add_updater(update_pie)
        # Rotate hand 3 hours (180°) + grow the sector together
        self.play(
            Rotate(hand, angle=-2 * PI / 3, about_point=hand_origin),
            angle_tracker.animate.set_value(2 * PI / 3),  # Gradually expand the sector
        )

        self.wait(0.5)

        #
        #
        # Create and fill the next 2-hour pie slice (120°)
        pie_3 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            start_angle=-PI / 2,
            fill_color=GREY_A,
            fill_opacity=0.5,
        )
        self.add(pie_2)  # Add it first so we can update its angle

        # Use a ValueTracker to animate the sector's angle
        angle_tracker2 = ValueTracker(0)

        def update_pie(m):
            new_pie = AnnularSector(
                inner_radius=0,
                outer_radius=2,
                angle=-angle_tracker2.get_value(),  # Negative to rotate clockwise
                start_angle=-PI / 2,
                fill_color=GREY_A,
                fill_opacity=0.5,
            )
            new_pie.shift(
                (ORIGIN - hand_origin) * LEFT
            )  # Keep the pie centered at hand origin
            m.become(new_pie)

        pie_2.add_updater(update_pie)

        # Rotate hand 3 hours (180°) + grow the sector together
        self.play(
            Rotate(hand, angle=-PI, about_point=hand_origin),
            angle_tracker2.animate.set_value(PI),  # Gradually expand the sector
        )

        # Final wait to show result
        self.wait()
