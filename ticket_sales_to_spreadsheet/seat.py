from dataclasses import dataclass, asdict

@dataclass
class Seat:
    id: int
    row: int
    column: int
    occupied: int

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
