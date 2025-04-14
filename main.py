from scripts.extraction import extract_urls, extract_players_events, extract_match_events
from scripts.processing import process_fEventosJogadores, process_fEventosPartida, process_dJogadores, process_dPartidas

def run_step(step_func, name):
    try:
        print(f"🚀 Executando: {name}")
        step_func.run()
        print(f"✅ {name} concluído!\n")
    except Exception as e:
        print(f"❌ Erro em {name}: {e}\n")

def run_pipeline():
    run_step(extract_urls, "Extração de URLs")
    run_step(extract_players_events, "Extração de Jogadores e Eventos")
    run_step(extract_match_events, "Extração de Eventos Cronológicos")
    run_step(process_fEventosJogadores, "fEventosJogadores")
    run_step(process_fEventosPartida, "fEventosPartida")
    run_step(process_dJogadores, "dJogadores")
    run_step(process_dPartidas, "dPartidas")

if __name__ == "__main__":
    run_pipeline()
