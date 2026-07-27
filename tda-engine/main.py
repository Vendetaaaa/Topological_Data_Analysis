import numpy as np
from tda import PersistentHomology, generate_noisy_circle, plot_persistence_results

def main():
    np.random.seed(42)
    data = generate_noisy_circle(n_samples=50, radius=2.0, noise=0.15)

    ph = PersistentHomology(data)
    h0 = ph.compute_h0_persistence()
    h1 = ph.compute_h1_persistence(max_edge_len=3.0)

    plot_persistence_results(data, h0, h1)

if __name__ == "__main__":
    main()
