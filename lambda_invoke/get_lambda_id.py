import json
import boto3

client = boto3.client('lambda', region_name='us-west-2')
ctx = {
  'Test':'test'
}
payload = json.dumps(ctx)

response = client.invoke(
  FunctionName='arn:aws:lambda:us-west-2:004460406077:function:KE_fetchingFuturesTW',
  InvocationType='RequestResponse',
  Payload=payload
)


''' may have the error message
{"errorMessage": "HTTPConnectionPool(host='isin.twse.com.tw', port=80): Max retries exceeded with url: /isin/C_public.jsp?strMode=2 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fa77c59e7b8>: Failed to establish a new connection: [Errno 111] Connection refused',))", "errorType": "ConnectionError", "stackTrace": [["/var/task/main.py", 11, "handler", "_first = FirstStep()"], ["/var/task/src/FirstStep.py", 5, "__init__", "self._IDobject = getCenterID()"], ["/var/task/src/getCenterID.py", 7, "__init__", "self.res = requests.get(\"http://isin.twse.com.tw/isin/C_public.jsp?strMode=2\")"], ["/var/task/requests/api.py", 75, "get", "return request('get', url, params=params, **kwargs)"], ["/var/task/requests/api.py", 60, "request", "return session.request(method=method, url=url, **kwargs)"], ["/var/task/requests/sessions.py", 533, "request", "resp = self.send(prep, **send_kwargs)"], ["/var/task/requests/sessions.py", 646, "send", "r = adapter.send(request, **kwargs)"], ["/var/task/requests/adapters.py", 516, "send", "raise ConnectionError(e, request=request)"]]}
'''

print(response)