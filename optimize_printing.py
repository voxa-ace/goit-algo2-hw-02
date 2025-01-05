from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    """
    A data class to represent a 3D printing job.
    """
    id: str  # Unique job ID
    volume: float  # Volume of the model in cm³
    priority: int  # Priority of the job (1: High, 2: Medium, 3: Low)
    print_time: int  # Time required to print the model in minutes


@dataclass
class PrinterConstraints:
    """
    A data class to represent printer constraints.
    """
    max_volume: float  # Maximum volume that the printer can handle in one batch
    max_items: int  # Maximum number of items the printer can handle in one batch


def optimize_printing(print_jobs, constraints):
    """
    Optimizes the print queue based on priorities and printer constraints.

    Args:
        print_jobs: List of print jobs (dicts).
        constraints: Printer constraints (dict).

    Returns:
        Dict with print order and total time.
    """
    max_volume = constraints['max_volume']
    max_items = constraints['max_items']

    # Sort jobs by priority (stable sorting ensures same-priority order is maintained)
    print_jobs.sort(key=lambda x: x['priority'])

    total_time = 0
    print_order = []

    current_group = []
    current_volume = 0

    for job in print_jobs:
        # Check if adding the current job exceeds constraints
        if (
            current_volume + job['volume'] > max_volume
            or len(current_group) + 1 > max_items
        ):
            # Calculate time for current group (max print time in the group)
            group_time = max(item['print_time'] for item in current_group)
            total_time += group_time
            print_order.extend(item['id'] for item in current_group)

            # Start a new group
            current_group = []
            current_volume = 0

        # Add the job to the current group
        current_group.append(job)
        current_volume += job['volume']

    # Add the last group
    if current_group:
        group_time = max(item['print_time'] for item in current_group)
        total_time += group_time
        print_order.extend(item['id'] for item in current_group)

    return {
        "print_order": print_order,
        "total_time": total_time,
    }



def test_printing_optimization():
    """
    Runs multiple test cases for the 3D printing optimization algorithm.
    """
    # Test Case 1: Jobs with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test Case 2: Jobs with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # Medium priority
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # High priority
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # Low priority
    ]

    # Test Case 3: Jobs exceeding constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (Same Priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print Order: {result1['print_order']}")
    print(f"Total Time: {result1['total_time']} minutes")

    print("\nTest 2 (Different Priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print Order: {result2['print_order']}")
    print(f"Total Time: {result2['total_time']} minutes")

    print("\nTest 3 (Exceeding Constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print Order: {result3['print_order']}")
    print(f"Total Time: {result3['total_time']} minutes")


if __name__ == "__main__":
    test_printing_optimization()
