class Velocity:
    """A class representing velocity."""

    def __init__(self, vx: int = 0, vy: int = 0):
        """Initialize the Velocity object with given x and y velocities."""
        self._vx = vx
        self._vy = vy

    @property
    def vx(self) -> int:
        """Get the x velocity."""
        return self._vx

    @property
    def vy(self) -> int:
        """Get the y velocity."""
        return self._vy

    @vx.setter
    def vx(self, value: int):
        """Set the x velocity."""
        self._vx = value

    @vy.setter
    def vy(self, value: int):
        """Set the y velocity."""
        self._vy = value
