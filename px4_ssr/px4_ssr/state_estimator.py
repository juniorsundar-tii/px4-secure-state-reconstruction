import rclpy
from rclpy.qos import HistoryPolicy, QoSProfile
import numpy as np
import scipy as sc
# from rclpy.duration import Duration
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from px4_ssr.drone_system import DroneSystem
from typing import List
import itertools

class XProb:
    
    def __init__(self, x0, A_gamma, gamma):
        self.x0 = x0
        self.A_gamma = A_gamma
        self.gamma = gamma

def nchoosek(v: List[int], k: int) -> List[List[int]]:
    """
    Returns a list of lists containing all possible combinations of the elements of vector v taken k at a time.
    
    Args:
        v (List[int]): A list of elements to take combinations from.
        k (int): The number of elements in each combination.
    
    Returns:
        List[List[int]]: A list of lists where each sublist is a combination of k elements from v.
    """
    return [list(comb) for comb in itertools.combinations(v, k)]

class StateEstimator(Node):
    """
    StateEstimator Node for reconstructing state given sensor readings.
    """

    def __init__(self):
        super().__init__("state_estimator", parameter_overrides=[])

        self.qos_profile = QoSProfile(history = HistoryPolicy.KEEP_LAST, depth = 5)

        self.drone = DroneSystem()
        # self.s = self.drone.p - 1
        self.s = 1
        self.y_vec = []
        self.u_vec = []
        self.gamma_set = []

        self.sensor_subscriber = self.create_subscription(
            Float64MultiArray,
            "/sensor_matrix",
            self.secure_state_estimator,
            self.qos_profile,
        )

    def secure_state_estimator(self, msg: Float64MultiArray):
        self.update_sensor_matrix(msg)

        # Prerequisite is to have enough past readings
        if len(self.y_vec) < self.drone.n:
            return
        elif len(self.y_vec) > self.drone.n:
            comb = self.gamma_set
        else:
            comb = nchoosek([i for i in range(1, self.drone.p + 1)], self.drone.p - self.s)

        X0_arr = []
        Gamma_set_new = []

        # comb = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
        for i in range(len(comb)):
            gamma = comb[i] # [1, 2, 3]
            O_gamma = np.zeros(((self.drone.p - self.s) * self.drone.n, self.drone.n)); # (6, 2)
            Y_gamma = np.zeros(((self.drone.p - self.s) * self.drone.n, 1)); # (6, 1)

            for j in range(len(gamma)):
                sensor_ind = gamma[j] # 1
                O = self.drone.O_cell[sensor_ind] # (2, 2)
                Y_tilde = np.array(self.y_vec)[:,sensor_ind].reshape(-1, 1) # (2, 1)
                O_gamma[self.drone.n * j:self.drone.n * (j + 1), :] = O
                Y = Y_tilde - self.drone.F_cell[sensor_ind] @ self.u_vec # (2, 1) - (2, 2) * (2, 1) --> (2, 1)
                Y_gamma[self.drone.n * j:self.drone.n * (j + 1)] = Y

            x0_gamma = np.divide(O_gamma, Y_gamma)

            if np.norm(Y_gamma - O_gamma @ x0_gamma) <= 1e-3:
                Gamma_set_new.append(gamma)

                if np.linalg.matrix_rank(O_gamma) < self.drone.n:
                    A_gamma = sc.linalg.null_space(O_gamma, rcond = 1e-4)
                else:
                    A_gamma = 0

                x0_prob = XProb(x0_gamma, A_gamma, gamma)
                X0_arr.append(x0_prob)

        Xt_cell: List[XProb] = []

        for i in range(len(X0_arr)):
            x0 = X0_arr[1].x0
            A_x0 = X0_arr[i].A_gamma
            
            xt = np.zeros_line(x0)
            A_xt = np.zeros_line(A_x0)

            x_history = np.zeros(self.drone.n, self.drone.n)
            x_history[:,0] = x0

            for j in range(1, self.drone.n):
                x_history[:,j] = self.drone.Ad @ x_history[:,j-1] + self.drone.Bd @ self.u_vec[:, j-1]

            xt = x_history[:, self.drone.n - 1]

            xt_prob =

        return Xt_cell, Gamma_set_new

    def update_sensor_matrix(self, msg: Float64MultiArray):
        # [[x0, y0, z0], ... , [xn-1, yn-1, zn-1]]
        self.y_vec.append(msg.data)

        # Keep only the last n readings
        if len(self.y_vec) > self.drone.n:
            self.y_vec = self.y_vec[1:]


def main(args=None):
    print("Starting state_estimator node...")
    rclpy.init(args=args)

    state_estimator = StateEstimator()

    try:
        rclpy.spin(state_estimator)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
