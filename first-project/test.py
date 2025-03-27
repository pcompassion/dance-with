#!/usr/bin/env python

from manimlib import *
from src.mobject.clock import Clock
from functools import partial


class ThreePolarizers(Scene):

    def construct(self):
        # Title
        title = Text("Three Polarizers Demo", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Polarizers (represented as rectangles with angle labels)
        polarizers = VGroup(
            self.create_polarizer("0°", LEFT * 4),
            self.create_polarizer("45°", ORIGIN),
            self.create_polarizer("90°", RIGHT * 4),
        )
        self.play(FadeIn(polarizers))

        # Incoming light (unpolarized)
        light_in = self.create_light_beam(color=YELLOW).shift(LEFT * 6)
        self.play(GrowArrow(light_in))

        # Pass through first polarizer (0° → Horizontal)
        pol1_arrow = self.polarized_wave(start=LEFT * 3.5, angle=0, color=BLUE)
        self.play(FadeOut(light_in), GrowArrow(pol1_arrow))

        # Through second (45°) → Partial projection
        pol2_arrow = self.polarized_wave(start=ORIGIN, angle=45, color=GREEN)
        self.play(GrowArrow(pol2_arrow))

        # Through third (90°) → Final projection
        pol3_arrow = self.polarized_wave(start=RIGHT * 3.5, angle=90, color=RED)
        self.play(GrowArrow(pol3_arrow))

        # Add final intensity label
        intensity = Text("Reduced Intensity (~25%)", font_size=24).next_to(
            pol3_arrow, DOWN
        )
        self.play(Write(intensity))

        self.wait(2)

    def create_polarizer(self, label, position):
        rect = Rectangle(width=0.2, height=4, fill_opacity=0.3, fill_color=WHITE)
        text = Text(label, font_size=24).next_to(rect, DOWN)
        group = VGroup(rect, text).move_to(position)
        return group

    def create_light_beam(self, color=YELLOW):
        return Arrow(start=LEFT * 6, end=LEFT * 3.5, buff=0, color=color)

    def polarized_wave(self, start, angle=0, color=BLUE):
        direction = np.array([np.cos(angle * DEGREES), np.sin(angle * DEGREES), 0])
        return Arrow(start=start, end=start + direction * 3, color=color)
