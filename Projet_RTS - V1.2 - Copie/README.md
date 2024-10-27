# AIge-Of-EmpAIres

# 1 Rules of the Game

AoE2 is my reference point, and we shall take a minuscule subset of rules from it.

    The game takes place on a map, which is a grid of size N × M tiles. The absolute minimum size you must be able to handle is 120 × 120, which corresponds to a "tiny" map in AoE2.

    The maps will be randomly generated — a fact that you must be able to demonstrate.

    You will support at least two different types of randomly generated maps, each with strategic and tactical implications: for instance, one with generous resources dotted across the map (take the Arabia map from AoE2 as a reference for what that looks like) and one where all the gold is at the centre of the map.

    Population limit = maximum number of units per player: 200.
    Actual limit in play determined by houses and town centres, within that maximum.

    The following resources:
        a. Wood (W), 100 per tile (tree)
        b. Food (through farms only) (F), 300 per farm
        c. Gold (G), 800 per tile

## Units:
    a. Villager: v
    Cost 50F, 25 HP, Training time 25s, 2 attack, speed 0.8 tile/second.
    Can build buildings.

    The nominal building time t of a building given below is the time required for one Villager to construct a building alone.

    If n Villagers are used, and t is the nominal building time remaining, the actual building time will be 3tn+2n+23t​.

    Can collect resources at a rate of 25/minute, can carry 20.

    b. Swordsman: s
    Cost 50F + 20G, Training time 20s, 40HP, 4 attack, speed .9.

    c. Horseman: h
    Cost 80F + 20G, Training time 30s, 45HP, 4 attack, speed 1.2.

    d. Archer: a
    Cost 25W + 45G, Training time 35s, 30HP, 4 attack, 4 range, speed 1.

## Buildings:

    a. Town Centre: T
    Cost 350W, Build time 150 seconds, 1000 HP, 4x4, Spawns Villagers, Drop point for resources, Population: +5.

    b. House: H
    Cost 25W, Build time 25 seconds, 200 HP, 2x2, Population: +5.

    c. Camp: C
    Cost 100W, Build time 25 seconds, 200 HP, 2x2, Drop point for resources.

    d. Farm: F
    Cost 60W, Build time 10 seconds, 100HP, 2x2, Contains 300 Food.
    Note: this is the only walkable building, cf. AoE2.

    e. Barracks: B
    Costs 175W, Build time 50 seconds, 500HP, 3x3, Spawns Swordsmen.

    f. Stable: S
    Costs 175W, Build time 50 seconds, 500HP, 3x3, Spawns Horsemen.

    g. Archery Range: A
    Costs 175W, Build time 50 seconds, 500HP, 3x3, Spawns Archers.

    h. Keep: K
    Costs 35W, 125G, Build time 80 seconds, 800HP, 1x1, Fires arrows: Attack 5, range 8.

## Starting conditions:

    a. Lean: 50F, 200W, 50G,
    Town Centre, 3 Villagers

    b. Mean: 2000(F,W,G)
    Town Centre, 3 Villagers

    c. Marines: 20000(F,W,G)
    3 Town Centres, 15 Villagers, 2 (Barracks, Stable, Archery Range)