import matplotlib.pyplot as plt

# 데이터 생성
x = [1, 2, 3, 4, 5]
y1 = [1, 2, 3, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [3, 4, 5, 6, 7]

# plot 생성
plt.plot(x, y1, label='y1')
plt.plot(x, y2, label='y2')
plt.plot(x, y3, label='y3')

# legend 생성
plt.legend()

# plot 표시
plt.show()
