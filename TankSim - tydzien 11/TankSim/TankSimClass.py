from enum import Enum

class PumpType(Enum):
    IN_PUMP = 0
    OUT_PUMP = 1

class TankSim:
    def __init__(self, capacity=40, waterLevel=0, ambientTemp=25, flowRate=1, heaterPower=1000):
        self.capacity = capacity
        self.waterLevel = waterLevel
        self.ambientTemp = ambientTemp
        self.waterTemp = ambientTemp
        self.heaterState = False
        self.pumpInState = False
        self.pumpOutState = False
        self.flowRate = flowRate # 1 -> water flow rate l/s
        self.heaterPower = heaterPower # 1000 W 
    
    def __str__(self):
        return f"Prowadzacy: Poziom Wody: {self.waterLevel}, Temperatura: {self.waterTemp}, Grzałka: {self.heaterState}"        

    def set_heater(self, state: bool) -> None:
        self.heaterState = state

    def set_pump(self, type: PumpType, state:bool) -> None:
        if type is PumpType.IN_PUMP:
            self.pumpInState = state
        else:
            self.pumpOutState = state

    def get_temp(self) -> float:
        return self.waterTemp
    
    def get_water_level(self) -> float:
        return self.waterLevel
    
    def run(self, time: float = 1) -> None:
        detla = self.pump_handler(time)
        self.termomix_handler(detla)
        # najpierw mieszamy wodę poźniej grzejemy
        self.heater_hanlder(time)

    def pump_handler(self, time) -> float:
        # implementujemy pompowanie/wypompowanie wody
        # flowRate * time
        detla = time*self.flowRate
        if self.pumpInState:
            self.waterLevel += detla
        # zwracamy ilość dopompowanej wody
        #potrzebyjemy tego do mieszania wody
        return detla


    def heater_hanlder(self, time) -> None:
        # implementujemy grzanie wody
        # Ciepło właściwe wody = 4200
        # delta t to nasz time
        if self.heaterState:
            if self.waterLevel > 0:
                self.waterTemp += 1 

    def termomix_handler(self, deltaLiters) -> None:
        # implementuje mieszkanie ciepłej i zimnej wody, gdy mamy PumpIn
        # temperatura zimnej wody to ambientTemp
        waterLevelBefore = self.waterLevel-deltaLiters
