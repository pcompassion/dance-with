#!/usr/bin/env python
from manimlib import *


class Clock(VGroup):
    def __init__(
        self, position=ORIGIN, radius=2, hand_color=YELLOW, num_hours=12, **kwargs
    ):
        super().__init__(**kwargs)

        clock_circle = Circle(radius=2, color=WHITE)
        self.clock_circle = clock_circle

        # Hour markings (12 numbers correctly positioned)
        numbers = VGroup()
        self.num_hours = num_hours

        for i in range(num_hours):
            angle = PI / 2 + -i * TAU / num_hours  # Counterclockwise placement

            digit = i % num_hours
            if digit == 0:
                digit = num_hours
            number = Text(str(digit)).scale(0.7)  # Adjusting for correct order
            number.move_to(2.3 * np.array([np.cos(angle), np.sin(angle), 0]))
            numbers.add(number)

        # Clock center dot
        center_dot = Dot(color=WHITE)

        self.hour_hand = hour_hand = Line(
            ORIGIN, ORIGIN + UP * 1.5, color=hand_color
        ).set_stroke(width=6)

        self.pie = pie = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=0,  # Start with no visible pie slice
            start_angle=PI / 2,  # Starts from the top
            fill_color=BLUE,
            fill_opacity=0.5,  # Keep it visible but initially empty
        )

        self.add(self.clock_circle, numbers, center_dot, hour_hand, pie)

    def animate_hand(self, start_angle, angle_delta, fill_color):

        pie = self.pie
        hand = self.hour_hand
        # Use a ValueTracker to animate the sector's angle
        angle_tracker = ValueTracker(0)
        hand_origin = hand.get_start()

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

        pie.add_updater(update_pie)

        animations = [
            Rotate(hand, angle=angle_delta, about_point=hand_origin),
            angle_tracker.animate.set_value(
                -angle_delta
            ),  # Gradually expand the sector
        ]
        return animations
