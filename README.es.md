# workingclass

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · **Español** · [Français](README.fr.md) · [Português](README.pt.md) · [Deutsch](README.de.md)

> Herramientas de IA del lado de las personas trabajadoras.
> AI tools that stand on the side of workers.

Este repositorio aloja agent skills y herramientas pensadas para servir a las personas trabajadoras. La primera, y la central, es **Laborer's Companion / 劳动者AI助手** — una herramienta para ver a través de la retórica laboral y tomar las decisiones que realmente te convienen.

---

## Por qué existe este proyecto

En el trabajo, la empresa, RR.HH. y tu jefe disponen de muchísimos recursos para gestionarte: consultoras de RR.HH., manuales de manipulación, sistemas de evaluación de desempeño, equipos legales, psicólogos de selección. Cada frase que dicen está cuidadosamente diseñada — no necesariamente para que veas claro, sino para que tomes la decisión que más beneficia a la empresa.

Tú solo te tienes a ti.

La era de la IA agrava esta asimetría — las empresas usan IA para destilar tu trabajo, sustituirte, vigilarte. Este proyecto da la vuelta a la IA: **IA de tu lado**.

---

## Qué incluye actualmente

### 1. `skills/laborer-companion/` — Laborer's Companion

9 módulos centrales + 4 herramientas de entrada que cubren todo el panorama laboral:

| Módulo | Propósito |
|--------|-----------|
| Herramienta 0a · Triaje | Te enruta cuando no sabes qué módulo usar |
| Herramienta 0b · Escaneo de banderas rojas | Diagnóstico de 60 segundos sobre el riesgo de tu situación |
| Herramienta 0c · Primeras 72 h tras un despido | Qué hacer — y qué no — justo después de un despido |
| Herramienta 0d · Privacidad y OPSEC | Cómo usar la herramienta de forma segura |
| Módulo 1 · Decodificador de retórica | Traducir lo que tu jefe/RR.HH. *de verdad* está diciendo |
| Módulo 2 · Decisión de horas extra | Análisis real de coste-beneficio |
| Módulo 3 · Decodificador de evaluación | Ver la intención detrás del *review* |
| Módulo 4 · Quedarse o irse | Decidir según tus intereses reales |
| Módulo 5 · Perspectiva histórica | Encontrar referentes en 150 años de historia laboral |
| Módulo 6 · Mapa de derecho laboral | 8 entradas jurisdiccionales que cubren 9 jurisdicciones/regiones nombradas (no es asesoramiento jurídico) |
| Módulo 7 · Negociación salarial | Playbook completo |
| Módulo 8 · Supervivencia al PIP | De la señal temprana a la negociación de la indemnización |
| Módulo 9 · Búsqueda de empleo y entrevistas | Ciclo completo |

Detalles: [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md).

---

## Instalación

```bash
# clonar el repositorio
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# Al abrir este repo en Cursor, Cursor lee .cursor/rules/laborer-companion.mdc.
# Para usarlo en otro repo, copia skills/laborer-companion/ y .cursor/rules/laborer-companion.mdc.

# Claude Code (legacy Claude skills)
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

Luego describe tu situación laboral en el agente y la skill se activará. O usa los slash commands:

```
/triage      - Empieza aquí cuando no sabes qué módulo encaja
/scan        - Escaneo de banderas rojas (60 s)
/decode      - Decodificar retórica de jefe/RR.HH.
/overtime    - Decisión sobre horas extra
/review      - Leer una evaluación de desempeño
/jump        - Quedarse o irse
/history     - Perspectiva histórica
/law         - Consulta de derecho laboral
/salary      - Negociación salarial
/pip         - Supervivencia al PIP
/jobsearch   - Búsqueda de empleo y entrevistas
```

---

## Soporte Codex / Cursor

- **Codex**: la skill vive en `skills/laborer-companion/`; los metadatos de UI viven en `skills/laborer-companion/agents/openai.yaml`. Tras instalarla en `${CODEX_HOME:-$HOME/.codex}/skills/`, se puede activar con `$laborer-companion`.
- **Cursor**: este repo incluye una Cursor Project Rule en `.cursor/rules/laborer-companion.mdc`. Al abrir el repo en Cursor, Agent puede usar esa regla para cargar `skills/laborer-companion/SKILL.md`.
- **Guía general para agentes**: `AGENTS.md` en la raíz ofrece instrucciones compatibles con Codex / Cursor.

Para reutilizar la skill en otro proyecto, copia `skills/laborer-companion/`, `.cursor/rules/laborer-companion.mdc` y `AGENTS.md`, manteniendo coherentes las rutas de la regla.

---

## Cobertura de derecho laboral

El Módulo 6 tiene actualmente **8 entradas jurisdiccionales** que cubren **9 jurisdicciones/regiones nombradas**:

| Entrada | Notas |
|---------|-------|
| China continental | Archivo independiente |
| Hong Kong / Taiwán | Dos regiones/jurisdicciones en un mismo archivo; las reglas no se mezclan; nunca se etiquetan como países |
| Estados Unidos | Federal + foco en California / Nueva York |
| Canadá | Federal + diferencias provinciales señaladas |
| Australia | Fair Work / Awards / unfair dismissal |
| Reino Unido | UK employment / ACAS / tribunal |
| Unión Europea | Visión regional con notas sobre Alemania/Francia/Países Bajos; no es una enciclopedia por estado miembro |
| India | Cuatro Labour Codes + preguntas frecuentes del sector IT |

Si cuentas Hong Kong y Taiwán por separado, son **9 jurisdicciones/regiones nombradas**; por archivo de referencia / entrada jurisdiccional son **8**. Hong Kong y Taiwán deben etiquetarse como **regiones/jurisdicciones**, nunca como países, dentro de este proyecto.

---

## Idiomas soportados

Actualmente:

- 简体中文 / Chino simplificado
- 繁體中文 / Chino tradicional
- English
- Español
- Français / Francés
- Português / Portugués
- Deutsch / Alemán

Regla por defecto: la skill responde en el mismo idioma soportado en el que escribe la persona usuaria. Los nombres de leyes, organismos y cláusulas contractuales se conservan en el original con traducción breve cuando ayuda. En chino tradicional se prefieren términos propios de Hong Kong / Taiwán.

---

## Ejemplos y tutoriales

Más ejemplos en [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md). Buenos puntos de partida:

```text
/triage
Mi manager está distante últimamente y no sé por qué. Ayúdame a decidir qué módulo usar.
```

```text
/law
Trabajo a tiempo parcial en Hong Kong, 17 horas por semana. RR.HH. dice que el salario mínimo legal solo cubre algunas industrias. ¿Es cierto?
```

```text
/review
Esta es mi evaluación de desempeño: [pega el contenido redactado]
El año pasado fui "exceeds" y este año bajé a "meets". ¿Es una señal peligrosa?
```

Damos la bienvenida a más tutoriales y casos reales — especialmente:

- Ejemplos de derecho laboral de distintas jurisdicciones/regiones
- Walkthroughs de PIP / despido / negociación de indemnización
- Scripts de negociación salarial
- Ejemplos de anti-manipulación en entrevistas
- Muestras redactadas de correos de RR.HH. / manager
- Casos reales de uso en español, francés, portugués y alemán

---

## Principios

1. **No convoca a la acción colectiva** — esta es una herramienta de claridad para personas trabajadoras individuales.
2. **Reconoce las restricciones reales** — nunca da consejos imprudentes del tipo "renuncia ya".
3. **Mantiene la honestidad intelectual** — no adapta el consejo por corrección política.
4. **Privacidad ante todo** — ver `skills/laborer-companion/references/privacy-and-opsec.md`.
5. **No suplanta a un abogado** — ofrece marcos y preguntas que conviene hacerse, no sustituye la asesoría legal profesional.

---

## Aviso de privacidad ⚠️

- Esta skill no sube tus conversaciones a terceros.
- Pero la conversación con tu proveedor de IA puede quedar registrada por la plataforma según tu cuenta y configuración de privacidad.
- **No uses esta herramienta en un dispositivo o red de la empresa.**
- **No pegues datos confidenciales de la empresa en la IA** — redacta antes.

Detalles: [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md).

---

## Inspiración

- La anti-distillation skill de Koki Xu (abril de 2026)
- Karl Marx sobre el valor del trabajo y la alienación
- E.P. Thompson, *La formación de la clase obrera en Inglaterra*
- 150 años de casos concretos de movimientos obreros
- Economía laboral y sociología del trabajo contemporáneas

Esta herramienta no inventa nada nuevo. Traduce 150 años de sabiduría colectiva de la clase trabajadora a una forma utilizable en la era de la IA de 2026.

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Especialmente bienvenidas:

- Nuevos casos de retórica (para reforzar el Módulo 1)
- Aportaciones de derecho laboral de tu país/región/jurisdicción
- Casos de éxito de negociación salarial / indemnización
- Experiencias con PIPs (anonimizadas)
- Traducciones de los README orientados a usuarios

---

## Licencia

Apache 2.0 — ver [LICENSE](LICENSE).

Única petición: **mantén la misión central de la herramienta — servir a las personas trabajadoras**.

---

## Un párrafo

Ver tu situación con claridad no cambia tu situación. Pero la claridad es la condición previa para el cambio. Y a menudo, aceptar la realidad con los ojos abiertos (incluido "todavía no puedo irme") es mejor que aguantar con los ojos cerrados.

Al menos sabes qué estás haciendo.
