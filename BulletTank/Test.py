from Game.GameDriver import add_user, start_game, move_player, players_list, update_grid, shoot_player, increase_range, send_ac_point
from utils.CustomExceptions import out_of_bounds, out_of_actions, occupied_space
if __name__ == '__main__':
    global_debug = False
    x_size = 20
    y_size = 10
    print("Debugging Logic")
    add_user("alpha", debug=global_debug)
    add_user("beta", debug=global_debug)
    add_user("gamma", debug=global_debug)
    if False:
        add_user("delta")
        add_user("epsilon")
        add_user("zeta")
        add_user("eta")
        add_user("theta")
        add_user("iota")
        add_user("kappa")
        add_user("eleven")
        add_user("twelve")
        add_user("thirteen")
    start_game(x_size, y_size, debug=global_debug)
    print("Attempting to move alpha N: ")
    try:
        move_player(players_list[0].user_id, "N")
    except out_of_bounds:
        print("cannot Move, out of bounds")

    print("Attempting to move alpha W: ")
    try:    
        move_player(players_list[0].user_id, "W")
    except out_of_bounds:
        print("Cannot Move, Out of bounds")

    print("Attempting to move alpha E: ",
          move_player(players_list[0].user_id, "E"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to give an action point: ",
          send_ac_point("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to give an action point: ",
          send_ac_point("alpha", "beta"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
