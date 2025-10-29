def create_instance():
    """
    This function demonstrates four ways of creating a TSP instance, using the well-known 14-city TSPLIB problem from Burma ("burma14").
    The burma14 TSPLIB file is described as follows:

    NAME: burma14
    TYPE: TSP
    COMMENT: 14-Staedte in Burma (Zaw Win)
    DIMENSION: 14
    EDGE_WEIGHT_TYPE: GEO
    EDGE_WEIGHT_FORMAT: FUNCTION 
    DISPLAY_DATA_TYPE: COORD_DISPLAY
    NODE_COORD_SECTION:
    1  16.47       96.10
    2  16.47       94.44
    3  20.09       92.54
    4  22.39       93.37
    5  25.23       97.24
    6  22.00       96.05
    7  20.47       97.02
    8  17.20       96.29
    9  16.30       97.38
    10  14.05       98.12
    11  16.53       97.38
    12  21.52       95.59
    13  19.41       97.13
    14  20.09       94.55
    EOF
    """
    
    from pytsp.structures.Instance import (
        create_instance_from_file,
        create_instance_from_coordinates,
        create_instance_from_cost_matrix
    )

    # Coordinates for the burma14 instance
    burma14_coordinates = [
        (16.47, 96.10),
        (16.47, 94.44),
        (20.09, 92.54),
        (22.39, 93.37),
        (25.23, 97.24),
        (22.00, 96.05),
        (20.47, 97.02),
        (17.20, 96.29),
        (16.30, 97.38),
        (14.05, 98.12),
        (16.53, 97.38),
        (21.52, 95.59),
        (19.41, 97.13),
        (20.09, 94.55)
    ]

    # Precomputed cost matrix for burma14
    burma14_cost_matrix = [
        [1, 153, 510, 706, 966, 581, 455, 70, 160, 372, 157, 567, 342, 398],
        [153, 1, 422, 664, 997, 598, 507, 197, 311, 479, 310, 581, 417, 376],
        [510, 422, 1, 289, 744, 390, 437, 491, 645, 880, 618, 374, 455, 211],
        [706, 664, 289, 1, 491, 265, 410, 664, 804, 1070, 768, 259, 499, 310],
        [966, 997, 744, 491, 1, 400, 514, 902, 990, 1261, 947, 418, 635, 636],
        [581, 598, 390, 265, 400, 1, 168, 522, 634, 910, 593, 19, 284, 239],
        [455, 507, 437, 410, 514, 168, 1, 389, 482, 757, 439, 163, 124, 232],
        [70, 197, 491, 664, 902, 522, 389, 1, 154, 406, 133, 508, 273, 355],
        [160, 311, 645, 804, 990, 634, 482, 154, 1, 276, 43, 623, 358, 498],
        [372, 479, 880, 1070, 1261, 910, 757, 406, 276, 1, 318, 898, 633, 761],
        [157, 310, 618, 768, 947, 593, 439, 133, 43, 318, 1, 582, 315, 464],
        [567, 581, 374, 259, 418, 19, 163, 508, 623, 898, 582, 1, 275, 221],
        [342, 417, 455, 499, 635, 284, 124, 273, 358, 633, 315, 275, 1, 247],
        [398, 376, 211, 310, 636, 239, 232, 355, 498, 761, 464, 221, 247, 1]
    ]

    # --- Example 1: Load instance from TSPLIB file ---
    my_instance = create_instance_from_file(name='burma14')
    print('Example 1: Load instance from TSPLIB file')
    print('  ', my_instance.get_info(), 'Exemplary cost from 1->2:', my_instance.get_weight_via_id(source_id=1, target_id=2))

    # --- Example 2: Create instance from coordinates (weights via default GEO function) ---
    my_instance = create_instance_from_coordinates(name='burma14_coordinates', 
                                             coordinates=burma14_coordinates,
                                             edge_weight_type="GEO",        # Note: This is the default value; it is explicitly stated here for completeness.
                                             edge_weight_format="FUNCTION"  # Note: This is the default value; it is explicitly stated here for completeness.
                                             )
    print('Example 2: Create instance from coordinates (weights via default GEO function)')
    print('   Note: When building from coordinates, node IDs begin at 1.')
    print('  ', my_instance.get_info(), 'Exemplary cost from 1->2:', my_instance.get_weight_via_id(source_id=1, target_id=2))
    
    # --- Example 3: Create instance from cost matrix ---
    my_instance = create_instance_from_cost_matrix(name="burma14_matrix", 
                                             cost_matrix=burma14_cost_matrix)
    print('Example 3: Create instance from cost matrix')
    print('   Note: When building from a cost matrix, node IDs begin at 0.')
    print('  ', my_instance.get_info(), 'Exemplary cost from 0->1:', my_instance.get_weight_via_id(source_id=0, target_id=1), ' (connection from the previous examples)')
    print('  ', my_instance.get_info(), 'Exemplary cost from 1->2:', my_instance.get_weight_via_id(source_id=1, target_id=2))

    # --- Example 4: Create instance from cost matrix and display coordinates ---
    my_instance = create_instance_from_cost_matrix(
        name="burma14_matrix",
        cost_matrix=burma14_cost_matrix,
        display_data_type="TWOD_DISPLAY",
        display_coordinates=burma14_coordinates
    )
    print('Example 4: Create instance from cost matrix and display coordinates')
    print('  ', my_instance.get_info(), 'Exemplary cost from 1->2:', my_instance.get_weight_via_id(source_id=1, target_id=2))
    
    # Plot TSP
    fig = my_instance.plot()  # returns a Plotly Figure object
    fig.show()

