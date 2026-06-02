# SPRINTS — RaceDash Balancer

Aplicação Python que recebe telemetria UDP do F1 25 e redireciona para iPad e iPhone com RaceDash.

---

## Sprint 1 — Fundação e pesquisa

**Objetivo:** Entender o protocolo e estruturar o projeto.

- Pesquisar o protocolo UDP de telemetria do F1 25 (porta padrão: 20777, formato de pacotes)
- Definir estrutura de diretórios do projeto (`src/`, `config/`, `tests/`)
- Criar `requirements.txt` com dependências iniciais
- Criar `README.md` com instruções de uso básico
- Configurar `.gitignore` para Python

**Entrega:** Repositório estruturado, protocolo documentado.

---

## Sprint 2 — Listener UDP

**Objetivo:** Receber e validar os pacotes de telemetria do jogo.

- Implementar socket UDP que escuta na porta 20777 (configurável)
- Receber pacotes brutos do F1 25 sem descartá-los ou interpretá-los
- Adicionar logging básico (pacotes recebidos, bytes, timestamp)
- Tratar erros de socket (timeout, bind falho, porta ocupada)

**Entrega:** Script que loga pacotes recebidos do F1 25 no terminal.

---

## Sprint 3 — Forwarder UDP

**Objetivo:** Redirecionar os pacotes para os dois dispositivos.

- Implementar envio UDP para múltiplos destinos simultâneos (iPad + iPhone)
- Garantir que o mesmo pacote é enviado para ambos os IPs sem perda
- Tratar falhas de envio por destino sem derrubar os demais
- Medir e logar latência de repasse

**Entrega:** Pacotes do F1 25 chegando em ambos os dispositivos em tempo real.

---

## Sprint 4 — Configuração

**Objetivo:** Tornar o app configurável sem alterar código.

- Criar arquivo `config.yaml` (ou `.env`) com:
  - IP e porta de escuta
  - Lista de destinos (IP + porta de cada dispositivo)
- Suporte a argumentos de linha de comando via `argparse` como alternativa ao arquivo
- Validação dos parâmetros na inicialização com mensagens de erro claras

**Entrega:** App configurável por arquivo ou flags, sem hardcode de IPs.

---

## Sprint 5 — Robustez e observabilidade

**Objetivo:** Deixar o app estável para uso contínuo durante sessões de corrida.

- Reconexão automática em caso de queda de rede
- Estatísticas em tempo real no terminal: pacotes/s, bytes/s, perdas por destino
- Modo `--verbose` e modo silencioso
- Graceful shutdown com `Ctrl+C` (fecha sockets corretamente)

**Entrega:** App que roda uma sessão completa de corrida sem intervenção manual.

---

## Sprint 6 — Testes e documentação final

**Objetivo:** Garantir qualidade e facilitar uso futuro.

- Testes unitários para o listener e o forwarder (mock de sockets)
- Teste de integração simulando envio de pacotes F1
- `README.md` completo: pré-requisitos, instalação, configuração, execução
- Script de inicialização rápida (`start.sh` ou `Makefile`)

**Entrega:** Projeto pronto para uso e manutenção.
