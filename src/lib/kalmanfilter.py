class KalmanFilter:
    def __init__(self):
        # Initialize Kalman filter variables
        self.q_angle = 0.001
        self.q_bias = 0.003
        self.r_measure = 0.03

        self.angle = 0.0  # Reset the angle
        self.bias = 0.0  # Reset bias

        self.P = [[0.0, 0.0], [0.0, 0.0]]  # Error covariance matrix

    def update(self, new_angle, new_rate, dt):
        # Predict
        rate = new_rate - self.bias
        self.angle += dt * rate

        self.P[0][0] += dt * (dt*self.P[1][1] - self.P[0][1] - self.P[1][0] + self.q_angle)
        self.P[0][1] -= dt * self.P[1][1]
        self.P[1][0] -= dt * self.P[1][1]
        self.P[1][1] += self.q_bias * dt

        # Update
        S = self.P[0][0] + self.r_measure
        K = [self.P[0][0] / S, self.P[1][0] / S]

        y = new_angle - self.angle
        self.angle += K[0] * y
        self.bias += K[1] * y

        P00_temp = self.P[0][0]
        P01_temp = self.P[0][1]

        self.P[0][0] -= K[0] * P00_temp
        self.P[0][1] -= K[0] * P01_temp
        self.P[1][0] -= K[1] * P00_temp
        self.P[1][1] -= K[1] * P01_temp

        return self.angle


