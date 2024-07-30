from syotools.models import Camera


class StrongLens:
    def __init__(self, row):
        self.z_source = row['z_source']
        self.z_lens = row['z_lens']
        self.stellar_mass = row['stellar_mass']
        self.einstein_radius = row['einstein_radius']
        self.velocity_dispersion = row['velocity_dispersion']
        
        c = Camera()
        self.source_magnitudes = {}
        self.lensed_source_magnitudes = {}
        self.lens_magnitudes = {}
        for band in c.bandnames:
            self.source_magnitudes[band] = row[f'source_mag_{band.lower()}']
            self.lensed_source_magnitudes[band] = row[f'lensed_source_mag_{band.lower()}']
            self.lens_magnitudes[band] = row[f'lens_mag_{band.lower()}']

    def get_source_mag(self, band):
        return self.source_magnitudes[band.upper()]
    
    def get_lensed_source_mag(self, band):
        return self.lensed_source_magnitudes[band.upper()]
    
    def get_lens_mag(self, band):
        return self.lens_magnitudes[band.upper()]
