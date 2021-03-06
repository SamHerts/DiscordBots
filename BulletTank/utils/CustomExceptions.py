class Error(Exception):
    pass

class out_of_actions(Error):
    pass

class out_of_bounds(Error):
    pass

class occupied_space(Error):
    pass

class out_of_range(Error):
    pass

class range_limited(Error):
    pass

class health_is_zero(Error):
    pass

class not_playing(Error):
    pass

class too_many_players(Error):
    pass

class already_playing(Error):
    pass
