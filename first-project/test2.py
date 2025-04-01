#!/usr/bin/env python


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
