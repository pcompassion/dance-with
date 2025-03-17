#!/usr/bin/env python

from manimlib import *


class SquareToCircle(Scene):
    def construct(self):
        # show circle

        # show circle
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        self.add(circle)
        self.remove(circle)

        # Create the blue circles (left side)
        circle1 = Circle(radius=0.5, color=BLUE)
        circle2 = Circle(radius=0.5, color=BLUE)
        circle3 = Circle(radius=0.5, color=BLUE)
        circle4 = Circle(radius=0.5, color=BLUE)

        # Create the green circles (right side)
        circle5 = Circle(radius=0.5, color=GREEN)
        circle6 = Circle(radius=0.5, color=GREEN)
        circle7 = Circle(radius=0.5, color=GREEN)

        # Create the orange circles (bottom side)
        circle8 = Circle(radius=0.5, color=ORANGE)
        circle9 = Circle(radius=0.5, color=ORANGE)
        circle10 = Circle(radius=0.5, color=ORANGE)
        circle11 = Circle(radius=0.5, color=ORANGE)
        circle12 = Circle(radius=0.5, color=ORANGE)

        # Create the blue squiggly shapes (on the bottom)
        squiggly1 = Ellipse(width=1.2, height=0.8, color=BLUE)
        squiggly2 = Ellipse(width=1.2, height=0.8, color=BLUE)

        # Position the circles in a clear, organized manner
        circle1.shift(LEFT * 4)
        circle2.next_to(circle1, RIGHT, buff=0.8)
        circle3.next_to(circle2, RIGHT, buff=0.8)
        circle4.next_to(circle3, RIGHT, buff=0.8)

        circle5.shift(RIGHT * 4)
        circle6.next_to(circle5, RIGHT, buff=0.8)
        circle7.next_to(circle6, RIGHT, buff=0.8)

        circle8.shift(LEFT * 4 + DOWN * 2)
        circle9.next_to(circle8, RIGHT, buff=0.8)
        circle10.next_to(circle9, RIGHT, buff=0.8)
        circle11.next_to(circle10, RIGHT, buff=0.8)
        circle12.next_to(circle11, RIGHT, buff=0.8)

        squiggly1.shift(LEFT * 3 + DOWN * 3)
        squiggly2.shift(RIGHT * 3 + DOWN * 3)

        # # Create text for the equation
        # equation = TextMobject(r"$M(A + B) = MA + MB$")
        # equation.to_edge(UP)

        # # Display the equation and the shapes
        # self.play(Write(equation))
        self.play(
            FadeIn(circle1),
            FadeIn(circle2),
            FadeIn(circle3),
            FadeIn(circle4),
            FadeIn(circle5),
            FadeIn(circle6),
            FadeIn(circle7),
            FadeIn(circle8),
            FadeIn(circle9),
            FadeIn(circle10),
            FadeIn(circle11),
            FadeIn(circle12),
            FadeIn(squiggly1),
            FadeIn(squiggly2),
        )


class BasicAnimations(Scene):
    def construct(self):
        # Basic Polygon
        polys = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(5)
            ]
        ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t),  # rate_func=linear
            Rotate(
                polys[1], PI, rate_func=smooth
            ),  # default behavior for most animations
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t * PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1 - 2 * t)),
            run_time=2,
        )
