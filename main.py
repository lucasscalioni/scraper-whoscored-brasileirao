import argparse
import os
import sys

# Adiciona o diretório 'scripts' ao sys.path para permitir importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Importa os módulos do pipeline
import Extraction_match_events_whoscored
import Extraction_players_events_whoscored
import fEventosPartidas
import fEventosJogadores
import dPartidas
import dJogador

def main():
    parser = argparse.ArgumentParser(description="Pipeline ETL - WhoScored Brasileirão")
    parser.add_argument("--extrair-eventos", action="store_true", help="Extrai eventos das partidas")
    parser.add_argument("--extrair-jogadores", action="store_true", help="Extrai estatísticas dos jogadores")
    parser.add_argument("--processar-eventos-partida", action="store_true", help="Processa os eventos das partidas")
    parser.add_argument("--processar-eventos-jogadores", action="store_true", help="Processa as estatísticas dos jogadores")
    parser.add_argument("--gerar-dpartidas", action="store_true", help="Gera a dimensão de partidas")
    parser.add_argument("--gerar-djogador", action="store_true", help="Gera a dimensão de jogadores")

    args = parser.parse_args()

    if args.extrair_eventos:
        print("🔄 Extraindo eventos das partidas...")
        Extraction_match_events_whoscored.run()

    if args.extrair_jogadores:
        print("🔄 Extraindo estatísticas dos jogadores...")
        Extraction_players_events_whoscored.run()

    if args.processar_eventos_partida:
        print("🔄 Processando eventos das partidas...")
        fEventosPartidas.run()

    if args.processar_eventos_jogadores:
        print("🔄 Processando estatísticas dos jogadores...")
        fEventosJogadores.run()

    if args.gerar_dpartidas:
        print("🔄 Gerando dimensão de partidas...")
        dPartidas.run()

    if args.gerar_djogador:
        print("🔄 Gerando dimensão de jogadores...")
        dJogador.run()

    if not any(vars(args).values()):
        print("⚠️ Nenhuma opção selecionada. Use --help para ver os comandos disponíveis.")

if __name__ == "__main__":
    main()
