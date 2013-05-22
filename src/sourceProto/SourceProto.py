# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='source.proto',
  package='stardroid_source',
  serialized_pb='\n\x0csource.proto\x12\x10stardroid_source\"J\n\x1aGeocentricCoordinatesProto\x12\x17\n\x0fright_ascension\x18\x01 \x01(\x02\x12\x13\n\x0b\x64\x65\x63lination\x18\x02 \x01(\x02\"\xaf\x01\n\x11PointElementProto\x12>\n\x08location\x18\x01 \x01(\x0b\x32,.stardroid_source.GeocentricCoordinatesProto\x12\x19\n\x05\x63olor\x18\x02 \x01(\r:\n4294967295\x12\x0f\n\x04size\x18\x03 \x01(\x05:\x01\x33\x12.\n\x05shape\x18\x04 \x01(\x0e\x32\x17.stardroid_source.Shape:\x06\x43IRCLE\"\xb1\x01\n\x11LabelElementProto\x12>\n\x08location\x18\x01 \x01(\x0b\x32,.stardroid_source.GeocentricCoordinatesProto\x12\x19\n\x05\x63olor\x18\x02 \x01(\r:\n4294967295\x12\x14\n\x0cstring_index\x18\x03 \x01(\x05\x12\x15\n\tfont_size\x18\x04 \x01(\x05:\x02\x31\x35\x12\x14\n\x06offset\x18\x05 \x01(\x02:\x04\x30.02\"\x84\x01\n\x10LineElementProto\x12\x19\n\x05\x63olor\x18\x01 \x01(\r:\n4294967295\x12\x17\n\nline_width\x18\x02 \x01(\x02:\x03\x31.5\x12<\n\x06vertex\x18\x03 \x03(\x0b\x32,.stardroid_source.GeocentricCoordinatesProto\"\xb7\x02\n\x17\x41stronomicalSourceProto\x12\x10\n\x08name_ids\x18\x01 \x03(\r\x12\x45\n\x0fsearch_location\x18\x02 \x01(\x0b\x32,.stardroid_source.GeocentricCoordinatesProto\x12\x17\n\x0csearch_level\x18\x03 \x01(\x02:\x01\x30\x12\x10\n\x05level\x18\x04 \x01(\x02:\x01\x30\x12\x32\n\x05point\x18\x05 \x03(\x0b\x32#.stardroid_source.PointElementProto\x12\x32\n\x05label\x18\x06 \x03(\x0b\x32#.stardroid_source.LabelElementProto\x12\x30\n\x04line\x18\x07 \x03(\x0b\x32\".stardroid_source.LineElementProto\"U\n\x18\x41stronomicalSourcesProto\x12\x39\n\x06source\x18\x01 \x03(\x0b\x32).stardroid_source.AstronomicalSourceProto*\xbf\x01\n\x05Shape\x12\n\n\x06\x43IRCLE\x10\x00\x12\x08\n\x04STAR\x10\x01\x12\x15\n\x11\x45LLIPTICAL_GALAXY\x10\x02\x12\x11\n\rSPIRAL_GALAXY\x10\x03\x12\x14\n\x10IRREGULAR_GALAXY\x10\x04\x12\x15\n\x11LENTICULAR_GALAXY\x10\x05\x12\x14\n\x10GLOBULAR_CLUSTER\x10\x06\x12\x10\n\x0cOPEN_CLUSTER\x10\x07\x12\n\n\x06NEBULA\x10\x08\x12\x15\n\x11HUBBLE_DEEP_FIELD\x10\tB\x02H\x03')

_SHAPE = descriptor.EnumDescriptor(
  name='Shape',
  full_name='stardroid_source.Shape',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='CIRCLE', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STAR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ELLIPTICAL_GALAXY', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='SPIRAL_GALAXY', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='IRREGULAR_GALAXY', index=4, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='LENTICULAR_GALAXY', index=5, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='GLOBULAR_CLUSTER', index=6, number=6,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='OPEN_CLUSTER', index=7, number=7,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='NEBULA', index=8, number=8,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='HUBBLE_DEEP_FIELD', index=9, number=9,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1005,
  serialized_end=1196,
)


CIRCLE = 0
STAR = 1
ELLIPTICAL_GALAXY = 2
SPIRAL_GALAXY = 3
IRREGULAR_GALAXY = 4
LENTICULAR_GALAXY = 5
GLOBULAR_CLUSTER = 6
OPEN_CLUSTER = 7
NEBULA = 8
HUBBLE_DEEP_FIELD = 9



_GEOCENTRICCOORDINATESPROTO = descriptor.Descriptor(
  name='GeocentricCoordinatesProto',
  full_name='stardroid_source.GeocentricCoordinatesProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='right_ascension', full_name='stardroid_source.GeocentricCoordinatesProto.right_ascension', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='declination', full_name='stardroid_source.GeocentricCoordinatesProto.declination', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=34,
  serialized_end=108,
)


_POINTELEMENTPROTO = descriptor.Descriptor(
  name='PointElementProto',
  full_name='stardroid_source.PointElementProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='location', full_name='stardroid_source.PointElementProto.location', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='color', full_name='stardroid_source.PointElementProto.color', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=4294967295,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='size', full_name='stardroid_source.PointElementProto.size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=3,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='shape', full_name='stardroid_source.PointElementProto.shape', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=111,
  serialized_end=286,
)


_LABELELEMENTPROTO = descriptor.Descriptor(
  name='LabelElementProto',
  full_name='stardroid_source.LabelElementProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='location', full_name='stardroid_source.LabelElementProto.location', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='color', full_name='stardroid_source.LabelElementProto.color', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=4294967295,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='string_index', full_name='stardroid_source.LabelElementProto.string_index', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='font_size', full_name='stardroid_source.LabelElementProto.font_size', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=15,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='offset', full_name='stardroid_source.LabelElementProto.offset', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0.02,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=289,
  serialized_end=466,
)


_LINEELEMENTPROTO = descriptor.Descriptor(
  name='LineElementProto',
  full_name='stardroid_source.LineElementProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='color', full_name='stardroid_source.LineElementProto.color', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=4294967295,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='line_width', full_name='stardroid_source.LineElementProto.line_width', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1.5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vertex', full_name='stardroid_source.LineElementProto.vertex', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=469,
  serialized_end=601,
)


_ASTRONOMICALSOURCEPROTO = descriptor.Descriptor(
  name='AstronomicalSourceProto',
  full_name='stardroid_source.AstronomicalSourceProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name_ids', full_name='stardroid_source.AstronomicalSourceProto.name_ids', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='search_location', full_name='stardroid_source.AstronomicalSourceProto.search_location', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='search_level', full_name='stardroid_source.AstronomicalSourceProto.search_level', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='level', full_name='stardroid_source.AstronomicalSourceProto.level', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='point', full_name='stardroid_source.AstronomicalSourceProto.point', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='label', full_name='stardroid_source.AstronomicalSourceProto.label', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='line', full_name='stardroid_source.AstronomicalSourceProto.line', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=604,
  serialized_end=915,
)


_ASTRONOMICALSOURCESPROTO = descriptor.Descriptor(
  name='AstronomicalSourcesProto',
  full_name='stardroid_source.AstronomicalSourcesProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='source', full_name='stardroid_source.AstronomicalSourcesProto.source', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=917,
  serialized_end=1002,
)

_POINTELEMENTPROTO.fields_by_name['location'].message_type = _GEOCENTRICCOORDINATESPROTO
_POINTELEMENTPROTO.fields_by_name['shape'].enum_type = _SHAPE
_LABELELEMENTPROTO.fields_by_name['location'].message_type = _GEOCENTRICCOORDINATESPROTO
_LINEELEMENTPROTO.fields_by_name['vertex'].message_type = _GEOCENTRICCOORDINATESPROTO
_ASTRONOMICALSOURCEPROTO.fields_by_name['search_location'].message_type = _GEOCENTRICCOORDINATESPROTO
_ASTRONOMICALSOURCEPROTO.fields_by_name['point'].message_type = _POINTELEMENTPROTO
_ASTRONOMICALSOURCEPROTO.fields_by_name['label'].message_type = _LABELELEMENTPROTO
_ASTRONOMICALSOURCEPROTO.fields_by_name['line'].message_type = _LINEELEMENTPROTO
_ASTRONOMICALSOURCESPROTO.fields_by_name['source'].message_type = _ASTRONOMICALSOURCEPROTO
DESCRIPTOR.message_types_by_name['GeocentricCoordinatesProto'] = _GEOCENTRICCOORDINATESPROTO
DESCRIPTOR.message_types_by_name['PointElementProto'] = _POINTELEMENTPROTO
DESCRIPTOR.message_types_by_name['LabelElementProto'] = _LABELELEMENTPROTO
DESCRIPTOR.message_types_by_name['LineElementProto'] = _LINEELEMENTPROTO
DESCRIPTOR.message_types_by_name['AstronomicalSourceProto'] = _ASTRONOMICALSOURCEPROTO
DESCRIPTOR.message_types_by_name['AstronomicalSourcesProto'] = _ASTRONOMICALSOURCESPROTO

class GeocentricCoordinatesProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GEOCENTRICCOORDINATESPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.GeocentricCoordinatesProto)

class PointElementProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _POINTELEMENTPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.PointElementProto)

class LabelElementProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LABELELEMENTPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.LabelElementProto)

class LineElementProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LINEELEMENTPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.LineElementProto)

class AstronomicalSourceProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ASTRONOMICALSOURCEPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.AstronomicalSourceProto)

class AstronomicalSourcesProto(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ASTRONOMICALSOURCESPROTO
  
  # @@protoc_insertion_point(class_scope:stardroid_source.AstronomicalSourcesProto)

# @@protoc_insertion_point(module_scope)
