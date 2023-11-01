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


class PaddleCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        no_collision = True
        if request["ball"].x == request["paddle"].x + 1:
            if (
                request["paddle"].y <= request["ball"].y
                and request["ball"].y <= request["paddle"].y + request["paddle"].width
            ):
                no_collision = False
                request["ball"].reverse_vx()
                request["ball"].reverse_vy()
                return request

        if no_collision:
            return super().handle(request)


class BoundaryCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        if request.type == "collision":
            self._paddle.move_down()
        return super().handle(request)


class BrickCollisionHandler(CollisionHandler):
    def handle(self, request: Any) -> None:
        if request.type == "collision":
            self._paddle.move_down()
        return super().handle(request)
