import numpy as np

# クォータニオン演算関連関数

# クォータニオンの加算(正直足すだけだからほとんど意味ない)
# 引数
# q1,q2:クォータニオン(np.array([w,x,y,z]))
# 戻り値
# クォータニオンの加算結果(np.array([w,x,y,z]))
def add_quaternion(q1:np.array, q2:np.array) -> np.array:
    return q1+q2
# クォータニオンの乗算
# 引数
# q1,q2:クォータニオン(np.array([w,x,y,z]))
# 戻り値
# クォータニオンの乗算結果(np.array([w,x,y,z]))
def mult_quaternion(q1:np.array, q2:np.array) -> np.array:
    out = np.zeros(4)
    out[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
    out[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
    out[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
    out[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
    return out

# クォータニオンの共役
# 引数
# q:クォータニオン(np.array([w,x,y,z]))
# 戻り値
# クォータニオンの共役(np.array([w,x,y,z]))
def conjugate_quaternion(q:np.array)->np.array:
    return np.array([q[0], -q[1], -q[2], -q[3]])

# クォータニオンの逆元
# 引数
# q:クォータニオン(np.array([w,x,y,z]))
# 戻り値
# クォータニオンの逆元(np.array([w,x,y,z]))
def inverse_quaternion(q:np.array)->np.array:
    return conjugate_quaternion(q) / np.dot(q, q)

# 角度と回転軸からクォータニオンを生成
# 引数
# angle:回転角度(度)
# axis:回転軸ベクトル
# 戻り値
# クォータニオン(np.array([w,x,y,z]))
def deg2quat(angle:float, axis:np.array = np.array([1., 0., 0.]))->np.array:
    if np.linalg.norm(axis) <= 0:
        return np.array([1., 0., 0., 0.])
    rad = angle * np.pi / 180
    axis = axis / np.linalg.norm(axis)
    return np.array([np.cos(rad/2), axis[0]*np.sin(rad/2), axis[1]*np.sin(rad/2), axis[2]*np.sin(rad/2)])