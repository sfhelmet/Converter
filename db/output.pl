state(idle).
state(configuring).
state(warming_up).
state(c2).
state(final).
initial(idle).
initial(waiting).
initial(building_up_temperature).
final(configuring_final).
final(warming_up_final).
final(final).
alias(configuring_final, '').
alias(warming_up_final, '').
alias(final, '').
superstate(configuring, reading).
superstate(configuring, waiting).
superstate(configuring, configuring_final).
superstate(warming_up, c1).
superstate(warming_up, building_up_temperature).
superstate(warming_up, warming_up_final).

transition(building_up_temperature, c1, event(call, "after(3m)"), nil, action(log, "ftemp := furnace temperature")).
transition(c2, warming_up, nil, "tempNow ≤ desiredTemperature - 1;  fan is off", nil).
transition(idle, c2, event(call, "after (2m)"), nil, action(log, "tempNow := current temperature")).
transition(c1, building_up_temperature, nil, "ftemp < desiredTemperature + 1", nil).
transition(configuring, idle, event(call, "cancel"), nil, action(log, "prolonged beep")).
transition(configuring, idle, nil, nil, action(log, "double beep")).
transition(idle, final, event(call, "shut off"), "fan is on", action(log, "turn fan off")).
transition(warming_up, idle, nil, nil, action(log, "turn on fan;  'click' sound")).
transition(configuring, idle, nil, "inactivity > 1m", nil).
transition(idle, configuring, event(call, "configure"), nil, action(log, "beep")).
transition(c2, warming_up, nil, "tempNow ≤ desiredTemperature - 1;  fan is on", action(log, "turn fan off")).
transition(c2, idle, nil, "tempNow ≥ desiredTemperature", nil).
transition(reading, configuring_final, event(call, "end"), nil, nil).
transition(c1, warming_up_final, nil, "ftemp ≥ desiredTemperature + 1", nil).
transition(reading, reading, event(call, "set(desiredTemperature)"), nil, action(log, "reset timer")).
transition(warming_up, configuring, event(call, "configure"), nil, action(log, "beep")).
transition(waiting, reading, event(call, "set(desiredTemperature)"), nil, action(log, "reset timer; ")).
