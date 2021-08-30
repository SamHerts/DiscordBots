class Error(Exception):
    pass

class out_of_actions(Error):
    pass

class out_of_bounds(Error):
    pass

class occupied_space(Error):
    pass
