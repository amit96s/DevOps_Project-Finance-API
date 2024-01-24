from marshmallow import fields, Schema

class StockDataSchema(Schema):
    ticker = fields.String(dump_only=True)
    company = fields.String(dump_only=True)
    change = fields.Float(dump_only=True)


class InfoSchema(Schema):
    brief = fields.String(dump_only=True)