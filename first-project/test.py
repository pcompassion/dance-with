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
