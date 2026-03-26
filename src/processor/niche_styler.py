class NicheStyler:
    """
    Provides visual styling (colors, fonts, overlays) for specific niches.
    """
    NICHES = {
        "Space": {
            "bg_color": (0, 0, 0),
            "text_color": "#FFFF00", # Space yellow
            "font": "Arial Black",
            "music_style": "ambient_nebula"
        },
        "Dark History": {
            "bg_color": (15, 15, 15),
            "text_color": "#FFC107", # Amber/Gold
            "font": "Georgia",
            "music_style": "tense_mystery"
        },
        "Mystery": {
            "bg_color": (10, 10, 40),
            "text_color": "#E0E0E0",
            "font": "Courier New",
            "music_style": "chilling_suspense"
        }
    }

    def get_style(self, niche_name):
        return self.NICHES.get(niche_name, self.NICHES["Space"])

    def apply_style(self, video_engine, niche_name):
        """
        Updates a VideoEngine's config with niche-specific styles.
        """
        style = self.get_style(niche_name)
        # Update config/renderer properties
        # This is a conceptual implementation of the styler.
        return style
