# workingclass

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · **Français** · [Português](README.pt.md) · [Deutsch](README.de.md)

> Des outils d'IA du côté des travailleuses et travailleurs.
> AI tools that stand on the side of workers.

Ce dépôt rassemble des agent skills et des outils au service des travailleuses et travailleurs. Le premier, et le central, est **Laborer's Companion / 劳动者AI助手** — un outil pour décrypter la rhétorique du monde du travail et prendre les décisions qui te conviennent vraiment.

---

## Pourquoi ce projet existe

Au travail, l'entreprise, les RH et ton ou ta manager disposent de ressources énormes pour te gérer : cabinets RH, manuels de manipulation, systèmes d'évaluation de performance, équipes juridiques, psychologues du recrutement. Chaque phrase est soigneusement conçue — pas forcément pour t'éclairer, mais pour t'amener à prendre la décision la plus favorable à l'entreprise.

Toi, tu n'as que toi.

L'ère de l'IA aggrave cette asymétrie — les entreprises utilisent l'IA pour distiller ton travail, te remplacer, te surveiller. Ce projet retourne l'IA dans l'autre sens : **une IA de ton côté**.

---

## Ce qui est inclus

### 1. `skills/laborer-companion/` — Laborer's Companion

9 modules principaux + 4 outils d'entrée couvrant l'ensemble du paysage professionnel :

| Module | Objet |
|--------|-------|
| Outil 0a · Triage | T'oriente quand tu ne sais pas quel module utiliser |
| Outil 0b · Scan des signaux d'alerte | Diagnostic en 60 secondes du danger de ta situation |
| Outil 0c · Premières 72 h après un licenciement | Quoi faire — et ne pas faire — juste après un licenciement |
| Outil 0d · Vie privée et OPSEC | Comment utiliser l'outil en sécurité |
| Module 1 · Décodeur de rhétorique | Traduire ce que ton manager / les RH disent *vraiment* |
| Module 2 · Décision sur les heures supplémentaires | Analyse réelle coût-bénéfice |
| Module 3 · Décodeur d'évaluation annuelle | Voir l'intention derrière le *review* |
| Module 4 · Rester ou partir | Décider sur la base de tes intérêts réels |
| Module 5 · Perspective historique | Trouver des références dans 150 ans d'histoire ouvrière |
| Module 6 · Carte du droit du travail | 8 entrées juridictionnelles couvrant 9 juridictions/régions nommées (ce n'est pas un avis juridique) |
| Module 7 · Négociation salariale | Playbook complet |
| Module 8 · Survie au PIP | Du signal précoce à la négociation de l'indemnité |
| Module 9 · Recherche d'emploi et entretiens | Cycle complet |

Détails : [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md).

---

## Installation

```bash
# cloner le dépôt
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# Quand ce dépôt est ouvert dans Cursor, Cursor lit .cursor/rules/laborer-companion.mdc.
# Pour l'utiliser dans un autre dépôt, copie skills/laborer-companion/ et .cursor/rules/laborer-companion.mdc.

# Claude Code (legacy Claude skills)
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

Décris ensuite ta situation à l'agent : la skill s'activera. Ou utilise les slash commands :

```
/triage      - Commencer ici si tu ne sais pas quel module choisir
/scan        - Scan des signaux d'alerte (60 s)
/decode      - Décoder la rhétorique manager/RH
/overtime    - Décision sur les heures supplémentaires
/review      - Lire une évaluation de performance
/jump        - Rester ou partir
/history     - Perspective historique
/law         - Recherche en droit du travail
/salary      - Négociation salariale
/pip         - Survie au PIP
/jobsearch   - Recherche d'emploi et entretiens
```

---

## Prise en charge Codex / Cursor

- **Codex** : la skill se trouve dans `skills/laborer-companion/` ; les métadonnées d'interface se trouvent dans `skills/laborer-companion/agents/openai.yaml`. Une fois installée dans `${CODEX_HOME:-$HOME/.codex}/skills/`, elle peut être déclenchée avec `$laborer-companion`.
- **Cursor** : ce dépôt contient une Cursor Project Rule dans `.cursor/rules/laborer-companion.mdc`. Quand le dépôt est ouvert dans Cursor, Agent peut utiliser cette règle pour charger `skills/laborer-companion/SKILL.md`.
- **Instructions générales pour agents** : `AGENTS.md` à la racine fournit des instructions compatibles Codex / Cursor.

Pour réutiliser la skill dans un autre projet, copie `skills/laborer-companion/`, `.cursor/rules/laborer-companion.mdc` et `AGENTS.md`, en gardant les chemins de la règle cohérents.

---

## Couverture du droit du travail

Le Module 6 contient actuellement **8 entrées juridictionnelles** couvrant **9 juridictions/régions nommées** :

| Entrée | Notes |
|--------|-------|
| Chine continentale | Fichier dédié |
| Hong Kong / Taïwan | Deux régions/juridictions dans un même fichier ; règles à ne pas mélanger ; jamais étiquetées comme pays |
| États-Unis | Fédéral + focus Californie / New York |
| Canada | Fédéral + différences provinciales signalées |
| Australie | Fair Work / Awards / unfair dismissal |
| Royaume-Uni | UK employment / ACAS / tribunal |
| Union européenne | Vue régionale avec notes Allemagne/France/Pays-Bas ; pas une encyclopédie par État membre |
| Inde | Quatre Labour Codes + FAQ secteur IT |

Si Hong Kong et Taïwan sont comptés séparément, on a **9 juridictions/régions nommées** ; en comptant par fichier de référence / entrée juridictionnelle, on a **8**. Hong Kong et Taïwan doivent être étiquetés **régions/juridictions**, jamais pays, dans ce projet.

---

## Langues prises en charge

Actuellement :

- 简体中文 / Chinois simplifié
- 繁體中文 / Chinois traditionnel
- English / Anglais
- Español / Espagnol
- Français
- Português / Portugais
- Deutsch / Allemand

Règle par défaut : la skill répond dans la langue prise en charge dans laquelle l'utilisatrice ou l'utilisateur écrit. Les noms de lois, d'organismes et les clauses contractuelles sont conservés en version originale avec une traduction courte si utile. En chinois traditionnel, on privilégie les termes propres à Hong Kong / Taïwan.

---

## Exemples et tutoriels

Plus d'exemples dans [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md). Bons points de départ :

```text
/triage
Mon manager est distant ces derniers temps, je n'arrive pas à expliquer pourquoi. Aide-moi à choisir le bon module.
```

```text
/law
Je travaille à temps partiel à Hong Kong, 17 heures par semaine. Les RH disent que le salaire minimum légal ne couvre que certains secteurs. Est-ce exact ?
```

```text
/review
Voici mon évaluation : [colle le contenu anonymisé]
L'année dernière j'étais "exceeds", cette année je suis passé à "meets". Est-ce un signal dangereux ?
```

Bienvenue aux tutoriels et cas réels — en particulier :

- Exemples de droit du travail de différentes juridictions/régions
- Walkthroughs PIP / licenciement / négociation d'indemnité
- Scripts de négociation salariale
- Exemples d'anti-manipulation en entretien
- Échantillons anonymisés d'e-mails RH / manager
- Cas d'usage réels en espagnol, français, portugais et allemand

---

## Principes

1. **Pas d'appel à l'action collective** — c'est un outil de clarté pour individus.
2. **Reconnaître les contraintes réelles** — pas de conseil imprudent du genre "démissionne tout de suite".
3. **Honnêteté intellectuelle** — pas d'adaptation par correction politique.
4. **Vie privée d'abord** — voir `skills/laborer-companion/references/privacy-and-opsec.md`.
5. **Pas un avocat** — l'outil fournit des cadres et les bonnes questions à se poser, jamais en remplacement d'un conseil juridique professionnel.

---

## Avertissement vie privée ⚠️

- Cette skill ne téléverse pas tes conversations vers un tiers.
- Mais la conversation avec ton fournisseur d'IA peut être enregistrée par la plateforme selon ton compte et tes paramètres.
- **N'utilise pas cet outil sur un appareil ou un réseau de l'entreprise.**
- **Ne colle pas de données confidentielles de l'entreprise dans l'IA** — anonymise d'abord.

Détails : [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md).

---

## Inspiration

- L'anti-distillation skill de Koki Xu (avril 2026)
- Karl Marx sur la valeur du travail et l'aliénation
- E.P. Thompson, *La Formation de la classe ouvrière anglaise*
- 150 ans de cas concrets de mouvements ouvriers
- Économie du travail et sociologie du travail contemporaines

Cet outil n'invente rien. Il traduit 150 ans de sagesse collective de la classe ouvrière dans une forme utilisable à l'ère de l'IA de 2026.

---

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Particulièrement bienvenus :

- Nouveaux cas de rhétorique (pour enrichir le Module 1)
- Compléments de droit du travail pour ton pays/région/juridiction
- Cas réussis de négociation salariale / indemnité
- Expériences de PIP (anonymisées)
- Traductions des README destinés aux utilisateurs

---

## Licence

Apache 2.0 — voir [LICENSE](LICENSE).

Seule demande : **garder la mission centrale de l'outil — servir les travailleuses et travailleurs**.

---

## Un paragraphe

Voir clairement sa situation ne change pas la situation. Mais la clarté est la condition préalable du changement. Et souvent, accepter la réalité les yeux ouverts (y compris "je ne peux pas encore partir") vaut mieux qu'endurer les yeux fermés.

Au moins, tu sais ce que tu fais.
