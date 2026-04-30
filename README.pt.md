# workingclass

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Français](README.fr.md) · **Português** · [Deutsch](README.de.md)

> Ferramentas de IA do lado de quem trabalha.
> AI tools that stand on the side of workers.

Este repositório reúne agent skills e ferramentas pensadas para servir trabalhadoras e trabalhadores. A primeira, e a central, é **Laborer's Companion / 劳动者AI助手** — uma ferramenta para ver através da retórica do mundo do trabalho e tomar decisões que sejam realmente boas para você.

---

## Por que este projeto existe

No trabalho, a empresa, o RH e a sua chefia têm muitos recursos para te gerir: consultorias de RH, manuais de manipulação, sistemas de avaliação de desempenho, equipas jurídicas, psicólogos de recrutamento. Cada frase é cuidadosamente desenhada — não necessariamente para te dar clareza, mas para te levar à decisão que mais beneficia a empresa.

Você só tem você.

A era da IA agrava essa assimetria — empresas usam IA para destilar o seu trabalho, substituir você, monitorar você. Este projeto vira a IA do outro lado: **IA do seu lado**.

---

## Um exemplo rápido

Sua chefia acabou de te mandar isto:

> *"Hey, I really appreciate your dedication. The team's vision for next year requires more cross-functional ownership and strategic impact — I'd love to see you stretch into broader leadership. That's the trajectory I see for you. Let's chat at our next 1:1."*

Rode `/decode` (ou cole a mensagem em qualquer agente com a skill instalada) e você recebe:

```
Padrão: recompensa-futura-vaga + ampliação de escopo sem compensação

O que de fato está sendo dito:
  - "broader leadership" / "strategic impact" / "trajectory" — expectativas
    não mensuráveis que a chefia pode redefinir a qualquer momento
  - Sem cronograma de promoção, sem delta salarial, sem redução de escopo
  - "That's the trajectory I see" ≠ "estamos te promovendo"

O que fazer esta semana:
  1. Responder pedindo os *critérios de promoção* por escrito — específicos, mensuráveis
  2. Perguntar qual escopo atual você pode largar ao assumir o novo
  3. Perguntar o delta salarial se você atingir esses critérios
  4. Guardar a resposta da chefia (ou o silêncio) — em qualquer caso é evidência
```

A skill nunca manda você **pedir demissão**, **bater de frente** ou "just push back". Ela expõe a estrutura do que está sendo dito; a decisão é sua.

---

## O que está incluído atualmente

### 1. `skills/laborer-companion/` — Laborer's Companion

9 módulos centrais + 4 ferramentas de entrada cobrindo todo o panorama do trabalho:

| Módulo | Para quê |
|--------|----------|
| Ferramenta 0a · Triagem | Te direciona quando você não sabe qual módulo usar |
| Ferramenta 0b · Varredura de bandeiras vermelhas | Diagnóstico de 60 segundos sobre o risco da sua situação |
| Ferramenta 0c · Primeiras 72 h após demissão | O que fazer — e não fazer — logo após uma demissão |
| Ferramenta 0d · Privacidade e OPSEC | Como usar a ferramenta com segurança |
| Módulo 1 · Decodificador de retórica | Traduzir o que a chefia / o RH *de fato* está dizendo |
| Módulo 2 · Decisão sobre horas extras | Análise real de custo-benefício |
| Módulo 3 · Decodificador de avaliação de desempenho | Ver a intenção por trás do *review* |
| Módulo 4 · Ficar ou sair | Decidir com base nos seus interesses reais |
| Módulo 5 · Perspectiva histórica | Encontrar referências em 150 anos de história do trabalho |
| Módulo 6 · Mapa do direito do trabalho | 8 entradas jurisdicionais cobrindo 9 jurisdições/regiões nomeadas (não é orientação jurídica) |
| Módulo 7 · Negociação salarial | Playbook completo |
| Módulo 8 · Sobrevivência ao PIP | Do alerta inicial à negociação da rescisão |
| Módulo 9 · Busca de emprego e entrevistas | Ciclo completo |

Detalhes: [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md).

---

## Instalação

```bash
# clone o repositório
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# Ao abrir este repositório no Cursor, o Cursor lê .cursor/rules/laborer-companion.mdc.
# Para usar em outro repo, copie skills/laborer-companion/ e .cursor/rules/laborer-companion.mdc.

# Claude Code (legacy Claude skills)
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

Depois descreva a sua situação no agente e a skill será ativada. Ou use os slash commands:

```
/triage      - Comece aqui quando não souber qual módulo escolher
/scan        - Varredura de bandeiras vermelhas (60 s)
/decode      - Decodificar retórica de chefia/RH
/overtime    - Decisão sobre horas extras
/review      - Ler uma avaliação de desempenho
/jump        - Ficar ou sair
/history     - Perspectiva histórica
/law         - Consulta de direito do trabalho
/salary      - Negociação salarial
/pip         - Sobrevivência ao PIP
/jobsearch   - Busca de emprego e entrevistas
```

---

## Suporte Codex / Cursor

- **Codex**: a skill fica em `skills/laborer-companion/`; os metadados de UI ficam em `skills/laborer-companion/agents/openai.yaml`. Depois de instalar em `${CODEX_HOME:-$HOME/.codex}/skills/`, ela pode ser acionada com `$laborer-companion`.
- **Cursor**: este repo inclui uma Cursor Project Rule em `.cursor/rules/laborer-companion.mdc`. Ao abrir o repo no Cursor, o Agent pode usar essa regra para carregar `skills/laborer-companion/SKILL.md`.
- **Guia geral para agentes**: `AGENTS.md` na raiz fornece instruções compatíveis com Codex / Cursor.

Para reutilizar a skill em outro projeto, copie `skills/laborer-companion/`, `.cursor/rules/laborer-companion.mdc` e `AGENTS.md`, mantendo os caminhos da regra consistentes.

---

## Cobertura de direito do trabalho

O Módulo 6 atualmente tem **8 entradas jurisdicionais** cobrindo **9 jurisdições/regiões nomeadas**:

| Entrada | Notas |
|---------|-------|
| China continental | Arquivo independente |
| Hong Kong / Taiwan | Duas regiões/jurisdições no mesmo arquivo; regras não devem ser misturadas; nunca rotuladas como países |
| Estados Unidos | Federal + foco em Califórnia / Nova York |
| Canadá | Federal + diferenças provinciais sinalizadas |
| Austrália | Fair Work / Awards / unfair dismissal |
| Reino Unido | UK employment / ACAS / tribunal |
| União Europeia | Visão regional com notas sobre Alemanha/França/Países Baixos; não é uma enciclopédia por Estado-membro |
| Índia | Quatro Labour Codes + FAQ do setor de TI |

Se Hong Kong e Taiwan forem contados separadamente, são **9 jurisdições/regiões nomeadas**; contando por arquivo de referência / entrada jurisdicional, são **8**. Hong Kong e Taiwan devem ser rotulados como **regiões/jurisdições**, nunca como países, neste projeto.

---

## Idiomas suportados

Atualmente:

- 简体中文 / Chinês simplificado
- 繁體中文 / Chinês tradicional
- English / Inglês
- Español / Espanhol
- Français / Francês
- Português
- Deutsch / Alemão

Regra padrão: a skill responde no mesmo idioma suportado em que a pessoa escreve. Nomes de leis, órgãos e cláusulas contratuais ficam no original, com uma tradução curta quando ajuda. Em chinês tradicional, prefere-se a terminologia de Hong Kong / Taiwan.

---

## Exemplos e tutoriais

Mais exemplos em [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md). Bons pontos de partida:

```text
/triage
Meu chefe está distante ultimamente e não sei explicar o porquê. Me ajude a decidir qual módulo usar.
```

```text
/law
Trabalho meio período em Hong Kong, 17 horas por semana. O RH diz que o salário mínimo legal só cobre alguns setores. Isso está correto?
```

```text
/review
Esta é minha avaliação de desempenho: [cole o conteúdo anonimizado]
No ano passado fui "exceeds" e este ano caí para "meets". É um sinal perigoso?
```

São bem-vindos mais tutoriais e casos reais — em especial:

- Exemplos de direito do trabalho de diferentes jurisdições/regiões
- Walkthroughs de PIP / demissão / negociação de rescisão
- Scripts de negociação salarial
- Exemplos de antimanipulação em entrevistas
- Amostras anonimizadas de e-mails de RH / chefia
- Casos reais de uso em espanhol, francês, português e alemão

---

## Princípios

1. **Não convoca ação coletiva** — é uma ferramenta de clareza para a pessoa trabalhadora individual.
2. **Reconhece restrições reais** — nunca dá conselhos imprudentes do tipo "peça demissão agora".
3. **Honestidade intelectual** — não adapta o conselho por correção política.
4. **Privacidade em primeiro lugar** — ver `skills/laborer-companion/references/privacy-and-opsec.md`.
5. **Não substitui um advogado** — fornece estruturas e perguntas a serem feitas, nunca substitui aconselhamento jurídico profissional.

---

## Aviso de privacidade ⚠️

- Esta skill não envia suas conversas a terceiros.
- Mas a conversa com seu provedor de IA pode ser registrada pela plataforma, dependendo da sua conta e configurações.
- **Não use esta ferramenta em dispositivos ou redes da empresa.**
- **Não cole dados confidenciais da empresa na IA** — anonimize antes.

Detalhes: [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md).

---

## Inspiração

- A anti-distillation skill de Koki Xu (abril de 2026)
- Karl Marx sobre valor do trabalho e alienação
- E.P. Thompson, *A Formação da Classe Operária Inglesa*
- 150 anos de casos concretos de movimentos operários
- Economia do trabalho e sociologia do trabalho contemporâneas

Esta ferramenta não cria nada novo. Traduz 150 anos de sabedoria coletiva da classe trabalhadora para uma forma utilizável na era da IA de 2026.

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Especialmente bem-vindos:

- Novos casos de retórica (para deixar o Módulo 1 mais completo)
- Adições de direito do trabalho do seu país/região/jurisdição
- Casos de sucesso de negociação salarial / rescisão
- Experiências de PIP (anonimizadas)
- Traduções dos READMEs voltados ao usuário

---

## Licença

Apache 2.0 — ver [LICENSE](LICENSE).

Único pedido: **manter a missão central da ferramenta — servir trabalhadoras e trabalhadores**.

---

## Um parágrafo

Ver sua situação com clareza não muda sua situação. Mas a clareza é pré-condição da mudança. E, muitas vezes, aceitar a realidade de olhos abertos (incluindo "ainda não consigo sair") é melhor do que aguentar de olhos fechados.

Pelo menos você sabe o que está fazendo.
