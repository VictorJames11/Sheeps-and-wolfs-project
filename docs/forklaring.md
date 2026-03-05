# Forklaring til fremlæggelse: Sheep & Wolves simulation

Denne guide er skrevet i et enkelt sprog, så du kan bruge den direkte i en fremlæggelse.

## Kort fortalt

Simulationen viser et lille økosystem på et grid:
- Får bevæger sig rundt og spiser græs.
- Ulve bevæger sig rundt og jager får.
- Græs vokser tilbage over tid.

Det hele kører i **ticks** (små tidstrin), hvor systemet opdaterer tilstanden trin for trin.

## Hvad betyder MQTT?

MQTT står for **Message Queuing Telemetry Transport**.

I denne simulation er MQTT den “besked-kanal”, som agenterne bruger til at tale sammen:
- Hver agent sender sine data på et topic.
- Andre agenter (og dashboardet) kan abonnere på de topics, de har brug for.
- På den måde er simulationen distribueret: hver notebook kan køre selvstændigt, men stadig samarbejde live.

## Hvad er en cell?

En cell er en enkelt “blok” i en Jupyter-notebook.

Der findes typisk to typer:
- **Code cell**: indeholder Python-kode, som du kan køre.
- **Markdown cell**: indeholder tekst og forklaring (som i en rapport).

I vores projekt betyder det, at vi kan bygge notebooken trin for trin:
- én cell til import og opsætning,
- én cell til simulation,
- én cell til visualisering eller output.

Det gør det nemt at forklare processen i en fremlæggelse, fordi man kan vise ét trin ad gangen.

## Sådan virker et tick

I hvert tick sker tingene i denne rækkefølge:
1. Agenter flytter sig.
2. De spiser (får spiser græs, ulve kan spise får).
3. De kan reproducere, hvis de har nok energi.
4. Dyr med for lav energi dør.
5. Græs gror tilbage i nogle felter.

Det giver en dynamik, hvor populationerne stiger og falder over tid.

## Hvad gør de enkelte agenter?

### `agent_sheep.ipynb`
- Styrer fårenes adfærd i hvert tick.
- Får flytter sig, mister lidt energi, og spiser græs hvis de lander på en celle med græs.
- Hvis et får har nok energi, kan det reproducere (der kommer et nyt får).
- Hvis energien bliver for lav, dør fåret.
- Sender løbende data ud, fx antal får, græs-forbrug og gennemsnitlig energi.

### `agent_wolf.ipynb`
- Styrer ulvenes adfærd i hvert tick.
- Læser fåre-data og tick-data fra MQTT.
- Beregner en estimeret predation ud fra ulveantal, fåretæthed og predation-capacity.
- Opdaterer ulveantal med en lille, simpel fødsel/død-logik per tick.
- Sender data ud om ulvebestand og estimeret predation.

### `agent_grass.ipynb`
- Holder styr på hvilke felter der har græs, og hvilke der er spist ned.
- Når græs bliver spist, starter en “regrow”-timer for den celle.
- Efter et antal ticks vokser græsset tilbage.
- Sender data ud om græsdækning, så de andre agenter kan reagere på ressource-niveauet.

### `agent_observer.ipynb`
- Fungerer som systemets “målecentral”.
- Lytter på data fra sheep-, wolf- og grass-agenter.
- Samler tallene til fælles metrics per tick (population, energi, events, græsdækning).
- Publicerer en samlet status, som dashboardet bruger direkte.

### `agent_controller.ipynb`
- Er den enkle styringslogik ovenpå simulationen.
- Læser observerens metrics og vurderer, om systemet er ved at komme i ubalance.
- Kan sende styringskommandoer (fx justering af parametre), hvis en tærskel overskrides.
- Formålet er at holde simulationen mere stabil, så én art ikke for hurtigt forsvinder.

## Hvad betyder dashboardet?

Dashboardet (`dashboard_observer.ipynb`) viser den samlede tilstand live.

Det indeholder to centrale visninger:

1. **Matrix-visning**
   - Et heatmap med grupperede metrics:
   - Population (fx får og ulve)
   - Miljø (fx græsdækning)
   - Dynamik (fx energi, fødsler/dødsfald/predation)
   - Jo højere tal, jo tydeligere/farverepræsenteret værdi i matrixen.

2. **Trend-graf over tid**
   - X-akse: tick (tid)
   - Y-akse: antal/procent
   - Kurver for:
     - Sheep (antal får)
     - Wolves (antal ulve)
     - Grass % (andel græs på grid)

Grafen bruges til at forklare, om systemet er stabilt eller i ubalance.

## Sådan kan du formulere det i fremlæggelsen

Du kan sige:

> “Vi har bygget en distribueret agent-baseret simulation, hvor hver del kører i sin egen notebook og kommunikerer via MQTT. Får, ulve og græs opdateres for hvert tick. Dashboardet samler data og viser både et øjebliksbillede (matrix) og udviklingen over tid (trend-graf), så vi kan se balancen mellem populationer og ressourcer.”

## Hvad man typisk ser i grafen

- Hvis der er meget græs, stiger fårene ofte først.
- Når der er mange får, får ulvene bedre jagtmuligheder og kan stige bagefter.
- Hvis ulvene bliver for mange, falder fårene.
- Når fårene falder, kan ulvene også falde igen.

Det giver ofte bølger i kurverne, som er en klassisk predator-byttedyr-dynamik.

## Hvorfor vokser ulvene ikke mere hos dig?

At ulvene ligger omkring 10–11 i din kørsel giver god mening med den nuværende model:

- Du starter med `initial_wolves: 8`.
- Ulve-fødsler er sat lavt (`~0.04` pr. tick), og dødschance er også til stede (`~0.02` pr. tick).
- Det giver kun en lille netto-vækst, så kurven bliver ofte flad eller langsomt stigende.
- Wolf-agenten bruger en enkel, stabil logik, så store hop i ulveantal er sjældne.
- Med fast seed (`seed: 42`) bliver forløbet desuden ret reproducérbart, så du ser samme niveau igen.

Kort sagt: din nuværende parameter-kombination er mere **stabiliserende** end **ekspansiv** for ulvene.

## Hvis du vil have flere ulve (kort)

- Hæv `wolf_reproduction_probability` lidt (fx 0.04 → 0.06).
- Sænk `wolf_move_cost` en smule (så ulve mister mindre energi pr. tick).
- Hæv `wolf_eat_gain` lidt (så jagt giver mere energi til overlevelse/reproduktion).

Start med små ændringer én ad gangen, så du tydeligt kan se effekten i grafen.
