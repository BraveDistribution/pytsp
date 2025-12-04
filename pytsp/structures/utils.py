from typing import Literal

# Define possibel EdgeWeightType for TSPLIB Class
EdgeWeightType = Literal[
    "EXPLICIT",  # Weights are listed explicitly in the corresponding section
    "EUC_2D",    # Weights are Euclidean distances in 2-D
    "EUC_3D",    # Weights are Euclidean distances in 3-D
    "MAX_2D",    # Weights are maximum distances in 2-D
    "MAX_3D",    # Weights are maximum distances in 3-D
    "MAN_2D",    # Weights are Manhattan distances in 2-D
    "MAN_3D",    # Weights are Manhattan distances in 3-D
    "CEIL_2D",   # Weights are Euclidean distances in 2-D rounded up
    "GEO",       # Weights are geographical distances
    "ATT",       # Special distance function for problems att48 and att532
    "XRAY1",     # Special distance function for crystallography problems (Version 1)
    "XRAY2",     # Special distance function for crystallography problems (Version 2)
    "SPECIAL"    # There is a special distance function documented elsewhere
]

# Define possibel EdgeWeightFormat for TSPLIB Class
EdgeWeightFormat = Literal[
    "FUNCTION",          # Weights are given by a function
    "FULL_MATRIX",       # Weights are given by a full matrix
    "UPPER_ROW",         # Upper triangular matrix (row-wise without diagonal entries)
    "LOWER_ROW",         # Lower triangular matrix (row-wise without diagonal entries)
    "UPPER_DIAG_ROW",    # Upper triangular matrix (row-wise including diagonal entries)
    "LOWER_DIAG_ROW",    # Lower triangular matrix (row-wise including diagonal entries)
    "UPPER_COL",         # Upper triangular matrix (column-wise without diagonal entries)
    "LOWER_COL",         # Lower triangular matrix (column-wise without diagonal entries)
    "UPPER_DIAG_COL",    # Upper triangular matrix (column-wise including diagonal entries)
    "LOWER_DIAG_COL"     # Lower triangular matrix (column-wise including diagonal entries)
]

# Define possibel DisplayDataType for TSPLIB Class
DisplayDataType = Literal[
    "COORD_DISPLAY",  # Display is generated from the node coordinates
    "TWOD_DISPLAY",   # Explicit coordinates in 2-D are given
    "NO_DISPLAY"      # No graphical display is possible
]
