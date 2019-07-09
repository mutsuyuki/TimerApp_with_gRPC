import timer_pb2
import timer_pb2_grpc

from concurrent import futures
import time
import grpc


# APIのロジック
class TimerServicer(timer_pb2_grpc.TimerServicer):
    leftTime = 0
    isRunning = False

    def StartTimer(self, request, context):
        self.leftTime = request.time
        self.isRunning = True

        while self.leftTime > 0:
            if self.isRunning: # 途中でStopTimerされてないかチェック
                yield self.makeTimerState()
                time.sleep(1)
                self.leftTime -= 1
            else:
                return

        self.isRunning = False
        yield self.makeTimerState()

    def StopTimer(self, request, context):
        self.isRunning = False
        return self.makeTimerState()

    def makeTimerState(self):
        return timer_pb2.TimerState(
            isRunning=self.isRunning,
            leftTime=self.leftTime
        )


# サーバーの実行
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    timer_pb2_grpc.add_TimerServicer_to_server(TimerServicer(), server)
    server.add_insecure_port('0.0.0.0:8082')
    server.start()
    print("Server Start!!")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
