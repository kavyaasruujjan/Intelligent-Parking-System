import { sleep } from './helpers';
import { ParkingSystem } from './ParkingSystem';
export class Simulation {
  parkingSystem: ParkingSystem;
  constructor(parkingSystem: ParkingSystem) {
    this.parkingSystem = parkingSystem;
  }
  async start() {
    var car = new Car(this.parkingSystem, 3000)

    var car2 = new Car(this.parkingSystem, 2500)
    await Promise.all([car.drive(), car2.drive()])
    /*
    while(true){
      this.parkingSystem.reserveRandom();
      await sleep(5000);
    }
    
    */
    
  }
}


class Car{
  parkingSystem!: ParkingSystem;
  delay: number;
  constructor(parkingSystem: ParkingSystem, delay: number ){
    this.parkingSystem = parkingSystem;
    this.delay = delay;
  }
  async drive(){
    while(true){
      let parkingspotID;
      while(parkingspotID===undefined){
        parkingspotID = await this.parkingSystem.getOpenParkingspotID();
        console.log("FOUND",parkingspotID);
      }
      
      this.parkingSystem.reserve(parkingspotID);
      await sleep(this.delay) // driving to the parkingspot
      this.parkingSystem.enter(parkingspotID);
      await sleep(this.delay) // parking
      this.parkingSystem.leave(parkingspotID);
      await sleep(this.delay) // driving away
    }
  }
}