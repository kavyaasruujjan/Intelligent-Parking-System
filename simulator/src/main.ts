import dnssd, { ServiceType } from 'dnssd';
import { FakeCoapServer } from './FakeCoapServer';
import { CoapParkingSystem } from './CoapParkingSystem';
import { Simulation } from './Simulation';


// Start looking for a broker

new dnssd.Browser(new ServiceType({
    name:     '_coap',
    protocol: '_udp',
    subtypes: []
  }))
  .on('serviceUp', service => {
    console.log("Device Up: ", service);
    if(service.name === 'broker'){
      const parkingSystem = new CoapParkingSystem(service.addresses[0]);
      const simulation = new Simulation(parkingSystem);
      simulation.start(); // When broker is found, start simulation
    }
  }) 
  .on('serviceDown', service => console.log("Device down: ", service))
  .start();

//Temporarily play the broker
const fakeServer = new FakeCoapServer();
fakeServer.start(()=>{});
const ad = new dnssd.Advertisement(dnssd.udp('fake-broker'), 5683);
ad.start();




