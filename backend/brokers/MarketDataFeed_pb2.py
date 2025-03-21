# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: MarketDataFeed.proto
# Protobuf Python Version: 5.29.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    1,
    '',
    'MarketDataFeed.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14MarketDataFeed.proto\x12%com.upstox.marketdatafeeder.rpc.proto\"9\n\x04LTPC\x12\x0b\n\x03ltp\x18\x01 \x01(\x01\x12\x0b\n\x03ltt\x18\x02 \x01(\x03\x12\x0b\n\x03ltq\x18\x03 \x01(\x03\x12\n\n\x02\x63p\x18\x04 \x01(\x01\"]\n\x0bMarketLevel\x12\x41\n\x0b\x62idAskQuote\x18\x01 \x03(\x0b\x32,.com.upstox.marketdatafeeder.rpc.proto.Quote\x12\x0b\n\x03lut\x18\x02 \x01(\x03\"G\n\nMarketOHLC\x12\x39\n\x04ohlc\x18\x01 \x03(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.OHLC\"m\n\x05Quote\x12\n\n\x02\x62q\x18\x01 \x01(\x05\x12\n\n\x02\x62p\x18\x02 \x01(\x01\x12\x0b\n\x03\x62no\x18\x03 \x01(\x05\x12\n\n\x02\x61q\x18\x04 \x01(\x05\x12\n\n\x02\x61p\x18\x05 \x01(\x01\x12\x0b\n\x03\x61no\x18\x06 \x01(\x05\x12\x0c\n\x04\x62idQ\x18\x07 \x01(\x03\x12\x0c\n\x04\x61skQ\x18\x08 \x01(\x03\"z\n\x0cOptionGreeks\x12\n\n\x02op\x18\x01 \x01(\x01\x12\n\n\x02up\x18\x02 \x01(\x01\x12\n\n\x02iv\x18\x03 \x01(\x01\x12\r\n\x05\x64\x65lta\x18\x04 \x01(\x01\x12\r\n\x05theta\x18\x05 \x01(\x01\x12\r\n\x05gamma\x18\x06 \x01(\x01\x12\x0c\n\x04vega\x18\x07 \x01(\x01\x12\x0b\n\x03rho\x18\x08 \x01(\x01\"\xbf\x02\n\x13\x45xtendedFeedDetails\x12\x0b\n\x03\x61tp\x18\x01 \x01(\x01\x12\n\n\x02\x63p\x18\x02 \x01(\x01\x12\x0b\n\x03vtt\x18\x03 \x01(\x03\x12\n\n\x02oi\x18\x04 \x01(\x01\x12\x10\n\x08\x63hangeOi\x18\x05 \x01(\x01\x12\x11\n\tlastClose\x18\x06 \x01(\x01\x12\x0b\n\x03tbq\x18\x07 \x01(\x01\x12\x0b\n\x03tsq\x18\x08 \x01(\x01\x12\r\n\x05\x63lose\x18\t \x01(\x01\x12\n\n\x02lc\x18\n \x01(\x01\x12\n\n\x02uc\x18\x0b \x01(\x01\x12\n\n\x02yh\x18\x0c \x01(\x01\x12\n\n\x02yl\x18\r \x01(\x01\x12\n\n\x02\x66p\x18\x0e \x01(\x01\x12\n\n\x02\x66v\x18\x0f \x01(\x05\x12\x0e\n\x06mbpBuy\x18\x10 \x01(\x03\x12\x0f\n\x07mbpSell\x18\x11 \x01(\x03\x12\n\n\x02tv\x18\x12 \x01(\x03\x12\x0c\n\x04\x64hoi\x18\x13 \x01(\x01\x12\x0c\n\x04\x64loi\x18\x14 \x01(\x01\x12\n\n\x02sp\x18\x15 \x01(\x01\x12\x0b\n\x03poi\x18\x16 \x01(\x01\"y\n\x04OHLC\x12\x10\n\x08interval\x18\x01 \x01(\t\x12\x0c\n\x04open\x18\x02 \x01(\x01\x12\x0c\n\x04high\x18\x03 \x01(\x01\x12\x0b\n\x03low\x18\x04 \x01(\x01\x12\r\n\x05\x63lose\x18\x05 \x01(\x01\x12\x0e\n\x06volume\x18\x06 \x01(\x05\x12\n\n\x02ts\x18\x07 \x01(\x03\x12\x0b\n\x03vol\x18\t \x01(\x03\"\xf8\x02\n\x0eMarketFullFeed\x12\x39\n\x04ltpc\x18\x01 \x01(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.LTPC\x12G\n\x0bmarketLevel\x18\x02 \x01(\x0b\x32\x32.com.upstox.marketdatafeeder.rpc.proto.MarketLevel\x12I\n\x0coptionGreeks\x18\x03 \x01(\x0b\x32\x33.com.upstox.marketdatafeeder.rpc.proto.OptionGreeks\x12\x45\n\nmarketOHLC\x18\x04 \x01(\x0b\x32\x31.com.upstox.marketdatafeeder.rpc.proto.MarketOHLC\x12P\n\x0c\x65\x46\x65\x65\x64\x44\x65tails\x18\x05 \x01(\x0b\x32:.com.upstox.marketdatafeeder.rpc.proto.ExtendedFeedDetails\"\xbc\x01\n\rIndexFullFeed\x12\x39\n\x04ltpc\x18\x01 \x01(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.LTPC\x12\x45\n\nmarketOHLC\x18\x02 \x01(\x0b\x32\x31.com.upstox.marketdatafeeder.rpc.proto.MarketOHLC\x12\x11\n\tlastClose\x18\x03 \x01(\x01\x12\n\n\x02yh\x18\x04 \x01(\x01\x12\n\n\x02yl\x18\x05 \x01(\x01\"\xaf\x01\n\x08\x46ullFeed\x12I\n\x08marketFF\x18\x01 \x01(\x0b\x32\x35.com.upstox.marketdatafeeder.rpc.proto.MarketFullFeedH\x00\x12G\n\x07indexFF\x18\x02 \x01(\x0b\x32\x34.com.upstox.marketdatafeeder.rpc.proto.IndexFullFeedH\x00\x42\x0f\n\rFullFeedUnion\"\xa8\x02\n\x0bOptionChain\x12\x39\n\x04ltpc\x18\x01 \x01(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.LTPC\x12\x41\n\x0b\x62idAskQuote\x18\x02 \x01(\x0b\x32,.com.upstox.marketdatafeeder.rpc.proto.Quote\x12I\n\x0coptionGreeks\x18\x03 \x01(\x0b\x32\x33.com.upstox.marketdatafeeder.rpc.proto.OptionGreeks\x12P\n\x0c\x65\x46\x65\x65\x64\x44\x65tails\x18\x04 \x01(\x0b\x32:.com.upstox.marketdatafeeder.rpc.proto.ExtendedFeedDetails\"\xd1\x01\n\x04\x46\x65\x65\x64\x12;\n\x04ltpc\x18\x01 \x01(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.LTPCH\x00\x12=\n\x02\x66\x66\x18\x02 \x01(\x0b\x32/.com.upstox.marketdatafeeder.rpc.proto.FullFeedH\x00\x12@\n\x02oc\x18\x03 \x01(\x0b\x32\x32.com.upstox.marketdatafeeder.rpc.proto.OptionChainH\x00\x42\x0b\n\tFeedUnion\"\x86\x02\n\x0c\x46\x65\x65\x64Response\x12\x39\n\x04type\x18\x01 \x01(\x0e\x32+.com.upstox.marketdatafeeder.rpc.proto.Type\x12M\n\x05\x66\x65\x65\x64s\x18\x02 \x03(\x0b\x32>.com.upstox.marketdatafeeder.rpc.proto.FeedResponse.FeedsEntry\x12\x11\n\tcurrentTs\x18\x03 \x01(\x03\x1aY\n\nFeedsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12:\n\x05value\x18\x02 \x01(\x0b\x32+.com.upstox.marketdatafeeder.rpc.proto.Feed:\x02\x38\x01*\'\n\x04Type\x12\x10\n\x0cinitial_feed\x10\x00\x12\r\n\tlive_feed\x10\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MarketDataFeed_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FEEDRESPONSE_FEEDSENTRY']._loaded_options = None
  _globals['_FEEDRESPONSE_FEEDSENTRY']._serialized_options = b'8\001'
  _globals['_TYPE']._serialized_start=2494
  _globals['_TYPE']._serialized_end=2533
  _globals['_LTPC']._serialized_start=63
  _globals['_LTPC']._serialized_end=120
  _globals['_MARKETLEVEL']._serialized_start=122
  _globals['_MARKETLEVEL']._serialized_end=215
  _globals['_MARKETOHLC']._serialized_start=217
  _globals['_MARKETOHLC']._serialized_end=288
  _globals['_QUOTE']._serialized_start=290
  _globals['_QUOTE']._serialized_end=399
  _globals['_OPTIONGREEKS']._serialized_start=401
  _globals['_OPTIONGREEKS']._serialized_end=523
  _globals['_EXTENDEDFEEDDETAILS']._serialized_start=526
  _globals['_EXTENDEDFEEDDETAILS']._serialized_end=845
  _globals['_OHLC']._serialized_start=847
  _globals['_OHLC']._serialized_end=968
  _globals['_MARKETFULLFEED']._serialized_start=971
  _globals['_MARKETFULLFEED']._serialized_end=1347
  _globals['_INDEXFULLFEED']._serialized_start=1350
  _globals['_INDEXFULLFEED']._serialized_end=1538
  _globals['_FULLFEED']._serialized_start=1541
  _globals['_FULLFEED']._serialized_end=1716
  _globals['_OPTIONCHAIN']._serialized_start=1719
  _globals['_OPTIONCHAIN']._serialized_end=2015
  _globals['_FEED']._serialized_start=2018
  _globals['_FEED']._serialized_end=2227
  _globals['_FEEDRESPONSE']._serialized_start=2230
  _globals['_FEEDRESPONSE']._serialized_end=2492
  _globals['_FEEDRESPONSE_FEEDSENTRY']._serialized_start=2403
  _globals['_FEEDRESPONSE_FEEDSENTRY']._serialized_end=2492
# @@protoc_insertion_point(module_scope)
