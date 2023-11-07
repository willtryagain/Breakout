import logging
import random
from math import copysign
from typing import Any, Optional


class CollisionHandler:
    _next_handler: Optional["CollisionHandler"] = None

    def set_next(self, next_handler: "CollisionHandler") -> None:
        self._next_handler = next_handler
        return next_handler

    def handle(self, request: Any) -> None:
        if self._next_handler is not None:
            return self._next_handler.handle(request)

        return None

    def __repr__(self) -> str:
        return "CollisionHandler"


class PaddleCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        if request["ball"].x == request["paddle"].x - 1:
            if (
                request["paddle"].y <= request["ball"].y
                and request["ball"].y + request["ball"].width
                <= request["paddle"].y + request["paddle"].width
            ):
                if request["ball"]._dead:
                    request["ball"]._dead = False
                    request["ball"].vx = -1
                    if random.randint(0, 1) == 0:
                        request["ball"].vy = -1
                    else:
                        request["ball"].vy = 1

                elif request["paddle"].grab:
                    request["ball"].set_vx(0)
                    request["ball"].set_vy(0)
                else:
                    logging.debug("Paddle collision")
                    request["ball"].reverse_vx()
                    paddle_mid = request["paddle"].y + request["paddle"].width // 2
                    bias = abs(request["ball"].y - paddle_mid) / request["paddle"].width
                    bias = int(bias)
                    request["ball"].vy = copysign(
                        abs(request["ball"].vy + bias), request["ball"].vy
                    )
                    logging.debug(request["ball"])
                return request

        return super().handle(request)

    def __repr__(self) -> str:
        return "PaddleCollisionHandler()"


class BoundaryCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        # collide with the top wall
        if request["ball"].x == 0:
            request["ball"].reverse_vx()
            return request

        # collide with side walls
        if (
            request["ball"].y == 0
            or request["ball"].y + request["ball"].width + 1 == request["display"].width
        ):
            request["ball"].reverse_vy()

        return super().handle(request)

    def __repr__(self) -> str:
        return "BoundaryCollisionHandler()"


class BrickCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        if request.type == "collision":
            self._paddle.move_down()
        return super().handle(request)
