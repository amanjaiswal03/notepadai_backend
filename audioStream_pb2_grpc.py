# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import audioStream_pb2 as audioStream__pb2


class AudioProcessorStub(object):
  """Interface to server
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.TranscriptAudio = channel.stream_stream(
        '/AudioProcessor/TranscriptAudio',
        request_serializer=audioStream__pb2.Sample.SerializeToString,
        response_deserializer=audioStream__pb2.Sentence.FromString,
        )


class AudioProcessorServicer(object):
  """Interface to server
  """

  def TranscriptAudio(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AudioProcessorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'TranscriptAudio': grpc.stream_stream_rpc_method_handler(
          servicer.TranscriptAudio,
          request_deserializer=audioStream__pb2.Sample.FromString,
          response_serializer=audioStream__pb2.Sentence.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'AudioProcessor', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
