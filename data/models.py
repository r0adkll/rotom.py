from jsonmodels import models, fields


class Attack(models.Base):
    name = fields.StringField(required=True)
    text = fields.StringField(nullable=True)
    damage = fields.StringField(nullable=True)
    convertedEnergyCost = fields.IntField(required=True)
    cost = fields.ListField(str, nullable=True)


class Ability(models.Base):
    name = fields.StringField(required=True)
    text = fields.StringField(required=True)
    type = fields.StringField(nullable=True)


class Effect(models.Base):
    type = fields.StringField(required=True)
    value = fields.StringField(required=True)


class Card(models.Base):
    id = fields.StringField(required=True)
    name = fields.StringField(required=True)
    supertype = fields.StringField(required=True)
    subtype = fields.StringField(required=True)
    imageUrl = fields.StringField(required=True)
    imageUrlHiRes = fields.StringField(required=True)
    number = fields.StringField(required=True)
    set = fields.StringField(required=True)
    series = fields.StringField(required=True)
    setCode = fields.StringField(required=True)

    nationalPokedexNumber = fields.IntField(nullable=True)
    artist = fields.StringField(nullable=True)
    hp = fields.IntField(nullable=True)
    rarity = fields.StringField(nullable=True)
    evolvesFrom = fields.StringField(nullable=True)
    types = fields.ListField(str, nullable=True)
    text = fields.ListField(str, nullable=True)
    attacks = fields.ListField([Attack], nullable=True)
    ability = fields.EmbeddedField(Ability, nullable=True)
    weaknesses = fields.ListField([Effect], nullable=True)
    resistances = fields.ListField([Effect], nullable=True)
    retreatCost = fields.ListField(str, nullable=True)

    def to_struct(self):

        self.validate()

        resp = {}
        for _, name, field in self.iterate_with_name():
            value = field.__get__(self)
            _type = type(field)
            if value is None or (isinstance(field, fields.ListField) and len(value) == 0):
                continue

            value = field.to_struct(value)
            resp[name] = value

        return resp


class DataCard(models.Base):
    id = fields.StringField(required=True)
    name = fields.StringField(required=True)
    supertype = fields.StringField(required=True)
    subtype = fields.StringField(required=True)
    number = fields.StringField(required=True)
    setCode = fields.StringField(required=True)

    imageUrl = fields.StringField(nullable=True)
    imageUrlHiRes = fields.StringField(nullable=True)
    series = fields.StringField(nullable=True)
    set = fields.StringField(nullable=True)
    artist = fields.StringField(nullable=True)

    nationalPokedexNumber = fields.IntField(nullable=True)
    hp = fields.IntField(nullable=True)
    rarity = fields.StringField(nullable=True)
    evolvesFrom = fields.StringField(nullable=True)
    types = fields.ListField(str, nullable=True)
    text = fields.ListField(str, nullable=True)
    attacks = fields.ListField([Attack], nullable=True)
    ability = fields.EmbeddedField(Ability, nullable=True)
    weaknesses = fields.ListField([Effect], nullable=True)
    resistances = fields.ListField([Effect], nullable=True)
    retreatCost = fields.ListField(str, nullable=True)

    def to_struct(self):

        self.validate()

        resp = {}
        for _, name, field in self.iterate_with_name():
            value = field.__get__(self)
            _type = type(field)
            if value is None or (isinstance(field, fields.ListField) and len(value) == 0):
                continue

            value = field.to_struct(value)
            resp[name] = value

        return resp
