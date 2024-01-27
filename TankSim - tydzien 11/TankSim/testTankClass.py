from TankSimClass import TankSim, PumpType
import time

def test1_pump():
    # test działania pompowania
    tank = TankSim(flowRate=1)
    tank.run(1)
    # samo run nie zmienia poziomu wody jeżeli pompy są wyłączone
    assert tank.get_water_level() == 0
    tank.set_pump(PumpType.IN_PUMP, True)
    # pompa uruchomiona
    tank.run(1)
    assert tank.get_water_level() == 1
    # test mniejszego kwantu czasu
    tank.run(0.5)
    assert tank.get_water_level() == 1.5
    # zmiana kierunku pompowania
    tank.set_pump(PumpType.IN_PUMP, False)
    tank.set_pump(PumpType.OUT_PUMP, True)
    tank.run(2)
    assert tank.get_water_level() == 0
    # wypompowanie poniżej zera powinno być niemożliwe
    tank.run(1)
    assert tank.get_water_level() == 0

def test2_pump():
    # test pompowania do maksymalnego poziomu wody 
    tank = TankSim(flowRate=2.5, capacity=10)
    tank.run(10)
    assert tank.get_water_level() == 0
    tank.set_pump(PumpType.IN_PUMP, True)
    tank.run(10)
    #zbiornik powinien osiągnąć maksymalny poziom
    assert tank.get_water_level() == 10

def test3_pump():
    # dwie pompy naraz
    tank = TankSim()
    # działa tylko pompa IN
    tank.set_pump(PumpType.IN_PUMP, True)
    tank.run(1)
    assert tank.get_water_level() == 1
    # teraz obie pompy działaja naraz
    tank.set_pump(PumpType.OUT_PUMP, True)
    tank.run(1)
    assert tank.get_water_level() == 1
    # działa tylko pompa OUT
    tank.set_pump(PumpType.IN_PUMP, False)
    tank.run(1)
    assert tank.get_water_level() == 0 

def test4_heater():
    # Postawowy test na grzanie
    # Zakładamy że ciepło właściwe wody wynosi 4200
    tank = TankSim(capacity=10, flowRate=1.0, heaterPower=1000, ambientTemp=20)
    tank.set_pump(PumpType.IN_PUMP, True)
    tank.run(5)
    tank.set_pump(PumpType.IN_PUMP, False)
    # warunki początkowe 5 litrów w zbiorniku i woda ma 20 stopni
    assert tank.get_water_level() == 5
    assert tank.get_temp() == 20

    #uruchamiamy grzałkę
    #grzałka 1000W jest uruchomiona przez 60s jest 5L wody
    tank.set_heater(True)
    tank.run(60)

    temp = tank.get_temp()
    # temperatura powinna mieć 22,85 stopni
    assert temp > 22 
    assert temp < 23
    
    #kontunujemy grzanie
    tank.run(150)
    temp = tank.get_temp()
    #temperatura powinna mieć 30 stopni
    assert temp == 30

def test5_heater():
    #Test grzania pustego zbiornika
    #Grzanie pustego zbiornika nie zmienia temperatury
    tank = TankSim(capacity=10, flowRate=1.0, heaterPower=1000, ambientTemp=20)
    assert tank.get_water_level() == 0
    assert tank.get_temp() == 20
    tank.set_heater(True)
    tank.run(10)
    assert tank.get_temp() == 20

def test6_termomix():
    tank = TankSim(capacity=10, flowRate=1.0, heaterPower=1000, ambientTemp=20)
    tank.set_pump(PumpType.IN_PUMP, True)
    tank.run(5)
    tank.set_pump(PumpType.IN_PUMP, False)
    # warunki początkowe: % 5 litrów wody o temperaturze 20 stopni
    assert tank.get_water_level() == 5
    assert tank.get_temp() == 20

    # grzejemy wodę
    tank.set_heater(True)
    tank.run(210)
    tank.set_heater(False)
    # temperatura wody powinna być w okolicach 30 stopni
    assert tank.get_temp() == 30
    # pompujemy zimną wodę

    tank.set_pump(PumpType.IN_PUMP, True)
    tank.run(5)
    # na początku mieliśmy 5 litów wody o temperaturze 30 stopni
    # dopompowaliśmy 5 litrów wody o temperaturze 20 stopni
    # powinnismy miec 10 litórw o temperaturze 25 stopni
    assert tank.get_temp() == 25

#uruchomienie testów
test1_pump()
test2_pump()
test3_pump()
test4_heater()
test5_heater()
test6_termomix()







