#!/usr/bin/env python3
"""
Nome: Camila Oliveira Gomes
"""

import math
import matplotlib.pyplot as plt

def capacidade_nyquist(largura_banda_hz: float, niveis: int) -> float:
    return 2.0 * largura_banda_hz * math.log2(niveis)

def capacidade_shannon(largura_banda_hz: float, snr_linear: float) -> float:
    return largura_banda_hz * math.log2(1.0 + snr_linear)

def snr_db_para_linear(snr_db: float) -> float:
    return 10.0 ** (snr_db / 10.0)

def ler_lista_floats(mensagem: str) -> list:
    while True:
        entrada = input(mensagem).strip()
        try:
            valores = [float(x.strip()) for x in entrada.split(",") if x.strip()]
            if len(valores) > 0:
                return valores
            print("Digite pelo menos um valor.")
        except ValueError:
            print("Formato inválido. Digite números separados por vírgula.")

def ler_lista_ints(mensagem: str, minimo: int = 2) -> list:
    while True:
        entrada = input(mensagem).strip()
        try:
            valores = [int(x.strip()) for x in entrada.split(",") if x.strip()]
            if all(v >= minimo for v in valores) and len(valores) > 0:
                return valores
            print(f"Todos os valores devem ser inteiros maiores ou iguais a {minimo}.")
        except ValueError:
            print("Formato inválido. Digite números inteiros separados por vírgula.")

def main():
    while True:
        print("\n" + "=" * 70)
        print(" ATIVIDADE 10 - ESCOLHA O EXPERIMENTO A EXECUTAR:")
        print("   1 - Experimento 1: Capacidade de Nyquist (C vs N)")
        print("   2 - Experimento 2: Capacidade de Shannon (C vs B)")
        print("   3 - Experimento 3: Influência do Ruído (C vs SNR em dB)")
        print("   4 - Experimento 4: Nyquist versus Shannon (Comparativo)")
        print("   0 - Sair")
        print("=" * 70)

        opcao = input("\nDigite a sua opção (0 a 4): ").strip()

        if opcao == "0":
            print("\nPrograma finalizado com sucesso!")
            break

     
        elif opcao == "1":
            print("\n--- Experimento 1: Capacidade de Nyquist ---")
            b_vals = ler_lista_floats("Digite as Larguras de Banda em kHz (ex: 1, 5, 10): ")
            n_vals = ler_lista_ints("Digite os Níveis N (ex: 2, 4, 8, 16): ", minimo=2)

            print("\n" + "-" * 72)
            print(f"{'B (kHz)':^10} | {'N (níveis)':^12} | {'bits/símbolo':^14} | {'Capacidade (kbit/s)':^22}")
            print("-" * 72)

            dados_grafico = {b: [] for b in b_vals}
            for b in b_vals:
                b_hz = b * 1000.0
                for n in n_vals:
                    c_bps = capacidade_nyquist(b_hz, n)
                    c_kbps = c_bps / 1000.0
                    dados_grafico[b].append(c_kbps)
                    bits = math.log2(n)
                    print(f"{b:^10.1f} | {n:^12} | {bits:^14.0f} | {c_kbps:^22.2f}")
                print("-" * 72)

            plt.figure(figsize=(9, 5.5))
            for b in b_vals:
                plt.plot(n_vals, dados_grafico[b], marker='o', linewidth=2, label=f"B = {b} kHz")
            plt.title("Experimento 1: Capacidade de Nyquist (C vs N)", fontsize=13, fontweight='bold')
            plt.xlabel("Número de Níveis de Sinalização (N)", fontsize=11)
            plt.ylabel("Capacidade C (kbit/s)", fontsize=11)
            plt.xticks(n_vals)
            plt.grid(True, linestyle=":", alpha=0.7)
            plt.legend(title="Largura de Banda")
            plt.tight_layout()
            plt.show()

       
        elif opcao == "2":
            print("\n--- Experimento 2: Capacidade de Shannon (C vs B) ---")
            b_vals = ler_lista_floats("Digite as Larguras de Banda em kHz (ex: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10): ")
            snr_vals = ler_lista_floats("Digite as SNR lineares (ex: 1000, 5000, 10000, 50000): ")

            print("\n" + "-" * 72)
            print(f"{'B (kHz)':^10} | {'SNR (linear)':^16} | {'Capacidade (kbit/s)':^22} | {'Capacidade (Mbit/s)':^18}")
            print("-" * 72)

            dados_grafico = {s: [] for s in snr_vals}
            for s in snr_vals:
                for b in b_vals:
                    b_hz = b * 1000.0
                    c_bps = capacidade_shannon(b_hz, s)
                    c_kbps = c_bps / 1000.0
                    c_mbps = c_bps / 1e6
                    dados_grafico[s].append(c_kbps)
                    print(f"{b:^10.1f} | {s:^16,.0f} | {c_kbps:^22.2f} | {c_mbps:^18.3f}")
                print("-" * 72)

            plt.figure(figsize=(9, 5.5))
            for s in snr_vals:
                plt.plot(b_vals, dados_grafico[s], marker='s', linewidth=2, label=f"SNR = {s:,.0f}")
            plt.title("Experimento 2: Capacidade de Shannon (C vs B)", fontsize=13, fontweight='bold')
            plt.xlabel("Largura de Banda B (kHz)", fontsize=11)
            plt.ylabel("Capacidade C (kbit/s)", fontsize=11)
            plt.xticks(b_vals)
            plt.grid(True, linestyle=":", alpha=0.7)
            plt.legend(title="Relação Sinal-Ruído")
            plt.tight_layout()
            plt.show()


        elif opcao == "3":
            print("\n--- Experimento 3: Influência do Ruído (C vs SNR em dB) ---")
            b_khz = float(input("Digite a Largura de Banda fixa B em kHz (ex: 5): "))
            b_hz = b_khz * 1000.0
            snr_db_vals = ler_lista_floats("Digite a faixa de SNR em dB (ex: 0, 5, 10, 15, 20, 25, 30, 35, 40): ")

            print("\n" + "=" * 72)
            print(f" TABELA CONSOLIDADA - B = {b_khz:.1f} kHz")
            print("=" * 72)
            print(f"{'SNR (dB)':^10} | {'SNR (linear)':^16} | {'Capacidade (kbit/s)':^22} | {'Capacidade (bit/s)':^18}")
            print("-" * 72)

            capacidades_kbps = []
            for s_db in snr_db_vals:
                s_lin = snr_db_para_linear(s_db)
                c_bps = capacidade_shannon(b_hz, s_lin)
                c_kbps = c_bps / 1000.0
                capacidades_kbps.append(c_kbps)
                print(f"{s_db:^10.1f} | {s_lin:^16.2f} | {c_kbps:^22.2f} | {c_bps:^18.2f}")
            print("-" * 72)

            # Gráfico C vs SNR (dB)
            plt.figure(figsize=(9, 5.5))
            plt.plot(snr_db_vals, capacidades_kbps, 's-', color='#d62728', linewidth=2, markersize=7, label=f"B = {b_khz} kHz")
            
            # Anotações nos pontos 10, 20, 30 e 40 dB se presentes
            for p in [10, 20, 30, 40]:
                if p in snr_db_vals:
                    idx = snr_db_vals.index(p)
                    plt.plot(p, capacidades_kbps[idx], 'o', color='black', markersize=8)
                    plt.annotate(f"{capacidades_kbps[idx]:.2f} kbit/s", 
                                 (p, capacidades_kbps[idx]), 
                                 textcoords="offset points", 
                                 xytext=(0, 10), 
                                 ha='center', 
                                 fontweight='bold', 
                                 fontsize=9)

            plt.title(f"Experimento 3: Capacidade versus SNR em dB (B = {b_khz} kHz)", fontsize=13, fontweight='bold')
            plt.xlabel("Relação Sinal-Ruído (SNR em dB)", fontsize=11)
            plt.ylabel("Capacidade C (kbit/s)", fontsize=11)
            plt.xticks(snr_db_vals)
            plt.grid(True, linestyle=":", alpha=0.7)
            plt.legend(fontsize=10)
            plt.tight_layout()
            plt.show()

    
        elif opcao == "4":
            print("\n--- Experimento 4: Nyquist versus Shannon ---")
            b_khz = float(input("Digite a Largura de Banda fixa B em kHz (ex: 3): "))
            b_hz = b_khz * 1000.0
            n_vals = ler_lista_ints("Digite os Níveis N para Nyquist (ex: 2, 4, 8, 16, 32, 64): ", minimo=2)
            snr_db = float(input("Digite a SNR em dB para Shannon (ex: 30): "))
            
            snr_lin = snr_db_para_linear(snr_db)
            limite_shannon_kbps = capacidade_shannon(b_hz, snr_lin) / 1000.0

            print("\n" + "=" * 75)
            print(f" COMPARAÇÃO: B = {b_khz} kHz | SNR = {snr_db:.1f} dB | Limite Shannon = {limite_shannon_kbps:.2f} kbit/s")
            print("=" * 75)
            print(f"{'N (níveis)':^12} | {'bits/símb.':^12} | {'Nyquist (kbit/s)':^20} | {'Supera Shannon?':^20}")
            print("-" * 75)

            c_nyq_lista = []
            for n in n_vals:
                c_kbps = capacidade_nyquist(b_hz, n) / 1000.0
                c_nyq_lista.append(c_kbps)
                supera = "SIM (Inviável)" if c_kbps > limite_shannon_kbps else "Não (Viável)"
                print(f"{n:^12} | {int(math.log2(n)):^12} | {c_kbps:^20.2f} | {supera:^20}")
            print("=" * 75)

            plt.figure(figsize=(9, 5.5))
            plt.plot(n_vals, c_nyq_lista, 'o-', color='#1f77b4', linewidth=2, label="Capacidade de Nyquist")
            plt.axhline(y=limite_shannon_kbps, color='#d62728', linestyle='--', linewidth=2.5,
                        label=f"Limite de Shannon ({limite_shannon_kbps:.2f} kbit/s)")
            plt.title(f"Experimento 4: Nyquist vs Shannon (B = {b_khz} kHz, SNR = {snr_db:.0f} dB)", fontsize=13, fontweight='bold')
            plt.xlabel("Níveis de Sinalização (N)", fontsize=11)
            plt.ylabel("Capacidade (kbit/s)", fontsize=11)
            plt.xticks(n_vals)
            plt.grid(True, linestyle=":", alpha=0.7)
            plt.legend(fontsize=10)
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()