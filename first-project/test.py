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


class SpinDemoScene(ThreeDScene):
    def construct(self):

        class Volumetric3DArrowWithCircle(VGroup):
            def __init__(self, color=YELLOW, scale=1.0, **kwargs):
                super().__init__(**kwargs)

                # Flat circle (still flat, no extrusion yet)
                circle = Circle(radius=1.5 * scale, color=WHITE)
                circle.set_fill(BLACK, opacity=1)
                circle.rotate(PI / 2)  # XY plane

                # Arrow body = cylinder
                shaft = Cylinder(
                    radius=0.05 * scale,
                    height=0.8 * scale,
                    # direction=OUT,
                    resolution=(6, 16),
                    # fill_opacity=1,
                    # stroke_width=0,
                    color=color,
                )
                shaft.shift(OUT * (0.8 * scale / 2))  # center the shaft

                # Arrow head = cone
                tip = Cone(
                    # base_radius=0.1 * scale,
                    height=0.3 * scale,
                    # direction=OUT,
                    resolution=(6, 16),
                    # fill_opacity=1,
                    # stroke_width=0,
                    color=color,
                )
                tip.shift(
                    OUT * (0.8 * scale + 0.15 * scale)
                )  # position at end of shaft

                self.circle = circle
                self.arrow = VGroup(shaft, tip)
                self.add(circle, self.arrow)

            def get_rotation_anim(self, angle=2 * PI, duration=2, rate_func=linear):
                return Rotating(
                    self.arrow,
                    angle=angle,
                    axis=UP,
                    run_time=duration,
                    rate_func=rate_func,
                )

        arrow_obj = Volumetric3DArrowWithCircle(color=BLUE)
        self.add(arrow_obj)
        self.begin_ambient_camera_rotation(rate=0.2)  # Optional, rotate around object
        self.play(arrow_obj.get_rotation_anim(angle=2 * PI, duration=3))
        self.wait()


class SpinDemoScene(ThreeDScene):  # Still use ThreeDScene in ManimGL
    def construct(self):

        class Spinning3DArrowWithCircle(VGroup):
            def __init__(self, color=YELLOW, scale=1.0, arrow_mode="both", **kwargs):
                super().__init__(**kwargs)

                # Flat circle
                circle = Circle(radius=1.2 * scale, color=WHITE)
                circle.set_fill(BLACK, opacity=1)
                circle.rotate(PI / 2)  # Lay it flat in XY plane

                def make_arrow():

                    return Polygon(
                        [0, 1.0, 0],  # top point
                        [0.3, 0.0, 0],  # bottom right
                        [-0.3, 0.0, 0],  # bottom left
                        color=WHITE,
                        fill_opacity=1,
                    )

                arrows = VGroup()

                if arrow_mode in ["up", "both"]:
                    up_arrow = make_arrow()
                    up_arrow.set_fill(ORANGE, opacity=1)
                    up_arrow.set_stroke(BLACK, width=1)
                    up_arrow.scale(scale)
                    arrows.add(up_arrow)

                if arrow_mode in ["down", "both"]:
                    down_arrow = make_arrow()
                    down_arrow.set_fill(GREEN, opacity=1)
                    down_arrow.set_stroke(BLACK, width=1)
                    down_arrow.scale(scale)
                    down_arrow.rotate(PI, axis=RIGHT)  # mirror it vertically

                    if arrow_mode == "both":
                        down_arrow.next_to(up_arrow, DOWN, buff=0)

                    arrows.add(down_arrow)

                self.circle = circle
                self.arrow = arrows
                self.add(circle, arrows)

            def get_rotation_anim(self, angle=2 * PI, duration=2, rate_func=linear):
                return Rotating(
                    self.arrow,
                    angle=angle,
                    axis=UP,
                    run_time=duration,
                    rate_func=rate_func,
                )

        # Try different arrow modes:
        obj = Spinning3DArrowWithCircle(color=BLUE, arrow_mode="both").move_to(ORIGIN)

        self.add(obj)
        # self.play(obj.get_rotation_anim(angle=2 * PI, duration=3))
        self.wait()


class RiemannScene(Scene):
    def construct(self):
        self.shift_all = LEFT * 2  # Easy-to-modify offset

        # 1. Load image of Riemann
        # riemann_image = ImageMobject("riemann.png")  # Place your image file in the same folder
        # riemann_image.scale(2).to_edge(LEFT).shift(self.shift_all)

        # 2. Complex plane
        plane = ComplexPlane()
        plane.set_stroke(opacity=0.3)
        plane.shift(self.shift_all)

        # 3. Critical line at Re(z) = 1/2
        critical_line = Line(
            plane.n2p(complex(0.5, -3)),
            plane.n2p(complex(0.5, 3)),
            color=YELLOW,
            stroke_width=4,
        ).shift(self.shift_all)

        # 4. Dots on critical line (example)
        zeros_imag = [-2, -1, 0, 1, 2, 3]
        zero_dots = VGroup(
            *[Dot(point=plane.n2p(complex(0.5, y)), color=YELLOW) for y in zeros_imag]
        ).shift(self.shift_all)

        # 5. Prime numbers at top
        primes = [2, 3, 5, 7, 11, 13, 17]
        prime_tex = Tex(",".join(str(p) for p in primes) + ",\\dots")
        prime_tex.to_corner(UP + RIGHT).shift(self.shift_all + LEFT * 0.5)

        # Add everything to scene
        self.add(plane, critical_line, zero_dots, prime_tex)


class RiemannScene(Scene):
    def construct(self):

        plane = ComplexPlane(
            x_range=[-2, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.8,
                "stroke_width": 1,
            },
        ).scale(1)

        plane.add_coordinate_labels()

        # Visual glow around critical line
        highlight_strip = Rectangle(
            height=6, width=0.1, fill_color=YELLOW, fill_opacity=0.3, stroke_width=0
        ).move_to(plane.n2p(complex(0.5, 0)))

        critical_line = Line(
            plane.n2p(complex(0.5, -3)),
            plane.n2p(complex(0.5, 3)),
            color=YELLOW,
            stroke_width=4,
        )

        zeros_imag = [-2, -1, 0, 1, 2, 3]
        zero_dots = VGroup(
            *[Dot(point=plane.n2p(complex(0.5, y)), color=WHITE) for y in zeros_imag]
        )

        primes = [2, 3, 5, 7, 11, 13, 17]
        prime_tex = Tex(",".join(str(p) for p in primes) + ",\\dots")
        prime_tex.to_corner(UP + RIGHT)

        self.add(plane, highlight_strip, critical_line, zero_dots, prime_tex)


from manimlib import *


class RiemannScene(Scene):
    def construct(self):
        # --- Setup complex plane
        plane = ComplexPlane(
            x_range=[-2, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.8,
                "stroke_width": 1,
            },
        ).scale(1)

        # Shift the plane left if needed
        self.shift_all = LEFT * 2
        plane.shift(self.shift_all)

        # --- Zeta formula on top-left
        zeta_tex = (
            Tex(
                r"\zeta(s) = \frac{1}{1^s} + \frac{1}{2^s} + \frac{1}{3^s} + \frac{1}{4^s} + \cdots",
                tex_to_color_map={"s": YELLOW},
            )
            .scale(0.9)
            .to_corner(UL)
            .shift(DOWN * 0.5)
        )

        # --- Highlight strip
        highlight_strip = (
            Rectangle(
                height=8, width=0.1, fill_color=YELLOW, fill_opacity=0.3, stroke_width=0
            )
            .move_to(plane.n2p(complex(0.5, 0)))
            .shift(self.shift_all)
        )

        # --- Create line with growing animation
        critical_line = Line(
            plane.n2p(complex(0.5, 0)),
            plane.n2p(complex(0.5, 0)),
            color=YELLOW,
            stroke_width=4,
        ).shift(self.shift_all)

        # --- Prime number label (will grow)
        primes = [2, 3, 5, 7, 11, 13, 17]
        prime_tex = Tex("")  # start empty
        prime_tex.to_corner(UR).shift(self.shift_all + LEFT * 0.5)

        # --- Animation: add plane and zeta function
        self.play(Write(plane), FadeIn(zeta_tex))
        self.add(highlight_strip)
        self.play(GrowFromCenter(critical_line))

        # --- Animate line growing upward and downward
        for i in range(1, 5):
            new_line = Line(
                plane.n2p(complex(0.5, -i)),
                plane.n2p(complex(0.5, i)),
                color=YELLOW,
                stroke_width=4,
            ).shift(self.shift_all)
            self.play(Transform(critical_line, new_line), run_time=0.2)

        self.wait(0.3)

        # --- Animate primes + dots on the line
        dots = []
        for idx, prime in enumerate(primes):
            y_val = idx - 2  # center around 0
            dot = Dot(point=plane.n2p(complex(0.5, y_val)), color=WHITE).shift(
                self.shift_all
            )
            dots.append(dot)

            # Animate: grow dot and update prime label
            new_tex = Tex(",".join(str(p) for p in primes[: idx + 1]) + ",\\dots")
            new_tex.to_corner(UR).shift(self.shift_all + LEFT * 0.5)

            self.play(FadeIn(dot), Transform(prime_tex, new_tex), run_time=0.3)

        self.wait()

        # self.add(edges)
        # self.add(spheres)


from manimlib import *
import math
import itertools as it
import random


from manimlib import *
import math
import itertools as it
import random


class ShowCube(ThreeDScene):
    def construct(self):
        # Camera setup
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

        # Cube vertices and edges
        vert_coords = [(n % 2, (n // 2) % 2, (n // 4) % 2) for n in range(8)]
        verts = [axes.c2p(*coords) for coords in vert_coords]

        coord_labels = VGroup()
        coord_labels_2d = VGroup()

        # (Removed adding spheres and labels here)

        # Edge connections
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

        # 2D case setup
        frame.move_to(1.5 * UP)
        self.add(plane)
        self.play(
            # LaggedStartMap(FadeIn, coord_labels_2d),
            # Skip spheres[:4]
            LaggedStartMap(GrowFromCenter, edges[:4]),
        )
        self.wait()

        # Transition to 3D cube
        frame.generate_target()
        frame.target.set_euler_angles(-25 * DEGREES, 70 * DEGREES)
        frame.target.move_to([1, 2, 0])
        frame.target.set_height(10)

        rf = squish_rate_func(smooth, 0.5, 1)
        to_grow = Group(*edges[4:], *coord_labels[4:])
        to_grow.save_state()
        to_grow.set_depth(0, about_edge=IN, stretch=True)

        self.play(
            MoveToTarget(frame),
            ShowCreation(axes.z_axis),
            Restore(to_grow, rate_func=rf),
            # FadeOut(coord_labels_2d, rate_func=rf),
            # *[
            #     FadeInFromPoint(
            #         cl, cl2.get_center(), rate_func=squish_rate_func(smooth, 0.5, 1)
            #     )
            #     for cl, cl2 in zip(coord_labels[:4], coord_labels_2d)
            # ],
            run_time=3,
        )

        # Camera rotation
        frame.start_time = self.time
        frame.scene = self
        frame.add_updater(
            lambda m: m.set_theta(
                -25 * DEGREES * math.cos((m.scene.time - m.start_time) * PI / 60)
            )
        )

        self.add(axes.z_axis)
        self.add(edges)

        # Skip the highlight animation
        self.play(LaggedStart(run_time=2, lag_ratio=0.1))


class NothingScene2(Scene):
    def construct(self):

        t1 = (
            Text(
                "없다를 표현할 수 있다. 0",
                font="BM Hanna 11yrs Old",
            ).scale(1.2)
        ).shift(UP * 3)
        self.play(Write(t1))


class ZeroPhilosophy(Scene):
    def construct(self):
        lines = [
            "없다는 것을 표현하는 0",
            "자연수: 1, 2, 3 이 아니다",
            "실수: 0.23, \\pi, 5 가 아니다.",
            "복소수: 3 + 4i 가 아니다. \\,\\, 0 + 0i 이다.",
            "",
            "아무 것도 아닌 것의 대상이 바뀌고, 형태가 바뀐다.",
            "모양이 변하는 0은 \\textbf{발견한 것인가} \\textbf{발명한 것인가}?",
        ]

        text_objs = []
        for line in lines:
            if line.strip() == "":
                text_objs.append(None)
                continue
            t = Text(line, font="BM Hanna 11yrs Old").scale(1.2)
            text_objs.append(t)

        spacing = 0.9
        for i, t in enumerate(text_objs):
            if t is None:
                continue
            t.to_edge(UP).shift(DOWN * spacing * i)

        # Sequential animation
        for t in text_objs:
            if t is None:
                self.wait(0.3)
                continue
            self.play(FadeIn(t), run_time=1)
            self.wait(1)

        self.wait(2)


from manimlib import *


class ZeroPhilosophy(Scene):
    def construct(self):
        lines = [
            ("text", "없다는 것을 표현하는 0"),
            ("text", "자연수: 1, 2, 3 이 아니다"),
            ("tex", r"\text{실수:} 0.23, \pi, 5 \text{ 가 아니다.}"),
            (
                "tex",
                r"\text{복소수:} 3 + 4i \text{ 가 아니다. } \quad 0 + 0i \text{ 이다.}",
            ),
            ("text", ""),  # spacer
            ("text", "아무 것도 아닌 것의 대상이 바뀌고, 형태가 바뀐다."),
            (
                "tex",
                r"\text{모양이 변하는 0은 } \textbf{발견한 것인가} \quad \textbf{발명한 것인가}?",
            ),
        ]

        text_objs = []
        for mode, line in lines:
            if line.strip() == "":
                text_objs.append(None)
                continue

            if mode == "tex":
                t = Tex(line).scale(0.9)
            else:
                t = Text(line, font="BM Hanna 11yrs Old").scale(1.2)

            text_objs.append(t)

        # Positioning
        spacing = 1.1
        for i, t in enumerate(text_objs):
            if t is None:
                continue
            t.to_edge(UP).shift(DOWN * spacing * i)

        # Sequential animation
        for t in text_objs:
            if t is None:
                self.wait(0.3)
                continue
            self.play(FadeIn(t), run_time=1)
            self.wait(1)

        self.wait(2)


from manimlib import *


class ZeroPhilosophy(Scene):
    def construct(self):
        lines = [
            "없다는 것을 표현하는 0",
            "자연수: 1, 2, 3 이 아니다",
            r"실수: 0.23, \pi, 5 가 아니다.",
            "복소수: 3 + 4i 가 아니다.   0 + 0i 이다.",
        ]

        text_objs = []
        for i, line in enumerate(lines):
            if line.strip() == "":
                text_objs.append(None)
                continue

            # Only line 2 (index 2) uses LaTeX
            if i == 2:
                text_pre = Text("실수: 0.23,", font="BM Hanna 11yrs Old").scale(1.2)
                pi_tex = Tex(r"\pi").scale(1.2)
                text_post = Text(", 5 가 아니다.", font="BM Hanna 11yrs Old").scale(1.2)

                # 나란히 배치
                pi_line = VGroup(text_pre, pi_tex, text_post)
                pi_line.arrange(RIGHT, buff=0.1)
                t = pi_line
            else:
                t = Text(line, font="BM Hanna 11yrs Old").scale(1.2)

            text_objs.append(t)

        # Positioning from top
        spacing = 1.1
        for i, t in enumerate(text_objs):
            if t is None:
                continue
            t.shift(UP * 2).shift(DOWN * spacing * i)

        # Animate sequentially
        for t in text_objs:
            if t is None:
                self.wait(0.3)
                continue
            self.play(FadeIn(t), run_time=1)
            self.wait(1)

        self.wait(2)


from manimlib import *


class ZeroPhilosophy(Scene):
    def construct(self):
        COLOR_MAP = {
            "자연수": RED,
            "실수": GREEN,
            "복소수": BLUE,
        }

        # Line content (first line is title)
        lines = [
            ("title", "없다는 것을 표현하는 0"),
            ("text", "자연수: 1, 2, 3 이 아니다"),
            ("mixed", r"실수: 0.23, \pi, 5 가 아니다."),
            ("text", "복소수: 3 + 4i 가 아니다.   0 + 0i 이다."),
        ]

        text_objs = []
        colon_x = None  # we'll use this to align all ":" positions

        for i, (mode, content) in enumerate(lines):
            if mode == "title":
                t = Text(content, font="BM Hanna 11yrs Old").scale(1.6)
            elif mode == "text":
                keyword, rest = content.split(":", 1)
                keyword_text = Text(keyword + ":", font="BM Hanna 11yrs Old").scale(1.2)
                keyword_text.set_color(COLOR_MAP.get(keyword, WHITE))
                rest_text = Text(rest.strip(), font="BM Hanna 11yrs Old").scale(1.2)

                t = VGroup(keyword_text, rest_text)
                t.arrange(RIGHT, buff=0.3)

            elif mode == "mixed":
                keyword, rest = content.split(":", 1)
                keyword_text = Text(keyword + ":", font="BM Hanna 11yrs Old").scale(1.2)
                keyword_text.set_color(COLOR_MAP.get(keyword, WHITE))

                pre, post = rest.split("\\pi")
                text_pre = Text(pre.strip(), font="BM Hanna 11yrs Old").scale(1.2)
                pi_tex = Tex(r"\pi").scale(1.2)
                text_post = Text(post.strip(), font="BM Hanna 11yrs Old").scale(1.2)

                rest_group = VGroup(text_pre, pi_tex, text_post)
                rest_group.arrange(RIGHT, buff=0.1)

                t = VGroup(keyword_text, rest_group)
                t.arrange(RIGHT, buff=0.3)

            text_objs.append(t)

        # Step 1: Set all x positions so ":" are aligned
        # First, find x position of each ':' character
        colon_positions = []
        for t in text_objs[1:]:  # skip title
            if isinstance(t, VGroup):
                keyword_text = t[0]
                for submob in keyword_text:
                    if ":" in submob.get_text():
                        colon_positions.append(submob.get_center()[0])

        if colon_positions:
            colon_x = sum(colon_positions) / len(colon_positions)

        # Step 2: shift everything so colons line up
        for t in text_objs[1:]:  # skip title
            if isinstance(t, VGroup):
                keyword_text = t[0]
                for submob in keyword_text:
                    if ":" in submob.get_text():
                        shift_amount = colon_x - submob.get_center()[0]
                        t.shift(RIGHT * shift_amount)

        # Step 3: Position vertically
        spacing = 1.1
        y_start = 2.5
        for i, t in enumerate(text_objs):
            if i == 0:
                t.move_to(UP * y_start)
            else:
                t.next_to(text_objs[i - 1], DOWN, buff=spacing)

        # Animate
        for t in text_objs:
            self.play(FadeIn(t), run_time=1)
            self.wait(1)

        self.wait(2)


from manimlib import *


class ZeroPhilosophy(Scene):
    def construct(self):
        # Title
        title = Text("없다는 것을 표현하는 0", font="BM Hanna 11yrs Old").scale(1.6)
        title.move_to(UP * 2.5)

        # 자연수 줄
        line1 = Text("자연수: 1, 2, 3 이 아니다", font="BM Hanna 11yrs Old").scale(1.2)
        line1.set_color_by_text("자연수", RED)

        # 실수 줄 (with \pi)
        keyword2 = Text("실수:", font="BM Hanna 11yrs Old").scale(1.2).set_color(GREEN)
        pre2 = Text("0.23,", font="BM Hanna 11yrs Old").scale(1.2)
        pi = Tex(r"\pi").scale(1.2)
        post2 = Text(", 5 가 아니다.", font="BM Hanna 11yrs Old").scale(1.2)

        line2 = VGroup(keyword2, pre2, pi, post2).arrange(RIGHT, buff=0.15)

        # 복소수 줄
        line3 = Text(
            "복소수: 3 + 4i 가 아니다.   0 + 0i 이다.", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        line3.set_color_by_text("복소수", BLUE)

        # Align colons
        colon_ref = keyword2  # 기준이 될 콜론
        line1[0].align_to(colon_ref, LEFT)
        line3[0].align_to(colon_ref, LEFT)

        # Positioning
        line1.next_to(title, DOWN, buff=1.0)
        line2.next_to(line1, DOWN, buff=0.9)
        line3.next_to(line2, DOWN, buff=0.9)

        # Animation
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeIn(line1))
        self.wait(1)
        self.play(FadeIn(line2))
        self.wait(1)
        self.play(FadeIn(line3))
        self.wait(2)


from manimlib import *


class ZeroPhilosophy(Scene):
    def construct(self):
        # Title (크게, 위에 위치)
        title = Text("없다는 것을 표현하는 0", font="BM Hanna 11yrs Old").scale(1.6)
        title.to_edge(U).shift(DOWN * 0.5)

        # 자연수 줄
        line1 = Text("자연수: 1, 2, 3 이 아니다", font="BM Hanna 11yrs Old").scale(1.2)
        line1.set_color_by_text("자연수", RED)
        line1.next_to(title, DOWN, aligned_edge=LEFT, buff=1)

        # 실수 줄 (with \pi)
        keyword2 = Text("실수:", font="BM Hanna 11yrs Old").scale(1.2).set_color(GREEN)
        pre2 = Text("0.23,", font="BM Hanna 11yrs Old").scale(1.2)
        pi = Tex(r"\pi").scale(1.2)
        post2 = Text(", 5 가 아니다.", font="BM Hanna 11yrs Old").scale(1.2)

        line2 = VGroup(keyword2, pre2, pi, post2).arrange(RIGHT, buff=0.15)
        line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.9)

        # 복소수 줄
        line3 = Text(
            "복소수: 3 + 4i 가 아니다.   0 + 0i 이다.", font="BM Hanna 11yrs Old"
        ).scale(1.2)
        line3.set_color_by_text("복소수", BLUE)
        line3.next_to(line2, DOWN, aligned_edge=LEFT, buff=0.9)

        # 애니메이션
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeIn(line1))
        self.wait(1)
        self.play(FadeIn(line2))
        self.wait(1)
        self.play(FadeIn(line3))
        self.wait(2)


from manimlib import *


class EntropyParticlesWithRadius(Scene):
    def construct(self):
        boundary_width = 6
        boundary_height = 4
        radius = 0.08

        # 경계 박스
        boundary = Rectangle(width=boundary_width, height=boundary_height, color=WHITE)
        self.add(boundary)

        num_particles = 15
        particles = VGroup()
        velocities = []

        for _ in range(num_particles):
            x = random.uniform(
                -boundary_width / 2 + radius, boundary_width / 2 - radius
            )
            y = random.uniform(
                -boundary_height / 2 + radius, boundary_height / 2 - radius
            )
            dot = Dot(point=np.array([x, y, 0]), radius=radius, color=YELLOW)
            particles.add(dot)

            vx = random.uniform(-0.05, 0.05)
            vy = random.uniform(-0.05, 0.05)
            velocities.append(np.array([vx, vy, 0]))

        self.add(particles)

        def update_particles(mob, dt):
            for i, dot in enumerate(mob):
                dot.shift(velocities[i])
                pos = dot.get_center()

                # X축 튕김 (경계에서 radius만큼 안쪽에서 반사)
                if abs(pos[0]) > (boundary_width / 2 - radius):
                    velocities[i][0] *= -1
                    dot.shift(velocities[i])

                # Y축 튕김
                if abs(pos[1]) > (boundary_height / 2 - radius):
                    velocities[i][1] *= -1
                    dot.shift(velocities[i])

        particles.add_updater(update_particles)
        self.add(particles)

        self.wait(6)


from manimlib import *
import random
import numpy as np


from manimlib import *


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

        up_s = UP * 1.3  # vertical offset for dog image

        # Draw line

        line = Line(start, end, color=YELLOW, stroke_width=7)
        bones = (
            ImageMobject("/Users/eugenekim/projects/dance-with/first-project/bones.png")
            .scale(0.5)
            .next_to(end, RIGHT)
        )

        self.play(FadeIn(line), FadeIn(bones))

        # Goal label and dog bones

        # Load transparent dog image
        character = ImageMobject(
            "/Users/eugenekim/projects/dance-with/first-project/dog-zeno.png"
        ).scale(0.5)
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
        ).scale(1.2)

        t2.next_to(t1, DOWN * 1.3)

        self.play(Write(t2))
        self.wait(1)

        t3 = Text(
            "몇번을 쪼개서 보든, 전체 시간은 정해져 있다",
            font="BM Hanna 11yrs Old",
        ).scale(1.2)

        t3.next_to(t2, DOWN * 1.3)
        t3.set_color_by_text("", BLUE)

        self.play(Write(t3))
        self.wait(1)


from manim import *
import random
import math

from manimlib import *


class PrisonerDilemmaMatrix(Scene):
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
        diagonals = VGroup()
        for i in range(2):
            for j in range(2):
                start = grid[i * 2 + j].get_corner(UL)
                end = grid[i * 2 + j].get_corner(DR)
                line = Line(start, end, stroke_opacity=0.4)
                diagonals.add(line)
        self.add(diagonals)

        # Payoff labels
        payoffs = [
            ("5", "5"),
            ("1", "10"),
            ("10", "1"),
            ("2", "2"),
        ]
        labels = VGroup()
        for idx, (a, b) in enumerate(payoffs):
            cell = grid[idx]
            a_text = Text(a, fill_color=YELLOW).scale(1)
            b_text = Text(b, fill_color=GREEN).scale(1)

            a_text.next_to(cell.get_corner(DL), direction=UP + RIGHT, buff=0.2)
            b_text.next_to(cell.get_corner(UR), direction=DOWN + LEFT, buff=0.2)

            labels.add(a_text, b_text)

        self.add(labels)

        # 죄수 A title
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

        self.add(a_title.next_to(a_actions, LEFT))
        self.add(a_actions)

        # 죄수 B title
        b_title = Text("죄수 B", fill_color=GREEN, font="BM Hanna 11yrs Old").scale(1.1)
        b_actions = (
            VGroup(
                Text("배신", font="BM Hanna 11yrs Old"),
                Text("협력", font="BM Hanna 11yrs Old"),
            )
            .arrange(RIGHT, buff=2)
            .next_to(grid, UP)
        )

        self.add(b_title.next_to(b_actions, UP * 1.5))
        self.add(b_actions)


from manim import *


class PrisonerDilemmaWithNash(Scene):
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
        diagonals = VGroup()
        for i in range(2):
            for j in range(2):
                start = grid[i * 2 + j].get_corner(UL)
                end = grid[i * 2 + j].get_corner(DR)
                line = Line(start, end, stroke_opacity=0.4)
                diagonals.add(line)
        self.add(diagonals)

        # Payoff labels
        payoffs = [
            ("5", "5"),
            ("1", "10"),
            ("10", "1"),
            ("2", "2"),
        ]
        labels = VGroup()
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
            labels.add(a_text, b_text)

        self.add(labels)

        # 죄수 A title
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

        self.add(a_title.next_to(a_actions, LEFT))
        self.add(a_actions)

        # 죄수 B title
        b_title = Text("죄수 B", fill_color=GREEN, font="BM Hanna 11yrs Old").scale(1.1)
        b_actions = (
            VGroup(
                Text("배신", font="BM Hanna 11yrs Old"),
                Text("협력", font="BM Hanna 11yrs Old"),
            )
            .arrange(RIGHT, buff=2)
            .next_to(grid, UP)
        )

        self.add(b_title.next_to(b_actions, UP * 1.5))
        self.add(b_actions)

        # --- Player B's best response animation

        # Case 1: A 배신 (row 0, grid[0] and grid[1])
        row0 = VGroup(grid[0], grid[1], a_texts[0], b_texts[0], a_texts[1], b_texts[1])
        # self.play(row0.set_opacity, 0.2)
        self.play(row0.animate.set_opacity(0.2))

        self.wait(0.5)

        highlight_b0 = SurroundingRectangle(b_texts[0], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b0))
        self.wait(1)
        self.play(FadeOut(highlight_b0))
        self.play(row0.animate.set_opacity(1))
        # self.play(row0.set_opacity, 1)

        # Case 2: A 협력 (row 1, grid[2] and grid[3])
        row1 = VGroup(grid[2], grid[3], a_texts[2], b_texts[2], a_texts[3], b_texts[3])
        # self.play(row1.set_opacity, 0.2)
        self.play(row1.animate.set_opacity(0.2))

        self.wait(0.5)

        highlight_b3 = SurroundingRectangle(b_texts[3], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b3))
        self.wait(1)
        self.play(FadeOut(highlight_b3))
        # self.play(row1.set_opacity, 1)
        self.play(row1.animate.set_opacity(1))

        # --- Player A's best response animation

        # Case 1: B 배신 (col 0, grid[0] and grid[2])
        col0 = VGroup(grid[0], grid[2], a_texts[0], b_texts[0], a_texts[2], b_texts[2])
        # self.play(col0.set_opacity, 0.2)
        self.play(col0.animate.set_opacity(0.2))

        self.wait(0.5)

        highlight_a0 = SurroundingRectangle(a_texts[0], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a0))
        self.wait(1)
        self.play(FadeOut(highlight_a0))
        # self.play(col0.set_opacity, 1)
        self.play(col0.animate.set_opacity(1))

        # Case 2: B 협력 (col 1, grid[1] and grid[3])
        col1 = VGroup(grid[1], grid[3], a_texts[1], b_texts[1], a_texts[3], b_texts[3])
        # self.play(col1.set_opacity, 0.2)
        self.play(col1.animate.set_opacity(0.2))

        self.wait(0.5)

        highlight_a3 = SurroundingRectangle(a_texts[3], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a3))
        self.wait(1)
        self.play(FadeOut(highlight_a3))
        # self.play(col1.set_opacity, 1)
        self.play(col1.animate.set_opacity(1))

        self.wait(2)


from manim import *


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

        # --- Player B's best response animation

        # Case 1: A 배신 (grid[0] vs grid[1])
        self.wait(0.5)
        self.play(b_texts[1].animate.set_opacity(0.2))
        highlight_b0 = SurroundingRectangle(b_texts[0], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b0))
        self.wait(1)
        self.play(FadeOut(highlight_b0), b_texts[1].animate.set_opacity(1))

        # Case 2: A 협력 (grid[2] vs grid[3])
        self.wait(0.5)
        self.play(b_texts[2].animate.set_opacity(0.2))
        highlight_b3 = SurroundingRectangle(b_texts[3], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b3))
        self.wait(1)
        self.play(FadeOut(highlight_b3), b_texts[2].animate.set_opacity(1))

        # --- Player A's best response animation

        # Case 1: B 배신 (grid[0] vs grid[2])
        self.wait(0.5)
        self.play(a_texts[2].animate.set_opacity(0.2))
        highlight_a0 = SurroundingRectangle(a_texts[0], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a0))
        self.wait(1)
        self.play(FadeOut(highlight_a0), a_texts[2].animate.set_opacity(1))

        # Case 2: B 협력 (grid[1] vs grid[3])
        self.wait(0.5)
        self.play(a_texts[1].animate.set_opacity(0.2))
        highlight_a3 = SurroundingRectangle(a_texts[3], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a3))
        self.wait(1)
        self.play(FadeOut(highlight_a3), a_texts[1].animate.set_opacity(1))

        self.wait(2)


from manim import *


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
        self.wait(0.5)
        self.play(row_highlights[0].animate.set_fill(opacity=0.7))
        highlight_b0 = SurroundingRectangle(b_texts[0], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b0))
        self.wait(1)
        self.play(FadeOut(highlight_b0), row_highlights[0].animate.set_fill(opacity=0))

        self.wait(0.5)
        self.play(row_highlights[1].animate.set_fill(opacity=0.7))
        highlight_b3 = SurroundingRectangle(b_texts[3], color=GREEN, buff=0.15)
        self.play(FadeIn(highlight_b3))
        self.wait(1)
        self.play(FadeOut(highlight_b3), row_highlights[1].animate.set_fill(opacity=0))

        # --- Player A's best response animation
        self.wait(0.5)
        self.play(col_highlights[0].animate.set_fill(opacity=0.7))
        highlight_a0 = SurroundingRectangle(a_texts[0], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a0))
        self.wait(1)
        self.play(FadeOut(highlight_a0), col_highlights[0].animate.set_fill(opacity=0))

        self.wait(0.5)
        self.play(col_highlights[1].animate.set_fill(opacity=0.7))
        highlight_a3 = SurroundingRectangle(a_texts[3], color=YELLOW, buff=0.15)
        self.play(FadeIn(highlight_a3))
        self.wait(1)
        self.play(FadeOut(highlight_a3), col_highlights[1].animate.set_fill(opacity=0))

        self.wait(2)


from manim import *


class DilemmaTopics(Scene):
    def construct(self):
        # Title
        title = Tex(r"1 + 1 = -1").scale(1.5)

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
        ]

        text_lines = VGroup()
        for i, item in enumerate(items):
            line = Text(item, font="BM Hanna 11yrs Old").scale(1.1)
            if i % 2 == 1:
                line.set_fill(GREY)
            text_lines.add(line)

        text_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        text_lines.next_to(title, DOWN * 2, aligned_edge=LEFT).shift(LEFT * 2)

        # Animate each line appearing
        for line in text_lines:
            self.play(FadeIn(line), run_time=0.5)

        self.wait(2)
