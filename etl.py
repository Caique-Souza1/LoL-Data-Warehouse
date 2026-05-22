import pandas as pd

def executar_etl():

    Challenger = pd.read_csv("dados/Challenger_Ranked_Games.csv")
    Grandmaster = pd.read_csv("dados/Grandmaster_Ranked_Games.csv")
    Master = pd.read_csv("dados/Master_Ranked_Games.csv")

    Challenger["elo_id"] = 1
    Challenger["elo_name"] = "Challenger"

    Grandmaster["elo_id"] = 2
    Grandmaster["elo_name"] = "Grandmaster"

    Master["elo_id"] = 3
    Master["elo_name"] = "Master"

    df = pd.concat([Challenger, Grandmaster, Master], ignore_index=True)

    df = df.drop_duplicates(subset=["gameId"])

    df["duration_mmss"] = df["gameDuration"].apply(
        lambda x: f"{x//60}:{x%60:02d}"
    )

    dim_elo = df[["elo_id", "elo_name"]].drop_duplicates().copy()
    dim_elo = dim_elo.sort_values("elo_id").reset_index(drop=True)

    dim_game = df[["gameId", "gameDuration", "duration_mmss"]].copy()

    dim_game = dim_game.drop_duplicates(
        subset=["gameId"]
    ).reset_index(drop=True)

    dim_game.insert(0, "id_game", range(1, len(dim_game) + 1))

    dim_team = pd.DataFrame({
        "team_id": [1, 2],
        "team_name": ["blue", "red"]
    })

    fato_blue = df[[
        "gameId",
        "elo_id",
        "blueWins",
        "blueKills",
        "blueDeath",
        "blueAssist",
        "blueChampionDamageDealt",
        "blueTotalGold",
        "blueFirstBlood",
        "blueFirstTower",
        "blueFirstBaron",
        "blueFirstDragon",
        "blueDragonKills",
        "blueBaronKills",
        "blueTowerKills",
        "blueWardPlaced"
    ]].copy()

    fato_blue["team_id"] = 1

    fato_blue = fato_blue.rename(columns={
        "blueWins": "wins",
        "blueKills": "kills",
        "blueDeath": "deaths",
        "blueAssist": "assists",
        "blueChampionDamageDealt": "damage",
        "blueTotalGold": "gold",
        "blueFirstBlood": "first_blood",
        "blueFirstTower": "first_tower",
        "blueFirstBaron": "first_baron",
        "blueFirstDragon": "first_dragon",
        "blueDragonKills": "dragon_kills",
        "blueBaronKills": "baron_kills",
        "blueTowerKills": "tower_kills",
        "blueWardPlaced": "wards_placed"
    })

    fato_red = df[[
        "gameId",
        "elo_id",
        "redWins",
        "redKills",
        "redDeath",
        "redAssist",
        "redChampionDamageDealt",
        "redTotalGold",
        "redFirstBlood",
        "redFirstTower",
        "redFirstBaron",
        "redFirstDragon",
        "redDragonKills",
        "redBaronKills",
        "redTowerKills",
        "redWardPlaced"
    ]].copy()

    fato_red["team_id"] = 2

    fato_red = fato_red.rename(columns={
        "redWins": "wins",
        "redKills": "kills",
        "redDeath": "deaths",
        "redAssist": "assists",
        "redChampionDamageDealt": "damage",
        "redTotalGold": "gold",
        "redFirstBlood": "first_blood",
        "redFirstTower": "first_tower",
        "redFirstBaron": "first_baron",
        "redFirstDragon": "first_dragon",
        "redDragonKills": "dragon_kills",
        "redBaronKills": "baron_kills",
        "redTowerKills": "tower_kills",
        "redWardPlaced": "wards_placed"
    })

    fato_partida = pd.concat(
        [fato_blue, fato_red],
        ignore_index=True
    )

    fato_partida["kda"] = (
        (fato_partida["kills"] + fato_partida["assists"]) /
        fato_partida["deaths"].replace(0, 1)
    ).round(1)

    fato_partida = fato_partida.merge(
        dim_game[["gameId", "id_game"]],
        on="gameId",
        how="left"
    )

    fato_partida = fato_partida.drop(columns=["gameId"])

    fato_partida = fato_partida.sort_values(
        by=["id_game", "team_id"]
    ).reset_index(drop=True)

    fato_partida = fato_partida[[
        "id_game",
        "elo_id",
        "team_id",
        "kills",
        "deaths",
        "assists",
        "kda",
        "gold",
        "damage",
        "wins",
        "first_blood",
        "first_tower",
        "first_baron",
        "first_dragon",
        "dragon_kills",
        "baron_kills",
        "tower_kills",
        "wards_placed"
    ]]

    return (dim_elo, dim_game, dim_team, fato_partida)


if __name__ == "__main__":

    (dim_elo, dim_game, dim_team, fato_partida) = executar_etl()

    dim_elo.to_csv("dados/dim_elo.csv", index=False)
    dim_game.to_csv("dados/dim_game.csv", index=False)
    dim_team.to_csv("dados/dim_team.csv", index=False)
    fato_partida.to_csv("dados/fato_partida.csv", index=False)

    print("ETL executado com sucesso.")