import { Location } from "./Location";

export interface ParkingSystem {
  enter(id: number): Promise<void>;
  leave(id: number): Promise<void>;
  reserve(id: number): Promise<void>;
  getOpenParkingspotID(): Promise<number|undefined>;
  reserveRandom(): void;
  reserveAround(location: Location): void;
}
