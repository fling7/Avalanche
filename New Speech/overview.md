# Avalanche Meta-Sprache (New Speech)

Die neue Struktur trennt die bisher monolithischen TextX-Grammatiken `avaAltered.tx` und `avalanche.tx`
in eine modulare Übersprache. Das Basismodul **Core** stellt zentrale Begriffe wie `Model`,
Namensräume, Typen, Werte, Annotationen und den Ausdrucksapparat bereit. Alle weiteren
Module deklarieren explizite Abhängigkeiten auf das Core-Modul und hängen sich modular
in die Sprache ein. Entwicklungs- und Analysewerkzeuge können zur Laufzeit nur die Module
laden, die für den jeweiligen Use Case benötigt werden.

## Modulares Ladeszenario

Jedes Modul wird über einen deklarativen Header eingebunden:

```text
module Communication requires Core, Actions;
```

Das Beispiel zeigt, wie das Kommunikationsmodul die Definitionen aus dem Core sowie
die in `Actions` beschriebenen Statements nutzt. Weitere Module können auf diese Weise
frei kombiniert werden. Nicht benötigte Module werden nicht geladen, wodurch die DSL
leichtgewichtig bleibt. Neue Module lassen sich hinzufügen, indem sie auf Core und –
falls erforderlich – andere Module referenzieren. Keine vorhandene Semantik geht dabei
verloren, da sämtliche Konstrukte aus beiden Ursprungsdateien in mindestens einem Modul
abgebildet sind.

## Modulübersicht

| Modul | Zweck | Enthaltene Konstrukte |
|-------|-------|------------------------|
| `Core` | Grundbegriffe der Sprache | `Model`, `Package`, `Import`, `FQN`, `Annotation`, `TypeDef`, `TypeRef`, `Literal`, `Expr`, `DistDef` |
| `Actions` | Blockstruktur, Anweisungen und Funktionsaufrufe | `ActionBlock`, `ActionStmt`, `Assignment`, `FunctionCall`, `Send`, `Emit`, `Log`, Lebenszyklus-Operationen |
| `Communication` | Nachrichten, Ports, Akteure, Kanäle | `Message`, `Actor`, `Port`, `Channel`, Attribute |
| `Events` | Ereignisse und Trigger | `Event`, `Trigger` inkl. Verteilungen und Bedingungen |
| `Scenarios` | Bewegungs- und Ablauf-Szenarien | `MovementScenario`, `Scenario`, `Step`-Varianten, `Expect`, `MovementStepExtension` |
| `StateMachines` | Zustands- und Modusmodelle | `StateMachine`, `State`, `Transition`, `Mode` |
| `Timing` | Zeitliche Randbedingungen | `TimeConstraint`, `Scheduler`, Zeitangaben, Cron |
| `Causality` | Kausalität und Parallelität | `Causality`, `CausalRel`, `Concurrency`, `ConcurrencyRule` |
| `Lifecycle` | Objekt-Lebenszyklen | `Lifecycle`, `CreateOp`, `UpdateOp`, `DeleteOp` |
| `Spatial` | Räumliche Konzepte | `Zone`, `SpatialRule`, `Shape`-Varianten, Proximity, `MoveStep` |
| `Quality` | Nicht-funktionale Eigenschaften | `NFR`, `Property`, `NFP` |
| `Testing` | Tests und Traceability | `Test`, `TraceLink`, `Tag` |
| `Simulation` | Simulationskonfiguration | `Simulation`, `SchedulerPolicy` |

Die Module bauen inhaltlich aufeinander auf, verzichten aber auf zyklische Abhängigkeiten.
So ist es möglich, das `Spatial`-Modul ohne `StateMachines` zu laden oder lediglich `Core`
und `Actions` für einfache analytische Aufgaben zu nutzen. Die modulare
Organisation erlaubt es zudem, später neue Domänenmodule (z. B. `Robotics`, `Energy`)
anzuhängen, ohne den Kern anzupassen. Über das neue Erweiterungsobjekt
`MovementStepExtension` lassen sich zusätzliche Bewegungs-Bausteine nachrüsten;
`Spatial` liefert beispielsweise einen `move … from … to …`-Schritt. Die optionale
`MovementDetailExtension` erlaubt zukünftigen Modulen, Haltungs- oder Gestik-Informationen
anzugeben, ohne das Basismodell zu belasten.

## Dateien

Jedes Modul besitzt eine eigene `.tx`-Datei im selben Ordner. Die Grammatiksegmente
folgen der TextX-Syntax, wurden jedoch kommentiert und in logische Abschnitte gegliedert.
Gemeinsame Tokens (`ID`, `INT`, `FLOAT`, `STRING`, Einheiten) liegen im `Core`-Modul.

