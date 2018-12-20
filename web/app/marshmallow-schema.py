from marshmallow import  Schema, fields
from facilties.functional import  ResponseModel


class ResponseSchema(Schema):
    # self.data = data;
    # self.code = code;
    # self.message = message;
    data = fields.Raw,
    code = fields.Str,
    message = fields.Str;
