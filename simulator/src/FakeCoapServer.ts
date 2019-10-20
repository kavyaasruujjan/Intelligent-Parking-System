import coap from 'coap';
export class FakeCoapServer {
  server: any;
  constructor() {
    this.server = coap.createServer();
    this.server.on('request', this.onRequest);
  }
  private onRequest(request: any, response: any) {
    const content = '1';
    response.end(content);
  }
  start(onStarted: () => void) {
    // the default CoAP port is 5683
    this.server.listen(onStarted);
  }
}
