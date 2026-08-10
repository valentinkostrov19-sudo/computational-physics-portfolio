"""
Классический маятник с трением

Система:
    dθ/dt = ω
    dω/dt = -(g/L) * sin(θ) - γ * ω
    
Параметры:
    g = 9.8 м/с², L = 1.0 м, γ = 0.3 (коэффициент трения)
    
Метод: RK4 (Рунге-Кутты 4-го порядка)
Визуализация: фазовый портрет, временные зависимости, анимация
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Параметры системы ---
g = 9.8
L = 1.0
gamma = 0.3

# --- Функция правой части ---
def pendulum_derivatives(state, g, L, gamma):
    theta, omega = state
    dtheta = omega
    domega = -(g / L) * np.sin(theta) - gamma * omega
    return np.array([dtheta, domega])

# --- Метод Рунге-Кутты 4-го порядка ---
def rk4_step(state, dt, g, L, gamma):
    k1 = pendulum_derivatives(state, g, L, gamma)
    k2 = pendulum_derivatives( + 0.5 * dt * k1, g, L, gamma)
    k3 = pendulum_derivatives(state + 0.5 * dt * k2, g, L, gamma)
    k4 = pendulum_derivatives(state + dt * k3, g, L, gamma)
    return state + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

# --- Параметры расчета ---
theta0 = np.pi / 2 # начальный угол (90 градусов)
omega0 = 0.0 # начальная скорость
dt = 0.01
T = 10.0

state0 = np.array([theta0, omega0])
t = np.arange(0, T, dt)

# --- Интегрирование ---
states = np.zeros((len(t), 2))
states[0] = state0

for i in range(1, len(t)):
    states[i] = rk4_step(states[i-1], dt, g, L, gamma)

theta = states[:, 0]
omega = states[:, 1]

# --- Энергия системы ---
E = 0.5 * L**2 * omega**2 + g * L * (1 - np.cos(theta))

# --- Графики ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. Угол
axes[0].plot(t, theta)
axes[0].set_xlabel("Время, с")
axes[0].set_ylabel("Угол, рад")
axes[0].set_title("θ(t)")
axes[0].grid()

# 2. Фазовый портрет
axes[1].plot(theta, omega, linewidth=0.8)
axes[1].set_xlabel("θ")
axes[1].set_ylabel("ω")
axes[1].set_title("Фазовый портрет")
axes[1].grid()

# 3. Энергия
axes[2].plot(t, E)
axes[2].set_xlabel("Время, с")
axes[2].set_ylabel("Энергия, Дж")
axes[2].set_title("Затухание энергии")
axes[2].grid()

plt.tight_layout()
plt.show()

# --- Анимация маятника ---
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def update(frame):
    theta_t = theta[frame]
    x_t = L * np.sin(theta_t)
    y_t = -L * np.cos(theta_t)
    line.set_data([0, x_t], [0, y_t])
    time_text.set_text(f't = {t[frame]:.2f} с')
    return line, time_text

anim = FuncAnimation(fig, update, frames=len(t), interval=20)
plt.show()
    
    
























