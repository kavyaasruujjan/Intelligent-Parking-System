import coap from 'coap';
import { Location } from "./Location";
import { ParkingSystem } from "./ParkingSystem";

export class CoapParkingSystem implements ParkingSystem {

  private async makeRequest(method: string, path: string, payload:string=''): Promise<Buffer> {
    const message = coap.request({
      host: this.host,
      method: method,
      pathname: path
    });

    return new Promise((resolve, reject) =>{
      const onResponse = (response: any) => {
        if(response.code!='2.00' && response.code!='2.05'){
          console.log("Parking system responded with status code:", response.code)
          return;
        }
        return resolve(response.payload);
      };
      message.on('response', onResponse);
      message.on('timeout', reject)
      message.on('error', reject)
      message.end(payload);
    })
    
  }

  async enter(id: number) {
    console.log("entering", id)
    await this.setStatus(id, "BUSY");
  }
  async leave(id: number) {
    console.log("leaving", id)
    await this.setStatus(id, "FREE");
  }
  async reserve(id: number) {
    console.log("Reserving", id)
    await this.setStatus(id, "RESERVED");
  }
  async getOpenParkingspotID(): Promise<number|undefined> {
    const largestID = await this.getLargestID();
    console.log("largestID", largestID)
    if(!largestID) return;
    for (let i = 0; i <= largestID; i++) {
      const status = await this.getStatus(i)
      console.log("status", i, status)
      if(status == "FREE") return i
    }
    console.log("Did not find free parking spots")
  }

  async getStatus(id: number): Promise<string|undefined> {
    console.log("Get stats "+id)
    const payload = await this.makeRequest('GET','/parkingspot/'+ id)
    if (!payload) return;
    
    return payload.toString();
  }

  async setStatus(id: number, status:string){
    console.log("Set status " + id)
    await this.makeRequest('PUT','/parkingspot/'+ id, status)
  }

  async getLargestID(): Promise<number|undefined> {
    console.log("Getting largest id")
    const payload = await this.makeRequest('GET','/parkingspot')
    console.log("LargestID payload", payload)
    if (!payload) return;
    return parseInt(payload.toString());
  }

  host: string;
  constructor(host: string) {
    this.host = host;
  }
  
  reserveRandom() {
    console.log("Reserving a random spot")
    const message = coap.request({
      host: this.host,
      method: 'POST',
      pathname: '/reserve'
    });
    const onResponse = (response: any) => {
      if(response.code!='2.00'){
        console.log("Parking system responded with status code:", response.code)
        return;
      }
      console.log("Parking system responded:", response.payload.toString())
    };
    message.on('response', onResponse);
    message.on('timeout', err => console.log("message timed out", err))
    message.on('error', err => console.log("Message errored", err))
    message.end();
  }
  reserveAround(location: Location) {
    //Not implemented
  }
}
