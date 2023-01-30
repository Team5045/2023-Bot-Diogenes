def limit(number: float, limits: list) -> float:
    """
    return a number within the limits, returning the limiting number if out of bounds
    number: any number
    limits: list of limits, first element is minimum, second is max
    ex:
        >>> limit(5, [-4, 4])
        >>> 4
    """
    return min(max(number, limits[0]), limits[1])
    