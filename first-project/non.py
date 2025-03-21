#!/usr/bin/env python


class RotatingDiskAnt(Scene):
    def construct(self):
        # Disk properties

        disk_radius = 2.7
        omega = 2 * PI / 5  # Angular velocity (full rotation in 5 sec)
        move_time = 4  # Time for the ant to move up by 1 unit in global frame
        move_speed = 1 / move_time

        def create_disc():
            # Create the rotating disk
            disk = Circle(radius=disk_radius, color=BLUE, fill_opacity=0.5)

            # Create polar coordinate lines
            polar_lines = VGroup()
            for angle in np.linspace(0, 2 * PI, 12, endpoint=False):
                line = Line(
                    ORIGIN,
                    disk_radius * np.array([np.cos(angle), np.sin(angle), 0]),
                    color=WHITE,
                )
                polar_lines.add(line)

            # Create radial circles
            radial_circles = VGroup()
            for r in np.linspace(0.5, disk_radius, 5):
                circle = Circle(radius=r, color=WHITE, stroke_opacity=0.5)
                radial_circles.add(circle)

            group = VGroup(disk, polar_lines, radial_circles)
            return group

        disc = create_disc()

        rotating_group = disc

        ant = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all = VGroup(rotating_group, ant)

        rotating_all.shift(LEFT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all))

        self.wait(1)

        # Animate ant moving along trajectory while rotating the disk

        def update_rotating_group(mob, alpha):
            origin = mob.get_center()
            time_prev = times[0]
            time = move_time * alpha
            dt = time - time_prev
            times[0] = time
            mob.rotate(omega * dt, about_point=origin)

        def update_ant_north(mob, alpha, disc, starting_pos=ORIGIN):
            time = move_time * alpha

            pos = starting_pos + [0, move_speed * time, 0]
            mob.move_to(pos)

            disc.add(mob.copy().set_fill(GREEN))

        def update_ant_east(mob, alpha, disc, starting_pos):
            time = move_time * alpha

            pos = starting_pos + [move_speed * time, 0, 0]
            mob.move_to(pos)

            disc.add(mob.copy().set_fill(RED))

        times = [0]

        starting_pos = rotating_all.copy().get_center()
        self.play(
            UpdateFromAlphaFunc(
                ant, partial(update_ant_north, disc=disc, starting_pos=starting_pos)
            ),
            UpdateFromAlphaFunc(rotating_all, partial(update_rotating_group)),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]
        starting_pos = ant.copy().get_center()

        self.play(
            UpdateFromAlphaFunc(
                ant, partial(update_ant_east, disc=disc, starting_pos=starting_pos)
            ),
            UpdateFromAlphaFunc(rotating_all, update_rotating_group),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        # second disc
        disc2 = create_disc()

        rotating_group2 = disc2

        ant2 = Dot(color=WHITE)

        # Group with rotating disk
        rotating_all2 = VGroup(rotating_group2, ant2)

        rotating_all2.shift(RIGHT * 3)

        # Add to scene
        self.play(FadeIn(rotating_all2))

        self.wait(1)

        times = [0]

        starting_pos = rotating_all2.copy().get_center()
        self.play(
            UpdateFromAlphaFunc(
                ant2, partial(update_ant_east, disc=disc2, starting_pos=starting_pos)
            ),
            UpdateFromAlphaFunc(rotating_all2, partial(update_rotating_group)),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)

        times = [0]
        starting_pos = ant2.copy().get_center()

        self.play(
            UpdateFromAlphaFunc(
                ant2, partial(update_ant_north, disc=disc2, starting_pos=starting_pos)
            ),
            UpdateFromAlphaFunc(rotating_all2, update_rotating_group),
            run_time=move_time,
            rate_func=linear,
        )

        self.wait(1)


class BallDrop(Scene):
    def construct(self):
        # Create a three-sided box (open top)
        floor = Line(LEFT * 3, RIGHT * 3, color=WHITE)
        left_wall = Line(UP * 2, DOWN * 2, color=WHITE)
        right_wall = Line(UP * 2, DOWN * 2, color=WHITE)

        # Position the walls correctly
        left_wall.move_to(LEFT * 3 + DOWN * 1)
        right_wall.move_to(RIGHT * 3 + DOWN * 1)
        box = VGroup(floor, left_wall, right_wall)

        # Create three balls (circles)
        balls = VGroup(
            *[
                Dot(radius=0.2, fill_color=BLUE).move_to(UP * 2 + LEFT * (1 - i))
                for i in range(2)
            ]
        )

        gravity = 3
        min_velocity = 1

        for ball in balls:
            velocity = ValueTracker(0)  # Initial velocity
            time_tracker = ValueTracker(0)  # Track time

            def update_ball(m, dt, time_tracker=time_tracker, velocity=velocity):
                damping_factor = 0.7  # Bounce energy loss

                time_tracker.increment_value(dt)
                v = velocity.get_value() + gravity * dt  # Apply gravity
                m.shift(DOWN * v * dt)  # Move the ball
                velocity.set_value(v)

                # Collision with floor (bouncing effect)
                if m.get_bottom()[1] <= floor.get_center()[1]:
                    new_v = -damping_factor * v  # Reduce bounce velocity
                    velocity.set_value(new_v)
                    m.move_to(
                        [m.get_x(), floor.get_center()[1] + 0.2, 0]
                    )  # Keep ball on floor

                    # Stop updating if the bounce velocity is too low or time exceeds 2 sec
                    if abs(new_v) < min_velocity:  # or time_tracker.get_value() > 2:
                        velocity.set_value(-1 * v)

            ball.add_updater(update_ball)

        # Animate dropping balls
        self.play(FadeIn(box), FadeIn(balls))
        self.wait(10)  # Let the balls bounce and settle
        # Acceleration due to gravity

        # # Stop updates to freeze the scene
        # for ball in balls:
        #     ball.clear_updaters()


class DistributiveArea2(Scene):
    def construct(self):
        # Title
        title = Tex("(3+2) \\cdot (4+1)").shift(UP * 3)
        bc = BLUE
        box_3_3_1 = SurroundingRectangle(title[1], color=bc)
        box_3_3_2 = SurroundingRectangle(title[7], color=bc)

        box_3_2_1 = SurroundingRectangle(title[1], color=bc)
        box_3_2_2 = SurroundingRectangle(title[9], color=bc)

        box_2_3_1 = SurroundingRectangle(title[3], color=bc)
        box_2_3_2 = SurroundingRectangle(title[7], color=bc)

        box_2_2_1 = SurroundingRectangle(title[3], color=bc)
        box_2_2_2 = SurroundingRectangle(title[9], color=bc)

        self.play(FadeIn(title))

        # Show the x-axis

        # Define bar lengths
        bar_3 = Rectangle(width=3, height=0.3, color=BLUE, fill_opacity=1)
        bar_2 = Rectangle(width=2, height=0.3, color=GREEN, fill_opacity=1)

        # Position horizontal bars
        top_3 = bar_3.move_to(LEFT + UP * 2)
        top_2 = bar_2.next_to(top_3, RIGHT, buff=0)
        corner = top_3.get_left()

        tick_marks = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=GREY_E)
            tick.move_to(top_3.get_left() + RIGHT * i)
            tick_marks.add(tick)

        # Position vertical bars
        left_3 = top_3.copy().rotate(-PI / 2, about_point=corner)
        left_2 = (
            top_2.copy()
            .rotate(PI / 2, about_point=corner)
            .next_to(left_3, DOWN, buff=0)
        )

        tick_marks_v = VGroup()
        for i in range(6):  # 0 to 5
            tick = Line(UP * 0.2, DOWN * 0.2, color=GREY_E)
            tick.move_to(top_3.get_left() + RIGHT * i)
            tick.rotate(-PI / 2, about_point=corner)

            tick_marks_v.add(tick)

        bar_4 = Rectangle(width=4, height=0.3, color=BLUE, fill_opacity=1)
        bar_1 = Rectangle(width=1, height=0.3, color=GREEN, fill_opacity=1)
        top_4 = bar_4.copy().move_to(corner + RIGHT * 4 / 2)
        top_1 = bar_1.copy().next_to(top_4, RIGHT, buff=0)

        self.play(FadeIn(top_4), FadeIn(top_1), FadeIn(tick_marks))

        self.play(FadeIn(left_3), FadeIn(left_2), FadeIn(tick_marks_v))
        self.wait(1)

        # Define rectangles for areas
        rect_3x3 = Rectangle(width=4, height=3, color=WHITE, fill_opacity=0.5)
        rect_3x2 = Rectangle(width=1, height=3, color=YELLOW, fill_opacity=0.5)
        rect_2x3 = Rectangle(width=4, height=2, color=ORANGE, fill_opacity=0.5)
        rect_2x2 = Rectangle(width=1, height=2, color=RED, fill_opacity=0.5)

        # Align rectangles properly
        rect_3x3.move_to(LEFT * 0.5 + UP * 0.5)
        rect_3x2.next_to(rect_3x3, RIGHT, buff=0, aligned_edge=UP)
        rect_2x3.next_to(rect_3x3, DOWN, buff=0, aligned_edge=LEFT)
        rect_2x2.next_to(rect_3x2, DOWN, buff=0, aligned_edge=LEFT)

        self.play(FadeIn(rect_3x3))
        self.play(FadeIn(rect_3x2))
        self.play(FadeIn(rect_2x3))
        self.play(FadeIn(rect_2x2))

        # Add labels inside rectangles
        label_3x3 = Tex("3 \\cdot 4").move_to(rect_3x3)
        box_3_3 = SurroundingRectangle(label_3x3, color=bc)
        label_3x2 = Tex("3 \\cdot 1").move_to(rect_3x2)
        box_3_2 = SurroundingRectangle(label_3x2, color=bc)
        label_2x3 = Tex("2 \\cdot 4").move_to(rect_2x3)
        box_2_3 = SurroundingRectangle(label_2x3, color=bc)
        label_2x2 = Tex("2 \\cdot 1").move_to(rect_2x2)
        box_2_2 = SurroundingRectangle(label_2x2, color=bc)

        self.play(
            FadeIn(label_3x3),
            FadeIn(box_3_3),
            FadeIn(box_3_3_1),
            FadeIn(box_3_3_2),
        )
        self.play(
            FadeOut(box_3_3),
            FadeOut(box_3_3_1),
            FadeOut(box_3_3_2),
        )

        self.play(
            FadeIn(label_3x2),
            FadeIn(box_3_2),
            FadeIn(box_3_2_1),
            FadeIn(box_3_2_2),
        )

        self.play(
            FadeOut(box_3_2),
            FadeOut(box_3_2_1),
            FadeOut(box_3_2_2),
        )

        self.play(
            FadeIn(label_2x3),
            FadeIn(box_2_3),
            FadeIn(box_2_3_1),
            FadeIn(box_2_3_2),
        )

        self.play(
            FadeOut(box_2_3),
            FadeOut(box_2_3_1),
            FadeOut(box_2_3_2),
        )

        self.play(
            FadeIn(label_2x2),
            FadeIn(box_2_2),
            FadeIn(box_2_2_1),
            FadeIn(box_2_2_2),
        )

        self.play(
            FadeOut(box_2_2),
            FadeOut(box_2_2_1),
            FadeOut(box_2_2_2),
        )

        self.wait(2)


class AddPolygon(Scene):
    def construct(self):
        # Basic Polygon

        polys_l = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=RED,
                    fill_opacity=0.5,
                )
                for j in range(3)
            ],
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(2)
            ],
        ).arrange(RIGHT, buff=0.2)
        # polys_l.shift(3 * LEFT)
        polys_l.shift(UP * 2)

        self.play(DrawBorderThenFill(polys_l), run_time=1)
        self.wait(0.5)

        polys = VGroup(
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=BLUE,
                    fill_opacity=0.5,
                )
                for j in range(2)
            ],
            *[
                RegularPolygon(
                    5,
                    radius=1,
                    # color=Color.from_hsv((j / 5, 1.0, 1.0)),
                    color=RED,
                    fill_opacity=0.5,
                )
                for j in range(3)
            ],
        ).arrange(RIGHT, buff=0.2)
        polys.shift(0.5 * DOWN)

        equal_sign = Text("=").scale(1.5)
        point = polys.get_left() + 0.5 * LEFT
        equal_sign.move_to(point)

        self.add(equal_sign)  # Add without animation (ManimGL optimized)

        self.play(DrawBorderThenFill(polys), run_time=1)

        self.wait(0.5)
        # equation
        equation = Tex(r"3 + 2 = 2 + 3").scale(1.5)
        equation.shift(DOWN * 2.5)

        self.play(Write(equation))
        self.wait(0.5)
        # self.interactive_embed()
