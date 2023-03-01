import random


class Randi:
    waifus = [
        {
            "name": "Mikasa Ackerman",
            "pic": "https://i.imgur.com/K7bP0nR.jpeg"
        },
        {
            "name": "Rem",
            "pic": "https://i.imgur.com/Y03Il8z.jpeg"
        },
        {
            "name": "Zero Two",
            "pic": "https://i.imgur.com/NSoBlbC.jpeg"
        },
        {
            "name": "Asuna Yuuki",
            "pic": "https://i.imgur.com/CwUonjL.jpeg"
        },
        {
            "name": "Kurumi Tokisaki",
            "pic": "https://i.imgur.com/1K8ZBpF.jpeg"
        },
        {
            "name": "Kaguya Shinomiya",
            "pic": "https://i.imgur.com/K1mZld9.jpeg"
        }
    ]

    @classmethod
    def get_random_waifu(cls):
        """
        Returns a random waifu object containing a name and pic.
        """
        return random.choice(cls.waifus)

    @classmethod
    def get_waifu_by_name(cls, name):
        """
        Returns the waifu object with the given name, or None if not found.
        """
        for waifu in cls.waifus:
            if waifu["name"].lower() == name.lower():
                return waifu
        return None
