import numpy as np
import matplotlib.pyplot as plt

def generate_noisy_circle(n_samples=50, radius=2.0, noise=0.15):
    angles = np.random.uniform(0, 2 * np.pi, n_samples)
    x = radius * np.cos(angles) + np.random.normal(0, noise, n_samples)
    y = radius * np.sin(angles) + np.random.normal(0, noise, n_samples)
    return np.column_stack((x, y))

def plot_persistence_results(data, h0, h1):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].scatter(data[:, 0], data[:, 1], color='crimson', zorder=3)
    ax[0].set_title("Input Point Cloud")
    ax[0].set_aspect('equal')
    ax[0].grid(True, linestyle='--', alpha=0.5)

    for birth, death in h0:
        if death != np.inf:
            ax[1].scatter(birth, death, color='blue', alpha=0.6, label='H0 (Connected Comp.)' if 'H0 (Connected Comp.)' not in ax[1].get_legend_handles_labels()[1] else "")
    for birth, death in h1:
        ax[1].scatter(birth, death, color='red', marker='^', s=50, label='H1 (1D Loops)' if 'H1 (1D Loops)' not in ax[1].get_legend_handles_labels()[1] else "")

    max_val = max([d for _, d in h0 if d != np.inf] + [d for _, d in h1]) * 1.1
    ax[1].plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Diagonal')
    ax[1].set_xlabel("Birth Radius")
    ax[1].set_ylabel("Death Radius")
    ax[1].set_title("Persistence Diagram")
    ax[1].legend()
    ax[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()
