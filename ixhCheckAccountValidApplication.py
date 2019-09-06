# -*- coding: utf-8 -*-
# @Time    : 2019年9月6日 15:09:34
# @Author  : ZHLH
# @FileName: ixhCheckAccountValidApplication.py

from school_api import SchoolClient
import account_pb2
import account_pb2_grpc
import grpc
from concurrent import futures
import time


class CheckServicer(account_pb2_grpc.checkServicer):
    def Check(self, request, context):
        school = SchoolClient(url='http://jw.xhsysu.edu.cn/')
        user = school.user_login(request.username, request.password)
        schedule_data = user.get_info()
        return account_pb2.Response(result=(0 if "error" not in schedule_data else 1))


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(10))
    account_pb2_grpc.add_checkServicer_to_server(CheckServicer(), server)
    server.add_insecure_port("localhost:1025")
    server.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        server.stop()
