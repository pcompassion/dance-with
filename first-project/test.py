#!/usr/bin/env python

from manimlib import *
from src.mobject.clock import Clock
from functools import partial
import math
import itertools as it
import random


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

        # Add and animate one by one
        # self.play(
        #     *[FadeIn(seg, run_time=0.3) for seg in segments],
        #     lag_ratio=0.1,
        # )
        # plane_g.rotate(
        #     angle=PI / 6,       # rotation angle
        #     axis=UP,         # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
        #     about_point=plane.c2p(0,0,0)  # pivot point
        # )

        # Optional: camera rotation to give "depth"


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

        plane.get_x_axis().set_stroke(BLUE)

        self.wait()


class StickMan(VGroup):
    def __init__(self, radius=0.3, height=1.2, leg_length=0.5, color=WHITE, **kwargs):
        super().__init__(**kwargs)

        self.body_bottom = ORIGIN + DOWN * (height / 2)
        self.rotation_angle = 0

        # Head
        head = Circle(radius=radius, color=color).shift(UP * (height / 2 + radius))

        # Body
        body = Line(start=ORIGIN + UP * (height / 2), end=self.body_bottom, color=color)

        # Legs
        self.left_leg = Line(
            start=self.body_bottom,
            end=self.body_bottom + DOWN * leg_length + LEFT * leg_length * 0.5,
            color=color,
        )
        self.right_leg = Line(
            start=self.body_bottom,
            end=self.body_bottom + DOWN * leg_length + RIGHT * leg_length * 0.5,
            color=color,
        )

        self.add(head, body, self.left_leg, self.right_leg)

    def walk_to(self, scene, axes, point, duration=2):
        """
        Animate walking to a 3D point, with bounce and swinging legs.
        """
        start = self.get_center()
        end = axes.c2p(*point)

        # Bounce function
        bounce = lambda t: 0.1 * np.sin(4 * PI * t)

        # Leg swing function
        swing_angle = lambda t: 0.4 * np.sin(8 * PI * t)  # back and forth motion

        def walk_updater(mob, alpha):
            new_point = interpolate(start, end, alpha)
            offset = bounce(alpha) * UP
            mob.move_to(new_point + offset)

            # Reset legs before reapplying swing
            self.left_leg.become(
                Line(
                    start=self.body_bottom,
                    end=self.body_bottom + self.down * 0.5 + self.left * 0.25,
                    color=self.left_leg.get_color(),
                )
            )
            self.right_leg.become(
                Line(
                    start=self.body_bottom,
                    end=self.body_bottom + self.down * 0.5 + self.right * 0.25,
                    color=self.right_leg.get_color(),
                )
            )

            # Apply swing
            self.left_leg.rotate(swing_angle(alpha), about_point=self.body_bottom)
            self.right_leg.rotate(-swing_angle(alpha), about_point=self.body_bottom)

        # Animate
        scene.play(
            UpdateFromAlphaFunc(self, walk_updater), run_time=duration, rate_func=linear
        )


class StickManWalkScene(ThreeDScene):
    def construct(self):

        class StickMan(VGroup):
            def __init__(
                self, radius=0.3, height=1.2, leg_length=0.5, color=WHITE, **kwargs
            ):
                super().__init__(**kwargs)
                self.facing_right = True  # Default facing direction
                self.rotation_angle = 0

                self.body_bottom = ORIGIN + DOWN * (height / 2)

                # Head
                self.head = Circle(radius=radius, color=color).shift(
                    UP * (height / 2 + radius)
                )

                # Body
                self.body = Line(
                    start=ORIGIN + UP * (height / 2), end=self.body_bottom, color=color
                )

                self.body_length = self.body_bottom - ORIGIN + UP * (height / 2)

                # Legs
                self.left_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + DOWN * leg_length + LEFT * leg_length * 0.5,
                    color=color,
                )
                self.right_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + DOWN * leg_length + RIGHT * leg_length * 0.5,
                    color=color,
                )

                self.add(self.head, self.body, self.left_leg, self.right_leg)

            def get_body_bottom(self):
                return (
                    self.body.get_end()
                )  # returns the bottom of the torso in world space

            def move_to_feet(self, target_point):
                shift = np.array(target_point) - self.get_body_bottom()
                self.shift(shift)

            def flip_horizontally(self):
                flip_matrix = np.array(
                    [
                        [-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                    ]
                )
                self.apply_matrix(flip_matrix)

            def face_point(self, target_point):
                my_x = self.get_center()[0]
                target_x = target_point[0]
                should_face_right = target_x >= my_x

                if self.facing_right != should_face_right:
                    self.flip_horizontally()
                    self.facing_right = should_face_right

            def wave(self, scene, times=2, angle=PI / 6):
                """Simple wave animation with head tilt."""

                head = self.head
                for _ in range(times):
                    scene.play(
                        Rotate(
                            head, angle=angle, axis=IN, about_point=head.get_center()
                        ),
                        run_time=0.2,
                    )
                    scene.play(
                        Rotate(
                            head, angle=-angle, axis=IN, about_point=head.get_center()
                        ),
                        run_time=0.2,
                    )

            def walk_to(self, scene, axes, point, duration=2):
                start = self.get_body_bottom()
                end = axes.c2p(*point)

                self.face_point(end)

                bounce = lambda t: 0.05 * np.sin(8 * PI * t)
                swing_angle = lambda t: 0.4 * np.sin(8 * PI * t)

                dummy = VMobject()  # ghost object to time animation

                def update_mob(mob, alpha):
                    # === Movement ===
                    foot_pos = interpolate(start, end, alpha)
                    bounce_offset = bounce(alpha) * UP

                    # Lean angle

                    lean_direction = 1 if self.facing_right else -1
                    lean = lean_direction * interpolate(0, -PI / 16, np.sin(PI * alpha))

                    # Move + rotate the entire group
                    self.move_to(foot_pos + UP * 0.6 + bounce_offset)
                    self.rotate(
                        lean - self.rotation_angle,
                        axis=OUT,
                        about_point=self.get_body_bottom(),
                    )
                    self.rotation_angle = lean  # track current lean to rotate delta

                    # === Legs ===
                    body_bottom = self.get_body_bottom()
                    self.left_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + DOWN * 0.5 + LEFT * 0.25,
                            color=self.left_leg.get_color(),
                        )
                    )
                    self.right_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + DOWN * 0.5 + RIGHT * 0.25,
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

        # Walk right

        axes = ThreeDAxes()
        self.add(axes)

        axes.rotate(
            angle=PI / 6,  # rotation angle
            axis=UP,  # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
            about_point=axes.c2p(0, 0, 0),  # pivot point
        )

        man = StickMan()
        man.move_to_feet(axes.c2p(0, 0, 0))
        self.add(man)

        frame = self.camera.frame
        frame.save_state()

        frame.set_euler_angles(
            theta=0, phi=0, gamma=0
        )  # φ = π/2.5 ≈ 72° (slightly tilted)

        man.walk_to(self, axes, point=(3, 0, 0), duration=3)
        self.wait(0.1)

        # # Wave hello
        # man.wave(self, times=2)

        # Walk left
        man.walk_to(self, axes, point=(-3, 0, 0), duration=3)
        self.wait(1)

        man.walk_to(self, axes, point=(4, 4, 0), duration=3)
        self.wait(1)


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma, theta=PI / 6, phi=0):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_peak = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            mountain_height = pdf_peak * earth_radius
            r_base = earth_radius - 0.95 * mountain_height

            cutoff_radius = 2 * sigma  # 95% 확률질량이 포함되는 반지름 범위

            def surface_fn(u, v):
                r = v * cutoff_radius
                height_profile = mountain_height * np.exp(-(r**2) / (2 * sigma**2))

                x_local = r * np.cos(u)
                y_local = r * np.sin(u)
                z_local = height_profile

                direction = np.array(
                    [
                        np.cos(theta) * np.cos(phi),
                        np.cos(theta) * np.sin(phi),
                        np.sin(theta),
                    ]
                )
                base_point = r_base * direction

                up = direction
                right = np.cross(np.array([0, 0, 1]), up)
                if np.linalg.norm(right) < 1e-6:
                    right = np.array([1, 0, 0])
                right /= np.linalg.norm(right)
                forward = np.cross(up, right)

                preliminary_point = (
                    base_point + x_local * right + y_local * forward + z_local * up
                )
                ray_dir = preliminary_point / np.linalg.norm(preliminary_point)
                projected_height = np.dot(preliminary_point, ray_dir)
                true_height = projected_height - earth_radius
                point = ray_dir * (earth_radius + true_height)
                return point

            return surface_fn, 1

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        # 여러 랜덤 산 생성
        num_mountains = 40
        mountains = Group()
        for i in range(num_mountains):

            sigma = np.random.uniform(0.6, 0.8)

            theta = np.random.normal(
                loc=PI - PI / 7, scale=PI / 5.5
            )  # 평균 PI, 90% 정도가 PI±PI/3 안에  # 앞쪽 적도 근처 범위       # 위도 범위
            phi = np.random.normal(
                loc=PI / 2 + PI / 6, scale=PI / 5.5
            )  # 평균 PI/2, 정면 중심  # 카메라 정면 중심         # 경도 범위

            surface_fn, max_radius = rotated_normal_mountain_generator(
                sigma, theta, phi
            )
            mountain = ParametricSurface(
                surface_fn,
                u_range=[0, TAU],
                v_range=[0, max_radius],
                resolution=(50, 20),
            )

            color = interpolate_color(BLUE_D, BLACK, 1 / num_mountains)

            mountain.set_color(color)
            mountain.set_opacity(0.9)

            self.play(FadeIn(mountain), run_time=2 / num_mountains)

            self.play(
                earth.animate.set_color(
                    interpolate_color(BLUE_E, GREY_D, 1 / num_mountains * i)
                ),
                run_time=1 / num_mountains,
            )
            mountains.add(mountain)

        self.wait(1)

        for mountain in mountains:
            self.play(mountain.animate.set_color(GREY_C), run_time=4 / num_mountains)


class Siddhartha3DWave(ThreeDScene):
    def construct(self):

        frame = self.camera.frame

        frame.set_euler_angles(
            phi=60 * DEGREES, theta=-20 * DEGREES
        )  # φ = π/2.5 ≈ 72° (slightly tilted)

        # Wave surface: like a flowing ribbon
        def wave_surface(u, v):
            x = u
            y = v  # slight width to the ribbon
            z = 0.2 * math.sin(u * 2)
            return np.array([x, y, z])

        surface = ParametricSurface(
            lambda u, v: np.array([u, v, 0.2 * math.sin(u * 2)]),
            u_range=[-10, 20],
            v_range=[-10, 10],
            resolution=(100, 10),
            # fill_opacity=0.6,
            # checkerboard_colors=[BLUE_D, BLUE_E],
        )

        surface.set_color(BLUE_D).set_opacity(0.6)

        # Quote and name
        quote = Text("강은 어디에나 동시에 존재한다.", font="BM Hanna 11yrs Old").scale(
            1.4
        )
        quote.set_color(BLUE_A).to_edge(UP)

        name = Text("– 싯다르타", font="BM Hanna 11yrs Old").scale(1.1)
        name.set_color(GREY_B).next_to(quote, DOWN, buff=0.3)

        # Add everything
        self.add(quote, name)
        self.add(surface)
        # self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)


class SinglePyramidScene(ThreeDScene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(phi=-15 * DEGREES, theta=0 * DEGREES)

        # === Add coordinate system ===
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)

        axes.rotate(
            angle=PI / 6,
            axis=UP,
            about_point=axes.c2p(0, 0, 0),
        )

        axes.add_coordinate_labels()

        # === Local helper: vertical text label ===
        def make_vertical_label(text_str, z_pos):
            txt = Text(text_str).scale(0.3)
            # txt.rotate(PI / 2, axis=RIGHT)  # make it vertical in Z
            txt.move_to(ORIGIN + UP * z_pos)
            return txt

        # === Local helper: pyramid ===
        def build_pyramid(label, layers, inverted=False):
            base_size = 2
            height = 2
            base = Square(side_length=base_size).set_color(GREY).set_opacity(0.4)
            base.rotate(PI / 2, axis=RIGHT)
            apex = ORIGIN + UP * height
            corners = base.get_vertices()

            face_colors = [RED, GREEN, BLUE, YELLOW]
            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_colors[i], opacity=0.4)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            # Layer labels
            level_texts = VGroup()
            for i, txt in enumerate(layers):
                z = (i - 1) * 0.8
                level_texts.add(make_vertical_label(txt, z))

            # title = Text(label).scale(0.4).next_to(base, DOWN)

            return VGroup(pyramid, level_texts)

        # === Create one pyramid at specific position ===
        math_pyramid = build_pyramid(
            label="Math", layers=["Division", "Set/Logic", "Mathematics"]
        )
        math_pyramid.move_to(ORIGIN)  # place it on x-y plane at origin
        self.add(math_pyramid)


class SinglePyramidScene(ThreeDScene):
    def construct(self):
        frame = self.camera.frame
        phi = 75
        theta = 0

        frame.save_state()
        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.move_to(axes.c2p(0, 0, 1))  # center on curve

        frame.set_width(10)  # or whatever width fits your pyramids

        # === Add coordinate system ===
        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 6, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)

        axes.add_coordinate_labels()

        # === Local helper: vertical text label ===
        def make_vertical_label(text_str, base_center, z_pos):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(0.8)
            txt.rotate(PI / 2, axis=RIGHT)  # Stand it up in Z-direction

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(
                0, 0, 0
            )  # a proper unit vector in rotated space
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        # === Local helper: pyramid ===
        def build_pyramid(label, layers, base_pos=ORIGIN, inverted=False, color=GREY):

            base_size = 4
            height = 4

            base = Square(side_length=base_size).set_color(color).set_opacity(0.4)

            base.move_to(base_pos)
            z_dir = axes.c2p(0, 0, 1) - axes.c2p(
                0, 0, 0
            )  # a proper unit vector in rotated space

            apex = base.get_center() + z_dir * height
            corners = base.get_vertices()
            face_color = TEAL
            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_color, opacity=0.2)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            print("base_center", base_center)
            level_texts = VGroup()
            for i, txt in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = height - z
                level_texts.add(make_vertical_label(txt, base_center, z))

            return VGroup(pyramid, level_texts)

        diff = 5

        math_pyramid = build_pyramid(
            label="Math",
            layers=["Set/논리", "Axiom", "수학"],
            base_pos=axes.c2p(0, 0, 0),
            color=GREY,
        )
        physics_pyramid = build_pyramid(
            label="Math",
            layers=["입자/에너지/정보", "최소단위", "물리"],
            base_pos=axes.c2p(diff, 0, 0),
            color=GREY,
        )

        darwin_pyramid = build_pyramid(
            label="Darwin",
            layers=["자연선택/변화/생존", "개체, 유전자", "진화"],
            base_pos=axes.c2p(diff * 2, 0, 0),
            color=BLUE,
        )
        econ_pyramid = build_pyramid(
            label="Darwin",
            layers=["self interest/이익", "개인", "경제"],
            base_pos=axes.c2p(diff * 3, 0, 0),
            color=BLUE,
        )

        hindu_pyramid = build_pyramid(
            label="Darwin",
            layers=["개인이 우주", "", "힌두"],
            base_pos=axes.c2p(diff * 0, 4, 0),
            color=BLUE,
            inverted=True,
        )

        self.add(
            math_pyramid, physics_pyramid, darwin_pyramid, econ_pyramid, hindu_pyramid
        )

        # frame.restore()


class SinglePyramidScene(ThreeDScene):
    def construct(self):
        frame = self.camera.frame
        phi = 75
        theta = 0

        # === Add coordinate system ===
        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 6, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)
        axes.add_coordinate_labels()

        # Camera initial state and animation
        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.set_width(10)
        self.play(frame.animate.move_to(axes.c2p(0, 0, 1)), run_time=2)

        # === Local helper: vertical text label ===
        def make_vertical_label(text_str, base_center, z_pos, z_dir):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(0.8)
            txt.rotate(PI / 2, axis=RIGHT)  # Stand it up in Z-direction
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        # === Local helper: pyramid ===
        def build_pyramid(
            label, layers, base_size=4, base_pos=ORIGIN, inverted=False, color=GREY
        ):

            height = base_size

            base = Square(side_length=base_size).set_color(color).set_opacity(0.4)
            base.move_to(base_pos)

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)
            apex = base.get_center() + z_dir * height

            corners = base.get_vertices()
            face_color = TEAL
            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_color, opacity=0.2)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            level_texts = VGroup()
            for i, txt in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = -z  # place labels *inside* inverted pyramid
                level_texts.add(make_vertical_label(txt, base_center, z, z_dir))

            group = VGroup(pyramid, level_texts)
            self.play(FadeIn(group, shift=IN), run_time=1.2)
            return group

        diff = 5

        math_pyramid = build_pyramid(
            label="Math",
            layers=["Set/논리", "Axiom", "수학"],
            base_pos=axes.c2p(0, 0, 0),
            color=GREY,
        )
        physics_pyramid = build_pyramid(
            label="Physics",
            layers=["입자/에너지/정보", "최소단위", "물리"],
            base_pos=axes.c2p(diff, 0, 0),
            color=GREY,
        )
        darwin_pyramid = build_pyramid(
            label="Darwin",
            layers=["자연선택/변화/생존", "개체, 유전자", "진화"],
            base_pos=axes.c2p(diff * 2, 0, 0),
            color=BLUE,
        )
        econ_pyramid = build_pyramid(
            label="Economics",
            layers=["self interest/이익", "개인", "경제"],
            base_pos=axes.c2p(diff * 3, 0, 0),
            color=BLUE,
        )

        big_pyramid = build_pyramid(
            label="Hindu",
            layers=["흰두교/불교/기독교/도교", "전체", ""],
            base_size=8,
            base_pos=axes.c2p(8, 8, 0),
            color=BLUE,
            inverted=True,
        )

        self.play(
            AnimationGroup(
                *[
                    math_pyramid,
                    physics_pyramid,
                    darwin_pyramid,
                    econ_pyramid,
                    big_pyramid,
                ],
                lag_ratio=0.2,
            )
        )


class SinglePyramidScene(ThreeDScene):
    def construct(self):

        phi = 75
        theta = 0

        frame.save_state()

        # Camera initial state and animation
        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.set_width(20)

        # === Add coordinate system ===
        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 10, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)
        axes.add_coordinate_labels()
        frame.move_to(axes.c2p(7, -1, 1.5))  # center on curve

        # === Local helper: vertical text label ===
        def make_vertical_label(text_str, base_center, z_pos, z_dir):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(0.8)
            txt.rotate(PI / 2, axis=RIGHT)
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        # === Local helper: pyramid ===
        def build_pyramid(
            label, layers, base_size=4, base_pos=ORIGIN, inverted=False, color=GREY
        ):

            height = base_size

            base = Square(side_length=base_size).set_color(color).set_opacity(0.4)
            base.move_to(base_pos)

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)
            apex = base.get_center() + z_dir * height

            corners = base.get_vertices()
            face_color = TEAL
            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_color, opacity=0.2)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            level_texts = VGroup()
            for i, txt_src in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = -z

                txt = make_vertical_label(txt_src, base_center, z, z_dir)
                level_texts.add(txt)
                if i == len(layers) - 1 and not inverted:
                    txt.scale(1.5).set_color(color)

                if inverted:
                    txt.scale(2)

            group = VGroup(pyramid, level_texts)
            return group

        diff = 5

        # === Create front pyramids with controlled animation ===
        pyramids = [
            build_pyramid(
                "Math",
                ["Set/논리", "Axiom", "수학"],
                base_pos=axes.c2p(0, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Physics",
                ["입자/에너지/정보", "최소단위", "물리"],
                base_pos=axes.c2p(diff, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Darwin",
                ["자연선택/변화/생존", "개체, 유전자", "진화"],
                base_pos=axes.c2p(diff * 2, 0, 0),
                color=BLUE,
            ),
            build_pyramid(
                "Economics",
                ["self interest/이익", "개인", "경제"],
                base_pos=axes.c2p(diff * 3, 0, 0),
                color=BLUE,
            ),
        ]

        for pyramid in pyramids:
            self.play(FadeIn(pyramid, shift=IN), run_time=1.2)
            self.wait(1)

        # === Add reductionist label ===

        self.wait()
        desc_label = Text(
            "reductionism: 부분의 합이 전체를 만든다", font="BM Hanna 11yrs Old"
        ).scale(1.0)

        desc_label.set_color_by_text("부분", ORANGE)

        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        # desc_label.move_to(axes.c2p(diff * 1, -6, 1))
        # desc_label.rotate(PI / 2, axis=RIGHT)
        self.play(Write(desc_label))
        self.wait(1.0)

        # === Add large back pyramid ===
        back_pyramid = build_pyramid(
            label="Spiritual",
            layers=["힌두교/불교/기독교/도교", "창발/시스템", ""],
            base_size=7,
            base_pos=axes.c2p(diff * 1.5, 13, -3),
            color=BLUE,
            inverted=True,
        )
        self.play(
            *[p.animate.set_opacity(0.1) for p in pyramids],
            FadeOut(desc_label),
            frame.animate.move_to(axes.c2p(7, 5, 1.5)),  # center on curve
            # frame.animate.set_euler_angles(phi=(phi-5) * DEGREES, theta=theta * DEGREES),
            FadeIn(back_pyramid, shift=IN),
            run_time=1.5,
        )

        desc_label = Text(
            "holism: 전체 안의 부분이 의미를 가진다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("전체", GREEN)

        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        # desc_label.move_to(axes.c2p(diff * 1, -6, 1))
        # desc_label.rotate(PI / 2, axis=RIGHT)
        self.play(Write(desc_label))
        self.wait(1.0)
        self.wait(2)


class SinglePyramidScene(ThreeDScene):
    def construct(self):

        phi = 75
        theta = 0

        frame = self.camera.frame
        frame.save_state()

        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.set_width(20)

        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 10, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)
        axes.add_coordinate_labels()
        frame.move_to(axes.c2p(7, -1, 1.5))

        def make_vertical_label(text_str, base_center, z_pos, z_dir):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(0.8)
            txt.rotate(PI / 2, axis=RIGHT)
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        def build_pyramid(
            label, layers, base_size=4, base_pos=ORIGIN, inverted=False, color=GREY
        ):
            height = base_size
            base = (
                Square(side_length=base_size)
                .set_fill(GREY_C, opacity=0.4)
                .set_stroke(WHITE, 0.5)
            )
            base.move_to(base_pos)

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)
            apex = base.get_center() + z_dir * height
            corners = base.get_vertices()

            face_colors = [
                interpolate_color(color, WHITE, alpha) for alpha in [0.1, 0.2, 0.3, 0.4]
            ]

            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_colors[i], opacity=0.4)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            level_texts = VGroup()
            for i, txt_src in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = -z

                txt = make_vertical_label(txt_src, base_center, z, z_dir)
                level_texts.add(txt)

                if i == len(layers) - 1 and not inverted:
                    txt.scale(1.5).set_color(color)
                if inverted:
                    txt.scale(2).set_color(WHITE)

            return VGroup(pyramid, level_texts)

        diff = 5

        pyramids = [
            build_pyramid(
                "Math",
                ["Set/논리", "Axiom", "수학"],
                base_pos=axes.c2p(0, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Physics",
                ["입자/에너지/정보", "최소단위", "물리"],
                base_pos=axes.c2p(diff, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Darwin",
                ["자연선택/변화/생존", "개체, 유전자", "진화"],
                base_pos=axes.c2p(diff * 2, 0, 0),
                color=BLUE,
            ),
            build_pyramid(
                "Economics",
                ["self interest/이익", "개인", "경제"],
                base_pos=axes.c2p(diff * 3, 0, 0),
                color=BLUE,
            ),
        ]

        for pyramid in pyramids:
            self.play(FadeIn(pyramid, shift=IN), run_time=1.2)
            self.wait(1)

        self.wait()
        desc_label = Text(
            "reductionism: 부분의 합이 전체를 만든다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("부분", ORANGE)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(1.0)

        back_pyramid = build_pyramid(
            label="Spiritual",
            layers=["힌두교/불교/기독교/도교", "창발/시스템", ""],
            base_size=7,
            base_pos=axes.c2p(diff * 1.5, 13, -3),
            color=GREEN,
            inverted=True,
        )

        self.play(
            *[p.animate.set_opacity(0.1) for p in pyramids],
            FadeOut(desc_label),
            frame.animate.move_to(axes.c2p(7, 5, 1.5)),
            FadeIn(back_pyramid, shift=IN),
            run_time=1.5,
        )

        desc_label = Text(
            "holism: 전체 안의 부분이 의미를 가진다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("전체", GREEN)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(3)


class SinglePyramidScene(ThreeDScene):
    def construct(self):

        phi = 75
        theta = 0

        frame = self.camera.frame
        frame.save_state()

        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.set_width(20)

        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 10, 1],
            z_range=[0, 5, 1],
        )
        self.add(axes)
        axes.add_coordinate_labels()
        frame.move_to(axes.c2p(7, -1, 1.5))

        def make_vertical_label(text_str, base_center, z_pos, z_dir):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(0.8)
            txt.rotate(PI / 2, axis=RIGHT)
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        def build_pyramid(
            label,
            layers,
            base_size=4,
            base_pos=ORIGIN,
            inverted=False,
            color=GREY,
            text_color=WHITE,
        ):
            height = base_size
            base = (
                Square(side_length=base_size)
                .set_fill(color, opacity=0.4)
                .set_stroke(WHITE, 0.5)
            )
            base.move_to(base_pos)

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)
            apex = base.get_center() + z_dir * height
            corners = base.get_vertices()

            face_colors = [color] * 4

            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(face_colors[i], opacity=0.4)
                    .set_stroke(WHITE, 0.5)
                    for i in range(4)
                ]
            )

            pyramid = VGroup(base, faces)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            level_texts = VGroup()
            for i, txt_src in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = -z

                txt = make_vertical_label(txt_src, base_center, z, z_dir)
                level_texts.add(txt)

                if i == len(layers) - 1 and not inverted:
                    txt.scale(1.5).set_color(text_color)
                if inverted:
                    txt.scale(2).set_color(WHITE)

            return VGroup(pyramid, level_texts)

        diff = 5

        pyramids = [
            build_pyramid(
                "Math",
                ["Set/논리", "Axiom", "수학"],
                base_pos=axes.c2p(0, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Physics",
                ["입자/에너지/정보", "최소단위", "물리"],
                base_pos=axes.c2p(diff, 0, 0),
                color=ORANGE,
            ),
            build_pyramid(
                "Darwin",
                ["자연선택/변화/생존", "개체, 유전자", "진화"],
                base_pos=axes.c2p(diff * 2, 0, 0),
                color=BLUE,
            ),
            build_pyramid(
                "Economics",
                ["self interest/이익", "개인", "경제"],
                base_pos=axes.c2p(diff * 3, 0, 0),
                color=BLUE,
            ),
        ]

        for pyramid in pyramids:
            self.play(FadeIn(pyramid, shift=IN), run_time=1.2)
            self.wait(1)

        self.wait()
        desc_label = Text(
            "reductionism: 부분의 합이 전체를 만든다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("부분", ORANGE)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(1.0)

        back_pyramid = build_pyramid(
            label="Spiritual",
            layers=["힌두교/불교/기독교/도교", "창발/시스템", ""],
            base_size=7,
            base_pos=axes.c2p(diff * 1.5, 13, -3),
            color=GREEN,
            inverted=True,
        )

        self.play(
            *[p.animate.set_opacity(0.1) for p in pyramids],
            FadeOut(desc_label),
            frame.animate.move_to(axes.c2p(7, 5, 1.5)),
            FadeIn(back_pyramid, shift=IN),
            run_time=1.5,
        )

        desc_label = Text(
            "holism: 전체 안의 부분이 의미를 가진다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("전체", GREEN)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(3)


class DomeScene(ThreeDScene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(phi=75 * DEGREES, theta=30 * DEGREES)
        frame.set_width(10)

        def dome(u, v):
            r = 3
            return np.array(
                [
                    r * np.cos(u) * np.sin(v),
                    r * np.sin(u) * np.sin(v),
                    r * np.cos(v),
                ]
            )

        surface = ParametricSurface(
            dome,
            u_range=[0, TAU],
            v_range=[0, PI / 2],
            resolution=(24, 12),
            # fill_opacity=0.2,
            # checkerboard_colors=[BLUE_E, BLUE_D],
        )
        surface.set_opacity(0.2)
        self.add(surface)


class SinglePyramidScene(ThreeDScene):
    def construct(self):

        phi = 75
        theta = 0

        frame = self.camera.frame
        frame.save_state()

        frame.set_euler_angles(phi=phi * DEGREES, theta=theta * DEGREES)
        frame.set_width(20)

        axes = ThreeDAxes(
            x_range=[-3, 6, 1],
            y_range=[-5, 10, 1],
            z_range=[0, 5, 1],
        )
        # self.add(axes)
        axes.add_coordinate_labels()
        frame.move_to(axes.c2p(7, -1, 1.5))

        def make_vertical_label(text_str, base_center, z_pos, z_dir):
            txt = Text(text_str, font="BM Hanna 11yrs Old").scale(1)
            txt.rotate(PI / 2, axis=RIGHT)
            txt.move_to(base_center + z_dir * z_pos)
            return txt

        def build_pyramid(
            label,
            layers,
            base_size=4,
            base_pos=ORIGIN,
            inverted=False,
            color=GREY,
            text_color=WHITE,
        ):
            height = base_size
            base = (
                Square(side_length=base_size)
                .set_fill(color, opacity=0.1)
                .set_stroke(color, 0.5)
            )
            base.move_to(base_pos)

            z_dir = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)
            apex = base.get_center() + z_dir * height
            corners = base.get_vertices()

            # Create the faces of the pyramid
            faces = VGroup(
                *[
                    Polygon(corners[i], corners[(i + 1) % 4], apex)
                    .set_fill(color, opacity=0.1)
                    .set_stroke(color, 0.5)
                    for i in range(4)
                ]
            )

            # Create the edge lines explicitly
            edges = VGroup(
                *[
                    Line(
                        corners[i], corners[(i + 1) % 4], color=color, stroke_width=1.5
                    )
                    for i in range(4)
                ],
                *[
                    Line(corners[i], apex, color=color, stroke_width=1.5)
                    for i in range(4)
                ],
            )

            pyramid = VGroup(base, faces, edges)

            if inverted:
                pyramid.rotate(PI, axis=RIGHT)

            base_center = base.get_center()
            level_texts = VGroup()
            for i, txt_src in enumerate(layers):
                z = (i + 0.5) * (height / len(layers))
                if inverted:
                    z = -z

                txt = make_vertical_label(txt_src, base_center, z, z_dir)
                txt.set_color(GREY_B)
                level_texts.add(txt)

                if i == len(layers) - 1 and not inverted:
                    txt.scale(1.5).set_color(text_color)
                if inverted:
                    if i == 0:
                        txt.scale(2.5).set_color(text_color)
                    else:
                        txt.scale(2)

            return VGroup(pyramid, level_texts)

        diff = 5

        text_color = WHITE
        body_color = "#4682B4"

        pyramids = [
            build_pyramid(
                "Math",
                ["Set/논리", "Axiom", "수학"],
                base_pos=axes.c2p(0, 0, 0),
                color=body_color,
                text_color=text_color,
            ),
            build_pyramid(
                "Physics",
                ["입자/에너지/정보", "최소단위", "물리"],
                base_pos=axes.c2p(diff, 0, 0),
                color=body_color,
                text_color=text_color,
            ),
            build_pyramid(
                "Darwin",
                ["자연선택/변화/생존", "개체, 유전자", "진화"],
                base_pos=axes.c2p(diff * 2, 0, 0),
                color=body_color,
                text_color=text_color,
            ),
            build_pyramid(
                "Economics",
                ["self interest/이익", "개인", "경제"],
                base_pos=axes.c2p(diff * 3, 0, 0),
                color=body_color,
                text_color=text_color,
            ),
        ]

        for pyramid in pyramids:
            self.play(FadeIn(pyramid, shift=IN), run_time=1.2)
            self.wait(1)

        self.wait()
        desc_label = Text(
            "reductionism: 부분의 합이 전체를 만든다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("부분", ORANGE)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(1.0)

        body_color = "#7B68EE"
        back_pyramid = build_pyramid(
            label="Spiritual",
            layers=["힌두교/불교/기독교/도교", "창발/시스템", ""],
            base_size=7,
            base_pos=axes.c2p(diff * 1.5, 13, -3),
            color=body_color,
            text_color=GREY_A,
            inverted=True,
        )

        self.play(
            *[p.animate.set_opacity(0.05) for p in pyramids],
            FadeOut(desc_label),
            frame.animate.move_to(axes.c2p(7, 5, 1.5)),
            FadeIn(back_pyramid, shift=IN),
            run_time=1.5,
        )

        desc_label = Text(
            "holism: 전체 안의 부분이 의미를 가진다", font="BM Hanna 11yrs Old"
        ).scale(1.0)
        desc_label.set_color_by_text("전체", GREEN)
        desc_label.fix_in_frame()
        desc_label.move_to(DOWN * 2)
        self.play(Write(desc_label))
        self.wait(3)
