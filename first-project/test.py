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


class StickManWalkScene(ThreeDScene):
    def construct(self):

        class StickMan(VGroup):
            def __init__(
                self,
                axes: ThreeDAxes,
                radius=0.3,
                height=1.2,
                leg_length=0.5,
                color=WHITE,
                **kwargs,
            ):
                super().__init__(**kwargs)
                self.axes = axes
                self.facing_right = True
                self.rotation_angle = 0

                # Build stickman upright in axes coordinates

                self.unit_x = axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)
                self.unit_y = axes.c2p(0, 1, 0) - axes.c2p(0, 0, 0)
                self.unit_z = axes.c2p(0, 0, 1) - axes.c2p(0, 0, 0)

                self.up = up = self.unit_y
                self.down = down = -self.unit_y
                self.left = left = -self.unit_z
                self.right = right = -left

                # up = self.axes.y_axis.get_vector()
                # down = -up
                # left = -self.axes.z_axis.get_vector()
                # right = -left

                # Body reference
                self.body_top = ORIGIN + up * (height / 2)
                self.body_bottom = ORIGIN + down * (height / 2)

                self.head = Circle(radius=radius, color=color)
                self.head.shift(self.body_top + up * radius)

                self.body = Line(self.body_top, self.body_bottom, color=color)

                self.left_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + down * leg_length + left * leg_length * 0.5,
                    color=color,
                )
                self.right_leg = Line(
                    start=self.body_bottom,
                    end=self.body_bottom + down * leg_length + right * leg_length * 0.5,
                    color=color,
                )

                self.add(self.head, self.body, self.left_leg, self.right_leg)

            def get_body_bottom(self):
                return self.body.get_end()

            def move_to_feet(self, point):
                shift = np.array(point) - self.get_body_bottom()
                self.shift(shift)

            def face_point(self, point):
                my_x = self.axes.p2c(self.get_center())[0]
                target_x = self.axes.p2c(point)[0]
                should_face_right = target_x >= my_x

                if self.facing_right != should_face_right:
                    self.rotate(
                        PI,
                        axis=self.axes.y_axis.get_vector(),
                        about_point=self.get_body_bottom(),
                    )
                    self.facing_right = should_face_right

            def walk_to(self, scene, point, duration=2):
                start = self.get_body_bottom()
                end = self.axes.c2p(*point)

                # self.face_point(end)

                bounce = lambda t: 0.05 * np.sin(8 * PI * t)
                swing_angle = lambda t: 0.4 * np.sin(8 * PI * t)

                dummy = VMobject()

                def update_mob(mob, alpha):
                    foot_pos = interpolate(start, end, alpha)
                    bounce_offset = bounce(alpha) * self.up

                    lean_dir = 1 if self.facing_right else -1
                    lean_angle = lean_dir * interpolate(0, -PI / 16, np.sin(PI * alpha))

                    self.move_to(foot_pos + self.up * 0.6 + bounce_offset)
                    self.rotate(
                        lean_angle - self.rotation_angle,
                        axis=self.axes.z_axis.get_vector(),
                        about_point=self.get_body_bottom(),
                    )
                    self.rotation_angle = lean_angle

                    body_bottom = self.get_body_bottom()

                    self.left_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + self.down * 0.5 + self.left * 0.25,
                            color=self.left_leg.get_color(),
                        )
                    )
                    self.right_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + self.down * 0.5 + self.right * 0.25,
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

        axes = ThreeDAxes(
            x_range=[-7, 9, 1],
            y_range=[-2, 5, 0.5],
            z_range=[-10, 8, 0.5],
        )
        self.add(axes)

        axes.rotate(
            angle=PI / 6,  # rotation angle
            axis=UP,  # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
            about_point=axes.c2p(0, 0, 0),  # pivot point
        )

        axes.rotate(
            angle=PI / 12,  # rotation angle
            axis=RIGHT,  # rotation axis: RIGHT = x-axis, UP = y-axis, OUT = z-axis
            about_point=axes.c2p(0, 0, 0),  # pivot point
        )

        man = StickMan(axes)
        man.move_to_feet(axes.c2p(10, 0, -10))
        self.add(man)

        frame = self.camera.frame
        frame.save_state()

        # frame.set_euler_angles(
        #     theta=0, phi=PI / 12, gamma=0
        # )  # φ = π/2.5 ≈ 72° (slightly tilted)

        man.walk_to(self, point=(6, 0, 5), duration=3)
        self.wait(0.1)

        # Walk left
        man.walk_to(self, point=(-3, 0, 0), duration=3)
        self.wait(0.1)

        man.walk_to(self, point=(5, 0, -5), duration=3)
        self.wait(2)

        frame.restore()


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        pass
        frame = self.camera.frame

        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        # self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # 1. 지구 (구)
        earth = Sphere(radius=2, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        # 2. 산 (적도 근처, 지름 0.4 정도)
        mountain = ParametricSurface(
            lambda u, v: self.mountain_func(u, v),
            u_range=[0, TAU],
            v_range=[0, 1],
            resolution=(30, 15),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        # 3. 오염된 지역 (산보다 약 1.5배 넓은 영역)
        contamination = ParametricSurface(
            lambda u, v: self.contamination_belt(u, v),
            u_range=[-PI / 6, PI / 6],
            v_range=[-PI / 10, PI / 10],
            resolution=(30, 15),
        )
        contamination.set_color(GREY_BROWN)
        contamination.set_opacity(0.6)
        self.add(contamination)

        self.wait(3)

    def mountain_func(self, u, v):
        """
        Parametric mountain on top of the sphere
        """
        # 위치: 위도 30도, 경도 0도
        theta = PI / 6  # 위도
        phi = 0  # 경도

        r_base = 2
        mountain_height = 0.6
        spread = 0.4

        x = (
            (r_base + mountain_height * v * (1 - np.cos(u)))
            * np.cos(theta)
            * np.cos(phi + spread * np.sin(u))
        )
        y = (
            (r_base + mountain_height * v * (1 - np.cos(u)))
            * np.cos(theta)
            * np.sin(phi + spread * np.sin(u))
        )
        z = (r_base + mountain_height * v * (1 - np.cos(u))) * np.sin(theta)

        return np.array([x, y, z])

    def contamination_belt(self, u, v):
        """
        Parametric patch near the mountain to simulate contamination
        """
        r = 2.01  # 살짝 띄워서 지구 위에 덮이게
        theta = PI / 6 + v  # 산 중심 근처의 위도
        phi = u  # 산 중심 근처의 경도

        x = r * np.cos(theta) * np.cos(phi)
        y = r * np.cos(theta) * np.sin(phi)
        z = r * np.sin(theta)

        return np.array([x, y, z])


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        # 1. 지구 (구)
        earth = Sphere(radius=2, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        # 2. 산 (정규분포를 회전시켜 만든 3D 형상)
        mountain = ParametricSurface(
            lambda u, v: rotated_normal_mountain(u, v),
            u_range=[0, TAU],
            v_range=[0, 1.5],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        # 3. 오염된 지역 (산보다 약 1.5배 넓은 영역)
        contamination = ParametricSurface(
            lambda u, v: contamination_belt(u, v),
            u_range=[-PI / 6, PI / 6],
            v_range=[-PI / 10, PI / 10],
            resolution=(30, 15),
        )
        contamination.set_color(GREY_BROWN)
        contamination.set_opacity(0.6)
        self.add(contamination)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        # test
        def rotated_normal_mountain(u, v):
            """
            회전된 정규분포 모양의 3D 산 생성
            u: 회전 각도 (0 to TAU)
            v: 높이 방향으로의 위치 (0 to something)
            """
            # 중심 위치 (위도/경도)
            theta = PI / 6
            phi = 0

            # r_base = 2
            max_height = 1
            r_base = 2 - 0.9 * max_height

            sigma = 1

            # normal distribution profile (z = height)
            r = v
            height_profile = max_height * np.exp(-(r**2) / (2 * sigma**2))

            # cylindrical to cartesian (then projected onto sphere)
            x_local = r * np.cos(u)
            y_local = r * np.sin(u)
            # z_local = height_profile
            z_local = height_profile

            # convert to global coordinates on sphere
            # rotate the local frame to (theta, phi) on sphere
            direction = np.array(
                [
                    np.cos(theta) * np.cos(phi),
                    np.cos(theta) * np.sin(phi),
                    np.sin(theta),
                ]
            )
            base_point = r_base * direction

            # build local basis (tangent vectors)
            up = direction
            right = np.cross(np.array([0, 0, 1]), up)
            if np.linalg.norm(right) < 1e-6:
                right = np.array([1, 0, 0])
            right /= np.linalg.norm(right)
            forward = np.cross(up, right)

            point = base_point + x_local * right + y_local * forward + z_local * up
            return point

        def contamination_belt(u, v):
            """
            Parametric patch near the mountain to simulate contamination
            """
            r = 2.01  # 살짝 띄워서 지구 위에 덮이게
            theta = PI / 6 + v  # 산 중심 근처의 위도
            phi = u  # 산 중심 근처의 경도

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        # 1. 지구 (구)
        earth = Sphere(radius=2, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        # 2. 산 (정규분포를 회전시켜 만든 3D 형상)
        mountain = ParametricSurface(
            lambda u, v: rotated_normal_mountain(u, v),
            u_range=[0, TAU],
            v_range=[0, 1],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        # 3. 오염된 지역 (산보다 약 1.5배 넓은 영역)
        # contamination = ParametricSurface(
        #     lambda u, v: contamination_belt(u, v),
        #     u_range=[-PI / 6, PI / 6],
        #     v_range=[-PI / 10, PI / 10],
        #     resolution=(30, 15),
        # )
        # contamination.set_color(GREY_BROWN)
        # contamination.set_opacity(0.6)
        # self.add(contamination)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        # test
        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """

            earth_radius = 2
            pdf_max = 1 / (sigma * np.sqrt(2 * np.pi))
            max_height = pdf_max * earth_radius
            r_base = earth_radius - 0.95 * max_height
            print(max_height)
            # r_base = 2 - 0.9 * max_height

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v
                height_profile = max_height * np.exp(-(r**2) / (2 * sigma**2))

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

                point = base_point + x_local * right + y_local * forward + z_local * up
                return point

            return surface_fn

        def contamination_belt(u, v):
            r = 2.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=2, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 1  # 원하는 산 넓이 지정
        mountain = ParametricSurface(
            rotated_normal_mountain_generator(sigma),
            u_range=[0, TAU],
            v_range=[0, 1],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        self.wait(3)


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_max = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            max_height = pdf_max * earth_radius
            r_base = earth_radius - 0.95 * max_height
            print(max_height)

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v
                height_profile = max_height * np.exp(-(r**2) / (2 * sigma**2))

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

                point = base_point + x_local * right + y_local * forward + z_local * up
                return point

            return surface_fn

        def contamination_belt(u, v):
            r = earth_radius + 0.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 1  # 원하는 산 넓이 지정
        mountain = ParametricSurface(
            rotated_normal_mountain_generator(sigma),
            u_range=[0, TAU],
            v_range=[0, 1.5],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_max = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            max_height = pdf_max * earth_radius
            r_base = earth_radius - 0.95 * max_height
            print(max_height)

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v
                height_profile = max_height * np.exp(-(r**2) / (2 * sigma**2))

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

                point = base_point + x_local * right + y_local * forward + z_local * up
                return point

            return surface_fn, 2 * sigma  # 최대 반지름도 함께 반환

        def contamination_belt(u, v):
            r = earth_radius + 0.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 1  # 원하는 산 넓이 지정
        surface_fn, max_radius = rotated_normal_mountain_generator(sigma)
        mountain = ParametricSurface(
            surface_fn,
            u_range=[0, TAU],
            v_range=[0, max_radius],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_max = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            max_height = pdf_max
            r_base = earth_radius * (1 - 0.9) * max_height

            # 정규분포에서 중앙에서 좌우로 약 95% 확률 질량은 [-2σ, 2σ] 범위에 있음
            cutoff_radius = min(
                0.8 * sigma, earth_radius * 0.1
            )  # 95% 확률질량이 포함되는 반지름 범위

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v * cutoff_radius  # v ∈ [0, 1] → [0, cutoff_radius]로 매핑
                height_profile = (
                    pdf_max * earth_radius * np.exp(-(r**2) / (2 * sigma**2))
                )

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

                point = base_point + x_local * right + y_local * forward + z_local * up
                return point

            return surface_fn, 1  # v는 [0, 1]로 고정하고 내부에서 scaling

        def contamination_belt(u, v):
            r = earth_radius + 0.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 1  # 원하는 산 넓이 지정
        surface_fn, max_radius = rotated_normal_mountain_generator(sigma)
        mountain = ParametricSurface(
            surface_fn,
            u_range=[0, TAU],
            v_range=[0, max_radius],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_max = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            max_height = pdf_max * earth_radius
            r_base = earth_radius - 0.95 * max_height

            # 정규분포에서 중앙에서 좌우로 약 95% 확률 질량은 [-2σ, 2σ] 범위에 있음
            cutoff_radius = 0.7 * sigma  # 95% 확률질량이 포함되는 반지름 범위

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v * cutoff_radius  # v ∈ [0, 1] → [0, cutoff_radius]로 매핑
                height_profile = max_height * np.exp(-(r**2) / (2 * sigma**2))

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

                # 초기 점 계산 (tangent 기반 좌표계에서 산 위 점)
                preliminary_point = (
                    base_point + x_local * right + y_local * forward + z_local * up
                )

                # 지구 중심 방향 벡터 기준 보정
                ray_dir = preliminary_point / np.linalg.norm(preliminary_point)
                projected_height = np.dot(preliminary_point, ray_dir)
                true_height = projected_height - earth_radius

                # 구 곡면을 기준으로 최종 산 위 점
                point = ray_dir * (earth_radius + true_height)
                return point

            return surface_fn, 1  # v는 [0, 1]로 고정하고 내부에서 scaling

        def contamination_belt(u, v):
            r = earth_radius + 0.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 1  # 원하는 산 넓이 지정
        surface_fn, max_radius = rotated_normal_mountain_generator(sigma)
        mountain = ParametricSurface(
            surface_fn,
            u_range=[0, TAU],
            v_range=[0, max_radius],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        self.wait(3)


from manimlib import *
import numpy as np


class MountainOnSphereScene(ThreeDScene):
    def construct(self):
        earth_radius = 2  # 지구 반지름을 변수로 통일

        def rotated_normal_mountain_generator(sigma):
            """
            sigma를 받아서 normal curve 기반의 산을 생성하는 함수 반환
            """
            pdf_peak = 1 / (sigma * np.sqrt(2 * np.pi))  # PDF의 최대값
            mountain_height = pdf_peak * earth_radius
            r_base = earth_radius - 0.95 * mountain_height

            # 정규분포에서 중앙에서 좌우로 약 95% 확률 질량은 [-2σ, 2σ] 범위에 있음
            cutoff_radius = sigma  # 95% 확률질량이 포함되는 반지름 범위

            def surface_fn(u, v):
                theta = PI / 6
                phi = 0

                r = v * cutoff_radius  # v ∈ [0, 1] → [0, cutoff_radius]로 매핑
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

                # 초기 점 계산 (tangent 기반 좌표계에서 산 위 점)
                preliminary_point = (
                    base_point + x_local * right + y_local * forward + z_local * up
                )

                # 지구 중심 방향 벡터 기준 보정
                ray_dir = preliminary_point / np.linalg.norm(preliminary_point)
                projected_height = np.dot(preliminary_point, ray_dir)
                true_height = projected_height - earth_radius

                # 구 곡면을 기준으로 최종 산 위 점
                point = ray_dir * (earth_radius + true_height)
                return point

            return surface_fn, 1  # v는 [0, 1]로 고정하고 내부에서 scaling

        def contamination_belt(u, v):
            r = earth_radius + 0.01
            theta = PI / 6 + v
            phi = u

            x = r * np.cos(theta) * np.cos(phi)
            y = r * np.cos(theta) * np.sin(phi)
            z = r * np.sin(theta)

            return np.array([x, y, z])

        frame = self.camera.frame
        frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)

        earth = Sphere(radius=earth_radius, resolution=(30, 30))
        earth.set_color(BLUE_E)
        self.add(earth)

        sigma = 0.7  # 원하는 산 넓이 지정
        surface_fn, max_radius = rotated_normal_mountain_generator(sigma)
        mountain = ParametricSurface(
            surface_fn,
            u_range=[0, TAU],
            v_range=[0, max_radius],
            resolution=(50, 20),
        )
        mountain.set_color(GOLD_B)
        self.add(mountain)

        # base_point 계산 및 시각화

        self.wait(3)


class DilemmaTopics(Scene):
    def construct(self):
        # Title
        title = Tex(r"1 + 1 = -1").scale(1.5)
        title[4:7].set_color(RED)
        title.to_edge(UP)
        self.play(FadeIn(title))


class GeometricSeriesVisualizationZero(Scene):

    def animate_epsilon_cut(
        self,
        origin,
        vertical_lines,
        bottom_line,
        r,
        scale_factor,
        epsilon_fraction,
        y_offset,
    ):
        limit_x = (1 / (1 - r)) * scale_factor
        epsilon_x = limit_x - epsilon_fraction * (limit_x)  # ← cut point

        # STEP 1: Draw vertical epsilon dashed line
        epsilon_line = DashedLine(
            start=origin + [epsilon_x, 0, 0],
            end=origin + [epsilon_x, 1 * scale_factor, 0],
            color=YELLOW,
            dash_length=0.1,
        )
        self.play(FadeIn(epsilon_line))

        # STEP 2: Brace and ε label (correctly from dashed line to limit point)
        limit_point = origin + [(1 / (1 - r)) * scale_factor, 0, 0]
        epsilon_start = origin + [epsilon_x, 0, 0]

        epsilon_segment = Line(epsilon_start, limit_point, color=YELLOW)
        epsilon_brace = Brace(epsilon_segment, direction=UP, color=YELLOW)
        epsilon_label = Tex(r"\epsilon").scale(0.8).next_to(epsilon_brace, UP, buff=0.1)

        self.play(FadeIn(epsilon_segment))
        self.play(GrowFromCenter(epsilon_brace), FadeIn(epsilon_label), run_time=0.8)
        self.wait(0.5)
        self.play(
            FadeOut(epsilon_segment),
            FadeOut(epsilon_brace),
            FadeOut(epsilon_label),
            run_time=0.5,
        )

        # STEP 3: Collect vertical bars to the right of ε
        bars_to_copy = []
        for vline in vertical_lines:
            if vline.get_start()[0] > origin[0] + epsilon_x:
                bars_to_copy.append(vline)

        # STEP 4: Copy and scale group
        copied_group = VGroup(*[bar.copy() for bar in bars_to_copy])

        # Add the bottom segment for visual closure
        rightmost_x = max([bar.get_start()[0] for bar in bars_to_copy])
        bottom_segment = Line(
            [epsilon_x, 0, 0] + origin,
            [rightmost_x - origin[0], 0, 0] + origin,
            color=WHITE,
        )

        copied_group.add(bottom_segment)

        # Scale and shift (half of original triangle height)
        copied_group.generate_target()
        copied_group.target.scale(1 / epsilon_fraction * 0.7).next_to(
            bottom_line, DOWN * y_offset
        )
        self.play(MoveToTarget(copied_group), run_time=1)

        self.wait(0.5)

        # Re-highlight copied bars

        for bar in copied_group[:-1]:  # skip the bottom line
            self.play(bar.animate.set_color(BLUE_E).set_stroke(width=10), run_time=0.1)
            self.play(bar.animate.set_stroke(width=2), run_time=0.05)

        self.wait(1)

        self.play(FadeOut(copied_group))

    def construct(self):
        r = 0.8
        scale_factor = 2.3
        shift_amount = LEFT * 5

        left_line = Line([0, 0, 0], [0, 1 * scale_factor, 0], color=WHITE).shift(
            shift_amount
        )
        origin = left_line.get_start()

        x_pos = 1 * scale_factor
        x_pos_prev = 0

        vertical_lines = []
        vertical_line_prev = left_line
        while x_pos < (1 / (1 - r)) * scale_factor - 0.01:
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
                    len_t = f"r^{{{len_v-1}}}"
                text = Tex(f"{len_t}").next_to(
                    horizontal_line, DOWN, buff=0.3, aligned_edge=DOWN
                )
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    FadeIn(text),
                    run_time=0.1,
                )
            else:
                self.play(
                    FadeIn(horizontal_line),
                    FadeIn(vertical_line_prev),
                    run_time=0.1,
                )

            x_pos += r ** len(vertical_lines) * scale_factor
            vertical_line_prev = vertical_line

        bottom_line = Line(
            origin + [0, 0, 0], origin + [1 / (1 - r) * scale_factor, 0, 0], color=WHITE
        )
        end = origin + [(1 / (1 - r)) * scale_factor, 0, 0]

        glow = Dot(point=end, color=BLUE, radius=0.3, fill_opacity=0.4)
        self.play(FadeIn(glow))
        self.wait()

        self.play(FadeIn(bottom_line))

        self.animate_epsilon_cut(
            origin,
            vertical_lines,
            bottom_line,
            r,
            scale_factor,
            epsilon_fraction=1 / 8 + 0.01,
            y_offset=2.5,
        )

        self.animate_epsilon_cut(
            origin,
            vertical_lines,
            bottom_line,
            r,
            scale_factor,
            epsilon_fraction=1 / 16 + 0.008,
            y_offset=4,
        )


class InfinityNumberLine(Scene):
    def highlight_beyond(self, number_line, start_n, end_n):
        # Move camera
        target_pos = number_line.number_to_point(start_n)
        self.play(self.camera.frame.animate.move_to(target_pos), run_time=2)

        # Draw dashed yellow line
        dash = DashedLine(target_pos + UP * 2, target_pos + DOWN * 0.5, color=YELLOW)
        self.play(FadeIn(dash), run_time=0.2)
        self.wait(0.5)

        # Highlight ticks to the right
        marks = []
        for i in range(start_n + 1, end_n + 1):
            tick = Line(
                number_line.number_to_point(i) + DOWN * 0.15,
                number_line.number_to_point(i) + UP * 0.15,
                color=BLUE,
            ).set_stroke(width=4)
            marks.append(tick)

        for tick in marks:
            self.play(GrowFromCenter(tick), run_time=0.1)

        self.wait(0.5)
        self.play(FadeOut(dash))
        self.play(*[FadeOut(tick) for tick in marks])

    def construct(self):
        # STEP 0: Title
        title = Text("큰 수 놀이", font="BM Hanna 11yrs Old").scale(1.2)
        title.shift(UP * 2.5)
        self.play(Write(title))

        # STEP 1: Number line setup
        number_line = NumberLine(
            x_range=[0, 200, 1],  # extended to allow multiple moves
            include_numbers=False,
            unit_size=0.6,
            color=WHITE,
        ).shift(DOWN * 2)

        self.add(number_line)

        self.camera.frame.move_to(number_line.n2p(0))

        self.wait(2)

        # Run steps as loopable function calls
        self.highlight_beyond(number_line, 30, 50)
        self.highlight_beyond(number_line, 60, 80)
        self.highlight_beyond(number_line, 90, 110)

        self.wait(1.5)


class InfinityNumberLine(Scene):
    def highlight_beyond(self, number_line, start_n, end_n):
        # Move camera
        target_pos = number_line.number_to_point(start_n)
        self.play(self.camera.frame.animate.move_to(target_pos), run_time=2)

        # Draw dashed yellow line
        dash = DashedLine(target_pos + UP * 1.7, target_pos + DOWN * 0.5, color=YELLOW)
        self.play(FadeIn(dash))
        self.wait(0.3)

        # Highlight ticks to the right
        marks = []
        for i in range(start_n + 1, end_n + 1):
            tick = Line(
                number_line.number_to_point(i) + DOWN * 0.15,
                number_line.number_to_point(i) + UP * 0.15,
                color=BLUE,
            ).set_stroke(width=4)
            marks.append(tick)

        for tick in marks:
            self.play(GrowFromCenter(tick), run_time=0.1)

        self.wait(0.5)
        self.play(FadeOut(dash))
        self.play(*[FadeOut(tick) for tick in marks])

    def construct(self):
        # STEP 0: Title
        title = Text("큰 수 놀이", font="BM Hanna 11yrs Old").scale(1.2)
        title.shift(UP * 2.5)
        title.fix_in_frame()
        self.play(Write(title))

        frame = self.camera.frame
        frame.move_to(number_line.n2p(0))
        frame.save_state()

        # STEP 1: Number line setup (for growing to the right)
        number_line = NumberLine(
            x_range=[0, 200, 1],
            include_numbers=False,
            unit_size=0.6,
            color=WHITE,
        ).shift(DOWN * 2)
        number_line.shift(ORIGIN - number_line.number_to_point(0))
        self.play(Write(number_line))

        self.wait(1)

        self.highlight_beyond(number_line, 30, 45)
        self.highlight_beyond(number_line, 60, 75)
        self.highlight_beyond(number_line, 90, 110)

        # STEP 2: New number line from 0 to 30 for approaching 0 from right

        frame.move_to(number_line.n2p(0))
        self.play(FadeOut(number_line))
        self.wait(2)

        self.play(FadeOut(title))
        title = Tex(r"0").scale(1.2)
        title.shift(UP * 2.5)
        self.play(Write(title))

        def cut_and_highlight(plane, x_cut, color, zoom=False):
            # Cut line
            cut_line = DashedLine(
                start=plane.coords_to_point(x_cut, -0.5),
                end=plane.coords_to_point(x_cut, 0.5),
                color=YELLOW,
                dash_length=0.1,
            )
            self.play(FadeIn(cut_line))

            # Highlight area from x_cut to 0
            highlight = Rectangle(
                width=plane.coords_to_point(0, 0)[0]
                - plane.coords_to_point(x_cut, 0)[0],
                height=1,
                fill_color=color,
                fill_opacity=0.5,
                stroke_width=0,
            )
            highlight.move_to(
                (plane.coords_to_point(0, 0)[0] + plane.coords_to_point(x_cut, 0)[0])
                / 2
                * RIGHT
                + plane.coords_to_point(0, 0)[1] * UP
            )
            if zoom:
                zoom_target = plane.coords_to_point(0, 0)
                self.camera.frame.save_state()

                self.play(
                    self.camera.frame.animate.scale(0.1).move_to(zoom_target),
                    run_time=2,
                )

            self.play(FadeIn(highlight))
            self.wait(0.5)

            self.play(FadeOut(highlight), FadeOut(cut_line))

            if zoom:
                self.wait(0.3)
                self.play(Restore(self.camera.frame))

        full_length = 7
        plane = NumberPlane(
            x_range=[0, full_length, 0.1],
            y_range=[-1, 1, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_opacity": 0.5,
                "stroke_width": 1,
            },
            axis_config={
                "include_ticks": False,
                "include_tip": False,
                "stroke_width": 2,
                "stroke_color": WHITE,
            },
        )
        plane.shift(UP * 1.5)
        plane.shift(ORIGIN - plane.coords_to_point(0, 0))
        self.play(Write(plane))

        # # Cut at x = 2
        cut_and_highlight(plane, 2, BLUE)
        self.wait()

        # # Cut at x = 1
        cut_and_highlight(plane, 1, BLUE)
        self.wait()

        cut_and_highlight(plane, 0.1, GREEN, True)
        # cut_and_highlight(1, GREEN)

        self.wait(2)


class InfinityNumberLine(Scene):
    def construct(self):
        # Title
        title = Text("큰 수 놀이", font="BM Hanna 11yrs Old").scale(1.2)
        title.shift(UP * 2.5)
        title.fix_in_frame()
        self.play(Write(title))

        frame = self.camera.frame
        frame.save_state()

        # STEP 1: Number line setup (for growing to the right)
        number_line = NumberLine(
            x_range=[0, 200, 1],
            include_numbers=False,
            unit_size=0.6,
            color=WHITE,
        ).shift(DOWN * 2)
        number_line.shift(ORIGIN - number_line.number_to_point(0))
        self.play(Write(number_line))

        def highlight_beyond(number_line, start_n, end_n):
            target_pos = number_line.number_to_point(start_n)
            self.play(self.camera.frame.animate.move_to(target_pos), run_time=2)

            dash = DashedLine(
                target_pos + UP * 1.7, target_pos + DOWN * 0.5, color=YELLOW
            )
            self.play(FadeIn(dash))
            self.wait(0.3)

            # Highlight region from start_n to end_n using Rectangle
            start_x = number_line.number_to_point(start_n)[0]
            end_x = number_line.number_to_point(end_n)[0]
            width = end_x - start_x

            highlight = Rectangle(
                width=width,
                height=1,
                fill_color=BLUE,
                fill_opacity=0.5,
                stroke_width=0,
            )
            highlight.move_to(
                (start_x + end_x) / 2 * RIGHT + number_line.number_to_point(0)[1] * UP
            )

            self.play(FadeIn(highlight))
            self.wait(0.5)
            self.play(FadeOut(highlight), FadeOut(dash))

        highlight_beyond(number_line, 30, 45)
        highlight_beyond(number_line, 60, 75)
        highlight_beyond(number_line, 90, 110)

        self.play(Restore(self.camera.frame), FadeOut(number_line), FadeOut(title))

        self.wait(1)

        title = Tex(r"0").scale(1.2)
        title.shift(UP * 2.5)
        self.play(Write(title))

        # STEP 2: Create number plane for limit visualization
        full_length = 7
        plane = NumberPlane(
            x_range=[0, full_length, 0.1],
            y_range=[-1, 1, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_opacity": 0.5,
                "stroke_width": 1,
            },
            axis_config={
                "include_ticks": False,
                "include_tip": False,
                "stroke_width": 2,
                "stroke_color": WHITE,
            },
        )
        plane.shift(UP * 1.5)
        plane.shift(ORIGIN - plane.coords_to_point(0, 0))
        self.play(Write(plane))

        def cut_and_highlight(x_cut, color, zoom=False):
            cut_line = DashedLine(
                start=plane.coords_to_point(x_cut, -0.5),
                end=plane.coords_to_point(x_cut, 0.5),
                color=YELLOW,
                dash_length=0.1,
            )
            self.play(FadeIn(cut_line))

            highlight = Rectangle(
                width=plane.coords_to_point(0, 0)[0]
                - plane.coords_to_point(x_cut, 0)[0],
                height=1,
                fill_color=color,
                fill_opacity=0.5,
                stroke_width=0,
            )
            highlight.move_to(
                (plane.coords_to_point(0, 0)[0] + plane.coords_to_point(x_cut, 0)[0])
                / 2
                * RIGHT
                + plane.coords_to_point(0, 0)[1] * UP
            )

            if zoom:
                zoom_target = plane.coords_to_point(0, 0)
                self.camera.frame.save_state()
                self.play(
                    self.camera.frame.animate.scale(0.1).move_to(zoom_target),
                    run_time=2,
                )

            self.play(FadeIn(highlight))
            self.wait(0.5)
            self.play(FadeOut(highlight), FadeOut(cut_line))

            if zoom:
                self.wait(0.3)
                self.play(Restore(self.camera.frame))

        cut_and_highlight(2, BLUE)
        self.wait()
        cut_and_highlight(1, BLUE)
        self.wait()
        cut_and_highlight(0.1, GREEN, zoom=True)

        self.wait(2)

        self.play(FadeOut(plane), FadeOut(title))

        t = Tex(r"\frac{1}{\infty} = 0").scale(1.4).shift(UP * 1.8)
        self.play(Write(t))
        self.wait(1)

        # Author data and quotes
        authors = ["우피니샤드", "반야심경", "도덕경", "성서"]
        quotes = [
            "그것은 가득 차 있으나 비어 있고, 비어 있으나 가득 차 있다.",
            "색즉시공, 공즉시색",
            "만물은 유에서 생기고, 유는 무에서 생긴다.",
            "나는 알파요 오메가요, 처음이자 마지막이다.",
        ]

        author_texts = VGroup()
        quote_texts = VGroup()

        colors = [BLUE_B, GREY_B, BLUE_B, GREY_B]
        for i, name in enumerate(authors):
            color = colors[i]
            author = Text(name, font="BM Hanna 11yrs Old").set_color(color)
            quote = Text(quotes[i], font="BM Hanna 11yrs Old").scale(0.8)
            author_texts.add(author)
            quote_texts.add(quote)

        author_texts.arrange(RIGHT, buff=0.5)
        # author_texts.move_to(DOWN)
        for quote in quote_texts:
            quote.next_to(author_texts, DOWN * 2, buff=0.3)
            quote.set_x(0)

        # Animate author + quote one by one
        for i in range(len(authors)):
            self.play(Write(author_texts[i]), run_time=0.4)
            self.play(Write(quote_texts[i]), run_time=1)
            self.wait(1.2)
            self.play(FadeOut(quote_texts[i]))

        self.wait(2)

        self.play(FadeOut(t), FadeOut(author_texts))



class InfinityNumberLine(Scene):
    def construct(self):
        t = Tex(r"\frac{1}{\infty} = 0").scale(1.5).shift(UP)
        self.play(Write(t))
        self.wait(1)

        # Author data and quotes
        authors = ["우피니샤드", "반야심경", "도덕경", "성서"]
        quotes = [
            "그는 무한하고, 또 무한이 그를 품고 있다.",
            "색즉시공, 공즉시색",
            "무위로써 천하를 다스린다",
            "마지막은 처음과 같으니, 만물은 그에게서 나왔도다",
        ]

        author_texts = VGroup()
        quote_texts = VGroup()

        for i, name in enumerate(authors):
            color = WHITE if i % 2 == 0 else GREY_B
            author = Text(name, font="BM Hanna 11yrs Old", color=color)
            quote = Text(quotes[i], font="BM Hanna 11yrs Old", color=color).scale(0.8)
            author_texts.add(author)
            quote_texts.add(quote)

        author_texts.arrange(RIGHT, buff=0.5)
        author_texts.move_to(DOWN)
        for quote in quote_texts:
            quote.next_to(author_texts, DOWN, buff=0.3)
            quote.set_x(0)

        # Animate author + quote one by one
        for i in range(len(authors)):
            self.play(Write(author_texts[i]), run_time=0.4)
            self.play(Write(quote_texts[i]), run_time=0.4)
            self.wait(1.2)
            self.play(FadeOut(quote_texts[i]))

        self.wait(2)


class InfinityNumberLine(Scene):
    def construct(self):
