from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
import numpy as np


def create_brownie():
    """Creates the brownie polygon"""
    brownie_coords = [(-2, -2), (1, -3), (3, 0), (2, 3), (-3, 2)]
    return Polygon(brownie_coords)


def create_knife(position, angle):
    """
    Creates the knife geometry (infinite half-plane)
    
    Args:
        position: Horizontal position of the knife
        angle: Rotation angle in degrees
    
    Returns:
        Polygon: Knife geometry
    """
    knife_base = Polygon([(-10, -10), (-10, 10), (0, 10), (0, -10)])
    knife_translated = translate(knife_base, xoff=position)
    knife_rotated = rotate(knife_translated, angle, origin=(0, 0))
    return knife_rotated


def calculate_cut(brownie, position, angle):
    """
    Calculates the cut area
    
    Args:
        brownie: Brownie polygon
        position: Knife position
        angle: Knife angle
    
    Returns:
        tuple: (cut piece, cut area)
    """
    knife = create_knife(position, angle)
    piece = brownie.intersection(knife)
    cut_area = piece.area
    return piece, cut_area


def calculate_error(cut_area, total_area):
    """
    Calculates the percentage error relative to the perfect cut (50%)
    
    Args:
        cut_area: Cut area
        total_area: Total brownie area
    
    Returns:
        float: Percentage error
    """
    target_area = total_area / 2
    error = ((cut_area - target_area) / target_area) * 100
    return error


def optimized_binary_search(brownie, angle, min_pos=-4.0, max_pos=4.0, num_iterations=20):
    """
    Executes binary search to find the optimal cut position
    
    Args:
        brownie: Brownie polygon
        angle: Knife angle (fixed during search)
        min_pos: Initial minimum position
        max_pos: Initial maximum position
        num_iterations: Number of iterations
    
    Returns:
        dict: {
            'optimal_position': float,
            'position_history': list,
            'error_history': list,
            'area_history': list
        }
    """
    total_area = brownie.area
    target_area = total_area / 2
    
    position_history = []
    error_history = []
    area_history = []
    
    for i in range(num_iterations):
        mid_pos = (min_pos + max_pos) / 2
        _, cut_area = calculate_cut(brownie, mid_pos, angle)
        error = calculate_error(cut_area, total_area)
        
        # Store history
        position_history.append(mid_pos)
        error_history.append(error)
        area_history.append(cut_area)
        
        # Adjust interval
        if cut_area < target_area:
            min_pos = mid_pos
        else:
            max_pos = mid_pos
    
    optimal_position = (min_pos + max_pos) / 2
    
    return {
         "optimal_position": optimal_position,
        "position_history": position_history,
        "error_history": error_history,
        "area_history": area_history
    }
