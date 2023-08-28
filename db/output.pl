state(idle).
state(configuring).
state(warming_up).
state(c2).
initial(idle).
initial(waiting).
initial(building_up_temperature).
final(final).
alias(final, '').
superstate(configuring, waiting).
superstate(configuring, reading).
superstate(warming_up, final).
superstate(warming_up, c1).
superstate(warming_up, building_up_temperature).

transition(reading, reading, event(call, "set(desiredTemperature)"), nil, action(log, "reset timer")).
transition(configuring, idle, nil, nil, action(log, "double beep")).
transition(building_up_temperature, c1, event(call, "after(3m)"), nil, action(log, "ftemp := furnace temperature")).
transition(c2, warming_up, nil, "tempNow ≤ desiredTemperature - 1; fan is off", nil).
transition(reading, final, event(call, "end"), nil, nil).
transition(configuring, idle, event(call, "cancel"), nil, action(log, "prolonged beep")).
transition(c2, warming_up, nil, "tempNow ≤ desiredTemperature - 1; fan is on", action(log, "turn fan off")).
transition(idle, final, event(call, "shut off"), "fan is on", action(log, "turn fan off")).
transition(warming_up, idle, nil, nil, action(log, "turn on fan; ‘click’ sound")).
transition(waiting, reading, event(call, "set(desiredTemperature)"), nil, action(log, "reset's timer")).
transition(idle, configuring, event(call, "configure"), nil, action(log, "beep")).
transition(warming_up, configuring, event(call, "configure"), nil, action(log, "beep")).
transition(c1, building_up_temperature, nil, "ftemp < desiredTemperature + 1", nil).
transition(idle, c2, event(call, "after (2m)"), nil, action(log, "tempNow := current temperature")).
transition(configuring, idle, nil, "inactivity > 1m", nil).
transition(c1, final, nil, "ftemp ≥ desiredTemperature + 1", nil).
transition(c2, idle, nil, "tempNow ≥ desiredTemperature", nil).
