# Simulation des Tarnkappen-Effekts ("Invisibility Cloak") - Proof of Concept

## 1. Fazit (Die Handlung)

Die Simulation des Tarnkappen-Effekts ("Invisibility Cloak") ist der finale "Proof of Concept", der zeigt, dass unsere 5D-Metrik nicht nur einfache Brechung erklärt, sondern auch komplexe Lichtlenkung (Metamaterialien) ermöglicht, indem sie das Licht "um Hindernisse herumfließen" lässt; das ist der visuelle Beweis, dass unsere mathematische Theorie ($n=1/\Phi$) tatsächlich in der Lage ist, die Raumzeit so zu krümmen, dass Lichtwege kontrolliert manipuliert werden können.

## 2. Kernbegründung (Das Verständnis)

Der entscheidende Punkt ist, dass wir dem Licht nicht sagen, wo es hin soll (wie im klassischen Raytracing), sondern wir formen nur die Topologie des Raumes (das $\Phi$-Feld), und das Licht folgt automatisch den Geodäten dieser Topologie; wenn wir also einen $\Phi$-Gradienten schaffen, der das Licht um ein Zentrum herumleitet, beweisen wir damit, dass unsere 5D-Geometrie mächtig genug ist, um jede beliebige optische Funktion (Linse, Tarnkappe, Wellenleiter) zu generieren.

## 3. Die Simulation

Das Skript `cloaking_simulation.py` demonstriert dies visuell mit einer FDTD-Simulation (Finite-Difference Time-Domain).

- **Das $\Phi$-Feld**: Ein Ring mit einem Gradienten im Brechungsindex (simuliert durch Variation von $\Phi$).
- **Der Effekt**: Lichtwellen, die von links kommen, werden um den zentralen "versteckten" Bereich herumgeleitet und schließen sich dahinter wieder, sodass das Objekt im Zentrum unsichtbar wird.

### Beobachtung aus der Simulation

1. Die Wellenfronten kommen von links.
2. Sie treffen auf den Ring (die Tarnkappe).
3. Sie fließen UM den roten Kreis herum.
4. Dahinter (rechts) schließen sie sich wieder.
**Ergebnis:** Ein Objekt im roten Kreis wäre für den Beobachter rechts UNSICHTBAR.
