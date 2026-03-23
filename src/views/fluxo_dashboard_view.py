from pathlib import Path
import time
import webbrowser

from src.core.config import PORTA_PADRAO
from src.infrastructure.dashboard.streamlit_dashboard import abrir_dashboard, encerrar_processo, obter_arquivo_controle_dashboard, obter_arquivo_log_dashboard


def painel_dashboard_em_execucao(
    caminho_arquivo: str | Path,
    caminho_script: str | Path | None = None,
    porta: int = PORTA_PADRAO,
    abrir_navegador: bool = True,
) -> None:
    try:
        processo, url = abrir_dashboard(
            caminho_arquivo=caminho_arquivo,
            caminho_script=caminho_script,
            porta=porta,
            abrir_navegador=abrir_navegador,
        )
    except Exception as erro:
        print("\nErro ao abrir o dashboard.")
        print(f"Detalhes: {erro}")
        print(f"Log: {obter_arquivo_log_dashboard().resolve()}")
        input("\nPressione Enter para voltar...")
        return

    while True:
        print("\n" + "=" * 70)
        print("DASHBOARD EM EXECUÇÃO")
        print("=" * 70)
        print(f"Arquivo base : {Path(caminho_arquivo).expanduser().resolve()}")
        print(f"Controle     : {obter_arquivo_controle_dashboard().resolve()}")
        print(f"Link         : {url}")
        print(f"Log          : {obter_arquivo_log_dashboard().resolve()}")
        print("\n[1] Abrir dashboard no navegador")
        print("[2] Voltar ao menu anterior")
        print("[3] Encerrar dashboard e voltar")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            try:
                webbrowser.open(url)
                print("\nAbrindo dashboard no navegador...")
            except Exception as erro:
                print(f"\nNão foi possível abrir o navegador automaticamente: {erro}")
                print(f"Acesse manualmente: {url}")

        elif opcao == "2":
            print("\nVoltando ao menu anterior...")
            print("O dashboard continuará rodando em segundo plano.")
            time.sleep(1.5)
            break

        elif opcao == "3":
            print("\nEncerrando dashboard...")
            encerrar_processo(processo)
            print("Dashboard encerrado com sucesso.")
            time.sleep(1.5)
            break

        else:
            print("Opção inválida.")