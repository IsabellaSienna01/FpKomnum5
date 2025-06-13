import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

def f(x):
    return x**3 - 100

def regula_falsi(func, a, b, tol=1e-6, max_iter=100):
    if func(a) * func(b) >= 0:
        print("Kondisi f(a) * f(b) < 0 tidak terpenuhi.")
        print(f"f({a}) = {func(a):.6f}, f({b}) = {func(b):.6f}")
        return None, []

    c = a 
    history = [] 
    
    print(f"Mencari akar untuk f(x) = x^3 - 100 pada interval [{a}, {b}]")
    print("-" * 60)

    for i in range(max_iter):
        fa = func(a)
        fb = func(b)
        
        c_prev = c
        c = (a * fb - b * fa) / (fb - fa)
        
        fc = func(c)
        
        if i > 0:
            error = abs((c - c_prev) / c) if c != 0 else abs(c-c_prev)
        else:
            error = float('inf') 
            
        history.append([i + 1, a, b, c, fa, fb, fc, error])

        if abs(fc) < tol:
            break
            
        if fa * fc < 0:
            b = c
        else:
            a = c
            
    headers = ["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Error Relatif"]
    print(tabulate(history, headers=headers, floatfmt=".7f", tablefmt="grid"))
    
    if abs(func(c)) < tol:
        print(f"\nKonvergensi tercapai setelah {len(history)} iterasi.")
        return c, history
    else:
        print(f"\nTidak konvergen setelah {max_iter} iterasi.")
        return c, history 

def ans(func, history, root):
    a_awal = history[0][1]
    b_awal = history[0][2]

    x_vals = np.linspace(a_awal - 0.5, b_awal + 0.5, 400)
    y_vals = func(x_vals)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(x_vals, y_vals, 'b-', label=f'f(x) = x³ - 100', linewidth=2)
    
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)

    for i, data in enumerate(history):
        iter_num, a, b, c, fa, fb, fc, err = data
        
        ax.plot([a, b], [fa, fb], 'r--', alpha=0.6, 
                label=f'Garis Iterasi {iter_num}' if i < 3 else "")
        
        ax.plot(a, fa, 'go', markersize=8, alpha=0.7)
        ax.plot(b, fb, 'go', markersize=8, alpha=0.7) 
        ax.plot(c, 0, 'kx', markersize=10, markeredgewidth=2)
        ax.plot(c, fc, 'ko', markersize=5)

    if root is not None:
        ax.plot(root, func(root), 'y*', markersize=15, markeredgewidth=1.5,
                markeredgecolor='black', label=f'Akar Ditemukan: x ≈ {root:.6f}')

    ax.set_title('Grafik Solusi Akar Persamaan dengan Regula Falsi', fontsize=16)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.legend(loc='upper left')
    ax.grid(True)
    
    last_a = history[-1][1]
    last_b = history[-1][2]
    ax.set_xlim([min(a_awal, last_a) - 0.2, max(b_awal, last_b) + 0.2])
    
    plt.show()


if __name__ == "__main__":
    a = 4.0 
    b = 5.0  
    toleransi = 1e-7 
    
    akar, iterationans = regula_falsi(f, a, b, tol=toleransi)

    if akar is not None and iterationans:
        print(f"\nAkar yang ditemukan adalah x = {akar:.7f}")
        print(f"Nilai f(x) pada akar tersebut adalah f({akar:.7f}) = {f(akar):.7f}")
        
        ans(f, iterationans, akar)
    else:
        print("\nTidak dapat menemukan akar atau proses dihentikan.")