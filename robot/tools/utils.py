class Lim():
    def limit(number: float, limits: list) -> float:
        return min(max(number, limits[0]), limits[1])