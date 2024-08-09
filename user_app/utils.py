GNOME_INCOME = 0.025


def get_gnome_reward():
    return GNOME_INCOME


def generate_tracking_link(link):
    return f'/track/{link.id}/'
