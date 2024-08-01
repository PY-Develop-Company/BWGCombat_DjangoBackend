GNOME_INCOME = 100


def get_gnome_reward():
    return GNOME_INCOME


def generate_tracking_link(link):
    return f'/track/{link.id}/'
