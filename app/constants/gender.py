class Genders:
    MALE = 0
    FEMALE = 1
    OTHER = 2

    @classmethod
    def get_name(cls, gener_value):
        gender_map = {
            cls.MALE: "Male",
            cls.FEMALE: "Female",
            cls.OTHER: "Other",
        }
        return gender_map.get(gener_value, "UNKNOWN")
