import math


def norm(vector):
    return math.sqrt(sum(x**2 for x in vector))


def copy(arr):
    if isinstance(arr, list):
        return [copy(item) for item in arr]
    else:
        return arr


def cross(a, b):
    if len(a) != 3 or len(b) != 3:
        raise ValueError("Both vectors must have three elements")

    result = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]

    return result


def array(lst):
    return list(lst)


def cosd(x):
    angle_rad = math.radians(x)
    return math.cos(angle_rad)


def sind(x):
    angle_rad = math.radians(x)
    return math.sin(angle_rad)


def normalise(vector: list) -> list:
    norm = math.sqrt(sum(x**2 for x in vector))
    return [x / norm for x in vector]


def normaliseAVectorWithAnotherNorm(vector: list, norm: float) -> list:
    return [x / norm for x in vector]


def c_(*arrays):
    num_rows = len(arrays[0])
    result = []
    for i in range(num_rows):
        row = []
        for arr in arrays:
            if isinstance(arr[i], list):
                row.extend(arr[i])
            else:
                row.append(arr[i])
        result.append(row)
    return result


def matmul(A, B):
    # Check dimensions
    if len(A[0]) != len(B):
        raise ValueError(
            "Matrix dimensions are not compatible for multiplication")

    # Create the result matrix
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    # Perform matrix multiplication
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result


def transpose(matrix):
    # Get the number of rows and columns
    rows = len(matrix)
    cols = len(matrix[0])

    # Create a new matrix with swapped dimensions
    result = [[0 for _ in range(rows)] for _ in range(cols)]

    # Copy elements from the original matrix to the transposed matrix
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]

    return result


def chiaverini(dcm):
    n = 0.5 * math.sqrt(dcm[0][0] + dcm[1][1] + dcm[2][2] + 1.0)
    e = [0.5 * math.copysign(math.sqrt(dcm[0][0] - dcm[1][1] - dcm[2][2] + 1.0), dcm[2][1] - dcm[1][2]),
         0.5 * math.copysign(math.sqrt(dcm[1][1] - dcm[2][2] - dcm[0][0] + 1.0), dcm[0][2] - dcm[2][0]),
         0.5 * math.copysign(math.sqrt(dcm[2][2] - dcm[0][0] - dcm[1][1] + 1.0), dcm[1][0] - dcm[0][1])]
    q = []
    q.append(n)
    for x in range(3):
        q.append(e[x])
    return q

def euler_to_dcm(euler:tuple | list):
    # Convert Euler angles to radians
    roll_rad = math.radians(euler[0])
    pitch_rad = math.radians(euler[1])
    yaw_rad = math.radians(euler[2])

    # Calculate trigonometric functions
    cy = math.cos(yaw_rad)
    sy = math.sin(yaw_rad)
    cp = math.cos(pitch_rad)
    sp = math.sin(pitch_rad)
    cr = math.cos(roll_rad)
    sr = math.sin(roll_rad)

    # Calculate the DCM
    dcm = (
        (cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr),
        (sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr),
        (-sp, cp * sr, cp * cr)
    )

    return dcm