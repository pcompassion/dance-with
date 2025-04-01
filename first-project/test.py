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

                self.face_point(end)

                up = self.up
                down = self.down
                left = self.left
                right = self.right

                bounce = lambda t: 0.05 * np.sin(8 * PI * t)
                swing_angle = lambda t: 0.4 * np.sin(8 * PI * t)

                dummy = VMobject()

                def update_mob(mob, alpha):
                    foot_pos = interpolate(start, end, alpha)
                    bounce_offset = bounce(alpha) * up

                    lean_dir = 1 if self.facing_right else -1
                    lean_angle = lean_dir * interpolate(0, -PI / 16, np.sin(PI * alpha))

                    self.move_to(foot_pos + up * 0.6 + bounce_offset)
                    self.rotate(
                        lean_angle - self.rotation_angle,
                        axis=self.axes.z_axis.get_vector(),
                        about_point=self.get_body_bottom(),
                    )
                    self.rotation_angle = lean_angle

                    body_bottom = self.get_body_bottom()

                    leg_len = 0.5
                    horiz = 0.25

                    self.left_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + down * leg_len + left * horiz,
                            color=self.left_leg.get_color(),
                        )
                    )
                    self.right_leg.become(
                        Line(
                            start=body_bottom,
                            end=body_bottom + down * leg_len + right * horiz,
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
            angle=PI / 6,
            axis=UP,
            about_point=axes.c2p(0, 0, 0),
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

        # Animate in-between grid lines

        # Add bounding box

        bounding_lines = VGroup(
            Line(axes.c2p(-7, -2, -10), axes.c2p(9, -2, -10)),
            Line(axes.c2p(9, -2, -10), axes.c2p(9, 5, -10)),
            Line(axes.c2p(9, 5, -10), axes.c2p(-7, 5, -10)),
            Line(axes.c2p(-7, 5, -10), axes.c2p(-7, -2, -10)),
            Line(axes.c2p(-7, -2, 8), axes.c2p(9, -2, 8)),
            Line(axes.c2p(9, -2, 8), axes.c2p(9, 5, 8)),
            Line(axes.c2p(9, 5, 8), axes.c2p(-7, 5, 8)),
            Line(axes.c2p(-7, 5, 8), axes.c2p(-7, -2, 8)),
            Line(axes.c2p(-7, -2, -10), axes.c2p(-7, -2, 8)),
            Line(axes.c2p(9, -2, -10), axes.c2p(9, -2, 8)),
            Line(axes.c2p(9, 5, -10), axes.c2p(9, 5, 8)),
            Line(axes.c2p(-7, 5, -10), axes.c2p(-7, 5, 8)),
        )
        bounding_lines.set_stroke(opacity=0.7, color=WHITE)
        self.play(FadeIn(bounding_lines))

        world_g = VGroup()
        world_g.add(axes, man, bounding_lines)

        world_g_up = world_g.copy()
        shift_up = axes.c2p(0, 7.5, 0) - axes.c2p(0, 0, 0)
        world_g_up.shift(shift_up)
        self.play(Write(world_g_up))

        world_g_down = world_g.copy()
        shift_down = axes.c2p(0, 0, 0) - axes.c2p(0, 7.5, 0)
        world_g_down.shift(shift_down)
        self.play(Write(world_g_down))

        world_g_x1 = world_g.copy()
        shift_x1 = axes.c2p(0, 0, 0) - axes.c2p(16.5, 0, 0)
        world_g_x1.shift(shift_x1)
        self.play(Write(world_g_x1))

        world_g_x2 = world_g.copy()
        shift_x2 = axes.c2p(16.5, 0, 0) - axes.c2p(0, 0, 0)
        world_g_x2.shift(shift_x2)
        self.play(Write(world_g_x2))

        world_g_z1 = world_g.copy()
        shift_z1 = axes.c2p(0, 0, 0) - axes.c2p(0, 0, 18.5)
        world_g_z1.shift(shift_z1)
        self.play(Write(world_g_z1))

        world_g_z2 = world_g.copy()
        shift_z2 = axes.c2p(0, 0, 18.5) - axes.c2p(0, 0, 0)
        world_g_z2.shift(shift_z2)
        self.play(Write(world_g_z2))

        self.wait(1)
